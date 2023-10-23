#!/usr/bin/env python3
import argparse
import logging
import logging.config
import yaml
from trackers.redmine.redmine_config import RedmineConfig
from trackers.redmine.redmine_dumper import RedmineDumper
# from trackers.bugzilla.bugzilla_suse import bzmain, bzlist_queries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',
                        action='store_true',
                        help='increase output verbosity')
    subparsers = parser.add_subparsers(dest='source', required=True)
    redmine_parser = subparsers.add_parser('redmine', help='redmine help')
    redmine_parser.add_argument('--project',
                                help="Project name",
                                required=True)
    redmine_parser.add_argument('--database',
                                help="SQLite file path",
                                required=True)
    redmine_parser.add_argument('--config',
                                help="Configuration file path",
                                default='trackers/redmine/redmine.yaml')

    bugzilla_parser = subparsers.add_parser('bugzilla', help='bugzilla help')
    bugzilla_parser.add_argument('-P', '--prod', metavar='string', type=str,
                                 help='Bugzilla product value')
    bugzilla_parser.add_argument('-s', '--status', metavar='string', type=str,
                                 choices=['NEW',
                                          'CONFIRMED',
                                          'IN_PROGRESS',
                                          'RESOLVED'],
                                 help='What status should be the bugs')
    bugzilla_parser.add_argument('-S', '--severity',
                                 metavar='string', type=str,
                                 choices=['Critical',
                                          'Major',
                                          'Normal',
                                          'Minor',
                                          'Enhancement'],
                                 help='what severity should the query use')
    bugzilla_parser.add_argument('-p', '--priority',
                                 metavar='string', type=str,
                                 choices=['P0 - Crit Sit',
                                          'P1 - Urgent',
                                          'P2 - High',
                                          'P3 - Medium',
                                          'P4 - Low',
                                          'P5 - None'],
                                 help='What priority should we query')
    bugzilla_parser.add_argument('-n', '--range',
                                 metavar='int', type=int,
                                 default=max,
                                 help='An integer value which will give the \
                                 range of the query since current date')
    bugzilla_parser.add_argument('-x', '--exec', nargs='*',
                                 help='List of bsc_queries to run')
    bugzilla_parser.add_argument('-l', action='store_true',
                                 dest='listqueries', required=False,
                                 help='List the metric queries \
                                 which can be used')
    args = parser.parse_args()

    with open('logging.yaml', mode="r", encoding="utf-8") as ymlfile:
        conf = yaml.safe_load(ymlfile)

    logging.config.dictConfig(conf)
    logger = logging.getLogger(__package__)
    if args.v is True:
        logger.setLevel(logging.DEBUG)

    if args.source == "redmine":
        RedmineConfig.get_instance().load(args.config)
        if args.project is None:
            raise TypeError("dumper.py: error: the following arguments are \
            required: --project when source is redmine")

        logger.info("Dumping from %s (project: %s) to database %s",
                    args.source, args.project, args.database)
        dumper = RedmineDumper(args.database, logger.level)
        dumper.dump_to_db(args.project)
    # elif args.source == "bugzilla":
    #     if args.listqueries:
    #         bzlist_queries()
    #     else:
    #         params = {'product': args.prod,
    #                   'status': args.status,
    #                   'severity': args.severity,
    #                   'priority': args.priority,
    #                   'range': args.range}
    #         for script in args.exec:
    #             logger.info("%s is passed to run", script)
    #         bzmain(args.exec, params)
    else:
        raise NotImplementedError(f"'--source {args.source}' not supported")


if __name__ == "__main__":
    main()
