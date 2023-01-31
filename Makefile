# Default container tag
CONT_TAG=pms

.PHONY: all
all: prepare test

.PHONY: prepare
prepare:
	pip install -r requirements_test.txt

.PHONY: test
test:
	flake8 ./db/
	pylint ./db/
	pytest --cov

.PHONY: codecov
codecov:
	pytest -v --cov --cov-report=html && xdg-open htmlcov/index.html

# Build containers
docker-container:
	docker build . -t ${CONT_TAG}
docker-container-test:
	docker build . -f Dockerfile_test -t ${CONT_TAG}_test
podman-container:
	podman build . -t ${CONT_TAG}
podman-container-test:
	podman build -f Dockerfile_test -t ${CONT_TAG}_test
