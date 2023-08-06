from datetime import timedelta, date
from math import log, floor
import logging
from pandas import DataFrame, concat, cut, get_dummies
from graphdb import Node, Relationship
from ingestor.common.constants import VIEW_COUNT, CUSTOMER_ID, CONTENT_ID, IS_PAY_TV, CONTENT_STATUS, CONTENT_LABEL, \
    LABEL, PROPERTIES, USER_LABEL, RELATIONSHIP
from ingestor.user_rating.config import DAYS, weight_duration, weight_top_rating, weight_very_positive, weight_positive, \
    weight_not_sure, SCALING_FACTOR, NUMBER_OF_BINS, RESOLUTION, HAS_RATING
from ingestor.user_rating.constants import BINS, NOT_SURE, POSITIVE, VERY_POSITIVE, TOP_RATING, AGE_OF_EVENT, \
    TIME_DECAY_FACTOR, IMPLICIT_RATING, RECENT_DATE, RECENT_DURATION, COUNT, DURATION_VALUE, \
    TOP_RATING_VALUE, VERY_POSITIVE_VALUE, POSITIVE_VALUE, NOT_SURE_VALUE, IMPLICIT_RATING_VALUE, \
    NORMALISED_IMPLICIT_RATING, MAX_RATING
from ingestor.user_rating.rating_utils import RatingUtils
from ingestor.repository.graph_db_connection import ANGraphDb


