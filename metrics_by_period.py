import sys
import argparse
from datetime import date, datetime, timedelta
from db.sqlite_query import SQLiteQuery
from metrics.metrics import Metrics, MetricsResults
from formatters.csv_formatter import MetricsCSVFormatter
from formatters.influxdb_formatter import MetricsInfluxdbFormatter
from formatters.json_formatter import MetricsJSONFormatter

# command line arguments
parser = argparse.ArgumentParser(description='Loop over a range of dates and apply a metric to each date')
parser.add_argument('--start_date', type=str, help='Start date (YYYY-MM-DD). If not provided, defaults to epoch.')
parser.add_argument('--end_date', type=str, help='End date (YYYY-MM-DD). If not provided, defaults to today.')
parser.add_argument('database', type=str, help='Name of database file to write results to.')
parser.add_argument('--metric', type=str, default='status_count',
                    help='Name of method to apply to each date. Defaults to "status_count".')
parser.add_argument('--output_format', type=str, default='influxdb',
                    help='Output format. Valid options are "json", "influxdb", and "csv". Defaults to "influxdb".')
parser.add_argument('--measurement_name', type=str, default='metrics', help='The name of the measurement name used in InfluxDB')
args = parser.parse_args()

query_manager = SQLiteQuery(args.database)
metrics = Metrics(query_manager)

# set default values for date_from and date_to, also for metric
if args.start_date is None:
    date_from = query_manager.get_first_date().replace(hour=0, minute=0, second=0, microsecond=0)
else:
    date_from = datetime.strptime(args.start_date, '%Y-%m-%d').date()

if args.end_date is None:
    date_to = date.today()  # today's date
else:
    date_to = datetime.strptime(args.end_date, '%Y-%m-%d').date()

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
delta = timedelta(days=1)
current_date = date_from
metric_result = MetricsResults()
while current_date.date() <= date_to:
    if args.metric == "status_count":
        period_result = metrics.status_count_by_date(current_date)
        metric_result.append_results(period_result)
    current_date += delta

for line in Formatter.format(args.measurement_name, metric_result):
    print(line)
