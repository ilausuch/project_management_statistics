FROM registry.suse.com/bci/python:3.10

COPY . /pms
WORKDIR /pms
RUN zypper -n in python310-devel gcc gcc-c++ make && pip3.10 install -r requirements.txt && rm -rf /var/cache

ENTRYPOINT ["sh", "-c"]
