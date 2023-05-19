from datetime import datetime, timedelta
import json
from formatters.json_formatter import MetricsJSONFormatter
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


def test_format():
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2}, metadata={"project": 1})
    result = MetricsJSONFormatter.format("test", metrics)
    parsed = json.loads(result)
    assert parsed["name"] == "test"
    assert parsed["filters"]["project"] == 1
    assert parsed["data"][0]["values"]["v1"] == 1


def test_format_metrics_time_series():
    date1 = datetime.now()
    date2 = date1 + timedelta(days=1)
    metrics_time_series = MetricsTimeSeries()

    metrics_time_series.add_serie(
        metadata={"project": "containers"},
        data=[
            {"date": date1, "v1": 1, "v2": 1, "v3": 2},
            {"date": date2, "v1": 2, "v2": 2, "v3": 3},
        ]
    )

    result = MetricsJSONFormatter.format("test", metrics_time_series)
    parsed = json.loads(result)
    assert parsed["name"] == "test"
    assert parsed["filters"]["project"] == "containers"
    assert parsed["data"][0]["values"]["v1"] == 1
    assert parsed["data"][0]["values"]["v2"] == 1
    assert parsed["data"][0]["values"]["v3"] == 2
    assert parsed["data"][1]["values"]["v1"] == 2
    assert parsed["data"][1]["values"]["v2"] == 2
    assert parsed["data"][1]["values"]["v3"] == 3


def test_print(capsys):
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2}, metadata={"project": 1})
    MetricsJSONFormatter.print("test", metrics)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert parsed["name"] == "test"
    assert parsed["filters"]["project"] == 1
    assert parsed["data"][0]["values"]["v1"] == 1
