import datetime
from sqlalchemy import Column, Float, Integer, String, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column
from dateutil import parser

Base = declarative_base()


# pylint: disable=too-few-public-methods
class Issue(Base):
    __tablename__ = 'issue'
    id = Column(Integer, primary_key=True, autoincrement=True)
    issue_id = Column(Integer)
    project_id = Column(Integer)
    type_id = Column(Integer)
    status_id = Column(Integer)
    priority_id = Column(Integer)
    author = Column(String)
    assigned_to = Column(String)
    subject = Column(String)
    start_date = Column(DateTime)
    due_date = Column(DateTime)
    estimated_hours = Column(Float)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    closed_on = Column(DateTime)
    __table_args__ = (UniqueConstraint(
        'issue_id', 'project_id', name='_unique_key'),)

    def __init__(self, issue_dict: dict):
        if 'id' in issue_dict:
            self.issue_id = issue_dict['id']
        if 'project' in issue_dict:
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
        self.start_date = Issue.get_date(issue_dict, 'start_date')
        self.due_date = Issue.get_date(issue_dict, 'due_date')
        self.created_on = Issue.get_date(issue_dict, 'created_on')
        self.updated_on = Issue.get_date(issue_dict, 'updated_on')
        self.closed_on = Issue.get_date(issue_dict, 'closed_on')

    @staticmethod
    def get_date(issue_dict: dict, date_field: str) -> 'datetime':
        if date_field in issue_dict:
            return parser.parse(issue_dict[date_field])

    def update(self, new_issue: 'Issue'):
        self.status_id = new_issue.status_id
        self.priority_id = new_issue.priority_id
        self.author = new_issue.author
        self.assigned_to = new_issue.assigned_to
        self.subject = new_issue.subject
        self.due_date = new_issue.due_date
        self.estimated_hours = new_issue.estimated_hours
        self.start_date = new_issue.start_date
        self.updated_on = new_issue.updated_on
        self.closed_on = new_issue.closed_on

    def __str__(self):
        return '{' + f"'id' : {self.id}, 'issue_id' : {self.issue_id}, 'project_id' : {self.project_id}," + \
            f" 'type_id': {self.type_id}, 'status_id': {self.status_id}, 'priority_id' : {self.priority_id}," + \
            f" 'author' : {self.author}, 'assigned_to' : {self.assigned_to}, 'subject' : {self.subject}," + \
            f" 'start_date' : {self.start_date}, 'due_date': {self.due_date}, 'estimated_hours': {self.estimated_hours}," + \
            f"'created_on' : {self.created_on}, 'updated_on' : {self.updated_on}, 'closed_on' : {self.closed_on}" + "}"


class IssueState(Base):
    __tablename__ = 'issue_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    issue_id = mapped_column(ForeignKey("issue.issue_id"))
    user_name = Column(String)
    created_on = Column(DateTime)
    field = Column(String)
    old_value = Column(String)
    new_value = Column(String)
    __table_args__ = (UniqueConstraint(
        'issue_id', 'created_on', name='_unique_key'),)
