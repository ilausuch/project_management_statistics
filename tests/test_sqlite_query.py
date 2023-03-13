from datetime import datetime
from db.models import Issue, IssueEvent
from db.sqlite_query import SQLiteQuery
from redmine.redmine_dumper import RedmineStatus


def test_status_snapshot():
    query = SQLiteQuery(":memory:")
    session = query.session

    date_on_new = datetime(2023, 1, 1)
    date_move_on_in_progress = datetime(2023, 1, 15)
    date_move_on_resolved = datetime(2023, 2, 1)

    session.add(
        Issue(
            issue_id=1,
            project_id=1,
            type_id=1,
            status_id=RedmineStatus.RESOLVED.value,
            created_on=date_on_new,
            closed_on=date_move_on_resolved,
        )
    )
    session.add(
        IssueEvent(
            issue_id=1,
            type="attr",
            field="status_id",
            created_on=date_on_new,
            new_value=RedmineStatus.NEW.value
        )
    )
    session.add(
        IssueEvent(
            issue_id=1,
            type="attr",
            field="status_id",
            created_on=date_move_on_in_progress,
            old_value=RedmineStatus.WORKABLE.value,
            new_value=RedmineStatus.IN_PROGRESS.value
        )
    )
    session.add(
        IssueEvent(
            issue_id=1,
            type="attr",
            field="status_id",
            created_on=date_move_on_resolved,
            old_value=RedmineStatus.IN_PROGRESS.value,
            new_value=RedmineStatus.RESOLVED.value
        )
    )
    session.commit()

    # Get the current state for the issue (should be one)
    result = query.issues(project_id=1)
    assert len(result) == 1
    assert result[0]["status_id"] == RedmineStatus.RESOLVED.value

    result = query.status_snapshot(date=date_on_new, project_id=1)
    assert len(result) == 1
    assert result[0]["status_id"] == RedmineStatus.NEW.value

    result = query.status_snapshot(date=date_move_on_in_progress, project_id=1)
    assert len(result) == 1
    assert result[0]["status_id"] == RedmineStatus.IN_PROGRESS.value

    result = query.status_snapshot(date=date_move_on_resolved, project_id=1)
    assert len(result) == 1
    assert result[0]["status_id"] == RedmineStatus.RESOLVED.value

    result = query.status_snapshot(date=datetime(2024, 1, 1), project_id=1)
    assert len(result) == 1
    assert result[0]["status_id"] == RedmineStatus.RESOLVED.value

    # The date before the issue is created
    result = query.status_snapshot(date=datetime(2022, 1, 1), project_id=1)
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
        project_id=1,
        status_id=RedmineStatus.RESOLVED.value,
        created_on=date_before_period_in_1,
        closed_on=date_before_period_in_2
    ))
    session.add(Issue(
        issue_id=2,
        project_id=1,
        status_id=RedmineStatus.RESOLVED.value,
        created_on=date_before_period_in_1,
        closed_on=date_period_1
    ))
    session.add(Issue(
        issue_id=3,
        project_id=1,
        status_id=RedmineStatus.RESOLVED.value,
        created_on=date_before_period_in_1,
        closed_on=date_after_period_out_1
    ))
    session.add(Issue(
        issue_id=4,
        project_id=1,
        status_id=RedmineStatus.RESOLVED.value,
        created_on=date_period_1,
        closed_on=date_period_2
    ))
    session.add(Issue(
        issue_id=5,
        project_id=1,
        status_id=RedmineStatus.RESOLVED.value,
        created_on=date_period_2,
        closed_on=date_after_period_out_1
    ))
    session.add(Issue(
        issue_id=6,
        project_id=1,
        status_id=RedmineStatus.RESOLVED.value,
        created_on=date_after_period_out_1,
        closed_on=date_after_period_out_2
    ))
    session.commit()

    result = query.issues_active_in_period(date_in=date_period_in, date_out=date_period_out, project_id=1)
    print(result)
    assert len(result) == 4

    session.close()
