"""

"""

from univariate.missing_value.strategy.handle_missing_value import (
    MissingValueHandleStrategy,
)
from pyspark.sql import DataFrame


class Interpolation(MissingValueHandleStrategy):
    """
    # todo : specify interpolation methods, and think about how to deal with sporadic data?
    https://medium.com/delaware-pro/interpolate-big-data-time-series-in-native-pyspark-d270d4b592a1
    """

    # todo: if ts is sporadic, then strategy decision must block use this

    def handle(
        self, missed_ts: DataFrame, time_col_name: str, data_col_name
    ) -> DataFrame:
        pass
