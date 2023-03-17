from datetime import datetime
from metrics.metrics_result import MetricsResults  # pylint: disable=import-error,no-name-in-module


class Metrics:

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

    def status_count(self, **filters):
        """
        Classify the issues by status and return the ammount in each category
        :param filter: A dict of filters e.g. project=1
        :return: A dict with the format <status:count>
        """
        issues = self.query_manager.issues(**filters)
        status_counters = self._status_count(issues)
        if issues:
            first_issue = issues[0]
            project = first_issue['project']
            filters['project'] = project
        result = MetricsResults(dict(filters))
        result.append_values(status_counters, datetime.now())
        return result

    def status_count_by_date(self, date, **filters):
        """
        Classify the issues by status and return the ammount in each category
        :param filter: A dict of filters e.g. project=1
        :return: A dict with the format <status:count>
        """
        issues = self.query_manager.status_snapshot(date, **filters)
        status_counters = self._status_count(issues)
        if issues:
            project = issues[0]['project']
            filters['project'] = project
        result = MetricsResults(dict(filters))
        result.append_values(status_counters, date)
        return result
