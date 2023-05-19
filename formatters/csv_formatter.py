from typing import Union
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


class MetricsCSVFormatter:
    @staticmethod
    def format(measurement_name: str, metrics: Union[MetricsResults, MetricsTimeSeries],
               separator: str = ",", date_format: str = "%Y-%m-%d"):
        """
        Constructs a list of dictionaries with the key:value
        :param measurement_name: Measurement name for the influx db
        :param metrics: A MetricsResults or MetricsTimeSeries object
        :return: A formatted list of strings
        """
        entries = metrics.as_array()
        metadata = metrics.metadata

        filter_str = separator.join(str(key) for key in metadata.keys())
        values_str = separator.join(str(key) for key in entries[0].keys() if key != "date")
        lines = [f"measurement{separator}date{separator}filter{separator}{values_str}"]

        for entry in entries:
            filter_str = ','.join(str(value) for value in metadata.values())
            entry_values = {key: value for key, value in entry.items() if key != "date"}
            values_str = ','.join(str(value) for value in entry_values.values())
            lines.append(f"{measurement_name}{separator}{entry['date'].strftime(date_format)}"
                         f"{separator}{filter_str}{separator}{values_str}")

        return lines

    @staticmethod
    def print(measurement_name: str, metrics: Union[MetricsResults, MetricsTimeSeries],
              separator: str = ",", date_format: str = "%Y-%m-%d"):
        for line in MetricsCSVFormatter.format(measurement_name, metrics, separator, date_format):
            print(line)
