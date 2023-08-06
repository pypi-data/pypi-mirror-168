"""

"""
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, LongType
from pyspark.sql.window import Window
import numpy as np
from univariate.analyzer import AnalysisReport
from univariate.missing_value.strategy.unmarked_detection import (
    UnmarkedMissingValueDetectionStrategy,
)


@udf(ArrayType(LongType()))
def span_udf(start, end, num):
    return (
        np.round(np.linspace(start=start, stop=end, num=int(num), endpoint=False)[1:])
        .astype(np.int_)
        .tolist()
    )


class DivideAndRound(UnmarkedMissingValueDetectionStrategy):
    """ """

    @staticmethod
    def detect(
        ts: DataFrame,
        time_col_name: str,
        data_col_name: str,
        regularity_report: AnalysisReport,
    ) -> DataFrame:
        """

        :param ts:
        :param time_col_name:
        :param data_col_name:
        :param regularity_report:
        :return: 'Null' interleaved dataframe as detected unmarked missing values
        """
        # todo: enhance algorithm
        # 1. Divide and Round
        bias = -0.2
        divide_df = (
            ts.select([time_col_name, data_col_name])
            .sort(time_col_name)
            .withColumn(
                "lagged_time", F.lag(time_col_name).over(Window.orderBy(time_col_name))
            )
            .withColumn(
                "ratio_by_period",
                (F.col(time_col_name) - F.col("lagged_time"))
                / regularity_report.parameters["period"],
            )
        )
        round_df = divide_df.filter("ratio_by_period >= 1.7").withColumn(
            "estimated_missing_count", F.round(F.col("ratio_by_period") - F.lit(bias))
        )

        # 2. Interleave null values
        estimated_unmarked_missing_df = round_df.withColumn(
            "missing_timestamps",
            span_udf("lagged_time", time_col_name, "estimated_missing_count"),
        ).select(
            F.explode("missing_timestamps").alias(time_col_name),
            F.lit(None).alias(data_col_name),
        )

        # 3. merge and sort
        interleaved_df = (
            ts.select([data_col_name, time_col_name])
            .unionByName(estimated_unmarked_missing_df)
            .sort(time_col_name)
        )
        return interleaved_df
