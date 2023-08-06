"""

"""

from abc import ABCMeta, abstractmethod
from enum import Enum
from univariate.analyzer import AnalysisReport
from pyspark.sql import DataFrame


class PeriodCalcType(Enum):
    ClusteringAndApproximateGCD = "ClusteringAndApproximateGCD"


class PeriodCalcStrategy(metaclass=ABCMeta):
    """
    Abstract strategy for calculating regular period between each observation if time series is regular
    """

    @classmethod
    def calc_period(cls, diff_df: DataFrame, diff_col_name: str) -> AnalysisReport:
        pass
