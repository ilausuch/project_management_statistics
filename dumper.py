#!/usr/local/bin/python3
import logging
import argparse
from redmine.redmine_dumper import RedmineDumper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source', help="Source from where ticket will be dumped. Possible values: (redmine|bugzilla). \
            Default: redmine", default='redmine')
    parser.add_argument('--database', help="SQLite file path", required=True)
    parser.add_argument('--project', help="Project name")
    parser.add_argument('-v', action='store_true', help='increase output verbosity')
    args = parser.parse_args()

    if args.v is True:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(logging_level)

    if args.source == "redmine":
        if args.project is None:
            raise TypeError("dumper.py: error: the following arguments are required: --project when source is redmine")

        logger.info("Dumping from %s (project: %s) to database %s", args.source, args.project, args.database)
        dumper = RedmineDumper(args.database, logging_level)
        dumper.dump_to_db(args.project)
    else:
        raise NotImplementedError(f"'--source {args.source}' not supported")


if __name__ == "__main__":
    main()
