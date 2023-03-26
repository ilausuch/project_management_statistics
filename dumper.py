#!/usr/bin/env python3
import argparse
import logging
import logging.config
import yaml

from redmine.redmine_dumper import RedmineDumper
from bsc.bugzilla_suse import bzmain

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', help="SQLite file path", required=True)
    parser.add_argument('-v', action='store_true', help='increase output verbosity')
    subparsers = parser.add_subparsers(dest='source', required=True)
    redmine_parser = subparsers.add_parser('redmine', help='redmine help')
    redmine_parser.add_argument('--project', help="Project name")
    
    bsc_parser = subparsers.add_parser('bugzilla', help='bugzilla help')
    bsc_parser.add_argument('-P', '--prod', metavar='string', type=str,
                        help='Bugzilla product value')
    bsc_parser.add_argument('-s', '--status', metavar='string', type=str,
                        choices=['NEW', 'CONFIRMED', 'IN_PROGRESS', 'RESOLVED'],
                        help='What status should be the bugs')  #[RESOLVED,]
    bsc_parser.add_argument('-S', '--severity', metavar='string', type=str,
                        choices=['Critical', 'Major', 'Normal', 'Minor', 'Enhancement'],
                        help='what severity should the query use')  #[Critical,]
    bsc_parser.add_argument('-p', '--priority', metavar='string', type=str,
                        choices=['P0 - Crit Sit', 'P1 - Urgent','P2 - High','P3 - Medium','P4 - Low', 'P5 - None'],
                        help='What priority should we query')  #[P2 - High,]
    bsc_parser.add_argument('-n', '--range', metavar='int', type=int, default=max,
                        help='An integer value which will give the range of the query since current date')
    bsc_parser.add_argument('-x', '--exec', nargs='*',
                        help='List of bsc_queries to run')
    args = parser.parse_args()

    with open('logging.yaml', 'r') as ymlfile:
        conf = yaml.safe_load(ymlfile)
    
    logging.config.dictConfig(conf)
    logger = logging.getLogger(__package__)
    if args.v is True:
        logger.setLevel(logging.DEBUG)
    logger.info('info log')
    logger.debug('debug log')
    
    print(args)
    if args.source == "redmine":
        if args.project is None:
            raise TypeError("dumper.py: error: the following arguments are required: --project when source is redmine")

        logger.info("Dumping from %s (project: %s) to database %s", args.source, args.project, args.database)
        dumper = RedmineDumper(args.database, logging_level)
        dumper.dump_to_db(args.project)
    elif args.source == "bugzilla":
        
        params = {'product': args.prod,
              'status': args.status,
              'severity': args.severity,
              'priority': args.priority,
              'range': args.range}
        for script in args.exec:
            logger.info("%s is passed to run" % script)
        bzmain(args.exec, params)
    else:
        raise NotImplementedError(f"'--source {args.source}' not supported")


if __name__ == "__main__":
    main()
