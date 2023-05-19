from datetime import datetime, timedelta
from formatters.csv_formatter import MetricsCSVFormatter
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


def test_format():
    date = datetime.now()
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2}, metadata={"project": 1}, date=date)
    lines = MetricsCSVFormatter.format("test", metrics)
    assert lines[0] == "measurement,date,filter,v1,v2,v3"
    assert lines[1] == f"test,{date.strftime('%Y-%m-%d')},1,1,1,2"


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
    assert lines[0] == "measurement,date,filter,v1,v2,v3"
    assert lines[1] == f"test,{date1.strftime('%Y-%m-%d')},containers,1,1,2"
    assert lines[2] == f"test,{date2.strftime('%Y-%m-%d')},containers,2,2,3"


def test_print(capsys):
    date = datetime.now()
    metrics = MetricsResults(data={"v1": 1, "v2": 1, "v3": 2}, metadata={"project": 1}, date=date)
    MetricsCSVFormatter.print("test", metrics)

    captured = capsys.readouterr()
    assert captured.out == f"measurement,date,filter,v1,v2,v3\ntest,{date.strftime('%Y-%m-%d')},1,1,1,2\n"
