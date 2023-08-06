"""

"""

from abc import ABCMeta, abstractmethod
from univariate.analyzer import AnalysisReport


class Hook(metaclass=ABCMeta):
    """
    Hook for some act in post analysis, such as storing result, notifying.
    It is intended for multi-threading in future.
    """

    @abstractmethod
    def do_post_analysis(self, report: AnalysisReport):
        pass
