import sys
import logging
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from db.models import Base, Issue, IssueEvent
from db.filter_builder import FilterBuilder  # pylint: disable=import-error,no-name-in-module


class SQLiteQuery:

    def __init__(self, database) -> None:
        self.logger = logging.getLogger(self.__module__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        engine = create_engine(f"sqlite:///{database}")
        Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()

    def __prepare_query_issues(self, filters):
        query = self.session.query(Issue)
        filter_builder = FilterBuilder(Issue)
        filter_conditions = filter_builder.build_filters(filters)
        query = query.filter(filter_conditions)
        return query

    def issues(self, filters):
        """
        Get all issues
        :param filter: A dict of filters e.g. project=1
        :return: A list of issues
        """
        query = self.__prepare_query_issues(filters)
        issues = query.all()
        return [issue.__dict__ for issue in issues]

    def status_snapshot(self, date, filters):
        """
        Get all the active and resolved issues with the status in a especific moment
        :param date (datetime): The date for the snapshot. None means the last values
        :param filter: A dict of filters e.g. project=1
        :return: A list of issues
        """
        query = self.__prepare_query_issues(filters)
        issues_to_date = query.filter(Issue.created_on <= date).all()
        issues_dict = [issue.as_dict() for issue in issues_to_date]

        for issue in issues_dict:
            state = self.session.query(IssueEvent).filter(
                IssueEvent.issue_id == issue["issue_id"],
                IssueEvent.type == "attr",
                IssueEvent.field == "status",
                IssueEvent.created_on <= date).order_by(
                    IssueEvent.created_on.desc()).first()

            if state is not None:
                issue["status"] = state.new_value
            else:
                state = self.session.query(IssueEvent).filter(
                    IssueEvent.issue_id == issue["issue_id"],
                    IssueEvent.type == "attr",
                    IssueEvent.field == "status",
                    IssueEvent.created_on > date).order_by(
                        IssueEvent.created_on.asc()).first()
                if state is not None:
                    issue["status"] = state.old_value
                else:
                    if issue["closed_on"] is not None and date < issue["closed_on"]:
                        issue["status"] = "New"

        return issues_dict

    def issues_active_in_period(self, date_in, date_out, filters):
        """
        Get all the issues that are active (not closed) during a period of time
        :param date_in (datetime): The begining of the period
        :param date_out (datetime): The end of the period
        :param filter: A dict of filters e.g. project=1
        :return: A list of issues
        """
        query = self.__prepare_query_issues(filters)
        query = query.filter(Issue.created_on < date_out)
        issues_in_period = query.filter(or_(Issue.closed_on is None, Issue.closed_on > date_in)).all()
        return [issue.__dict__ for issue in issues_in_period]

    def get_first_date(self, **filters):
        """
        Retrieve the date for the first object created, filtered by the specified criteria
        based on the created_on attribute.
        :param filter: A dict of filters e.g. project=1
        :return: A datetime object
        """
        query = self.__prepare_query_issues(filters)
        first_object = query.order_by(Issue.created_on.asc()).first()
        return first_object.__dict__["created_on"]
