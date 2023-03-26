import sys
import logging
import pymongo


class MetricDB:

    #db = None
    #client = None
    
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__module__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # Establish connection
        conn = "mongodb://localhost:27017"
        client = pymongo.MongoClient(conn)
        # Create a database
        self.db = client.classDB

    def insert_bsc_records(self, records):
        self.db.bugzilla.insert_many(records)
    def insert_redmine_records(self, records):
        self.db.redmine.insert_many(records)
