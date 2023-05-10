import argparse
from utils.filter_parser import FilterParser


def test_filter_parser():
    parser = argparse.ArgumentParser()
    filter_parser = FilterParser()
    filter_parser.add_filtering_arguments(parser)

    args = parser.parse_args(['--filter-project', 'Project B',
                              '--filter-priority', 'High',
                              '--filter', '''
        {
            "project": {"op": "eq", "value": "Project A"},
            "author": "John Doe",
            "tags": {"op": "ilike", "value": "%tag1%"},
            "status": {
                "op": "or",
                "value": [
                    {"op": "eq", "value": "New"},
                    {"op": "eq", "value": "In Progress"}
                ]
            },
            "start_date": {"op": "gt", "value": "2022-01-01"}
        }
    '''])

    filters = filter_parser.get_filters(args)
    assert filters == {
        'project': {'op': 'eq', 'value': 'Project B'},
        'priority': {'op': 'eq', 'value': 'High'},
        'author': {'op': 'eq', 'value': 'John Doe'},
        'tags': {'op': 'ilike', 'value': '%tag1%'},
        'status': {
            'op': 'or',
            'value': [
                {'op': 'eq', 'value': 'New'},
                {'op': 'eq', 'value': 'In Progress'}
            ]
        },
        'start_date': {'op': 'gt', 'value': '2022-01-01'}
    }
