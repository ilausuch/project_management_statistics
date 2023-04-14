import sys
import argparse
from datetime import datetime
from db.sqlite_query import SQLiteQuery
from metrics.metrics_status_count import MetricsStatusCount
from formatters.csv_formatter import MetricsCSVFormatter
from formatters.influxdb_formatter import MetricsInfluxdbFormatter
from formatters.json_formatter import MetricsJSONFormatter

# command line arguments
parser = argparse.ArgumentParser(description='Loop over a range of dates and apply a metric to each date')
parser.add_argument('--date', type=str, help='Spot date (YYYY-MM-DD). If not provided, defaults to epoch.')
parser.add_argument('database', type=str, help='Name of database file to write results to.')
parser.add_argument('--metric', type=str, default='status_count',
                    help='Name of method to apply to each date. Defaults to "status_count".')
parser.add_argument('--output_format', type=str, default='influxdb',
                    help='Output format. Valid options are "json", "influxdb", and "csv". Defaults to "influxdb".')
parser.add_argument('--measurement_name', type=str, default='metrics', help='The name of the measurement name used in InfluxDB')
args = parser.parse_args()

query_manager = SQLiteQuery(args.database)
metrics = MetricsStatusCount(query_manager)

if args.metric != 'status_count':
    print(f"Metric '{args.metric}' is not implemented.", file=sys.stderr)
    sys.exit(1)

# select formatter based on output format
if args.output_format == 'json':
    Formatter = MetricsJSONFormatter
elif args.output_format == 'influxdb':
    Formatter = MetricsInfluxdbFormatter
elif args.output_format == 'csv':
    Formatter = MetricsCSVFormatter
else:
    print(f"Invalid output format '{args.output_format}'. Valid options are 'json', 'influxdb', and 'csv'.", file=sys.stderr)
    sys.exit(1)

# generate the output
if args.metric == "status_count":
    if args.date is not None:
        date_snapshot = datetime.combine(datetime.strptime(args.date, '%Y-%m-%d').date(), datetime.min.time())
        metric_result = metrics.status_count_by_date(date=date_snapshot)
    else:
        metric_result = metrics.status_count()

for line in Formatter.format(args.measurement_name, metric_result):
    print(line)
