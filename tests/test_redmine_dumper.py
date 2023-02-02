from redmine.redmine_dumper import RedmineDumper
from datetime import datetime
import pytest


class FakeDumper(RedmineDumper):

    def __init__(self):
        pass


@pytest.fixture
def expected_filter_template():
    return "f[]={0}&op[{0}]={3}&v[{0}][]={1}&v[{0}][]={2}"


def test_prepare_filter(expected_filter_template):

    dumper = FakeDumper()
    expected_filter = expected_filter_template.format(
        "status_id", "new", "closed", "=")
    assert expected_filter == dumper.prepare_filter(
        "status_id", ["new", "closed"], "=")

    with pytest.raises(ValueError):
        dumper.prepare_filter("status", [], '=')


def test_filter_status(expected_filter_template):
    dumper = FakeDumper()
    expected_filter = expected_filter_template.format(
        "status_id", "new", "closed", "=")
    assert expected_filter == dumper.filter_status(["new", "closed"])
    assert expected_filter == dumper.filter_status(["new", "closed"], '=')
    expected_filter = expected_filter_template.format(
        "status_id", "new", "closed", "><")
    assert expected_filter == dumper.filter_status(["new", "closed"], '><')


def test_filter_tracker(expected_filter_template):
    dumper = FakeDumper()
    expected_filter = expected_filter_template.format(
        "tracker_id", "1", "2", "=")
    assert expected_filter == dumper.filter_tracker(["1", "2"])
    assert expected_filter == dumper.filter_tracker(["1", "2"], '=')
    expected_filter = expected_filter_template.format(
        "tracker_id", "1", "2", "><")
    assert expected_filter == dumper.filter_tracker(["1", "2"], '><')


def test_filter_date():
    dumper = FakeDumper()
    expected_filter_template = "f[]={0}&op[{0}]={2}&v[{0}][]={1}"
    expected_filter = expected_filter_template.format(
        'created_on', '1999-01-01', '=')
    assert expected_filter == dumper.filter_date('created_on',
                                                 datetime.strptime('1999-01-01', '%Y-%m-%d'), '=')
    expected_filter = expected_filter_template.format(
        'created_on', '1999-01-01', '><')
    assert expected_filter == dumper.filter_date('created_on',
                                                 datetime.strptime('1999-01-01', '%Y-%m-%d'), '><')


def test_issues(monkeypatch):
    issues_list = [{'str': 1}, {'str': 1}]
    monkeypatch.setattr(RedmineDumper, "raw_query",
                        lambda self, project, filters: {'issues': issues_list})
    dumper = FakeDumper()
    assert issues_list == dumper.issues('test')
