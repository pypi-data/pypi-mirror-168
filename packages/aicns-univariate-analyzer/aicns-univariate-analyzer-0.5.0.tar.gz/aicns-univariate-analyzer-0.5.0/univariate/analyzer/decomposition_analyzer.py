"""

"""

from univariate.analyzer import Analyzer
from univariate.analyzer import AnalysisReport
from pyspark.sql import DataFrame
import plotly.express as px
from enum import Enum, auto
from statsmodels.tsa.seasonal import STL


class SeasonType(Enum):
    HOURLY = auto()
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()
    QUARTERLY = auto()
    YEARLY = auto()

class DecompositionAnalyzer(Analyzer):
    """
    Decompose Time series
    """
    def __init__(self):
        """

        """
        # todo: decide decomposition strategy
        pass

    def analyze(self, ts: DataFrame, time_col_name: str, data_col_name: str, ) -> AnalysisReport:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :return:
        """
        period = self.__calc_period(ts, time_col_name)
        stl = STL(ts.select(data_col_name).toPandas().values.reshape((-1,)), period=period).fit()  # todo: strategies for ts decompositions  #todo: multi seasonal

        report = AnalysisReport()
        report.parameters["observed"] = stl.observed
        report.parameters["trend"] = stl.trend
        report.parameters["seasonal"] = stl.seasonal
        report.parameters["resid"] = stl.resid

        report.plots["observed"] = px.line(stl.observed)
        report.plots["seasonal"] = px.line(stl.seasonal)
        report.plots["trend"] = px.line(stl.trend)
        report.plots["resid"] = px.line(stl.resid)

        return report

    def __calc_period(self, ts: DataFrame, time_col_name: str, season_type: SeasonType=SeasonType.WEEKLY):
        # todo:
        temp = 144
        return temp
