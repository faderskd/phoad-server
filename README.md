# Phoad-server

[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

App for memorizing your photos at specific locations. Check out the project's [documentation](http://faderskd.github.io/Phoad-server/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development in Docker

Start the dev server:
```bash
make run_docker_app
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Local Development without Docker
```bash
terminal1: > make run_docker_database
temrinal2: > make run_app_locally
```


# Run tests in Docker
```bash
make test_in_docker
```

# Run tests without Docker
```bash
terminal1: > make run_docker_database
terminal2: > make test_locally
```

# Debug in Intellij
Run app in debug mode using `debug.py` config. Use the following configuration in your IDE:
```
DJANGO_CONFIGURATION=Debug;PYTHON_PATH=/path/to/app/directory/Phoad-server/phoad;DJANGO_SETTINGS_MODULE=phoad.config
```