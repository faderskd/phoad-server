# Phoad-server

[![Build Status](https://travis-ci.org/faderskd/Phoad-server.svg?branch=master)](https://travis-ci.org/faderskd/Phoad-server)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

App for memorizing your photos at specific locations. Check out the project's [documentation](http://faderskd.github.io/Phoad-server/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development in Docker

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Local Development for app debug
```bash
docker-compose run -p "5432:5432" --rm postgres
set -x DJANGO_CONFIGURATION Debug;python manage.py migrate
```

Run app in debug mode using `debug.py` config. Use the following configuration in your IDE:
```bash
DJANGO_CONFIGURATION=Debug;PYTHON_PATH=/path/to/app/directory/Phoad-server/phoad;DJANGO_SETTINGS_MODULE=phoad.config
```

# Run tests
```bash
docker-compose run --rm web bash -c "python wait_for_postgres.py && ./manage.py test" && docker kill (docker ps --filter "name=phoad_postgres" -q)
```