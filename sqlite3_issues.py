import argparse
from datetime import datetime
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from db.models import Issue
from db.filter_builder import FilterBuilder
from utils.filter_parser import FilterParser

# Initialize argument parser
parser = argparse.ArgumentParser(description='Loop over a range of dates and apply a metric to each date')
parser.add_argument('--start_date', type=str, help='Start date (YYYY-MM-DD). If not provided, defaults to epoch.')
parser.add_argument('--end_date', type=str, help='End date (YYYY-MM-DD). If not provided, defaults to today.')
parser.add_argument('database', type=str, help='Name of database file to write results to.')
parser.add_argument('--output-mode', type=str, choices=['print', 'count'], default='print',
                    help='Output mode. If "print", prints the issues. If "count", prints the count of issues.')

# Parse filters arguments
filter_parser = FilterParser()
filter_parser.add_filtering_arguments(parser)
args = parser.parse_args()
filters = filter_parser.get_filters(args)
filter_builder = FilterBuilder(Issue)
filter_conditions = filter_builder.build_filters(filters)

# Apply start_date and end_date filters
date_filter_conditions = []
if args.start_date:
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    date_filter_conditions.append(Issue.created_on >= start_date)
if args.end_date:
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    date_filter_conditions.append(Issue.created_on <= end_date)


# Query the database
engine = create_engine(f"sqlite:///{args.database}")
Session = sessionmaker(bind=engine)
session = Session()
issues = session.query(Issue).filter(and_(filter_conditions, *date_filter_conditions))

if args.output_mode == 'print':
    for issue in issues:
        print(issue.as_json())
else:
    print(issues.count())

session.close()
