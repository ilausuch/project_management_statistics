from datetime import datetime, timedelta
from formatters.influxdb_formatter import MetricsInfluxdbFormatter
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


def test_format_metrics_results():
    date = datetime.now()
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2}, metadata={"project": 1}, date=date)
    lines = MetricsInfluxdbFormatter.format("test", metrics)
    assert lines[0] == f"test project=1 v1=1,v2=1,v3=2 {date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"


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

    lines = MetricsInfluxdbFormatter.format("test", metrics_time_series)
    assert lines[0] == f"test project=containers v1=1,v2=1,v3=2 {date1.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"
    assert lines[1] == f"test project=containers v1=2,v2=2,v3=3 {date2.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"


def test_print_metrics_results(capsys):
    date = datetime.now()
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2}, metadata={"project": 1}, date=date)
    MetricsInfluxdbFormatter.print("test", metrics)

    captured = capsys.readouterr()
    assert captured.out == f"test project=1 v1=1,v2=1,v3=2 {date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}\n"
