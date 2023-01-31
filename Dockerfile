FROM registry.suse.com/bci/python:3.10

COPY requirements.txt /pms
WORKDIR /pms
RUN pip3.10 install -r requirements.txt && rm -rf /var/cache
COPY dumper.py ./db ./redmine /pms

ENTRYPOINT ["sh", "-c"]
