from datetime import datetime
from formatters.influxdb_formatter import MetricsInfluxdbFormatter
from metrics.metrics_result import MetricsResults


def test_format():
    date = datetime.now()
    metrics = MetricsResults({"project": 1})
    metrics.append_values({"v1": 1, "v2": 1, "v3": 2}, date)
    lines = MetricsInfluxdbFormatter.format("test", metrics)
    assert lines[0] == f"test project=1 v1=1,v2=1,v3=2 {date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"
