"""

"""

from univariate.analyzer import Analyzer
from univariate.analyzer import AnalysisReport
from univariate.strategy.period import PeriodCalcStrategy, PeriodCalcType
from typing import Dict, Optional
from enum import Enum
import importlib
from pyspark.sql import DataFrame
from pyspark.sql.window import Window
import pyspark.sql.functions as F
import logging

logger = logging.getLogger()


class RegularityAnalyzer(Analyzer):
    """ """

    def __init__(
        self,
        period_strategy_type: PeriodCalcType = PeriodCalcType.ClusteringAndApproximateGCD,
    ):
        """

        :param period_strategy_type: Enum val for calc period strategy, default ClusteringAndApproximateGCD
        """
        concrete_cls = getattr(
            importlib.import_module("univariate.strategy.period"),
            period_strategy_type.value,
        )
        self.period_strategy: PeriodCalcStrategy = concrete_cls()

    def analyze(self, ts: DataFrame, **kwargs) -> AnalysisReport:
        """

        :param ts: Time series spark dataframe containing timestamp, data
        :param time_col_name:
        :return:
        """
        logger.debug("analyze called")
        diff_col_name = kwargs["time_col_name"] + "_diff"
        differenced_timestamp = self.__make_difference_series_of_timestamp(
            ts, kwargs["time_col_name"], diff_col_name
        )
        logger.debug("analyze finish")
        return self.period_strategy.calc_period(differenced_timestamp, diff_col_name)

    def __make_difference_series_of_timestamp(
        self, ts: DataFrame, time_col_name: str, diff_col_name: str
    ) -> DataFrame:
        """

        :param ts:
        :param time_col_name:
        :param diff_col_name:
        :return:
        """
        logger.debug("make difference series of timestamp called")
        window = Window.partitionBy().orderBy(time_col_name)

        diff_df = (
            ts.withColumn(
                diff_col_name,
                F.col(time_col_name) - F.lag(F.col(time_col_name), 1).over(window),
            )
            .select(diff_col_name)
            .na.drop()
        )
        logger.debug("make difference series of timestamp finish")
        return diff_df
        # todo : think less column exception
