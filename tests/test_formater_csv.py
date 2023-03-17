from datetime import datetime
from formatters.csv_formatter import MetricsCSVFormatter
from metrics.metrics_result import MetricsResults


def test_format():
    date = datetime.now()
    metrics = MetricsResults({"project": 1})
    metrics.append_values({"v1": 1, "v2": 1, "v3": 2}, date)
    lines = MetricsCSVFormatter.format("test", metrics)
    assert lines[0] == "measurement,project,v1,v2,v3,date"
    assert lines[1] == f"test,1,1,1,2,{date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"
