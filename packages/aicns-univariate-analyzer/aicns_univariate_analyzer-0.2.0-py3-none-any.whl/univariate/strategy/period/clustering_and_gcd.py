"""

"""

from univariate.strategy.period import PeriodCalcStrategy
from univariate.analyzer import AnalysisReport
from pyspark.sql import DataFrame
from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from pyspark import SparkContext, SQLContext
import plotly.express as px
import logging

logger = logging.getLogger()


class ClusteringAndApproximateGCD(PeriodCalcStrategy):
    """ """

    @classmethod
    def calc_period(cls, diff_df: DataFrame, diff_col_name: str) -> AnalysisReport:
        """

        :param diff_df:
        :param diff_col_name:
        :return:
        """
        logger.debug("calc period called")
        # 1. Mean shift Clustering  todo : Implement Spark DataFrame-native mean-shift clustering
        diff_array = np.array(diff_df.select(diff_col_name).collect())
        bandwidth = estimate_bandwidth(
            diff_array, quantile=0.5
        )  # todo : adjust quantile index
        bandwidth = round(bandwidth, 3)
        meanshift = MeanShift(bandwidth=bandwidth if bandwidth > 0 else None)
        cluster_labels = meanshift.fit_predict(diff_array)
        cluster_label_df = diff_df.sql_ctx.createDataFrame(
            enumerate(cluster_labels.tolist(), start=1), ["id", "label"]
        )
        clustered_diff_df = diff_df.withColumn(
            "id", F.row_number().over(Window.orderBy(F.monotonically_increasing_id()))
        ).join(
            cluster_label_df, on="id", how="inner"
        )  # todo: no partition window operation will move all data to a single partition
        clustered_diff_df.cache()

        # 2. approximated gcd  todo : enhance algorithm
        period = -1
        preset_unit = 1000  # todo : parameterize
        stopping_criteria: bool = False
        while not stopping_criteria:
            max_label = (
                clustered_diff_df.groupBy("label")
                .agg(F.count("*").alias("label_cnt"))
                .sort(F.col("label_cnt").desc())
                .first()
                .asDict()["label"]
            )
            period = (
                clustered_diff_df.filter(cluster_label_df["label"] == max_label)
                .agg(F.mean(diff_col_name).alias("period"))
                .first()
                .asDict()["period"]
                // preset_unit
                * preset_unit
            )
            stopping_criteria = True

        # 2-1. (optional) leave outlier cluster out # todo

        # 3. make a decision & report  # todo: enhance todo: report builder
        report = AnalysisReport()
        # 3-1. Period, Error, Regularity
        if period is not -1:
            report.parameters["period"] = period
            report.parameters["periodic_error"] = None
            report.parameters["regularity"] = "regular"
        else:
            report.parameters["regularity"] = "irregular"
        # 3-2. Report diff distribution, plot histogram
        report.parameters["distribution"] = clustered_diff_df
        # 3-3. Plot scatter one-dimension clustered time diff
        report_df = clustered_diff_df.withColumn("title", F.lit(diff_col_name))
        report.plots["cluster"] = px.scatter(
            report_df.toPandas(),
            y="title",
            x=diff_col_name,
            color="label",
            symbol="label",
        )

        # 3-4. Count missing value
        # 3-5. Outlier detect, plot, and do processing
        # 3-6. Explainable Validation report(p-value, Prediction interval...)
        logger.debug("calc period finish")
        return report
