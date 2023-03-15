from datetime import datetime
from redmine.redmine_dumper import RedmineDumper, RedmineIssue, RedmineIssueEvent


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


def test_redmine_issue():
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
                "name": "In Progress"
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
    assert issue.project_id == data["issue"]["project"]["id"]
    assert issue.type_id == data["issue"]["tracker"]["id"]
    assert issue.status_id == data["issue"]["status"]["id"]
    assert issue.priority_id == data["issue"]["priority"]["id"]
    assert issue.author == data["issue"]["author"]["name"]
    assert issue.assigned_to == data["issue"]["assigned_to"]["name"]
    assert issue.subject == data["issue"]["subject"]
    assert issue.start_date == datetime.strptime(data["issue"]["start_date"], "%Y-%m-%d")
    assert issue.due_date == datetime.strptime(data["issue"]["start_date"], "%Y-%m-%d")
    assert issue.estimated_hours == data["issue"]["estimated_hours"]
    assert issue.created_on == datetime.strptime(data["issue"]["created_on"], "%Y-%m-%dT%H:%M:%SZ")
    assert issue.updated_on == datetime.strptime(data["issue"]["updated_on"], "%Y-%m-%dT%H:%M:%SZ")
    assert issue.closed_on == datetime.strptime(data["issue"]["updated_on"], "%Y-%m-%dT%H:%M:%SZ")


def test_redmine_issue_event():
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
                "name": "status_id",
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
