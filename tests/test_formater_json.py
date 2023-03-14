from datetime import datetime
import json
from formatters.json_formatter import MetricsJSONFormatter
from metrics.metrics_result import MetricsResults


def test_format():
    date = datetime.now()
    metrics = MetricsResults({"project_id": 1})
    metrics.append_values({"v1": 1, "v2": 1, "v3": 2}, date)
    result = MetricsJSONFormatter.format("test", metrics)
    parsed = json.loads(result)
    assert parsed["name"] == "test"
    assert parsed["filters"]["project_id"] == 1
    assert parsed["data"][0]["values"]["v1"] == 1
