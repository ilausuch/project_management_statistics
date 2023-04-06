from datetime import datetime
from db.models import Issue, IssueEvent
from db.sqlite_query import SQLiteQuery


def test_status_snapshot():
    query = SQLiteQuery(":memory:")
    session = query.session

    date_on_new = datetime(2023, 1, 1)
    date_move_on_in_progress = datetime(2023, 1, 15)
    date_move_on_resolved = datetime(2023, 2, 1)

    session.add(
        Issue(
            issue_id=1,
            project=1,
            status="RESOLVED",
            created_on=date_on_new,
            closed_on=date_move_on_resolved,
        )
    )
    session.add(
        IssueEvent(
            issue_id=1,
            type="attr",
            field="status",
            created_on=date_on_new,
            new_value="NEW"
        )
    )
    session.add(
        IssueEvent(
            issue_id=1,
            type="attr",
            field="status",
            created_on=date_move_on_in_progress,
            old_value="WORKABLE",
            new_value="IN_PROGRESS"
        )
    )
    session.add(
        IssueEvent(
            issue_id=1,
            type="attr",
            field="status",
            created_on=date_move_on_resolved,
            old_value="IN_PROGRESS",
            new_value="RESOLVED"
        )
    )
    session.commit()

    # Get the current state for the issue (should be one)
    result = query.issues(project=1)
    assert len(result) == 1
    assert result[0]["status"] == str("RESOLVED")

    result = query.status_snapshot(date=date_on_new, project=1)
    assert len(result) == 1
    assert result[0]["status"] == str("NEW")

    result = query.status_snapshot(date=date_move_on_in_progress, project=1)
    assert len(result) == 1
    assert result[0]["status"] == str("IN_PROGRESS")

    result = query.status_snapshot(date=date_move_on_resolved, project=1)
    assert len(result) == 1
    assert result[0]["status"] == str("RESOLVED")

    result = query.status_snapshot(date=datetime(2024, 1, 1), project=1)
    assert len(result) == 1
    assert result[0]["status"] == str("RESOLVED")

    # The date before the issue is created
    result = query.status_snapshot(date=datetime(2022, 1, 1), project=1)
    assert len(result) == 0

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
        status="RESOLVED",
        created_on=date_before_period_in_1,
        closed_on=date_before_period_in_2
    ))
    session.add(Issue(
        issue_id=2,
        project=1,
        status="RESOLVED",
        created_on=date_before_period_in_1,
        closed_on=date_period_1
    ))
    session.add(Issue(
        issue_id=3,
        project=1,
        status="RESOLVED",
        created_on=date_before_period_in_1,
        closed_on=date_after_period_out_1
    ))
    session.add(Issue(
        issue_id=4,
        project=1,
        status="RESOLVED",
        created_on=date_period_1,
        closed_on=date_period_2
    ))
    session.add(Issue(
        issue_id=5,
        project=1,
        status="RESOLVED",
        created_on=date_period_2,
        closed_on=date_after_period_out_1
    ))
    session.add(Issue(
        issue_id=6,
        project=1,
        status="RESOLVED",
        created_on=date_after_period_out_1,
        closed_on=date_after_period_out_2
    ))
    session.commit()

    result = query.issues_active_in_period(date_in=date_period_in, date_out=date_period_out, project=1)
    print(result)
    assert len(result) == 4

    session.close()
