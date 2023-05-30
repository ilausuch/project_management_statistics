import sys
import argparse
from datetime import date
from db.sqlite_query import SQLiteQuery
from metrics.metrics_status_count import MetricsStatusCount
from utils.filter_parser import FilterParser
from utils.config_parser import ConfigParser
from utils.date_parser import parse_date
from utils.formater_parser import parse_formatter

# command line arguments
parser = argparse.ArgumentParser(description='Loop over a range of dates and apply a metric to each date')
parser.add_argument('database', type=str, help='Name of database file to write results to.')
parser.add_argument('--date', type=str, help='Spot date (YYYY-MM-DD). If not provided, defaults to epoch.')
parser.add_argument('--metric', type=str, default='status_count',
                    help='Name of method to apply to each date. Defaults to "status_count".')
parser.add_argument('--output_format', type=str, default='influxdb',
                    help='Output format. Valid options are "json", "influxdb", and "csv". Defaults to "influxdb".')
parser.add_argument('--output_date_format', type=str, default='%Y-%m-%d',
                    help='Output date format. Only valid for csv output. Defaults to "%Y-%m-%d".')

parser.add_argument('--measurement_name', type=str, default='metrics', help='The name of the measurement name used in InfluxDB')
filter_parser = FilterParser()
filter_parser.add_filtering_arguments(parser)
config_parser = ConfigParser(parser)
args = config_parser.parse_args()

query_manager = SQLiteQuery(args['database'])
metrics = MetricsStatusCount(query_manager)

if args['metric'] != 'status_count':
    print(f"Metric '{args['metric']}' is not implemented.", file=sys.stderr)
    sys.exit(1)

date_to = parse_date(args['date'], date.today())
Formatter = parse_formatter(args['output_format'])

# prepare the filters
filters = filter_parser.get_filters(args)

# generate the output
if args['metric'] == "status_count":
    metric_result = metrics.status_count_by_date(date=date_to, filters=filters)

Formatter.print(measurement_name=args['measurement_name'], metrics=metric_result, date_format=args['output_date_format'])
