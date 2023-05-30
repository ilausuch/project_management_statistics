import sys
from formatters.csv_formatter import MetricsCSVFormatter
from formatters.influxdb_formatter import MetricsInfluxdbFormatter
from formatters.json_formatter import MetricsJSONFormatter


def parse_formatter(value):
    if value == 'json':
        return MetricsJSONFormatter
    if value == 'influxdb':
        return MetricsInfluxdbFormatter
    if value == 'csv':
        return MetricsCSVFormatter

    print(f"Invalid output format '{value}'. Valid options are 'json', 'influxdb', and 'csv'.", file=sys.stderr)
    sys.exit(1)
