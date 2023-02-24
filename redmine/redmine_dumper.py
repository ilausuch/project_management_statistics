import datetime
from enum import Enum
from typing import Dict, Any
import sys
import logging
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redmine import config
from db.models import Base, Issue, IssueEvent


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


REDMINE_DATE_FORMAT = '%Y-%m-%d'
REDMINE_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


# pylint: disable=too-many-branches
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
# pylint: disable=super-init-not-called
class RedmineIssue(Issue):
    def __init__(self, issue_dict):
        if 'id' in issue_dict:
            self.issue_id = issue_dict['id']
        if 'project_' in issue_dict:
            self.project_id = issue_dict['project']['id']
        if 'status' in issue_dict:
            self.status_id = issue_dict['status']['id']
        if 'priority' in issue_dict:
            self.priority_id = issue_dict['priority']['id']
        if 'author' in issue_dict:
            self.author = issue_dict['author']['name']
        if 'assigned_to' in issue_dict:
            self.assigned_to = issue_dict['assigned_to']['name']
        if 'subject' in issue_dict:
            self.subject = issue_dict['subject']
        if 'estimated_hours' in issue_dict:
            self.estimated_hours = issue_dict['estimated_hours']
        if 'start_date' in issue_dict and issue_dict['start_date'] is not None:
            self.start_date = datetime.datetime.strptime(issue_dict['start_date'], REDMINE_DATE_FORMAT)
        if 'due_date' in issue_dict and issue_dict['due_date'] is not None:
            self.due_date = datetime.datetime.strptime(issue_dict['due_date'], REDMINE_DATE_FORMAT)
        if 'created_on' in issue_dict and issue_dict['created_on'] is not None:
            self.created_on = datetime.datetime.strptime(issue_dict['created_on'], REDMINE_DATETIME_FORMAT)
        if 'updated_on' in issue_dict and issue_dict['updated_on'] is not None:
            self.updated_on = datetime.datetime.strptime(issue_dict['updated_on'], REDMINE_DATETIME_FORMAT)
        if 'closed_on' in issue_dict and issue_dict['closed_on'] is not None:
            self.closed_on = datetime.datetime.strptime(issue_dict['closed_on'], REDMINE_DATETIME_FORMAT)


class RedmineIssueEvent(IssueEvent):
    def __init__(self, journal_dict, change_dict, issue_id):
        self.issue_id = issue_id
        if 'user' in journal_dict:
            self.user_name = journal_dict['user']['name']
        if 'created_on' in journal_dict and journal_dict['created_on'] is not None:
            self.created_on = datetime.datetime.strptime(journal_dict['created_on'], REDMINE_DATETIME_FORMAT)

        if change_dict["property"] == 'attr':
            self.type = 'attr'
            self.field = change_dict['name']
            self.old_value = change_dict['old_value']
            self.new_value = change_dict['new_value']

    @staticmethod
    def get_events(journal_dict, issue_id):
        result = []
        if 'details' in journal_dict:
            for change_dict in journal_dict['details']:
                if change_dict["property"] == 'attr':
                    result.append(RedmineIssueEvent(journal_dict, change_dict, issue_id))
        return result

# pylint: enable=too-many-branches
# pylint: enable=too-few-public-methods
# pylint: enable=too-many-instance-attributes
# pylint: enable=super-init-not-called

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
        self.logger.info("Init connection to %s", config.REDMINE_URL)
        engine = create_engine(f"sqlite:///{config.MIRROR_SQLITE_DB}")
        Base.metadata.create_all(
            engine, Base.metadata.tables.values(), checkfirst=True)
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()

    def raw_query(self, url_ending: str, filters: Dict[str, list] = {}) -> Any:
        query = f"{config.REDMINE_URL}{url_ending}?utf8=✓"
        if len(filters) > 0:
            query = f"{query}&set_filter=1"
            for filter_key in filters:
                filter_str = self.prepare_filter(
                    filter_key, filters[filter_key], '=')
                query = f"{query}&{filter_str}"
        self.logger.debug("Resulting request %s", query)
        response = requests.get(query, headers={
            'X-Redmine-API-Key': config.REDMINE_KEY}, timeout=60)
        response.raise_for_status()
        response_json = response.json()
        return response_json

    def issues(self, project: str, filters: Dict[str, list] = {}) -> list:
        response = self.raw_query(f"/projects/{project}/issues.json", filters)
        return response['issues']

    def issue(self, issue_id, filters: Dict[str, list] = {}):
        response = self.raw_query(f"/issues/{issue_id}.json", filters)
        return response['issue']

    def journals(self, issue_id):
        issue = self.issue(issue_id, {"include": ["journals"]})
        return issue['journals']

    def prepare_filter(self, key: str, values: list, operator: str) -> str:
        if len(values) == 0:
            raise ValueError("List of values can not be empty")
        if len(values) == 1:
            return f"{key}={values[0]}"

        filter_str = f"f[]={key}&op[{key}]={operator}"
        for value in values:
            filter_str = f"{filter_str}&v[{key}][]={value}"
        return filter_str

    def dump_to_db(self, project_name: str) -> None:
        self.logger.info("Dump data into local DB")
        offset = 0
        limit = 100
        while True:
            redmine_issues = self.issues(project_name, {"status_id": "*", "limit": [limit],
                                                        "offset": [offset]})
            if len(redmine_issues) > 0:
                for redmine_issue in redmine_issues:
                    redmine_sql_issue = RedmineIssue(redmine_issue)
                    from_db = self.session.query(Issue).filter(
                        Issue.issue_id == redmine_sql_issue.issue_id,
                        Issue.project_id == redmine_sql_issue.project_id).first()
                    if from_db:
                        self.logger.debug(
                            "Issue with id=%d already exists updating", from_db.id)
                        for attribute, value in vars(redmine_sql_issue).items():
                            setattr(from_db, attribute, value)
                    else:
                        self.logger.debug(
                            "Issue with issue_id=%d not exists. Creating new record", redmine_sql_issue.issue_id)
                        self.session.add(redmine_sql_issue)

                    self.dump_to_db_journals(redmine_sql_issue.issue_id)

                self.logger.debug("Processed %s", len(redmine_issues))
                offset += limit
            else:
                break

        self.session.commit()

    def dump_to_db_journals(self, issue_id: int) -> None:
        journals = self.journals(issue_id)
        for journal in journals:
            events = RedmineIssueEvent.get_events(journal, issue_id)
            for event in events:
                event_from_db = self.session.query(IssueEvent).filter(
                    IssueEvent.issue_id == event.issue_id,
                    IssueEvent.type == event.type,
                    IssueEvent.field == event.field,
                    IssueEvent.created_on == event.created_on).first()
                if event_from_db:
                    self.logger.debug(
                        "IssueEvent with id=%d and already exists updating", event_from_db.id)
                    for attribute, value in vars(event).items():
                        setattr(event_from_db, attribute, value)
                else:
                    self.logger.debug(
                        "IssueEvent for issue_id=%d not exists. Creating new record", event.issue_id)
                    self.session.add(event)
