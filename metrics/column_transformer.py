from typing import Union
import pandas as pd
from metrics.metrics_result import MetricsResults, MetricsTimeSeries


class ColumnTransformer:
    def __init__(self, metrics: Union[MetricsResults, MetricsTimeSeries], columns):
        self.metrics = metrics
        self.columns = columns
        self.data = metrics.as_array()

    def execute(self):
        for column in self.columns:
            column_name = column['column']
            operation = column['operation']
            arguments = column.get('arguments', [])

            if operation == 'hide':
                self.hide(column_name)
            elif operation == 'sum':
                self.sum(column_name, *arguments)
            elif operation == 'avg':
                self.avg(column_name, *arguments)
            elif operation == 'mult':
                self.mult(column_name, *arguments)
            elif operation == 'div':
                self.div(column_name, *arguments)
            elif operation == 'incr':
                self.incr(column_name, *arguments)
            elif operation == 'diff':
                self.diff(column_name, *arguments)
            else:
                raise ValueError(f'Invalid operation: {operation}')

        if isinstance(self.metrics, MetricsResults):
            self.metrics.data = self.data[0]
        else:
            dataframe = pd.DataFrame(self.data)
            self.metrics.data = dataframe

    def hide(self, column):
        for entry in self.data:
            if column in entry:
                del entry[column]
        return self

    def sum(self, new_column, *columns):
        if len(columns) < 1:
            raise ValueError(f"'sum' operation requires at least one argument, got {len(columns)}")
        for entry in self.data:
            entry[new_column] = sum(entry[col] for col in columns)
        return self

    def avg(self, new_column, *columns):
        if len(columns) < 1:
            raise ValueError(f"'avg' operation requires at least one argument, got {len(columns)}")
        for entry in self.data:
            entry[new_column] = sum(entry[col] for col in columns) / len(columns)
        return self

    def mult(self, new_column, column1, column2):
        if column1 is None or column2 is None:
            raise ValueError("'mult' operation requires exactly two arguments, got fewer.")
        for entry in self.data:
            entry[new_column] = entry[column1] * entry[column2]
        return self

    def div(self, new_column, column1, column2):
        if column1 is None or column2 is None:
            raise ValueError("'div' operation requires exactly two arguments, got fewer.")
        for entry in self.data:
            if column2 is not None:
                entry[new_column] = entry[column1] / entry[column2]
        return self

    def incr(self, new_column, column):
        if column is None:
            raise ValueError("'incr' operation requires exactly one argument, got fewer.")
        initial = self.data[0][column]
        for entry in self.data:
            entry[new_column] = entry[column] - initial
        return self

    def diff(self, new_column, column):
        if column is None:
            raise ValueError("'diff' operation requires exactly one argument, got fewer.")
        prev = self.data[0][column]
        for entry in self.data:
            entry[new_column] = entry[column] - prev
            prev = entry[column]
        return self

    @staticmethod
    def process(metrics, columns):
        transformer = ColumnTransformer(metrics, columns)
        transformer.execute()
