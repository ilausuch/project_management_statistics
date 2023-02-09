from redmine.redmine_dumper import RedmineDumper


# pylint: disable=super-init-not-called
class FakeDumper(RedmineDumper):

    def __init__(self):
        pass


def test_issues(monkeypatch):
    issues_list = [{'str': 1}, {'str': 1}]
    monkeypatch.setattr(RedmineDumper, "raw_query",
                        lambda self, project, filters: {'issues': issues_list})
    dumper = FakeDumper()
    assert issues_list == dumper.issues('test')
