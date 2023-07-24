# Project Management Statistics for Developers

## Development in situ

### Prepare the venv

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements_test.txt
```

### Testing with redmine

If you have already a redmine/config.py skip this step
```bash
cp ./redmine/config_example.py ./redmine/config.py
```

Run the tests with
```bash
make test
```

## Development in a container

### Build the containers

There are four alternatives:

- podman-container: Create the main container using podman
- podman-container-test: Create the container for testing using podman
- docker-container: Create the main container with docker
- docker-container-test: Create the container for testing using docker

e.g.

```bash
make docker-container
```

The containers created are:

- **pms**: For the main container
- **pms_test**: For the testing container

### Execute

With podman or docker

```bash
podman run --rm pms <command>
```

### Testing

With podman or docker

```bash
podman run --rm pms_test make test
```

### Development in a container

With podman or docker

```bash
podman run -ti --rm -v <your_code_path>:/pms pms_test bash
```

## Code organization

The code is organized in the following way (in alphabetical order):
- **db**: Database related code. Includes the models, the query class and the filter builder
- **docs**: Documentation
- **formatters**: Formatters for the metrics results
- **metrics**: Metrics related code. Includes the metrics classes and the metrics results. Additionally the column tranformations class
- **tests**: Tests for the code
- **trackers**: Trackers related code. Includes redmine and bugzilla
- **utils**: Utilities for the code

## Specific documentation

- [Normalized model](models.md)
- [Develop a tracker](trackers.md)
- [Develop a metrics algorithm](metrics.md)
- [Develop a formatter](formatters.md)
