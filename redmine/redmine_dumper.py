import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redmine.redmine_connector import RedmineConnector
from db.models import Base, Issue, IssueEvent


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
        if 'project' in issue_dict:
            self.project = issue_dict['project']['name']
        if 'tracker' in issue_dict:
            self.type = issue_dict['tracker']['name']
        if 'status' in issue_dict:
            self.status = issue_dict['status']['name']
        if 'priority' in issue_dict:
            self.priority = issue_dict['priority']['name']
        if 'author' in issue_dict:
            self.author = issue_dict['author']['name']
        if 'assigned_to' in issue_dict:
            self.assigned_to = issue_dict['assigned_to']['name']
        if 'subject' in issue_dict:
            self.subject = issue_dict['subject']
        if 'estimated_hours' in issue_dict:
            self.estimated_hours = issue_dict['estimated_hours']
        if 'fixed_version' in issue_dict:
            self.target_version = issue_dict['fixed_version']
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


class RedmineDumper (RedmineConnector):

    def __init__(self, database: str, logging_level: int):
        super().__init__(logging_level)
        engine = create_engine(f"sqlite:///{database}")
        Base.metadata.create_all(
            engine, Base.metadata.tables.values(), checkfirst=True)
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()

    def dump_to_db(self, project_name: str) -> None:
        self.logger.info("Dump data into local DB")
        offset = 0
        limit = 100
        while True:
            redmine_issues = self.issues(project_name, {"sort": "id:desc",
                                                        "f[]": "status_id",
                                                        "op[status_id]": "*",
                                                        "limit": [limit],
                                                        "offset": [offset]})
            if len(redmine_issues) > 0:
                for redmine_issue in redmine_issues:
                    redmine_sql_issue = RedmineIssue(redmine_issue)
                    issue_id = redmine_sql_issue.issue_id
                    from_db = self.session.query(Issue).filter(
                        Issue.issue_id == issue_id,
                        Issue.project == redmine_sql_issue.project).first()
                    if from_db:
                        self.logger.debug(
                            "Issue with id=%d already exists updating", from_db.id)
                        for attribute, value in vars(redmine_sql_issue).items():
                            setattr(from_db, attribute, value)
                    else:
                        self.logger.debug(
                            "Issue with issue_id=%d not exists. Creating new record", issue_id)
                        self.session.add(redmine_sql_issue)

                    events = self.dump_to_db_journals(issue_id)
                    self.dump_to_db_tags(redmine_sql_issue, events)

                self.logger.debug("Processed %s", len(redmine_issues))
                offset += limit
            else:
                self.logger.info("No more issues")
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
        return events

    def dump_to_db_tags(self, redmine_sql_issue, events) -> None:
        tags = ""
        for event in events:
            if event.type == 'attr' and event.field == 'tag_list':
                tags = event.new_value
        redmine_sql_issue.tags = tags
