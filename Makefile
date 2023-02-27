# Default container tag
CONT_TAG=pms

.PHONY: all
all: prepare test

.PHONY: prepare
prepare:
	pip install -r requirements_test.txt
	cp ./redmine/config_example.py ./redmine/config.py

.PHONY: test
test:
	PYTHONPATH=. python3 -m pytest

# Build containers
docker-container:
	docker build . -t ${CONT_TAG}
docker-container-test:
	docker build . -f Dockerfile_test -t ${CONT_TAG}_test
podman-container:
	podman build . -t ${CONT_TAG}
podman-container-test:
	podman build -f Dockerfile_test -t ${CONT_TAG}_test
