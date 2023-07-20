

podman rm -f telegraf 2>/dev/null

# Telegraf
podman run --name telegraf -dt --pod monitoring_pod \
  -v $(pwd)/telegraf.conf:/etc/telegraf/telegraf.conf \
  -v $(pwd)/database.db:/database.db \
  telegraf:latest

podman exec -ti telegraf apt update
podman exec -ti telegraf apt install -y git python3 python3-venv python3-pip
podman exec -ti telegraf git clone https://github.com/ilausuch/project_management_statistics
podman exec -ti telegraf bash -c "cd project_management_statistics && pip3 install -r requirements.txt"
