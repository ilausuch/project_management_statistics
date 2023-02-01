import sys
from redminelib import Redmine
import redmine.config as config
from db.models import Base, Issue
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class RedmineDumper:

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__module__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info(f"Init connection to {config.PROGRESS_URL}")
        self.redmine = Redmine(config.PROGRESS_URL, key=config.PROGRESS_URL)
        engine = create_engine(f"sqlite:///{config.REDMINE_DB}")
        Base.metadata.create_all(
            engine, Base.metadata.tables.values(), checkfirst=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.issue_query = self.session.query(Issue)

    def dump_to_db(self, query_id) -> None:
        self.logger.info("Dump data into local DB")
        if query_id:
            self.logger.info(f"using query ID={query_id} to filter entities")
            issues = self.redmine.issue.all().filter(query_id=query_id)
        else:
            self.logger.warning(
                "Because query id was not specified we will limit fetched entitied to 100")
            issues = self.redmine.issue.all(limit=100)
        self.logger.info(len(issues))
