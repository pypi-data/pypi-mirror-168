"""
Standard output hook
"""

from univariate.hook import Hook
from univariate.analyzer import AnalysisReport


class StdoutHook(Hook):
    """
    Stdout Concrete hook for develop
    """

    def do_post_analysis(self, report: AnalysisReport):
        """
        Print metrics, parameters, plots

        :return:
        """
        print("parameters:")
        for parameter_key in report.parameters.keys():
            print(f"/t{parameter_key}: {report.parameters[parameter_key]}")
        print()

        print("metrics:")
        for metric_key in report.metrics.keys():
            print(f"/t{metric_key}: {report.metrics[metric_key]}")
        print()

        print("plot:")
        for plot_key in report.plots.keys():
            report.plots[plot_key].show()
