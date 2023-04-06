from datetime import datetime
from db.models import Issue, IssueEvent
from db.sqlite_query import SQLiteQuery
from metrics.metrics import Metrics


def test_count_status():
    query = SQLiteQuery(":memory:")
    session = query.session

    date_on_new = datetime(2023, 1, 1)
    date_move_on_resolved = datetime(2023, 2, 1)

    # 1 new, 1 workable, 2 in progress, 1 resolved
    session.add(
        Issue(
            issue_id=1,
            project=1,
            status="NEW",
            created_on=date_on_new
        )
    )
    session.add(
        Issue(
            issue_id=2,
            project=1,
            status="WORKABLE",
            created_on=date_on_new
        )
    )
    session.add(
        Issue(
            issue_id=3,
            project=1,
            status="IN_PROGRESS",
            created_on=date_on_new
        )
    )
    session.add(
        Issue(
            issue_id=4,
            project=1,
            status="IN_PROGRESS",
            created_on=date_on_new
        )
    )
    session.add(
        Issue(
            issue_id=5,
            project=1,
            status="RESOLVED",
            created_on=date_on_new,
            closed_on=date_move_on_resolved,
        )
    )
    session.commit()

    metrics = Metrics(query)
    status_counters = metrics.status_count().get_first().values
    assert status_counters[str("NEW")] == 1
    assert status_counters[str("WORKABLE")] == 1
    assert status_counters[str("IN_PROGRESS")] == 2
    assert status_counters[str("RESOLVED")] == 1

    session.close()


def test_status_count_by_date():
    query = SQLiteQuery(":memory:")
    session = query.session

    date_on_new = datetime(2023, 1, 1)
    date_on_in_progress_1 = datetime(2023, 1, 10)
    date_on_in_progress_2 = datetime(2023, 1, 15)
    date_move_on_resolved = datetime(2023, 2, 1)

    # Issue 1
    session.add(
        Issue(
            issue_id=1,
            project=1,
            status="NEW",
            created_on=date_on_new
        )
    )
    # Issue 2
    session.add(
        Issue(
            issue_id=2,
            project=1,
            status="IN_PROGRESS",
            created_on=date_on_new
        )
    )
    session.add(
        IssueEvent(
            issue_id=2,
            type="attr",
            field="status",
            created_on=date_on_new,
            new_value="NEW"
        )
    )
    session.add(
        IssueEvent(
            issue_id=2,
            type="attr",
            field="status",
            created_on=date_on_in_progress_2,
            new_value="IN_PROGRESS"
        )
    )
    # Issue 3
    session.add(
        Issue(
            issue_id=3,
            project=1,
            status="RESOLVED",
            created_on=date_on_new,
            closed_on=date_move_on_resolved,
        )
    )
    session.add(
        IssueEvent(
            issue_id=3,
            type="attr",
            field="status",
            created_on=date_on_in_progress_1,
            new_value="IN_PROGRESS"
        )
    )
    session.add(
        IssueEvent(
            issue_id=3,
            type="attr",
            field="status",
            created_on=date_move_on_resolved,
            new_value="RESOLVED"
        )
    )
    session.commit()

    metrics = Metrics(query)
    status_counters = metrics.status_count_by_date(date_on_in_progress_2).get_first().values
    print(status_counters)
    assert status_counters[str("NEW")] == 1
    assert status_counters[str("IN_PROGRESS")] == 2
    assert "RESOLVED" not in status_counters

    session.close()
