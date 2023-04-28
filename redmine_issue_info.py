import argparse
import json
import logging
from redmine.redmine_connector import RedmineConnector


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("issue_id", help="the ID of the Redmine issue to retrieve")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    redmine = RedmineConnector(logging.WARNING)
    issue = redmine.issue_full(args.issue_id)
    print(json.dumps(issue))
