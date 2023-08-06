"""

"""

from abc import ABCMeta, abstractmethod
from enum import Enum
from univariate.analyzer import AnalysisReport
from pyspark.sql import DataFrame


class AgreementType(Enum):
    BLAND_ALTMAN = "BlandAltmanPlot"


class AgreementStrategy(metaclass=ABCMeta):
    """
    Abstract strategy for making a decision that sample set values are agreed.
    """

    @classmethod
    def measure_agreement(cls, sample: DataFrame) -> AnalysisReport:
        pass
