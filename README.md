# project_management_statistics

## Usage

### Dumping progress issues into local DB for further processing

1. under [/redmine](/redmine/) folder create `config.py`
2. define following variables in this file:
    - PROGRESS_URL - URL to target Redmine from where tickets will be dumped
    - PROGRESS_KEY - API key allowing to access PROGRESS_URL
    - REDMINE_DB - Sqlite DB where tickets will be dumped
3. execute :

```bash
podman run  -ti --rm -v <your_code_path>:/pms  pms_test "./dumper.py --queryid <query_id>"
```

## Containers

### Create the containers

There are four alternatives:

- podman-container: Create the main container using podman
- podman-container-test: Create the container for testing using podman
- docker-container: Create the main container with docker
- docker-container-test: Create the container for testing using docker

e.g.

```bash
make docker-container
```

The container created are:

- **pms**: For the main container
- **pms_test**: For the testing container

### Execution

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
