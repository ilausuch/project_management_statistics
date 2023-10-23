from datetime import datetime, timedelta
from formatters.influxdb_formatter import MetricsInfluxdbFormatter
from metrics.metrics_result import MetricsResults, MetricsTimeSeries
import pytz


def test_format_metrics_results():
    date = datetime.now()
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2},
                             metadata={"project": 1},
                             date=date)
    lines = MetricsInfluxdbFormatter.format("test", metrics)
    date_as_e9 = int(date.timestamp() * 1e9)
    assert lines[0] == f"test,project=1 v1=1,v2=1,v3=2 {date_as_e9}"


def test_format_metrics_time_series():
    date1 = datetime.now(tz=pytz.UTC)
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
    date1_as_e9 = int(date1.timestamp() * 1e9)
    date2_as_e9 = int(date2.timestamp() * 1e9)
    assert lines[0] == f"test,project=containers v1=1,v2=1,v3=2 {date1_as_e9}"
    assert lines[1] == f"test,project=containers v1=2,v2=2,v3=3 {date2_as_e9}"


def test_print_metrics_results(capsys):
    date = datetime.now()
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2},
                             metadata={"project": 1},
                             date=date)
    MetricsInfluxdbFormatter.print("test", metrics)

    captured = capsys.readouterr()
    assert captured.out == f"test,project=1 v1=1,v2=1,v3=2 {int(date.timestamp() * 1e9)}\n"
