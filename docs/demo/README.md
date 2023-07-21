# Introduction

This demo shows how to use influxdb and grafana to show metrics.
There are two approaches:
- Populate the database with data
- Use telegraf to get the metrics

Both are complementary. 

Case A:
The first one is useful to prepopulate the database with data that is not monitored by telegraf. Historic data.
Then use telegraf to get the metrics regularly.

Case B:
The first one is useful to show metrics from a database that is not monitored by telegraf. Manually will be populated with new data.
The second one is useful to show metrics from a database that is monitored by telegraf.

# Requeriments
* podman

# Installation and configuration
Whit the script launch.sh you can start a podman pod and the necessary containers.
```
./launch.sh
```

Check your containers using
```
podman ps
```

These containers exports the port 8086 for influxdb and 3000 for grafana.


## Configure influxDB

First is necessary to configure the database access. 
And get the token to access the database from the grafana.

1. Access to the web http://localhost:8086
2. Fill the info. By default for the demo use metrics as organization and as a name for the bucket.
3. Copy the token

## Configure grafana

Secondly is necessary to configure grafana to access the database.

1. Access to the web page at http://localhost:3000 (user: admin, pass: admin)
2. Add a new data source:
3. select influxdb
4. select query language: flux
5. set the url for the DB to http://influxdb:8086
6. set the organization to metrics
7. set the token
8. set the default bucket to metrics


# Populate the database

## Option 1: From pre-generated data

There is a data file pre-generatred that you can use.
But you can generate your own data (see the section for dump data from progress/bugzilla and generate metrics)

Load the data. Execute the following commands:
Note: replace <token> with the token generated in the previous section. Also ensure the bucket and organization are correct.

```
podman cp data.txt influxdb:/tmp
podman exec -ti influxdb influx write -b metrics -o metrics -t <token>  -p ns --format=lp -f /tmp/data.txt
```

Try it on grafana creating a new dashboard and a new panel. Create a query using flux. E.g.:
```
from(bucket: "metrics")
  |> range(start: -20d)
  |> filter(fn: (r) => r["_measurement"] == "metrics")
  |> filter(fn: (r) => r["_field"] == "IN_PROGRESS")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```

## Option 2: Use telegraf

1. Copy your database (obtained with the dumpper) to the demo directory with the name database.db
2. Copy telegraf_template to telegraf.conf
3. Modify the telegraf.com to specify the correct token
4. Execute the following command:
```
./launch_telegraf.sh
```
This will execute all the necessary commands to allow the execution of the script metrics_snapshot.sh
Note: In the configuration of telegraf, the first execution for metrics_snapshot.sh will start 2 minutes after the start of telegraf. If the inicialization proces didn't finish in 2 minutes, the first execution will fail. But the next executions will work.

