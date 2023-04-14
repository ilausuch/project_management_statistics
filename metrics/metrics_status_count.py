from datetime import datetime, timedelta
from datetime import date as Date
from metrics.metrics_result import MetricsResults, MetricsTimeSeries  # pylint: disable=import-error,no-name-in-module


class MetricsStatusCount:
    def __init__(self, query_manager):
        self.query_manager = query_manager

    def _status_count(self, issues_list):
        """
        Internal function to classify the issues by status and return the ammount in each category
        :param issues_list: List of issues (dict)
        :return: A dict with the format <status:count>
        """
        status_counters = {}
        for issue in issues_list:
            status = str(issue["status"])
            if status not in status_counters:
                status_counters[status] = 0

            status_counters[status] = status_counters[status] + 1

        return status_counters

    def status_count(self, extract_metadata=[], **filters):
        """
        Classify the issues by status and return the ammount in each category
        :param filter: A dict of filters e.g. project=1
        :return: A dict with the format <status:count>
        """
        issues = self.query_manager.issues(**filters)
        status_counters = self._status_count(issues)
        metadata = {}
        if issues:
            first_issue = issues[0]
            for key in extract_metadata:
                metadata[key] = first_issue[key]

        return MetricsResults(data=status_counters, metadata=metadata)

    def status_count_by_date(self, date, extract_metadata=[], **filters):
        """
        Classify the issues by status and return the ammount in each category
        :param filter: A dict of filters e.g. project=1
        :return: A dict with the format <status:count>
        """
        issues = self.query_manager.status_snapshot(date, **filters)
        status_counters = self._status_count(issues)
        metadata = {}
        if issues:
            first_issue = issues[0]
            for key in extract_metadata:
                metadata[key] = first_issue[key]

        return MetricsResults(data=status_counters, metadata=metadata)

    def status_count_by_date_range(self, start_date, end_date, extract_metadata=[], increment_days=1, **filters):
        """
        Classify the issues by status and return the amount in each category for each date within the given range
        :param start_date: Starting date of the range
        :param end_date: Ending date of the range
        :param extract_metadata: List of metadata keys to extract
        :param date_increment: Number of days between consecutive dates in the range (default is 1)
        :param filters: Additional filters as keyword arguments
        :return: A MetricsTimeSeries object with the aggregated status counts by date
        """
        if isinstance(start_date, Date) and not isinstance(start_date, datetime):
            start_date = datetime.combine(start_date, datetime.min.time())
        if isinstance(end_date, Date) and not isinstance(end_date, datetime):
            end_date = datetime.combine(end_date, datetime.min.time())

        current_date = start_date
        delta = timedelta(days=increment_days)
        results = MetricsTimeSeries()

        while current_date <= end_date:
            date_result = self.status_count_by_date(current_date, extract_metadata, **filters)
            date_data = {**date_result.metadata, **date_result.data}
            date_data["date"] = current_date
            results.add_date(current_date, date_data)
            current_date += delta
        results.force_zeros()

        return results
