import sys
import re


def print_help():
    print("""
hide()
    Hide the current column.

sum(columns...)
    Generate a new column as the sum of the listed columns.

avg(columns...)
    Generate a new column as the average of the listed columns.

mult(column1, column2)
    Generate a new column as the product of column1 and column2.

div(column1, column2)
    Generate a new column as the division of column1 by column2.

incr(column1)
    Generate a new column as the accumulation of values for column1.

diff(column1)
    Generate a new column as the difference between the previous and current value in column1.
""")


def extract_parts(expression):
    patterns = [r'^(\w+)\.(\w+)\(?([\w\,\s]*)\)?$', r'^(\w+)=(\w+)\(?([\w\,\s]*)\)?$']

    for pattern in patterns:
        match = re.match(pattern, expression)

        if match:
            arguments_str = match.group(3)
            if arguments_str:
                arguments = [arg.strip() for arg in arguments_str.split(',')]
            else:
                arguments = []

            return {"column": match.group(1), "operation": match.group(2), "arguments": arguments}

    return None


class ColumnParser:
    def add_column_arguments(self, parser):
        parser.add_argument('--column', help="Specify a column operation. See README.md or write --column help", action='append')

    def _parse_columns(self, args):
        columns = []
        if "column" in args and args["column"] is not None:
            for column_operation in args["column"]:
                column_operation = column_operation.strip()
                parts = extract_parts(column_operation)
                if parts is not None:
                    columns.append(parts)
                else:
                    if not column_operation == "help":
                        print("Invalid column operation format:", column_operation)
                    print_help()
                    sys.exit(1)

        return columns

    def get_columns(self, args):
        return self._parse_columns(args)
