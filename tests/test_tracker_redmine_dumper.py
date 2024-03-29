from datetime import datetime
from trackers.redmine.redmine_dumper import RedmineDumper, RedmineIssue, RedmineIssueEvent
from trackers.redmine.redmine_config import RedmineConfig


# pylint: disable=super-init-not-called
class FakeDumper(RedmineDumper):

    def __init__(self):
        pass


# pylint: disable=unused-argument
def redmine_config_load(self, config_file):
    self.data = {
        'STATUS_CODE_TO_STRING': {
            '1': 'NEW',
            '2': 'IN PROGRESS',
            '3': 'RESOLVED',
            '4': 'FEEDBACK',
            '5': 'CLOSED',
            '6': 'REJECTED',
            '12': 'WORKABLE',
            '15': 'BLOCKED'
        }
    }


def test_issues(monkeypatch):
    issues_list = [{'str': 1}, {'str': 1}]
    monkeypatch.setattr(RedmineDumper, "raw_query",
                        lambda self, project, filters: {'issues': issues_list})
    dumper = FakeDumper()
    assert issues_list == dumper.issues('test')


def test_redmine_issue(monkeypatch):
    monkeypatch.setattr(RedmineConfig, "load", redmine_config_load)
    RedmineConfig.get_instance().load("")

    a_datetime = "2023-03-14T16:19:48Z"
    a_date = "2023-03-14"
    data = {
        "issue": {
            "id": 126017,
            "project": {
                "id": 230,
                "name": "project1"
            },
            "tracker": {
                "id": 4,
                "name": "action"
            },
            "status": {
                "id": 2,
                "name": "IN PROGRESS"
            },
            "priority": {
                "id": 4,
                "name": "Normal"
            },
            "author": {
                "id": 34361,
                "name": "author1"
            },
            "assigned_to": {
                "id": 34361,
                "name": "terst"
            },
            "parent": {
                "id": 123178
            },
            "subject": "",
            "description": "",
            "start_date": a_date,
            "due_date": a_date,
            "done_ratio": 0,
            "is_private": False,
            "estimated_hours": 3,
            "total_estimated_hours": None,
            "spent_hours": 0.0,
            "total_spent_hours": 0.0,
            "custom_fields": [
                {
                    "id": 16,
                    "name": "Difficulty",
                    "value": ""
                },
                {
                    "id": 22,
                    "name": "Relevance",
                    "value": "P5"
                }
            ],
            "created_on": a_datetime,
            "updated_on": a_datetime,
            "closed_on": a_datetime
        }
    }

    issue = RedmineIssue(data["issue"])
    assert issue.issue_id == data["issue"]["id"]
    assert issue.project == data["issue"]["project"]["name"]
    assert issue.type == data["issue"]["tracker"]["name"]
    assert issue.status == data["issue"]["status"]["name"]
    assert issue.priority == data["issue"]["priority"]["name"]
    assert issue.author == data["issue"]["author"]["name"]
    assert issue.assigned_to == data["issue"]["assigned_to"]["name"]
    assert issue.subject == data["issue"]["subject"]
    assert issue.start_date == datetime.strptime(data["issue"]["start_date"], "%Y-%m-%d")
    assert issue.due_date == datetime.strptime(data["issue"]["start_date"], "%Y-%m-%d")
    assert issue.estimated_hours == data["issue"]["estimated_hours"]
    assert issue.created_on == datetime.strptime(data["issue"]["created_on"], "%Y-%m-%dT%H:%M:%SZ")
    assert issue.updated_on == datetime.strptime(data["issue"]["updated_on"], "%Y-%m-%dT%H:%M:%SZ")
    assert issue.closed_on == datetime.strptime(data["issue"]["updated_on"], "%Y-%m-%dT%H:%M:%SZ")


def test_redmine_issue_event(monkeypatch):
    monkeypatch.setattr(RedmineConfig, "load", redmine_config_load)
    RedmineConfig.get_instance().load("")

    issue_id = 1234
    data = {
        "id": 602570,
        "user": {
            "id": 25856,
            "name": "name"
        },
        "notes": "",
        "created_on": "2023-02-15T14:26:21Z",
        "private_notes": False,
        "details": [
            {
                "property": "attr",
                "name": "status",
                "old_value": "12",
                "new_value": "15"
            }
        ]
    }
    issue_event = RedmineIssueEvent(data, data["details"][0], issue_id)
    assert issue_event.issue_id == issue_id
    assert issue_event.user_name == data["user"]["name"]
    assert issue_event.created_on == datetime.strptime(data["created_on"], "%Y-%m-%dT%H:%M:%SZ")
    assert issue_event.type == data["details"][0]["property"]
    assert issue_event.field == data["details"][0]["name"]
    assert issue_event.old_value == data["details"][0]["old_value"]
    assert issue_event.new_value == data["details"][0]["new_value"]