class ConsumerRatingGenerator:

    def define_rating_events(
            self,
            data: DataFrame
    ) -> DataFrame:
        """
        Define rating events based on view counts:
        TOP RATING : Occurs in top first bin (maximum view counts)
        VERY POSITIVE : Occurs in second top bin
        POSITIVE : third bin
        NOT SURE : last bin (least view counts)
        """
        data = RatingUtils.cap_ubd_data(data)
        bins = data[VIEW_COUNT].value_counts(bins=NUMBER_OF_BINS, sort=False).rename_axis(BINS).reset_index(name=COUNT)
        bins_list = bins[BINS].to_list()
        data[BINS] = cut(data[VIEW_COUNT],
                         bins=[floor(bins_list[0].left), floor(bins_list[0].right), floor(bins_list[1].right),
                               floor(bins_list[2].right),
                               floor(bins_list[3].right)], labels=[NOT_SURE, POSITIVE, VERY_POSITIVE, TOP_RATING])
        rating_data = get_dummies(data[BINS])
        data = concat([data, rating_data], axis=1)
        return data.reset_index()

    def calculate_time_decay(
            self,
            data: DataFrame
    ) -> DataFrame:
        """
        Find two rating parameters:
        1. Age of most recent view events (in days) = "created_on" (date) to days conversion
        2. time decay factor = 1/age of view events
        Add all 2 above computed parameters as additional attributes in final dataframe
        """
        data = self.define_rating_events(data)

        data = RatingUtils.get_recent_viewed_date(data)
        data = RatingUtils.get_recent_duration(data)

        data[AGE_OF_EVENT] = (date.today() - data[RECENT_DATE]) // timedelta(days=DAYS)
        data[TIME_DECAY_FACTOR] = 1 / data[AGE_OF_EVENT]

        return data

    def calculate_implicit_rating_with_inverse_user_frequency(
            self,
            data: DataFrame
    ) -> DataFrame:
        """
        Inverse user frequency = log(N/(1 + n)), where:
                                 N = Total number of usersto in the catalog
                                 n = total number of top rating events
        """
        data = self.calculate_time_decay(data)

        INVERSE_USER_FREQUENCY = log(RatingUtils.get_number_of_users(data) / (1 + data[TOP_RATING].sum()))
        data = RatingUtils.milliseconds_to_minutes(data)
        data[DURATION_VALUE] = weight_duration * data[RECENT_DURATION] * data[
            TIME_DECAY_FACTOR] * INVERSE_USER_FREQUENCY
        data[TOP_RATING_VALUE] = weight_top_rating * data[TOP_RATING] * data[VIEW_COUNT] * data[
            TIME_DECAY_FACTOR] * INVERSE_USER_FREQUENCY
        data[VERY_POSITIVE_VALUE] = weight_very_positive * data[VERY_POSITIVE] * data[VIEW_COUNT] * data[
            TIME_DECAY_FACTOR] * INVERSE_USER_FREQUENCY
        data[POSITIVE_VALUE] = weight_positive * data[POSITIVE] * data[VIEW_COUNT] * data[
            TIME_DECAY_FACTOR] * INVERSE_USER_FREQUENCY
        data[NOT_SURE_VALUE] = weight_not_sure * data[NOT_SURE] * data[VIEW_COUNT] * data[
            TIME_DECAY_FACTOR] * INVERSE_USER_FREQUENCY

        data[IMPLICIT_RATING_VALUE] = data[DURATION_VALUE] + data[TOP_RATING_VALUE] + data[VERY_POSITIVE_VALUE] + data[
            POSITIVE_VALUE] + data[NOT_SURE_VALUE]

        data = RatingUtils.get_maximum_of_two_implicit_ratings(data)

        data[NORMALISED_IMPLICIT_RATING] = data[IMPLICIT_RATING_VALUE] / data[MAX_RATING]

        data[IMPLICIT_RATING] = RatingUtils.round_partial((SCALING_FACTOR * data[NORMALISED_IMPLICIT_RATING]),
                                                          RESOLUTION)

        data = data[[CUSTOMER_ID, CONTENT_ID, IMPLICIT_RATING, IS_PAY_TV, CONTENT_STATUS, CONTENT_LABEL]]
        # Drop exisiting realtions
        self.drop_relations(data)
        # Dump new relations
        self.dump_relation(data)

        return data

    def drop_relations(
            self,
            data: DataFrame
    ):
        """
        Drop existing Has_Rating relations
        :param data: Dataframe object pandas
        :return: None, updates graphdb
        """
        graph = ANGraphDb.new_connection_config().graph
        for index in range(len(data)):
            node_from = Node.parse_obj({LABEL: USER_LABEL,
                                        PROPERTIES: {CUSTOMER_ID: str(data.loc[index, CUSTOMER_ID])}})
            node_to = Node.parse_obj({LABEL: data.loc[index, CONTENT_LABEL],
                                      PROPERTIES: {CONTENT_ID: int(data.loc[index, CONTENT_ID])}})
            relationship = Relationship.parse_obj({RELATIONSHIP: HAS_RATING})
            try:
                graph.delete_relationship(node_from=node_from, node_to=node_to, rel=relationship)
            except StopIteration:
                logging.warning(f"No HAS_RATING relation found on graph between {node_from} to {node_to}")
            except Exception as e:
                logging.error(f"Unable to drop HAS_RATING relation between {node_from} to {node_to}, Error: {e}")
            finally:
                continue
        graph.connection.close()

    def dump_relation(
            self,
            data: DataFrame):
        """
        Plot has rating relation in graphdb
        :param data: Dataframe object pandas
        :return: None, updates graphdb
        """
        graph = ANGraphDb.new_connection_config().graph
        for index in range(len(data)):
            user_node = Node.parse_obj(
                {
                    LABEL: USER_LABEL,
                    PROPERTIES: {CUSTOMER_ID: str(data.loc[index, CUSTOMER_ID])}
                }
            )
            content_node = Node.parse_obj(
                {
                    LABEL: str(data.loc[index, CONTENT_LABEL]),
                    PROPERTIES: {CONTENT_ID: int(data.loc[index, CONTENT_ID])}
                }
            )
            rel = Relationship.parse_obj({RELATIONSHIP: HAS_RATING,
                                          PROPERTIES: {IMPLICIT_RATING: data.loc[index, IMPLICIT_RATING]}})
            try:
                graph.create_multi_relationship_without_upsert(node_from=user_node, node_to=content_node, rel=rel)
            except Exception as e:
                logging.error(f"Error while creating HAS_RATING relation {user_node} to {content_node} in graphdb, Error: {e}")
        graph.connection.close()
