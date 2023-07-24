
# Project Management Statistics for Users

## Dumping progress issues into local DB for further processing (Redmine)

To set up the environment for dumping Progress issues into a local database for further processing, follow these steps:

1. Create a file named redmine_config.yaml at the root of your project. Use the following structure for the file:

```yaml
REDMINE:
  url: <REDMINE_URL>  # The URL to target the Redmine instance from where tickets will be dumped.
  key: <REDMINE_API_KEY>  # The API key that allows access to the REDMINE_URL.
  query_ratio: <MAX_REQUESTS_PER_MIN>  # The maximum number of requests per minute to the Redmine API.

STATUS_CODE_TO_STRING:
  '1': 'NEW'
  '2': 'IN PROGRESS'
  '3': 'RESOLVED'
  '4': 'FEEDBACK'
  '5': 'CLOSED'
  '6': 'REJECTED'
  '12': 'WORKABLE'
  '15': 'BLOCKED'
```

Replace <REDMINE_URL> with the URL of your Redmine instance, <REDMINE_API_KEY> with your API key,
and <MAX_REQUESTS_PER_MIN> with the maximum number of requests per minute allowed by Redmine API.

2. Execute the following command, replacing <project_name> and <sqlite_file> with appropriate values:

```bash
podman run -ti --rm -v $(pwd)/redmine_config.yaml:/pms/redmine_config.yaml pms "./dumper.py \
  redmine --project <project_name> --database <sqlite_file>"
```
    
This command runs the dumper.py script, which will dump the Progress issues from Redmine into the specified SQLite file. Ensure that you have the pms container available.

Once you have completed these steps, you will obtain an SQLite file containing the dumped database with all the relevant Progress issues.
If the database already exists, the dumper script will update it with the latest information from Redmine,
ensuring that your local database remains up-to-date for further processing and analysis.

It is recommended to reuse the previously dumped DB file, as the script is designed to update the existing database efficiently,minimizing API calls.
By optimizing the update process, the script reduces the load on the Redmine API and helps prevent reaching any imposed rate limits, preventing IP abbuse blocker systems.


## Generating metrics

### metrics_by_period

metrics_by_period.py allows users to extract metrics for a specified period or the entire dataset. 
The script supports the status_count metric and can output the results in various formats.

The script accepts the following command line arguments:

```bash
usage: metrics_by_period.py [-h] [--start_date START_DATE] [--end_date END_DATE] [--increment_days INCREMENT_DAYS] [--metric METRIC] [--output_format OUTPUT_FORMAT] [--measurement_name MEASUREMENT_NAME] [--config config_file] [filters] [columns] database
```

- **--start_date**: Start date (YYYY-MM-DD). If not provided, defaults to the epoch.
- **--end_date**: End date (YYYY-MM-DD). If not provided, defaults to today.
- **--increment_days**:  Specify the number of days to increment between each date in the specified period
- **--metric**: Name of the method to apply to each date. Defaults to "status_count".
- **--output_format**: Output format. Valid options are "json", "influxdb", and "csv". Defaults to "influxdb".
- **--measurement_name**: The name of the measurement used in InfluxDB.
- **--config**: Path to the metrics YAML configuration file. See metrics configuration section.
- **filters**: see filters configuration section
- **columns**: see column configuration section
- **database**: Name of the database file where are the issues


With these parameters, users can customize the metric extraction process according to their needs, making it easy to generate the desired output format and apply the appropriate metric method.

As the project expands, more scripts can be added to further enhance the user experience and capabilities.


```bash
python metrics_by_period.py --start_date 2022-03-01 --end_date 2023-03-30 \
   --metric status_count --output_format influxdb \
   --measurement_name my_measurement my_database.db
```

### metrics_snapshot

metrics_snapshot.py is a script that applies a metric method to a specified date or to the epoch, and outputs the result in the desired format.
The script currently supports the status_count metric and can output the result in JSON, InfluxDB, or CSV format.

The script accepts the following command line arguments:

```bash
usage: metrics_snapshot.py [-h] [--date DATE] [--metric METRIC] [--output_format OUTPUT_FORMAT] [--measurement_name MEASUREMENT_NAME] [--config config_file] [filters] [columns] database
```

- **--date**: Spot date (YYYY-MM-DD). If not provided, defaults to today.
- **--metric**: Name of the method to apply to each date. Defaults to "status_count".
- **--output_format**: Output format. Valid options are "json", "influxdb", and "csv". Defaults to "influxdb".
- **--measurement_name**: The name of the measurement used in InfluxDB.
- **--config**: Path to the metrics YAML configuration file. See metrics configuration section.
- **database**: Name of the database file where are the issues
- **<filters>**: see filters section

Usage

To use the script, simply run the metrics_snapshot.py file with the appropriate command line arguments.

Here is an example of how to use the script:

```bash
python metrics_snapshot.py --date 2023-04-01 my_database.db
```

This command will apply the status_count metric to the date 2023-04-01 and output the result in InfluxDB format to the my_database.db file, with the measurement name set to metrics.


### Filter Arguments

Before seing the different scripts, we need to understand the filter arguments.
The filter arguments allow you to filter your data based on specific conditions.
You can use these arguments to filter by project, type, tags, context, status, priority, author, or assigned_to. Additionally,
you can provide a JSON string to define more complex filters.

#### Basic Usage

To filter by project, type, tags, context, status, priority, author, or assigned_to, you can use the following flags:

