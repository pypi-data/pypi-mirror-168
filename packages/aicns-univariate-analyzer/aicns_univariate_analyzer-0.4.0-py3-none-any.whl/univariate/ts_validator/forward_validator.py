"""

"""

import logging
from univariate.ts_validator import Validator
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from univariate.ts_validator.helper import NonMonotonicForwardException

logger = logging.getLogger()


class ForwardValidator(Validator):
    """
    Validate ts has monotonic forward timestamps only, not backward and equal
    """

    def __call__(self, ts: DataFrame, **kwargs):
        logger.debug("Forward validator called")
        lagged_time_ts = (
            ts.select(kwargs["time_col_name"])
            .withColumn("idx", F.monotonically_increasing_id())
            .withColumn(
                "lagged_time",
                F.lag(kwargs["time_col_name"]).over(Window.orderBy("idx")),
            )
        )
        non_forward_ts = (
            lagged_time_ts.withColumn(
                "diff",
                lagged_time_ts[kwargs["time_col_name"]] - lagged_time_ts["lagged_time"],
            )
            .filter(F.col("diff") <= 0.0)
            .cache()
        )
        if non_forward_ts.count() > 0:  # invalid ts
            msg = (
                "Time series has invalid timestamp, with non-monotonic forward increasing. check this\n"
                + non_forward_ts.toPandas().to_string()
            )
            non_forward_ts.unpersist()
            logger.error(msg)
            raise NonMonotonicForwardException(msg=msg)
        logger.info("Forward validation success!")
        non_forward_ts.unpersist()
