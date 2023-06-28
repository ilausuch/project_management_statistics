import json
from bugzilla import Bugzilla


def fetch_scripts():
    return {'bugs_resolved_per_product': bugs_resolved_per_product,
            }


def bugs_resolved_per_product(bz: Bugzilla, params):
    query = bz.build_query(product=params['product'],
                           status="RESOLVED",
                           include_fields=['bug_status',
                                           'bug_id',
                                           'summry',
                                           'assigned_to',
                                           'creation_time',
                                           'resolution'])
    bugs = bz.query(query)
    js_bugs = json.dumps([bug.get_raw_data() for bug in bugs], default=str)
    js_bugs = json.loads(js_bugs)
    return js_bugs
