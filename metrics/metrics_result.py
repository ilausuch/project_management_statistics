from typing import List, Dict
from datetime import datetime


class MetricsResultsEntry:
    def __init__(self, values: List, date: datetime):
        self.values = values
        self.date = date


class MetricsResults:
    def __init__(self, filters: Dict = {}, metadata: Dict = None, entries: List = None):
        self.filters = filters
        self.metadata = metadata
        if entries is not None:
            self.entries = entries
        else:
            self.entries = []

    def append_values(self, values: List, date: datetime):
        self.append(MetricsResultsEntry(values, date))

    def append(self, entry: MetricsResultsEntry):
        self.entries.append(entry)

    def append_results(self, other: 'MetricsResults'):
        self.entries.extend(other.entries)
        if self.filters and other.filters and self.filters != other.filters:
            raise ValueError("The filters dicts are not equal.")
        self.filters.update(other.filters or {})
        if not self.metadata and other.metadata:
            self.metadata = other.metadata
        elif self.metadata and other.metadata and self.metadata != other.metadata:
            raise ValueError("The metadata dicts are not equal.")

    def get_first(self):
        return self.entries[0]

    def value_keys(self):
        return self.get_first().values.keys()

    def filter_keys(self):
        return self.filters.keys()

    def import_entries(self, metric_result_list: List):
        for metric_result in metric_result_list:
            if metric_result is not self:
                if self.metadata is None:
                    self.metadata = metric_result.metadata
                elif self.metadata and metric_result.metadata and self.metadata != metric_result.metadata:
                    raise ValueError("The metadata dicts are not equal.")

                if self.filters is None or len(self.filters) == 0:
                    self.filters = metric_result.filters
                else:
                    if self.filters != metric_result.filters:
                        raise ValueError("The filters dicts are not equal.")
                    self.filters.update(metric_result.filters or {})

                for entry in metric_result.entries:
                    self.append(entry)
