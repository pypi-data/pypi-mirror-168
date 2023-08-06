"""

"""

from univariate.duplicate import DuplicateReport
from pyspark.sql import DataFrame
import logging

logger = logging.getLogger()


class DuplicateProcessor:
    """

    """

    @staticmethod
    def detect_duplicates(ts: DataFrame, time_col_name: str, data_col_name: str) -> DuplicateReport:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :return:
        """
        duplicate_df = ts.groupBy([time_col_name, data_col_name]).count().where('count > 1')
        report = DuplicateReport(duplicate_df)
        return report

    @staticmethod
    def drop_duplicates(ts: DataFrame) -> DataFrame:
        """

        :param ts:
        :return:
        """
        distinct_df = ts.distinct()
        logger.info("Duplicates dropped")
        return distinct_df
