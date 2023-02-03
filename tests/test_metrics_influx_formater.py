from datetime import datetime
from metrics.influxdb_formater import MetricsInfluxdbFormater


def test_format_dict():
    status_count = {"1": 1, "2": 1, "3": 2}
    date = datetime.now()
    line = MetricsInfluxdbFormater.format_dict("test", status_count, date, project_id=1)
    assert line == f"test project_id=1 1=1,2=1,3=2 {date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}"
