import json
from metrics.metrics_result import MetricsResults


class MetricsJSONFormatter:
    @staticmethod
    def format(measurement_name: str, metrics: MetricsResults):
        """
        Constructs a json with the filters and the values with the struecture
        :param measurement_name: Measurement name for the influx db
        :param metrics: A MetricsResults object
        :return: A json
        """
        entries = []
        for entry in metrics.entries:
            entries.append({"values": entry.values, "date": entry.date.isoformat()})

        result = {
            "name": measurement_name,
            "filters": metrics.filters,
            "data": entries
        }
        print(result)
        return json.dumps(result)
