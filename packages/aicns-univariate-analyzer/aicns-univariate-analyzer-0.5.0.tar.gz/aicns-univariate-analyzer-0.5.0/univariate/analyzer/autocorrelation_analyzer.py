"""

"""

from univariate.analyzer import Analyzer
from univariate.analyzer import AnalysisReport
from pyspark.sql import DataFrame
from statsmodels.tsa.stattools import pacf, acf
import plotly.graph_objects as go
import numpy as np


class AutocorrelationAnalyzer(Analyzer):
    """ """
    def analyze(self, ts: DataFrame, data_col_name: str, regularity_report: AnalysisReport) -> AnalysisReport:
        """
        Analyze autocorrelation. Missing values will be ignored
        :param ts: DataFrame has to be sorted by col(time_col_name)
        :param time_col_name:
        :param data_col_name:
        :param regularity_report: Yielded by Univariate Analyzer
        :return:
        """
        # todo: Deep-unstand how statsmodels handle missing values
        # todo: this version is only for regular, so have to diverge strategies by regular and irregular

        num_lags = ts.count()  # todo: adjusted nlags (priority: high)
        plot_pacf = False  # todo: what is pacf, what is diff
        corr_array = pacf(ts.select(data_col_name).toPandas().values.reshape((-1,)), alpha=0.05, missing="conservative", nlags=num_lags) if plot_pacf else acf(ts.select(data_col_name).toPandas().values.reshape((-1,)),
                                                                                                       alpha=0.05,
                                                                                                       missing="conservative",
                                                                                                       nlags=num_lags)
        lower_confident_interval = corr_array[1][:, 0] - corr_array[0]  # todo: have to know which algorithm used to find the confidence interval
        upper_confident_interval = corr_array[1][:, 1] - corr_array[0]

        correlogram = go.Figure()
        [correlogram.add_scatter(x=(x, x), y=(0, corr_array[0][x]), mode='lines', line_color='#3f3f3f', line_width=0.6)
         for x in range(len(corr_array[0]))]  # todo: adjusted line_width
        correlogram.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4')
        correlogram.add_scatter(x=np.arange(len(corr_array[0])), y=upper_confident_interval, mode='lines', line_color='rgba(255,255,255,0)')
        correlogram.add_scatter(x=np.arange(len(corr_array[0])), y=lower_confident_interval, mode='lines', fillcolor='rgba(32, 146, 230,0.3)',
                        fill='tonexty', line_color='rgba(255,255,255,0)')
        correlogram.update_traces(showlegend=False)
        # fig.update_xaxes(range=[-1,42])
        correlogram.update_yaxes(zerolinecolor='#000000')

        title = 'Partial Autocorrelation (PACF)' if plot_pacf else 'Autocorrelation (ACF)'
        correlogram.update_layout(title=title)

        # Build report
        report = AnalysisReport()

        report.parameters["acf"] = corr_array[0].tolist()
        report.parameters["num_lags"] = num_lags
        report.parameters["lower_confident_interval"] = lower_confident_interval.tolist()
        report.parameters["upper_confident_interval"] = upper_confident_interval.tolist()

        report.plots["correlogram"] = correlogram

        return report
