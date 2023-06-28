import pandas as pd
from metrics.metrics_result import MetricsResults, MetricsTimeSeries
from metrics.column_transformer import ColumnTransformer


def test_column_transformer():
    data = {
        'col1': 10,
        'col2': 5,
        'col3': 2
    }
    metrics = MetricsResults(data)

    transformations = [
        {'column': 'col1', 'operation': 'hide', 'arguments': []},
        {'column': 'col4', 'operation': 'sum', 'arguments': ['col2', 'col3']},
        {'column': 'col5', 'operation': 'mult', 'arguments': ['col2', 'col3']}
    ]

    transformer = ColumnTransformer(metrics, transformations)
    transformer.execute()

    transformed_data = transformer.metrics.data
    assert 'col1' not in transformed_data
    assert transformed_data['col4'] == 7
    assert transformed_data['col5'] == 10


def test_column_transformer_with_time_series():
    data = [
        {
            'date': pd.to_datetime('2021-01-01'),
            'col1': 10,
            'col2': 5,
            'col3': 2
        },
        {
            'date': pd.to_datetime('2021-01-02'),
            'col1': 20,
            'col2': 10,
            'col3': 4
        }
    ]
    metrics = MetricsTimeSeries(data)

    transformations = [
        {'column': 'col1', 'operation': 'hide', 'arguments': []},
        {'column': 'col4', 'operation': 'sum', 'arguments': ['col2', 'col3']},
        {'column': 'col5', 'operation': 'mult', 'arguments': ['col2', 'col3']}
    ]

    transformer = ColumnTransformer(metrics, transformations)
    transformer.execute()

    transformed_data = transformer.metrics.as_array()
    assert 'col1' not in transformed_data[0]
    assert transformed_data[0]['col4'] == 7
    assert transformed_data[0]['col5'] == 10
    assert 'col1' not in transformed_data[1]
    assert transformed_data[1]['col4'] == 14
    assert transformed_data[1]['col5'] == 40
