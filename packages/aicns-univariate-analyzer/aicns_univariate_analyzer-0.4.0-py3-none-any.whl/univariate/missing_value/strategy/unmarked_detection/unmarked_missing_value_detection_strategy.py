"""

"""

from enum import Enum
from abc import ABCMeta
from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport


class UnmarkedMissingValueDetectionStrategyType(Enum):
    divide_and_round = "DivideAndRound"
    do_not_detect = "DoNotDetect"


class UnmarkedMissingValueDetectionStrategy(metaclass=ABCMeta):
    """ """

    @staticmethod
    def detect(
        ts: DataFrame,
        time_col_name: str,
        data_col_name: str,
        regularity_report: AnalysisReport,
    ) -> DataFrame:
        pass
