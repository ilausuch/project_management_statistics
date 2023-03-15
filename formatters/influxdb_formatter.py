from metrics.metrics_result import MetricsResults


class MetricsInfluxdbFormatter:
    @staticmethod
    def format(measurement_name: str, metrics: MetricsResults):
        """
        Constructs a list of dictionaries with the key:value
        :param measurement_name: Measurement name for the influx db
        :param metrics: A MetricsResults object
        :return: A formated list of strings
        """
        lines = []
        for entry in metrics.entries:
            if len(metrics.filters) > 0:
                filter_str = ','.join([f"{key}={value}" for key, value in metrics.filters.items()])
            else:
                filter_str = "dummy=dummy"

            values_str = ','.join([f"{key}={value}" for key, value in entry.values.items()])
            lines.append(f"{measurement_name} {filter_str} {values_str} {entry.date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}")
        return lines
