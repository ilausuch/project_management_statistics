import json
from typing import Union
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


class MetricsJSONFormatter:
    @staticmethod
    def format(measurement_name: str, metrics: Union[MetricsResults, MetricsTimeSeries]):
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
            formatted_entries.append({"values": entry_values, "date": entry["date"].isoformat()})

        result = {
            "name": measurement_name,
            "filters": metadata,
            "data": formatted_entries
        }
        return json.dumps(result)
