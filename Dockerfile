FROM registry.suse.com/bci/python:3.10

RUN mkdir /pms
COPY requirements.txt /pms
WORKDIR /pms
RUN zypper -n in python310-devel gcc gcc-c++ && pip3.10 install -r requirements.txt && rm -rf /var/cache
COPY dumper.py ./db ./trackers ./formatters /pms/

ENTRYPOINT ["sh", "-c"]
