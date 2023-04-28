from typing import Dict, Any
import sys
import logging
import requests
from ratelimiter import RateLimiter
from redmine import config


class RedmineConnector:
    def __init__(self, logging_level: int):
        self.logger = logging.getLogger(self.__module__)
        self.logger.setLevel(logging_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("Init connection to %s", config.REDMINE_URL)
        self.rate_limiter = RateLimiter(max_calls=config.REDMINE_QUERY_RATIO, period=60)

    def raw_query(self, url_ending: str, filters: Dict[str, list] = {}) -> Any:
        query = f"{config.REDMINE_URL}{url_ending}?utf8=✓"
        if len(filters) > 0:
            query = f"{query}&set_filter=1"
            for filter_key in filters:
                filter_str = self.prepare_filter(
                    filter_key, filters[filter_key], '=')
                query = f"{query}&{filter_str}"
        self.logger.debug("Resulting request %s. Waiting for rate_limiter...", query)
        with self.rate_limiter:
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

    def relations(self, issue_id):
        issue = self.issue(issue_id, {"include": ["relations"]})
        return issue['relations']

    def issue_full(self, issue_id):
        issue = self.issue(issue_id, {"include": ["relations", "journals", "children",
                                                  "attachments", "changesets", "watchers",
                                                  "allowed_statuses"]})
        return issue

    def prepare_filter(self, key: str, values: list, operator: str) -> str:
        if len(values) == 0:
            raise ValueError("List of values can not be empty")
        if len(values) == 1:
            return f"{key}={values[0]}"

        if key == "include":
            return f"include={','.join(values)}"

        filter_str = f"f[]={key}&op[{key}]={operator}"
        for value in values:
            filter_str = f"{filter_str}&v[{key}][]={value}"
        return filter_str
