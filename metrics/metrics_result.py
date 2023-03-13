from typing import List, Dict
from datetime import datetime


class MetricsResultsEntry:
    def __init__(self, values: List, date: datetime):
        self.values = values
        self.date = date


class MetricsResults:
    def __init__(self, filters: Dict, metadata: Dict = None, entries: List = None):
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

    def get_first(self):
        return self.entries[0]

    def value_keys(self):
        return self.get_first().values.keys()

    def filter_keys(self):
        return self.filters.keys()
