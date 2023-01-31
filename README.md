# project_management_statistics


## Containers
### Create the containers

There are four alternatives:
* podman-container: Create the main container using podman
* podman-container-test: Create the container for testing using podman
* docker-container: Create the main container with docker
* docker-container-test: Create the container for testing using docker

e.g.

```
make docker-container
```

The container created are:
* **pms**: For the main container
* **pms_test**: For the testing container

### Execution

With podman or docker

```
podman run --rm pms <command>
```


### Testing

With podman or docker

```
podman run --rm pms_test make test
```

### Development in a container

With podman or docker

```
podman run -ti --rm -v <your_code_path>:/pms pms_test bash
```