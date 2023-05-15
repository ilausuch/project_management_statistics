import sys
import argparse
from datetime import date, datetime
from db.sqlite_query import SQLiteQuery
from metrics.metrics_status_count import MetricsStatusCount
from formatters.csv_formatter import MetricsCSVFormatter
from formatters.influxdb_formatter import MetricsInfluxdbFormatter
from formatters.json_formatter import MetricsJSONFormatter
from utils.filter_parser import FilterParser

# command line arguments
parser = argparse.ArgumentParser(description='Loop over a range of dates and apply a metric to each date')
parser.add_argument('--start_date', type=str, help='Start date (YYYY-MM-DD). If not provided, defaults to epoch.')
parser.add_argument('--end_date', type=str, help='End date (YYYY-MM-DD). If not provided, defaults to today.')
parser.add_argument('--increment_days', type=int, default=1, help='Number of days to increment by. Defaults to 1.')
parser.add_argument('database', type=str, help='Name of database file to write results to.')
parser.add_argument('--metric', type=str, default='status_count',
                    help='Name of method to apply to each date. Defaults to "status_count".')
parser.add_argument('--output_format', type=str, default='influxdb',
                    help='Output format. Valid options are "json", "influxdb", and "csv". Defaults to "influxdb".')
parser.add_argument('--output_date_format', type=str, default='%Y-%m-%d',
                    help='Output date format. Only valid for csv output. Defaults to "%Y-%m-%d".')
parser.add_argument('--measurement_name', type=str, default='metrics', help='The name of the measurement name used in InfluxDB')
filter_parser = FilterParser()
filter_parser.add_filtering_arguments(parser)
args = parser.parse_args()

query_manager = SQLiteQuery(args.database)
metrics = MetricsStatusCount(query_manager)

# set default values for date_from and date_to, also for metric
if args.start_date is None:
    date_from = query_manager.get_first_date().replace(hour=0, minute=0, second=0, microsecond=0)
else:
    date_from = datetime.strptime(args.start_date, '%Y-%m-%d')

if args.end_date is None:
    date_to = date.today()  # today's date
else:
    date_to = datetime.strptime(args.end_date, '%Y-%m-%d')

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

# prepare the filters
filters = filter_parser.get_filters(args)

# generate the output
if args.metric == "status_count":
    metric_result = metrics.status_count_by_date_range(start_date=date_from, end_date=date_to,
                                                       increment_days=args.increment_days, filters=filters)
else:
    print(f"Metric '{args.metric}' is not implemented.", file=sys.stderr)
    sys.exit(1)

for line in Formatter.format(measurement_name=args.measurement_name, metrics=metric_result, date_format=args.output_date_format):
    print(line)
