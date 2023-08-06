"""

"""

from pyspark.sql import DataFrame
from univariate.analyzer import AnalysisReport
from univariate.missing_value.helper import ParseReportException
from univariate.missing_value.strategy.unmarked_detection import UnmarkedMissingValueDetectionStrategyType, UnmarkedMissingValueDetectionStrategy
from univariate.missing_value import MissingValueReport
from typing import Optional
import pyspark.sql.functions as F
import logging
import importlib

logger = logging.getLogger()


class MissingValueDetector:
    """
    Detect missing value in univariate time series
    If time series is 'regular', it can detect marked and unmarked missing value.


    If time series is 'irregular' for now, it can only detect marked missing value, not unmarked.
    """
    # todo: support 'irregular' time series mssing value processing
    regularity_report: AnalysisReport
    unmarked_strategy: UnmarkedMissingValueDetectionStrategy

    def __init__(self, regularity_report: AnalysisReport, unmarked_detection_strategy_type: Optional[UnmarkedMissingValueDetectionStrategyType]=None, marked_only: bool=False):
        """

        :param regularity_report:
        :param unmarked_detection_strategy_type: Enum type. If it is None strategy will depend on default strategy
        :param marked_only: If marked_only is True, then detect both marked and unmarked missing value.
                            if marked_only is False, then detect only marked missing value.
        """
        if "regularity" not in regularity_report.parameters.keys():
            logger.error("Can't parse regularity report")
            raise ParseReportException(msg="Can't parse regularity report")

        self.regularity_report = regularity_report
        self.__instantiate_unmarked_detector(unmarked_detection_strategy_type, marked_only)

    def __instantiate_unmarked_detector(self, strategy_type: Optional[UnmarkedMissingValueDetectionStrategyType], marked_only: bool):
        logger.debug("__instatntiate_unmarked_detector is called")
        if marked_only:
            strategy_type = UnmarkedMissingValueDetectionStrategyType.do_not_detect
        elif strategy_type is None and self.regularity_report.parameters["regularity"] == "regular":
            strategy_type = UnmarkedMissingValueDetectionStrategyType.divide_and_round  # todo: configurable
        elif strategy_type is None and self.regularity_report.parameters["regularity"] == "irregular":
            strategy_type = UnmarkedMissingValueDetectionStrategyType.do_not_detect  # todo: configurable
        logger.info(f"unmarked_detection strategy type: {strategy_type.value}")
        print(f"unmarked_detection strategy type: {strategy_type.value}")

        # Instantiate
        concrete_cls = getattr(
            importlib.import_module("univariate.missing_value.strategy.unmarked_detection"),
            strategy_type.value,
        )
        self.unmarked_strategy = concrete_cls()

    def detect_missing_values(self, ts: DataFrame, time_col_name: str, data_col_name: str) -> MissingValueReport:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :return:
        """
        # todo: how to handle time col missing value (deletion?)
        # todo: enhance report
        report = MissingValueReport()

        # 1. marked missing values
        report.marked["count"] = ts.select([F.count(F.when(F.isnan(data_col_name) | F.col(data_col_name).isNull() , True))]).first()[0]

        # 2. unmarked missing values
        marked_df = self.unmarked_strategy.detect(ts=ts, time_col_name=time_col_name, data_col_name=data_col_name, regularity_report=self.regularity_report).cache()
        report.unmarked["count"] = marked_df.count() - ts.count()
        report.unmarked["marking_df"] = marked_df

        # 3. total
        report.total["count"] = report.marked["count"] + report.unmarked["count"]
        # todo: enhance report
        return report
