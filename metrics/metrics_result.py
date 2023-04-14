from datetime import datetime
import pandas as pd


class MetricsResults:
    def __init__(self, data, metadata=None, date=datetime.now()):
        if metadata is None:
            metadata = {}

        self.date = date
        self.data = data
        self.metadata = metadata

    def as_array(self):
        return [{**self.data, "date": self.date}]


class MetricsTimeSeries:
    def __init__(self, data=None, metadata=None):
        if data is None:
            data = []
        if metadata is None:
            metadata = {}

        self.data = pd.DataFrame(data)
        if not self.data.empty:
            self.data["date"] = pd.to_datetime(self.data["date"])
            self.data.set_index("date", inplace=True)
        self.metadata = metadata

    def add_serie(self, metadata, data=None):
        if data is None:
            data = []

        self.metadata.update(metadata)

        if not data:
            return

        new_data = pd.DataFrame(data)
        new_data["date"] = pd.to_datetime(new_data["date"])
        new_data.set_index("date", inplace=True)

        if self.data.empty:
            self.data = new_data
        else:
            self.data = self.data.merge(new_data, left_index=True, right_index=True, how='outer')

    def add_date(self, date, date_data):
        date = pd.to_datetime(date)
        date_data["date"] = date
        new_data = pd.DataFrame([date_data]).set_index("date")
        if self.data.empty:
            self.data = new_data
        else:
            self.data.update(new_data)
            self.data = self.data.combine_first(new_data)

    def get_first(self):
        return self.data.iloc[0]

    def value_keys(self):
        return [col for col in self.data.columns if col != 'date']

    def filter_keys(self):
        return list(self.metadata.keys())

    def merge(self, other_metrics_results):
        merged_data = self.data.merge(other_metrics_results.data, left_index=True, right_index=True, how='outer')
        merged_metadata = {**self.metadata, **other_metrics_results.metadata}
        return MetricsResults(merged_data.reset_index().to_dict(orient='records'), merged_metadata)

    def as_array(self):
        return self.data.reset_index().to_dict(orient="records")

    def force_zeros(self):
        self.data.fillna(0, inplace=True)
