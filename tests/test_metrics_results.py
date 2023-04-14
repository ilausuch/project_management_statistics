from metrics.metrics_result import MetricsTimeSeries, MetricsResults


def test_metrics_time_series():
    example_data = [
        {"date": "2023-04-01", "serie_A": 1.1, "serie_B": 2.2},
        {"date": "2023-04-02", "serie_A": 1.3, "serie_B": 2.4},
        {"date": "2023-04-03", "serie_A": 1.2, "serie_B": 2.1},
    ]
    example_metadata = {
        "serie_A": {"project": "containers"},
        "serie_B": {"project": "public cloud"},
    }
    mts = MetricsTimeSeries(data=example_data, metadata=example_metadata)

    assert mts.get_first().equals(mts.data.iloc[0])
    assert set(mts.value_keys()) == {"serie_A", "serie_B"}
    assert set(mts.filter_keys()) == {"serie_A", "serie_B"}

    mts.add_serie({"serie_C": {"project": "private cloud"}}, [{"date": "2023-04-01", "serie_C": 5.0}])

    assert "serie_C" in mts.value_keys()
    assert "serie_C" in mts.filter_keys()

    mts.add_date("2023-04-04", {"serie_A": 1.5, "serie_B": 2.3, "serie_C": 5.2})

    assert "2023-04-04" in mts.data.index.strftime("%Y-%m-%d")


def test_metrics_result():
    data = {"serie_A": 1.1, "serie_B": 2.2}
    metadata = {
        "serie_A": {"project": "containers"},
        "serie_B": {"project": "public cloud"},
    }
    results = MetricsResults(data=data, metadata=metadata)

    assert results.data == data
    assert results.metadata == metadata
