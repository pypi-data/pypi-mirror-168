"""
    Univariate Time Series Analyzer module
"""

from pyspark.sql import DataFrame
from typing import Optional, List
from univariate.hook import Hook
from univariate.analyzer import (
    AnalysisReport,
    Analyzer,
    RegularityAnalyzer,
    DescriptiveStatAnalyzer,
)
from univariate.ts_validator import Validator
from univariate.duplicate import DuplicateProcessor, DuplicateReport
import logging

logger = logging.getLogger()


class UnivariateAnalyzer:
    """
    Univariate Time Series Analyzer
    """

    def __init__(
        self,
        ts: DataFrame,
        val_col: str = "value",
        time_col: str = "time",
        hooks: Optional[List[Hook]] = [],
        validators: Optional[List[Validator]] = [],
        drop_duplicates: bool = True,
    ):
        """

        :param ts: Spark dataframe that has one datatime column, and has one timeseries value(float or number) column
        :param val_col: string column name containing timeseries values
        :param time_col: string column name containing pyspark.sql.DatetimeType
        :param hooks: list of hooks that want to be notified analysis reports
        """
        logger.debug(
            f"Setup Analyzer start, ts: {ts}, val_col: {val_col}, time_col: {time_col}, hooks: {hooks or '[]'}"
        )
        self.validators: List[
            Validator
        ] = validators  # todo : default validator  # todo : who is creator that has responsibility
        self.duplicate_report: DuplicateReport = DuplicateProcessor.detect_duplicates(ts=ts, time_col_name=time_col, data_col_name=val_col)
        if drop_duplicates and self.duplicate_report.duplicated:
            ts = DuplicateProcessor.drop_duplicates(ts=ts)
        self.__validate_ts(ts=ts, time_col_name=time_col, data_col_name=val_col)
        self.hooks: List[Hook] = hooks  # todo : default post analysis hook
        self.ts: DataFrame = ts.sort(time_col).select([time_col, val_col])
        self.analysis_queue: List[Analyzer] = list()
        self.time_col_name: str = time_col
        self.data_col_name: str = val_col

        regularity_analyzer: Analyzer = RegularityAnalyzer()
        self.regularity_report: AnalysisReport = regularity_analyzer.analyze(
            ts=self.ts, time_col_name=time_col
        )
        self.__notify_report(self.regularity_report)
        self.__enqueue_analysis_job()
        logger.debug("Setup Analyzer finish")

    def __validate_ts(self, ts: DataFrame, time_col_name: str, data_col_name: str):
        """
        If has validation error, it raise exception
        :param val_col:
        :param time_col:
        :return:
        """
        logger.debug("Validate ts")
        for validator in self.validators:
            validator(ts=ts, time_col_name=time_col_name, data_col_name=data_col_name)
        # map(lambda validator: validator(ts=ts, time_col_name=time_col_name, data_col_name=data_col_name), self.validators)

    def __notify_report(self, report: AnalysisReport):
        map(lambda hook: hook.do_post_analysis(report), self.hooks)
        logger.debug("Notify all hook")
        logger.debug("Notify hook finish")

    def __enqueue_analysis_job(self):
        """

        :return:
        """
        logger.debug("enqueue analysis job start")
        if self.regularity_report.parameters["regularity"] == "regular":
            logger.debug("regularity: regular")
            self.analysis_queue.append(DescriptiveStatAnalyzer())
            pass
        elif self.regularity_report.parameters["regularity"] == "irregular":
            logger.debug("regularity: irregular")
            pass
        logger.debug("enqueue analysis job finish")

    def analyze(self):
        """

        :return:
        """
        logger.debug("analyze called")

        reports = list(
            map(
                lambda job: job.analyze(
                    ts=self.ts,
                    time_col_name=self.time_col_name,
                    data_col_name=self.data_col_name,
                ),
                self.analysis_queue,
            )
        )  # todo : Explore parallezing with spark sub(child) context & python asyncio?
        map(
            lambda report: map(lambda hook: hook.do_post_analysis(report), self.hooks),
            reports,
        )
        """
        reports = []
        for job in self.analysis_queue:
            report = job.analyze(ts=self.ts, time_col_name=self.time_col_name, data_col_name=self.data_col_name)
            reports.append(report)
        """  # todo : clean dummy code
        logger.debug("analyze return")
        return reports
