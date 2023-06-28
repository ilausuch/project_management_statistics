import argparse
import logging
import logging.config

import bugzilla
# N/A yet
# from db.metricdb import MetricDB

try:
    import config
    import bugzilla_queries
except ImportError:
    # TODO
    from . import config
    from . import bugzilla_queries

logger = logging.getLogger(__name__)
logger.info('INSIDE bugzilla_suse')


class BugzillaSuse:
    """A Class which initializes a connection to the Bugzilla server."""
    _initialized = False
    _instance = None
    server = None

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self.__class__._initialized = True

        self.url = 'https://bugzilla.suse.com'
        self._apikey = config.APIKEY
        self.server = bugzilla.Bugzilla(url="https://bugzilla.suse.com",
                                        api_key=self._apikey)
        logger.info("%s is ready", self.url)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BugzillaSuse, cls).__new__(cls,
                                                             *args,
                                                             **kwargs)
            logger.debug("new instance %s", cls._instance)
        return cls._instance


class BugzillaScriptRunner:
    """BugzillaScriptRunner handles and runs the queries against the Bugzilla
    server.
    """
    scripts = {}

    def __init__(self):
        self.bz = BugzillaSuse()
        self.scripts = bugzilla_queries.fetch_scripts()

    def run(self, scriptlist, bugzilla_filters):
        """Bugzilla script runner.

        :param scriptlist:
        List of bugzilla_queries
        :param bugzilla_filters:
        Various Bugzilla parameter passing to the scripts as query filters
        """
        results = ['Not used yet']
        logger.debug("variable results %s", results)
        if not scriptlist:
            logger.debug('Not Implemented yet and it is unused: scriptlist')
        if not bugzilla_filters:
            logger.debug('Not Implemented yet and it is unused: bugzilla_filters')
        # TODO
        # db = MetricDB()
        # for s in scriptlist:
        #     results.append(self.scripts[s](self.bz.server, bugzilla_filters))
        # NOTE: is this the best design?
        # db.insert_bugzilla_records(results)


def bzlist_queries():
    """Displays all the implemented bugzilla scripts.

    Those scripts are required by bzmain.
    """
    runner = BugzillaScriptRunner()
    print("*/ Metric Scripts /*")
    print("-" * 20)
    for key in runner.scripts.keys():
        print(key)
    print("")


def bzmain(script_list, params):
    """Bugzilla script runner.

    Running `bzmain` will initiate a BugzillaScriptRunner instance and will
    run the given set of scripts. The queries results will stored in the DB.

    :param script_list:
     List of bugzilla_queries
    :param params:
     Various Bugzilla parameter passing to the scripts
    """
    runner = BugzillaScriptRunner()
    logger.info("Connection to Bugzilla.suse.com is established")
    runner.run(script_list, params)


if __name__ == '__main__':
    logger = logging.getLogger(__package__)
    parser = argparse.ArgumentParser(description='Bugzilla arguments')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-P', '--prod', metavar='string', type=str,
                        help='Bugzilla product value')
    parser.add_argument('-s', '--status', metavar='string', type=str,
                        choices=['NEW',
                                 'CONFIRMED',
                                 'IN_PROGRESS',
                                 'RESOLVED'],
                        help='What status should be the bugs')
    parser.add_argument('-S', '--severity', metavar='string', type=str,
                        choices=['Critical',
                                 'Major',
                                 'Normal',
                                 'Minor',
                                 'Enhancement'],
                        help='what severity should the query use')
    parser.add_argument('-p', '--priority', metavar='string', type=str,
                        choices=['P0 - Crit Sit',
                                 'P1 - Urgent',
                                 'P2 - High',
                                 'P3 - Medium',
                                 'P4 - Low',
                                 'P5 - None'],
                        help='What priority should we query')
    parser.add_argument('-n', '--range', metavar='int', type=int, default=max,
                        help='An integer value which will give the range \
                        of the query since current date')
    parser.add_argument('-x', '--exec', nargs='*',
                        help='List of bugzilla_queries to run')

    main_args = parser.parse_args()
    print("--__main__-- run")
    scripts = main_args.exec
    filters = {'product': main_args.prod,
               'status': main_args.status,
               'severity': main_args.severity,
               'priority': main_args.priority,
               'range': main_args.range}

    bzmain(scripts, filters)
