from datetime import datetime, timedelta
from formatters.csv_formatter import MetricsCSVFormatter
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


def test_format():
    date = datetime.now()
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2}, metadata={"project": 1}, date=date)
    lines = MetricsCSVFormatter.format("test", metrics)
    assert lines[0] == "measurement,project,v1,v2,v3,date"
    assert lines[1] == f"test,1,1,1,2,{date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"


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

    lines = MetricsCSVFormatter.format("test", metrics_time_series)
    assert lines[0] == "measurement,project,v1,v2,v3,date"
    assert lines[1] == f"test,containers,1,1,2,{date1.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"
    assert lines[2] == f"test,containers,2,2,3,{date2.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"
