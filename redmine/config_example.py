# Edit this and rename as config.py

# Redmine url
REDMINE_URL = "https://progress.opensuse.org"

# API token
REDMINE_KEY = ""

# Max calls per minute
REDMINE_QUERY_RATIO = 100


# Status code to string mappings
STATUS_CODE_TO_STRING = {
    '1': 'NEW',
    '2': 'IN_PROGRESS',
    '3': 'RESOLVED',
    '4': 'FEEDBACK',
    '5': 'CLOSED',
    '6': 'REJECTED',
    '12': 'WORKABLE',
    '15': 'BLOCKED'
}
