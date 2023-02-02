import datetime
from enum import Enum
from typing import Dict, Any
import sys
import logging
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redmine import config
from db.models import Base, Issue


class RedmineStatus(Enum):
    NEW = 1
    WORKABLE = 12
    IN_PROGRESS = 2
    BLOCKED = 15
    FEEDBACK = 4

    # Closed
    RESOLVED = 3
    CLOSED = 5
    REJECTED = 6
    UNKNOWN = 0

    def is_closed(self):
        return self.name in [RedmineStatus.RESOLVED, RedmineStatus.CLOSED, RedmineStatus.REJECTED]

    def is_open(self):
        return self.name not in [RedmineStatus.RESOLVED, RedmineStatus.CLOSED, RedmineStatus.REJECTED]

# pylint: disable=too-many-instance-attributes
# pylint: disable=dangerous-default-value


class RedmineDumper:

    def __init__(self):
        self.logger = logging.getLogger(self.__module__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("Init connection to %s", config.PROGRESS_URL)
        engine = create_engine(f"sqlite:///{config.REDMINE_DB}")
        Base.metadata.create_all(
            engine, Base.metadata.tables.values(), checkfirst=True)
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()

    def raw_query(self, url_ending: str, filters: Dict[str, list] = {}) -> Any:
        query = f"{config.PROGRESS_URL}{url_ending}?utf8=✓"
        if len(filters) > 0:
            query = f"{query}&set_filter=1"
            for filter_key in filters:
                filter_str = self.prepare_filter(
                    filter_key, filters[filter_key], '=')
                query = f"{query}&{filter_str}"
        self.logger.debug("Resulting request %s", query)
        response = requests.get(query, headers={
            'X-Redmine-API-Key': config.PROGRESS_KEY}, timeout=60)
        response.raise_for_status()
        response_json = response.json()
        self.logger.debug("Got %d issues", response_json['total_count'])
        return response_json

    def prepare_filter(self, key: str, values: list, operator: str) -> str:
        if len(values) == 0:
            raise ValueError("List of values can not be empty")
        filter_str = f"f[]={key}&op[{key}]={operator}"
        for value in values:
            filter_str = f"{filter_str}&v[{key}][]={value}"
        return filter_str

    def filter_status(self, values: list, operator: str = '=') -> str:
        return self.prepare_filter("status_id", values, operator)

    def filter_tracker(self, values: list, operator: str = '=') -> str:
        return self.prepare_filter("tracker_id", values, operator)

    def filter_date(self, key: str, date: 'datetime', operator: str) -> str:
        return self.prepare_filter(key, [date.strftime('%Y-%m-%d')], operator)

    def issues(self, project: str, filters: Dict[str, list] = {}) -> list:
        response = self.raw_query(f"/projects/{project}/issues.json", filters)
        return response['issues']

    def dump_to_db(self, project_name: str) -> None:
        self.logger.info("Dump data into local DB")
        redmine_issues = self.issues(project_name)
        for redmine_issue in redmine_issues:
            sql_issue = Issue(redmine_issue)
            from_db = self.session.query(Issue).filter(
                Issue.issue_id == sql_issue.issue_id, Issue.project_id == sql_issue.project_id).first()
            if from_db:
                self.logger.debug(
                    "Issue with id=%d already exists updating", from_db.id)
                from_db.update(sql_issue)
            else:
                self.logger.debug(
                    "Issue with issue_id=%d not exists. Creating new record", sql_issue.issue_id)
                self.session.add(sql_issue)
            self.session.commit()
