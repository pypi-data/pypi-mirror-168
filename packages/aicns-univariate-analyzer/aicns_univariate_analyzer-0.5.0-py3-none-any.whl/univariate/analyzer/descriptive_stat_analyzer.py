"""
 Descriptive Statistics analyzer
"""

from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark import StorageLevel
from pyspark.sql.types import TimestampType
from univariate.analyzer import Analyzer, AnalysisReport
import logging
import plotly.express as px
import plotly.figure_factory as ff
from scipy.stats import gaussian_kde


logger = logging.getLogger()


class DescriptiveStatAnalyzer(Analyzer):
    """
    Descriptvie Statistics analyzer
    Items
      - count
      - mean (arithmetic, geometric, harmonic)
      - mode, median
      - max, min
      - std dev
      - skewness
      - kurtosis
      - coefficient of variation
    """

    def __init__(self):
        """ """

    def analyze(self, ts: DataFrame, **kwargs) -> AnalysisReport:
        """

        :return:
        """
        # todo: refactor long method
        logger.debug("analyze called")
        ts_df = (
            ts.select(kwargs["data_col_name"])
            .dropna()
            .persist(StorageLevel.MEMORY_ONLY)
        )
        ts_np_array = ts_df.toPandas().to_numpy()
        report = AnalysisReport()

        # 1. Aggregate (max, min, mean, median, count, stddev, skewness, kurtosis)
        stats_dict = (
            ts_df.agg(
                F.max(kwargs["data_col_name"]).alias("max"),
                F.min(kwargs["data_col_name"]).alias("min"),
                F.count(kwargs["data_col_name"]).alias("count"),
                F.mean(kwargs["data_col_name"]).alias("mean"),
                F.percentile_approx(kwargs["data_col_name"], percentage=0.5).alias(
                    "median"
                ),
                F.percentile_approx(kwargs["data_col_name"], percentage=0.25).alias(
                    "Q1"
                ),
                F.percentile_approx(kwargs["data_col_name"], percentage=0.7).alias(
                    "Q3"
                ),
                F.stddev_samp(kwargs["data_col_name"]).alias("stddev"),
                F.skewness(kwargs["data_col_name"]).alias("skewness"),
                F.kurtosis(kwargs["data_col_name"]).alias("kurtosis"),
            )
            .first()
            .asDict()
        )

        # 2. mode # todo: except iid
        stats_dict["mode"] = (
            ts_df.groupBy(kwargs["data_col_name"])
            .count()
            .orderBy("count", ascending=False)
            .first()[0]
        )

        # 3. coefficient of variation
        stats_dict["cv"] = stats_dict["stddev"] / stats_dict["mean"]

        report.parameters = stats_dict.copy()

        # 4. histogram (with max, min, mean, median, mode)
        histogram = px.histogram(ts_df.toPandas(), x="input_data", marginal="violin")
        histogram.add_vline(
            x=stats_dict["min"], annotation_text="min", line_width=1, line_dash="dash"
        )
        histogram.add_vline(
            x=stats_dict["max"], annotation_text="max", line_width=1, line_dash="dash"
        )
        histogram.add_vline(
            x=stats_dict["mode"], annotation_text="mode", line_width=1, line_dash="dash"
        )
        report.plots["histogram"] = histogram

        # 2. timeseries plot with range slider
        timeseries_plot = px.line(
            ts.withColumn(
                kwargs["time_col_name"],
                (ts[kwargs["time_col_name"]] / 1000).cast(TimestampType()),
            )
            .select(kwargs["data_col_name"], kwargs["time_col_name"])
            .toPandas(),
            x=kwargs["time_col_name"],
            y=kwargs["data_col_name"],
            title="Time Series with Range Slider and Selector",
        )
        timeseries_plot.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
        )
        report.plots["timeseries_plot"] = timeseries_plot

        # 5. dist plot (density curve, skewness, median, mean, mode)
        pallete = px.colors.qualitative.Plotly
        dist_plot = ff.create_distplot(
            ts_np_array.reshape((1, -1)), group_labels=["input_data"], show_hist=False
        )  # from plotly-python v5.10.0, curve is estimated 'kde'
        dist_plot.update_layout(title_text="Density Curve")
        kde = gaussian_kde(ts_np_array.reshape((-1,)))
        dist_plot.add_shape(
            type="line",
            x0=stats_dict["mean"],
            x1=stats_dict["mean"],
            y0=0.0,
            y1=kde(stats_dict["mean"])[0],
            opacity=0.5,
            name="mean",
            line_dash="dash",
            line=dict(color=pallete[0], width=2),
        )
        dist_plot.add_annotation(
            x=stats_dict["mean"],
            y=kde(stats_dict["mean"])[0],
            text="mean",
            font=dict(color=pallete[0]),
            arrowcolor=pallete[0],
        )
        dist_plot.add_shape(
            type="line",
            x0=stats_dict["mean"],
            x1=stats_dict["mean"],
            y0=0.0,
            y1=kde(stats_dict["mean"])[0],
            opacity=0.5,
            name="mode",
            line_dash="dash",
            line=dict(color=pallete[1], width=2),
        )
        dist_plot.add_annotation(
            x=stats_dict["mean"],
            y=kde(stats_dict["mean"])[0],
            text="mode",
            font=dict(color=pallete[1]),
            arrowcolor=pallete[1],
        )
        dist_plot.add_shape(
            type="line",
            x0=stats_dict["median"],
            x1=stats_dict["median"],
            y0=0.0,
            y1=kde(stats_dict["median"])[0],
            opacity=0.5,
            name="median",
            line_dash="dash",
            line=dict(color=pallete[2], width=2),
        )
        dist_plot.add_annotation(
            x=stats_dict["median"],
            y=kde(stats_dict["median"])[0],
            text="median",
            font=dict(color=pallete[2]),
            arrowcolor=pallete[2],
        )
        dist_plot.add_annotation(
            text=f"<b>mean</b>: {round(stats_dict['mean'], 3)}<br>"
            f"<b>mode</b>: {round(stats_dict['mode'], 3)}<br>"
            f"<b>Q1</b>: {round(stats_dict['Q1'], 3)}<br>"
            f"<b>Q2(median)</b>: {round(stats_dict['median'], 3)}<br>"
            f"<b>Q3</b>: {round(stats_dict['Q3'], 3)}<br>"
            f"<b>skewness</b>: {round(stats_dict['skewness'], 3)}<br>"
            f"<b>kurtosis</b>: {round(stats_dict['kurtosis'], 3)}<br>"
            f"<b>coefficient of variation</b>: {round(stats_dict['cv'], 3)}",
            align="right",
            showarrow=False,
            xref="paper",
            x=1,
            yref="paper",
            y=1,
        )
        report.plots["dist_plot"] = dist_plot

        return report
