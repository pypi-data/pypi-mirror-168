"""

"""

from enum import Enum
from abc import ABCMeta, abstractmethod
from pyspark.sql import DataFrame


class MissingValueHandleStrategyType(Enum):
    deletion = "Deletion"
    mean_imputation = "MeanImputation"
    median_imputation = "MedianImputation"
    mode_imputation = "ModeImputation"
    zero_imputation = "ZeroImputation"
    constant_imputation = "ConstantImputation"
    # k_nn_imputation = "KNNImputation" #multi
    # mice_imputation = "MICEImputation" #multi
    hot_deck_imputation = "HOT_DECK_IMPUTATION"
    datawig = "Datawig"
    interpolation = "Interpolation"  # todo: SOTA
    # todo: continous update
    # todo: where cross-informated strategy will be
    # todo: enhance
    # todo: process exceptions with sufficient test coverage


class MissingValueHandleStrategy(metaclass=ABCMeta):
    """
    Missing
    """

    @abstractmethod
    def handle(
        self, missed_ts: DataFrame, time_col_name: str, data_col_name
    ) -> DataFrame:
        pass
