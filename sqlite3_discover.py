import argparse
import sqlite3


def get_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()


def get_columns(cursor, table):
    cursor.execute(f"PRAGMA table_info({table})")
    return [column[1] for column in cursor.fetchall()]


def get_unique_field_values(cursor, table, field):
    cursor.execute(f"SELECT DISTINCT {field} FROM {table}")
    return cursor.fetchall()


def main(database, table, field):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    if table is None:
        print('Tables:')
        for tbl in get_tables(cursor):
            print(tbl[0])
    elif field is None:
        print(f'Columns for table {table}:')
        for col in get_columns(cursor, table):
            print(col)
    else:
        print(f'Unique values for field {field} in table {table}:')
        for val in get_unique_field_values(cursor, table, field):
            print(val[0])

    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process SQLite database.')
    parser.add_argument('--database', required=True, help='Database file name')
    parser.add_argument('--table', help='Table name')
    parser.add_argument('--field', help='Field name')

    args = parser.parse_args()
    main(args.database, args.table, args.field)
