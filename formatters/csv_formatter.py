from metrics.metrics_result import MetricsResults


class MetricsCSVFormatter:
    @staticmethod
    def format(measurement_name: str, metrics: MetricsResults, separator: str = ","):
        """
        Constructs a list of dictionaries with the key:value
        :param measurement_name: Measurement name for the influx db
        :param metrics: A MetricsResults object
        :return: A formated list of strings
        """
        filter_str = separator.join(metrics.filter_keys())
        values_str = separator.join(metrics.value_keys())
        lines = [f"measurement{separator}{filter_str}{separator}{values_str},date"]
        for entry in metrics.entries:
            filter_str = ','.join(str(value) for value in metrics.filters.values())
            values_str = ','.join(str(value) for value in entry.values.values())
            lines.append(f"{measurement_name}{separator}{filter_str}{separator}"
                         f"{values_str}{separator}{entry.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}")
        return lines
