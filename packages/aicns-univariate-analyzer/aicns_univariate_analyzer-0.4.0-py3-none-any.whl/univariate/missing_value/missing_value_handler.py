"""

"""

from pyspark.sql import DataFrame
from univariate.missing_value import MissingValueReport
from univariate.missing_value.strategy.handle_missing_value import MissingValueHandleStrategy
import importlib

class MissingValueHandler:
    """
    It can handle missing value with some strategies, such as imputation, deletion, filling constant, interpolation, and so on
    """
    def handle_missing_value(self, missed_ts: DataFrame, time_col_name: str, data_col_name: str) -> DataFrame:
        """

        :param ts:
        :param report:
        :return:
        """
        # todo: decision logic decoupling, decision rule-engine?
        # Instantiate
        concrete_cls = getattr(
            importlib.import_module("univariate.missing_value.strategy.handle_missing_value"),
            "MeanImputation"
        )
        handling_strategy: MissingValueHandleStrategy = concrete_cls()
        return handling_strategy.handle(missed_ts=missed_ts, time_col_name=time_col_name, data_col_name=data_col_name)
