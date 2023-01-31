#!/usr/local/bin/python3

from redmine.redmine_dumper import RedmineDumper


def main():
    dumper = RedmineDumper()
    dumper.dump_to_db()


if __name__ == "__main__":
    main()
