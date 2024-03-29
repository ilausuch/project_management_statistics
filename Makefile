# Default container tag
CONT_TAG=pms

.PHONY: all
all: prepare test

.PHONY: prepare
prepare:
	pip install -r requirements_test.txt

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

# Devel tools
podman-flake8:
	podman run --rm -v `pwd`:/pms pms_test "flake8 --max-line-length 130 *.py db/ trackers/ metrics/ tests/ formatters/ utils/"
podman-pylint:
	podman run --rm -v `pwd`:/pms pms_test "PYTHONPATH=. python3 -m pylint *.py metrics/ db/ trackers/ formatters/ tests/ utils/"
podman-pylint-metrics:
	podman run --rm -v `pwd`:/pms pms_test "PYTHONPATH=. python3 -m pylint metrics/"
podman-pylint-db:
	podman run --rm -v `pwd`:/pms pms_test "PYTHONPATH=. python3 -m pylint db/"
podman-pylint-redmine:
	podman run --rm -v `pwd`:/pms pms_test "PYTHONPATH=. python3 -m pylint trackers/"
podman-pylint-formatters:
	podman run --rm -v `pwd`:/pms pms_test "PYTHONPATH=. python3 -m pylint formatters/"
podman-pylint-tests:
	podman run --rm -v `pwd`:/pms pms_test "PYTHONPATH=. python3 -m pylint tests/"
podman-pylint-utils:
	podman run --rm -v `pwd`:/pms pms_test "PYTHONPATH=. python3 -m pylint utils/"
podman-test:
	podman run --rm -v `pwd`:/pms pms_test "PYTHONPATH=. python3 -m pytest"
podman-check:
	make podman-container-test
	make podman-flake8
	make podman-pylint
	make podman-test
