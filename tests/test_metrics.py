from datetime import datetime
from db.models import Issue, IssueState
from metrics.sqlite_query import SQLiteQuery
from metrics.metrics import Metrics

# Open
NEW = 1
WORKABLE = 12
IN_PROGRESS = 2
BLOCKED = 15
FEEDBACK = 4

# Closed
RESOLVED = 3
CLOSED = 5
REJECTED = 6


def test_count_status():
    query = SQLiteQuery(":memory:")
    session = query.session

    date_on_new = datetime(2023, 1, 1)
    date_move_on_resolved = datetime(2023, 2, 1)

    # 1 new, 1 workable, 2 in progress, 1 resolved
    session.add(
        Issue(
            issue_id=1,
            project_id=1,
            type_id=1,
            status_id=NEW,
            created_on=date_on_new
        )
    )
    session.add(
        Issue(
            issue_id=2,
            project_id=1,
            type_id=1,
            status_id=WORKABLE,
            created_on=date_on_new
        )
    )
    session.add(
        Issue(
            issue_id=3,
            project_id=1,
            type_id=1,
            status_id=IN_PROGRESS,
            created_on=date_on_new
        )
    )
    session.add(
        Issue(
            issue_id=4,
            project_id=1,
            type_id=1,
            status_id=IN_PROGRESS,
            created_on=date_on_new
        )
    )
    session.add(
        Issue(
            issue_id=5,
            project_id=1,
            type_id=1,
            status_id=RESOLVED,
            created_on=date_on_new,
            closed_on=date_move_on_resolved,
        )
    )
    session.commit()

    metrics = Metrics(query)
    status_counters = metrics.status_count()
    assert status_counters[NEW] == 1
    assert status_counters[WORKABLE] == 1
    assert status_counters[IN_PROGRESS] == 2
    assert status_counters[RESOLVED] == 1

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
            project_id=1,
            type_id=1,
            status_id=NEW,
            created_on=date_on_new
        )
    )
    # Issue 2
    session.add(
        Issue(
            issue_id=2,
            project_id=1,
            type_id=1,
            status_id=IN_PROGRESS,
            created_on=date_on_new
        )
    )
    session.add(
        IssueState(
            issue_id=2,
            field="status",
            created_on=date_on_new,
            new_value=NEW
        )
    )
    session.add(
        IssueState(
            issue_id=2,
            field="status",
            created_on=date_on_in_progress_2,
            new_value=IN_PROGRESS
        )
    )
    # Issue 3
    session.add(
        Issue(
            issue_id=3,
            project_id=1,
            type_id=1,
            status_id=RESOLVED,
            created_on=date_on_new,
            closed_on=date_move_on_resolved,
        )
    )
    session.add(
        IssueState(
            issue_id=3,
            field="status",
            created_on=date_on_in_progress_1,
            new_value=IN_PROGRESS
        )
    )
    session.add(
        IssueState(
            issue_id=3,
            field="status",
            created_on=date_move_on_resolved,
            new_value=RESOLVED
        )
    )
    session.commit()

    metrics = Metrics(query)
    status_counters = metrics.status_count_by_date(date_on_in_progress_2)
    assert status_counters[NEW] == 1
    assert status_counters[IN_PROGRESS] == 2
    assert RESOLVED not in status_counters

    session.close()
