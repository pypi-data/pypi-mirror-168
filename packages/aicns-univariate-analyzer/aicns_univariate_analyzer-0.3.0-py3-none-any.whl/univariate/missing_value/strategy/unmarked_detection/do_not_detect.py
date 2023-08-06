"""

"""

from univariate.missing_value.strategy.unmarked_detection import (
    UnmarkedMissingValueDetectionStrategy,
)
from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport


class DoNotDetect(UnmarkedMissingValueDetectionStrategy):
    """
    Do nothing
    """

    @staticmethod
    def detect(
        ts: DataFrame,
        time_col_name: str,
        data_col_name: str,
        regularity_report: AnalysisReport,
    ) -> DataFrame:
        return ts
