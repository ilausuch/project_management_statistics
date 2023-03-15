import sys
import logging
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from db.models import Base, Issue, IssueEvent


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

    def issues(self, **filters):
        """
        Get all issues
        :param filter: A dict of filters e.g. project_id=1
        :return: A list of issues
        """
        issues = self.session.query(Issue).filter_by(**filters).all()
        return [issue.__dict__ for issue in issues]

    def status_snapshot(self, date, **filters):
        """
        Get all the active and resolved issues with the status in a especific moment
        :param date (datetime): The date for the snapshot. None means the last values
        :param filter: A dict of filters e.g. project_id=1
        :return: A list of issues
        """
        issues_to_date = self.session.query(Issue).filter_by(**filters).filter(Issue.created_on <= date).all()
        issues_dict = [issue.__dict__ for issue in issues_to_date]
        for issue in issues_dict:
            state = self.session.query(IssueEvent).filter(
                IssueEvent.issue_id == issue["issue_id"],
                IssueEvent.type == "attr",
                IssueEvent.field == "status_id")
            state = state.filter(IssueEvent.created_on <= date).order_by(IssueEvent.created_on.desc()).first()
            if state is not None:
                issue["status_id"] = int(state.new_value)

        return issues_dict

    def issues_active_in_period(self, date_in, date_out, **filters):
        """
        Get all the issues that are active (not closed) during a period of time
        :param date_in (datetime): The begining of the period
        :param date_out (datetime): The end of the period
        :param filter: A dict of filters e.g. project_id=1
        :return: A list of issues
        """
        query = self.session.query(Issue).filter_by(**filters).filter(Issue.created_on < date_out)
        issues_in_period = query.filter(or_(Issue.closed_on is None, Issue.closed_on > date_in)).all()
        return [issue.__dict__ for issue in issues_in_period]

    def get_first_date(self, **filters):
        """
        Retrieve the date for the first object created, filtered by the specified criteria
        based on the created_on attribute.
        :param filter: A dict of filters e.g. project_id=1
        :return: A datetime object
        """
        first_object = self.session.query(Issue).filter_by(**filters).order_by(Issue.created_on.asc()).first()
        return first_object.__dict__["created_on"]
