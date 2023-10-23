FROM registry.suse.com/bci/python:3.10

RUN mkdir /pms
COPY requirements.txt /pms
WORKDIR /pms
RUN zypper -n in python310-devel gcc gcc-c++ && pip3.10 install -r requirements.txt && rm -rf /var/cache
COPY dumper.py logging.yaml /pms
RUN mkdir -p /pms/db && \
mkdir -p /pms/formatters && \
mkdir -p /pms/trackers && \
mkdir -p /pms/metrics && \
mkdir -p /pms/utils
ADD db /pms/db
ADD trackers /pms/trackers
ADD formatters /pms/formatters
ADD metrics /pms/metrics
ADD utils /pms/utils

ENTRYPOINT ["sh", "-c"]
