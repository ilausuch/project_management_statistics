from datetime import datetime
from metrics.metrics_result import MetricsResults, MetricsResultsEntry


def test_append_values():
    results = MetricsResults()
    values = {'key': 'value'}
    date = datetime.now()
    results.append_values(values, date)
    assert len(results.entries) == 1
    assert results.entries[0].values == values
    assert results.entries[0].date == date


def test_append():
    results = MetricsResults()
    entry = MetricsResultsEntry({'key': 'value'}, datetime.now())
    results.append(entry)
    assert len(results.entries) == 1
    assert results.entries[0] == entry


def test_append_results():
    results = MetricsResults({'key': 'value'})
    other = MetricsResults({'key': 'value'})
    other.append_values({'other_key': 'other_value'}, datetime.now())

    results.append_results(other)

    assert len(results.entries) == 1
    assert results.filters == {'key': 'value'}
    assert results.metadata is None


def test_get_first():
    results = MetricsResults()
    entry1 = MetricsResultsEntry({'key1': 'value1'}, datetime.now())
    entry2 = MetricsResultsEntry({'key2': 'value2'}, datetime.now())
    results.append(entry1)
    results.append(entry2)
    assert results.get_first() == entry1


def test_value_keys():
    results = MetricsResults()
    entry = MetricsResultsEntry({'key': 'value'}, datetime.now())
    results.append(entry)
    assert results.value_keys() == {'key'}


def test_filter_keys():
    results = MetricsResults({'key': 'value'})
    assert results.filter_keys() == {'key'}


def test_import_entries():
    results1 = MetricsResults({'key': 'value'})
    results2 = MetricsResults({'key': 'value'})
    results2.append_values({'other_key': 'other_value'}, datetime.now())
    results2.metadata = {'metadata_key': 'metadata_value'}

    results1.import_entries([results2])

    assert len(results1.entries) == 1
    assert results1.filters == {'key': 'value'}
    assert results1.metadata == {'metadata_key': 'metadata_value'}
