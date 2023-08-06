"""

"""

from pyspark.sql import DataFrame


class DuplicateReport:
    """

    """
    # todo: refactor generalization with analysis report, property pattern, report builder and so on
    def __init__(self, duplicate_df: DataFrame):
        self.duplicated = True if duplicate_df.count() > 0 else False
        self.duplicate_df = duplicate_df or None

    def __str__(self):
        pass
