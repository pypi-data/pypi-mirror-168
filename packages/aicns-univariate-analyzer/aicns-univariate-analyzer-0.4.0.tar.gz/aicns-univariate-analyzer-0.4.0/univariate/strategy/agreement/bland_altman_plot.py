"""

"""

from univariate.strategy.agreement import AgreementStrategy
from univariate.analyzer import AnalysisReport
from pyspark.sql import DataFrame


class BlandAltmanPlot(AgreementStrategy):
    """ """

    @classmethod
    def measure_agreement(cls, sample: DataFrame) -> AnalysisReport:
        pass
