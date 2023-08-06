"""

"""

from univariate.missing_value.strategy.handle_missing_value import (
    MissingValueHandleStrategy,
)
from pyspark.sql import DataFrame
import pyspark.sql.functions as F


class MeanImputation(MissingValueHandleStrategy):
    """ """

    def handle(
        self, missed_ts: DataFrame, time_col_name: str, data_col_name
    ) -> DataFrame:
        return missed_ts.fillna(
            value=round(missed_ts.agg(F.mean(data_col_name)).first()[0], 3),
            subset=data_col_name,
        )
