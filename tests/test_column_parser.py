import pytest
from utils.column_parser import extract_parts, ColumnParser


def test_extract_parts():
    # Test a function call with multiple arguments
    parts = extract_parts('ACTIVE.sum(IN PROGRESS, WORKABLE, NEW)')
    assert parts == {
        'column': 'ACTIVE',
        'operation': 'sum',
        'arguments': ['IN PROGRESS', 'WORKABLE', 'NEW']
    }

    # Test a function call with no arguments
    parts = extract_parts('UNKNOWN.hide()')
    assert parts == {
        'column': 'UNKNOWN',
        'operation': 'hide',
        'arguments': []
    }

    # Test a function call with single argument
    parts = extract_parts('SPEED=diff(RESOLVED)')
    assert parts == {
        'column': 'SPEED',
        'operation': 'diff',
        'arguments': ['RESOLVED']
    }


def test_column_parser():
    # Test the ColumnParser with some arguments
    column_parser = ColumnParser()
    args = {
        'column': [
            'UNKNOWN.hide()',
            'ACTIVE.sum(IN PROGRESS, WORKABLE, NEW)',
            'SPEED=diff(RESOLVED)'
        ]
    }
    columns = column_parser.get_columns(args)
    assert columns == [
        {'column': 'UNKNOWN', 'operation': 'hide', 'arguments': []},
        {'column': 'ACTIVE', 'operation': 'sum', 'arguments': ['IN PROGRESS', 'WORKABLE', 'NEW']},
        {'column': 'SPEED', 'operation': 'diff', 'arguments': ['RESOLVED']}
    ]

    # Test the ColumnParser with a help request
    args = {
        'column': [
            'help'
        ]
    }
    with pytest.raises(SystemExit):
        columns = column_parser.get_columns(args)
