import json
from sqlalchemy import Column, Float, Integer, String, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()


def as_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def as_json(obj):
    res = {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}
    return json.dumps(res)


# pylint: disable=too-few-public-methods
class Issue(Base):
    __tablename__ = 'issue'
    id = Column(Integer, primary_key=True, autoincrement=True)
    issue_id = Column(String)
    project = Column(String)
    type = Column(String)
    tags = Column(String)
    context = Column(String)
    status = Column(String)
    priority = Column(String)
    author = Column(String)
    assigned_to = Column(String)
    subject = Column(String)
    start_date = Column(DateTime)
    due_date = Column(DateTime)
    estimated_hours = Column(Float)
    target_version = Column(String)
    parent_issue_id = Column(String)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)
    closed_on = Column(DateTime)
    __table_args__ = (UniqueConstraint(
        'issue_id', 'project', name='_unique_key'),)

    def as_dict(self):
        return as_dict(self)

    def as_json(self):
        return as_json(self)


class IssueEvent(Base):
    __tablename__ = 'issue_event'
    id = Column(Integer, primary_key=True, autoincrement=True)
    issue_id = mapped_column(ForeignKey("issue.issue_id"))
    user_name = Column(String)
    created_on = Column(DateTime)
    type = Column(String)  # Type of change
    field = Column(String)
    old_value = Column(String)
    new_value = Column(String)
    __table_args__ = (UniqueConstraint(
        'issue_id', 'type', 'field', 'created_on', name='_unique_key'),)

    def as_dict(self):
        return as_dict(self)

    def as_json(self):
        return as_json(self)


class IssueAttribute(Base):
    __tablename__ = 'issue_atrribute'
    id = Column(Integer, primary_key=True, autoincrement=True)
    issue_id = mapped_column(ForeignKey("issue.issue_id"))
    key = Column(String)
    values = Column(String)
    _table_args__ = (UniqueConstraint(
        'issue_id', 'key', name='_unique_key'),)

    def as_dict(self):
        return as_dict(self)

    def as_json(self):
        return as_json(self)


class IssueRelation(Base):
    __tablename__ = 'issue_relations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    relation_id = Column(String)
    issue_id = mapped_column(ForeignKey("issue.issue_id"))
    relation_issue_id = Column(String)
    relation_type = Column(String)
    _table_args__ = (UniqueConstraint(
        'relation_id', 'issue_id', name='_unique_key'),)

    def as_dict(self):
        return as_dict(self)

    def as_json(self):
        return as_json(self)
