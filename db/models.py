from sqlalchemy import Column, Float, Integer, String, DateTime, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column

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
