import json
from typing import Union
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


class MetricsJSONFormatter:
    @staticmethod
    def format(measurement_name: str, metrics: Union[MetricsResults, MetricsTimeSeries],
               date_format: str = "%Y-%m-%d"):
        """
        Constructs a json with the filters and the values with the struecture
        :param measurement_name: Measurement name for the influx db
        :param metrics: A MetricsResults object
        :return: A json
        """

        entries = metrics.as_array()
        metadata = metrics.metadata

        formatted_entries = []
        for entry in entries:
            entry_values = {key: value for key, value in entry.items() if key != "date"}
            formatted_entries.append({"values": entry_values, "date": entry['date'].strftime(date_format)})

        result = {
            "name": measurement_name,
            "filters": metadata,
            "data": formatted_entries
        }
        return json.dumps(result)

    @staticmethod
    def print(measurement_name: str, metrics: Union[MetricsResults, MetricsTimeSeries],
              date_format: str = "%Y-%m-%d"):
        print(MetricsJSONFormatter.format(measurement_name, metrics, date_format))
