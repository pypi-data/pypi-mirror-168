"""

"""

from abc import ABCMeta, abstractmethod
from pyspark.sql import DataFrame


class Validator(metaclass=ABCMeta):
    """
    Callable validator then ts is valid, before analyze
    """

    @abstractmethod
    def __call__(self, ts: DataFrame, **kwargs):
        pass
