#!/usr/local/bin/python3

from redmine.redmine_dumper import RedmineDumper
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source', help="Source from where ticket will be dumped. Possible values: (redmine|bugzilla). \
            Default: redmine", default='redmine')
    parser.add_argument('--project', help="Project name", required=True)

    args = parser.parse_args()
    if args.source == "redmine":
        dumper = RedmineDumper()
        dumper.dump_to_db(args.project)
    else:
        raise NotImplementedError(f"'--source {args.source}' not supported")


if __name__ == "__main__":
    main()
