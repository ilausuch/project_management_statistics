from typing import Union
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


class MetricsInfluxdbFormatter:
    @staticmethod
    def format(measurement_name: str, metrics: Union[MetricsResults, MetricsTimeSeries]):
        """
        Constructs a list of dictionaries with the key:value
        :param measurement_name: Measurement name for the influx db
        :param metrics: A MetricsResults or MetricsTimeSeries object
        :return: A formated list of strings
        """
        lines = []

        entries = metrics.as_array()
        metadata = metrics.metadata

        for entry in entries:
            if len(metadata) > 0:
                filter_str = ','.join([
                    f"{str(key).replace(' ', '_')}={str(value).replace(' ', '_')}"
                    for key, value in metadata.items()
                ])
            else:
                filter_str = "filter=none"

            entry_values = {key: value for key, value in entry.items() if key != "date"}
            values_str = ','.join([
                f"{str(key).replace(' ', '_')}={str(value).replace(' ', '_')}"
                for key, value in entry_values.items()
            ])
            lines.append(f"{measurement_name} {filter_str} {values_str} {entry['date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')}")
        return lines
