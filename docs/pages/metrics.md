
# Develop a metrics system

## requeriments

Import Metrics and SQLiteQuery if is necessary
```

from db.sqlite_query import SQLiteQuery
```

Create the objects
```
query = SQLiteQuery(<file>)
metrics = Metrics(query)
```


## Methods

TODO: Add methods


## Metrics results

Use MetricsResults or MetricsTimeSeries Classes

### MetricsResults

Represents a metric snapshot in a certain moment of time.
Contains:
- date: The date of the snapshot
- data: The data of the snapshot
- metadata: The metadata of the snapshot. e.g. filters used

### MetricsTimeSeries

Represents a metric in a certain period of time. Can have multiple time series.
It uses pandas DataFrame to store the data.

Contains:
- data: The list of series (Pandas DataFrame)
- metadata: The metadata of the metric. e.g. filters used
