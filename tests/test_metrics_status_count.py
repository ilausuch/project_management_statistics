from datetime import datetime
from db.models import Issue, IssueEvent
from db.sqlite_query import SQLiteQuery
from metrics.metrics_status_count import MetricsStatusCount


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

    metrics = MetricsStatusCount(query)
    status_counters = metrics.status_count().data
    assert status_counters[str("NEW")] == 1
    assert status_counters[str("WORKABLE")] == 1
    assert status_counters[str("IN_PROGRESS")] == 2
    assert status_counters[str("RESOLVED")] == 1

    session.close()


def prepare_data(session):
    '''
    Legend:
        N - NEW
        P - IN_PROGRESS
        R - RESOLVED
        . - No event

    Issue Events:
        Issue 1: N..............
        Issue 2: N.......P......
        Issue 3: N...P....R.....

    Status Count at Each Moment:
    index  date     N  P  R
        0  Jan 1:   3  0  0
        9  Jan 10:  2  1  0
       14  Jan 15:  1  2  0
       31  Feb 1:   1  1  1

    '''
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
            old_value="NEW",
            new_value="IN_PROGRESS"
        )
    )
    session.add(
        IssueEvent(
            issue_id=3,
            type="attr",
            field="status",
            created_on=date_move_on_resolved,
            old_value="IN_PROGRESS",
            new_value="RESOLVED"
        )
    )
    session.commit()


def test_status_count_by_date():
    query = SQLiteQuery(":memory:")
    session = query.session

    prepare_data(session)

    metrics = MetricsStatusCount(query)
    status_counters = metrics.status_count_by_date(datetime(2023, 1, 15)).data
    assert status_counters[str("NEW")] == 1
    assert status_counters[str("IN_PROGRESS")] == 2
    assert "RESOLVED" not in status_counters

    session.close()


def test_status_count_by_date_range():
    query = SQLiteQuery(":memory:")
    session = query.session

    prepare_data(session)

    metrics = MetricsStatusCount(query)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 2, 1)
    time_series = metrics.status_count_by_date_range(start_date=start_date, end_date=end_date)
    results = time_series.as_array()

    assert len(time_series.data) == 32
    assert results[0]['NEW'] == 3
    assert results[0]['IN_PROGRESS'] == 0
    assert results[0]['RESOLVED'] == 0
    assert results[9]['NEW'] == 2
    assert results[9]['IN_PROGRESS'] == 1
    assert results[9]['RESOLVED'] == 0
    assert results[14]['NEW'] == 1
    assert results[14]['IN_PROGRESS'] == 2
    assert results[14]['RESOLVED'] == 0
    assert results[31]['NEW'] == 1
    assert results[31]['IN_PROGRESS'] == 1
    assert results[31]['RESOLVED'] == 1

    session.close()