```bash
--filter-project <project_name>
--filter-type <type_name>
--filter-tags <tag_name>
--filter-context <context_name>
--filter-status <status_name>
--filter-priority <priority_name>
--filter-author <author_name>
--filter-assigned_to <assigned_to_name>
--filter-target_version <target_version>
```
For example, to filter by project and author:

```bash
python your_script.py --filter-project "Project A" --filter-author "John Doe"
```

Quering for Null:

```bash
python your_script.py --filter-author "<null>"
```

#### Complex Filters

To define more complex filters, you can provide a JSON string using the --filter flag.
The JSON string should contain a dictionary with keys corresponding to the attributes you want to filter by,
and values containing the operation and the value for the filter.

The supported operations are:

- **'eq'** (equal)
- **'ne'** (not equal)
- **'lt'** (less than)
- **'le'** (less than or equal)
- **'gt'** (greater than)
- **'ge'** (greater than or equal)
- **'like'** (case-sensitive pattern match)
- **'ilike'** (case-insensitive pattern match)
- **'or'** (logical OR between multiple filter conditions)

Here's an example of a complex filter:

```bash
python <script>.py --filter '{
  "project": {"op": "eq", "value": "Project A"},
  "tags": {"op": "ilike", "value": "%tag1%"},
  "status": {
    "op": "or",
    "value": [
      {"op": "eq", "value": "New"},
      {"op": "eq", "value": "In Progress"}
    ]
  },
  "start_date": {"op": "gt", "value": "2022-01-01"}
}'

```

This filter will return items that belong to "Project A", have a tag containing "tag1" (case-insensitive), 
have a status of either "New" or "In Progress", and have a start date greater than "2022-01-01".

Note: eq is optional, so you can use "status": `{{"op": "eq", "value": "New"}}` or `{"status": "New"}`.

For quering for Null using the `--filter` there are two options:

Option 1: using the value `<null>`
```bash
{
  "project": {"op": "eq", "value": "<null>"},
}
```

Option 2: using the operation `{"op": "is_null"}`

```bash
{
  "project": {"op": "is_null"},
}
```

### Column configuration

The scripts allow for transformations on the data columns
The transformations can be specified through the --column command line argument.

Each column transformation is represented as a string of the form
```<column_name>.<operation>(<arg1>, <arg2>, ...).```
Here, <column_name> is the name of the column to be transformed or created,
<operation> is the operation to be applied, and <arg1>, <arg2>, ... are the
arguments to the operation, if any.

The available operations are:

- **hide()**: Removes the specified column from the data.
- **sum(<col1>, <col2>, ...)**: Creates a new column that is the sum of the specified columns.
- **avg(<col1>, <col2>, ...)**: Creates a new column that is the average of the specified columns.
- **mult(<col1>, <col2>)**: Creates a new column that is the product of the specified columns.
- **div(<col1>, <col2>)**: Creates a new column that is the division of the specified columns.
- **incr(<col1>)**: Creates a new column that represents the increment of the specified column.
- **diff(<col1>)**: Creates a new column that represents the difference between the current and previous value of the specified column.

Examples:

Hide the "UNKNOWN" column and create a new "ACTIVE" column which is the sum of "IN PROGRESS", "WORKABLE", and "NEW":

```bash
python3 metrics_snapshot.py database --column "UNKNOWN.hide()" --column "ACTIVE.sum(IN PROGRESS, WORKABLE, NEW)"
```

Compute the difference of "RESOLVED" and assign it to a new column named "SPEED":

```bash
python3 metrics_by_period.py database --start_date 2023-05-01 --end_date 2023-05-30 --column "SPEED.diff(RESOLVED)"
```


### Metrics configuration YAML

You can manage the configurations for the scripts more effectively using a YAML configuration file.
The YAML file allows you to define parameters such as --start_date and --output_format in a structured
and easy-to-understand manner.

You can load the configuration settings from the YAML file using the --config argument followed by the
path to your YAML file.

For example:

```bash
python your_script.py --config /path/to/your/config.yaml
```

Your YAML configuration file might look something like this:

```yaml
start_date: "2023-01-01"
output_format: "json"
```

Please note that if you pass an argument through the command line, this will take precedence over the values
defined in the YAML configuration file.

For instance, if you run:

```bash
python your_script.py --config /path/to/your/config.yaml --start_date "2023-02-01"
```

The start_date will be set to "2023-02-01", even though the configuration file specifies a different value.
This allows for convenient overriding of specific settings without having to modify the YAML file.


## Other scripts

### Redmine: get issue full information

This script allows you to retrieve the full information of a Redmine issue using its ID.

Usage

```bash
python get_issue_full_info.py <issue_id>
```

The script will output the full information of the specified issue in JSON format.

Arguments:

- **issue_id (required)**: the ID of the Redmine issue to retrieve.

## Other tools

### SQLite3 Database discover

This Python script is used to interact with an SQLite database. 
It can list all table names, all column names in a specified table, or all distinct values in a specified field of a specified table.

Usage

```bash
python script.py --database=my_database.db --table=my_table --field=my_field
```

This script takes the following command-line arguments:

- **--database**: Required. The name of the SQLite database file.
- **--table**: Optional. The name of the table in the database.
- **--field**: Optional. The name of the field in the specified table.

If no --table argument is provided, the script lists all the table names in the database.

If a --table argument is provided but no --field argument is provided, the script lists all the column names in the specified table.

If both --table and --field arguments are provided, the script lists all the distinct values in the specified field of the specified table.
