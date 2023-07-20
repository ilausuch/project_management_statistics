#!/bin/bash
mkdir -p data/{influxdb,grafana} 2>/dev/null
chmod a+w data/{influxdb,grafana}

podman pod create --name monitoring_pod -p 8086:8086 -p 3000:3000

# InfluxDB
podman run --name influxdb -dt --pod monitoring_pod \
  -e INFLUXDB_DB=mydb -e INFLUXDB_ADMIN_USER=admin -e INFLUXDB_ADMIN_PASSWORD=admin \
  -v $(pwd)/data/influxdb:/var/lib/influxdb \
  influxdb:latest

# Grafana
podman run --name grafana -dt --pod monitoring_pod \
  -e GF_SECURITY_ADMIN_USER=admin -e GF_SECURITY_ADMIN_PASSWORD=admin \
  -v $(pwd)/data/grafana:/var/lib/grafana \
  grafana/grafana:latest
