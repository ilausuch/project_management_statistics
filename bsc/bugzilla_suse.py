import argparse
import datetime
import logging
import logging.config
import sys
from typing import Dict, Any
from enum import Enum

import bugzilla
from db.metricdb import MetricDB


try:
    import config
    import bsc_queries
except:
    # TODO
    from . import config
    from . import bsc_queries


class BugzillaSuse:
    _initialized = False
    _instance = None
    bsc = None
    
    def __init__(self, *args, **kwargs):
        if self._initialized:
            return
        super(BugzillaSuse, self).__init__(*args, **kwargs)
        self.__class__._initialized = True
        
        self.url = 'https://bugzilla.suse.com'
        self._apikey = ''  # TODO Either api or USER/PASSWORD
        self._user = config.USER
        self._password = config.PASSWORD
        self.bsc = bugzilla.Bugzilla(url="https://bugzilla.suse.com", user=self._user, password=self._password)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BugzillaSuse, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
class BugzillaScriptRunner:
    scripts = {}
    
    def __init__(self):
        self.bz = BugzillaSuse()
        self.scripts = bsc_queries.fetch_scripts()
        
    def run(self, scriptlist, params):
        #print(params)
        results = []
        db = MetricDB()
        for s in scriptlist:
            results.append(self.scripts[s](self.bz.bsc, params))
        print(results)
        # NOTE: is this the best design? 
        #db.insert_bsc_records(results)

def bzmain(scripts, params):
    logger = logging.getLogger(__package__)
    runner = BugzillaScriptRunner()
    logger.info("Connection to Bugzilla.suse.com is established")
    logger.debug("Connection to Bugzilla.suse.com is established")
    #runner.run(scripts, params)
    
if __name__ == '__main__':
    #logging.config.dictConfig(LOGGING)
    #logging.config.fileConfig(LOGGING)
    #logger = logging.getLogger(__module__)
    #logger.setLevel(logging_level)
    #logger.debug('Connection to %s initialized' % self.usrl)
    parser = argparse.ArgumentParser(description='Bugzilla arguments')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-P', '--prod', metavar='string', type=str,
                        help='Bugzilla product value')
    parser.add_argument('-s', '--status', metavar='string', type=str,
                        choices=['NEW', 'CONFIRMED', 'IN_PROGRESS', 'RESOLVED'],
                        help='What status should be the bugs')  #[RESOLVED,]
    parser.add_argument('-S', '--severity', metavar='string', type=str,
                        choices=['Critical', 'Major', 'Normal', 'Minor', 'Enhancement'],
                        help='what severity should the query use')  #[Critical,]
    parser.add_argument('-p', '--priority', metavar='string', type=str,
                        choices=['P0 - Crit Sit', 'P1 - Urgent','P2 - High','P3 - Medium','P4 - Low', 'P5 - None'],
                        help='What priority should we query')  #[P2 - High,]
    parser.add_argument('-n', '--range', metavar='int', type=int, default=max,
                        help='An integer value which will give the range of the query since current date')
    parser.add_argument('-x', '--exec', nargs='*',
                        help='List of bsc_queries to run')
    
    args = parser.parse_args()
    print("--__main__-- run")
    scripts = args.exec
    params = {'product': args.prod,
              'status': args.status,
              'severity': args.severity,
              'priority': args.priority,
              'range': args.range}

    bzmain(scripts, params)
