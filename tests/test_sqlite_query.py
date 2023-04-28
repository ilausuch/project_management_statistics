from datetime import datetime
from db.models import Issue, IssueEvent
from db.sqlite_query import SQLiteQuery


filter_project_1 = {'project': {'op': 'eq', 'value': '1'}}


def test_status_snapshot():
    query = SQLiteQuery(":memory:")
    session = query.session

    # Dates
    date_on_new = datetime(2023, 1, 1)
    date_move_on_in_progress = datetime(2023, 1, 15)
    date_move_on_resolved = datetime(2023, 2, 1)
    date_move_on_closed = datetime(2023, 2, 15)

    # Issues
    issue1 = Issue(issue_id=1, project=1, status="Closed", created_on=date_on_new, closed_on=date_move_on_closed)
    issue2 = Issue(issue_id=2, project=1, status="Resolved", created_on=date_on_new, closed_on=date_move_on_resolved)
    issue3 = Issue(issue_id=3, project=1, status="Resolved", created_on=date_on_new, closed_on=date_move_on_resolved)
    issue4 = Issue(issue_id=4, project=1, status="In_Progress", created_on=date_on_new, closed_on=None)

    session.add_all([issue1, issue2, issue3, issue4])

    # Issue events for issue 1
    session.add_all([
        IssueEvent(issue_id=1, type="attr", field="status", created_on=date_on_new, new_value="New"),
        IssueEvent(issue_id=1, type="attr", field="status", created_on=date_move_on_in_progress,
                   old_value="New", new_value="In_Progress"),
        IssueEvent(issue_id=1, type="attr", field="status", created_on=date_move_on_resolved,
                   old_value="In_Progress", new_value="Resolved"),
        IssueEvent(issue_id=1, type="attr", field="status", created_on=date_move_on_closed,
                   old_value="Resolved", new_value="Closed"),
    ])

    # Issue events for issue 2
    session.add_all([
        IssueEvent(issue_id=2, type="attr", field="status", created_on=date_on_new, new_value="New"),
        IssueEvent(issue_id=2, type="attr", field="status", created_on=date_move_on_in_progress,
                   old_value="New", new_value="In_Progress"),
        IssueEvent(issue_id=2, type="attr", field="status", created_on=date_move_on_resolved,
                   old_value="In_Progress", new_value="Resolved"),
    ])

    # Issue events for issue 4
    session.add_all([
        IssueEvent(issue_id=4, type="attr", field="status", created_on=date_move_on_in_progress,
                   old_value="New", new_value="In_Progress")
    ])

    session.commit()

    # Test case 1: Snapshot for an issue without an initial IssueEvent
    result = query.status_snapshot(date=date_on_new, filters=filter_project_1)
    assert len(result) == 4
    assert result[0]["status"] == "New"
    assert result[1]["status"] == "New"
    assert result[2]["status"] == "New"
    assert result[3]["status"] == "New"

    # Test case 2: Snapshot on the date of issue2 being resolved
    result = query.status_snapshot(date=date_move_on_in_progress, filters=filter_project_1)
    assert len(result) == 4
    assert result[0]["status"] == "In_Progress"
    assert result[1]["status"] == "In_Progress"
    assert result[2]["status"] == "New"
    assert result[3]["status"] == "In_Progress"

    # Test case 3: Snapshot on the date of issue2 being resolved
    result = query.status_snapshot(date=date_move_on_resolved, filters=filter_project_1)
    assert len(result) == 4
    assert result[0]["status"] == "Resolved"
    assert result[1]["status"] == "Resolved"
    assert result[2]["status"] == "Resolved"
    assert result[3]["status"] == "In_Progress"

    # Test case 4: Snapshot on the date of issue1 being closed
    result = query.status_snapshot(date=date_move_on_closed, filters=filter_project_1)
    assert len(result) == 4
    assert result[0]["status"] == "Closed"
    assert result[1]["status"] == "Resolved"
    assert result[2]["status"] == "Resolved"
    assert result[3]["status"] == "In_Progress"

    # Test case 5: Snapshot on a date after all the events
    result = query.status_snapshot(date=datetime(2023, 3, 1), filters=filter_project_1)
    assert len(result) == 4
    assert result[0]["status"] == "Closed"
    assert result[1]["status"] == "Resolved"
    assert result[2]["status"] == "Resolved"
    assert result[3]["status"] == "In_Progress"

    session.close()


def test_issues_active_in_period():
    query = SQLiteQuery(":memory:")
    session = query.session

    date_before_period_in_1 = datetime(2023, 2, 1)
    date_before_period_in_2 = datetime(2023, 2, 1)
    date_period_in = datetime(2023, 3, 1)
    date_period_1 = datetime(2023, 4, 1)
    date_period_2 = datetime(2022, 5, 1)
    date_period_out = datetime(2024, 6, 1)
    date_after_period_out_1 = datetime(2023, 7, 1)
    date_after_period_out_2 = datetime(2023, 8, 1)

    session.add(Issue(
        issue_id=1,
        project=1,
        status="Resolved",
        created_on=date_before_period_in_1,
        closed_on=date_before_period_in_2
    ))
    session.add(Issue(
        issue_id=2,
        project=1,
        status="Resolved",
        created_on=date_before_period_in_1,
        closed_on=date_period_1
    ))
    session.add(Issue(
        issue_id=3,
        project=1,
        status="Resolved",
        created_on=date_before_period_in_1,
        closed_on=date_after_period_out_1
    ))
    session.add(Issue(
        issue_id=4,
        project=1,
        status="Resolved",
        created_on=date_period_1,
        closed_on=date_period_2
    ))
    session.add(Issue(
        issue_id=5,
        project=1,
        status="Resolved",
        created_on=date_period_2,
        closed_on=date_after_period_out_1
    ))
    session.add(Issue(
        issue_id=6,
        project=1,
        status="Resolved",
        created_on=date_after_period_out_1,
        closed_on=date_after_period_out_2
    ))
    session.commit()

    result = query.issues_active_in_period(date_in=date_period_in, date_out=date_period_out, filters=filter_project_1)
    assert len(result) == 4

    session.close()
