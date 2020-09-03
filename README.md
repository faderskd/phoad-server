# Phoad-server

[![Build Status](https://travis-ci.org/faderskd/Phoad-server.svg?branch=master)](https://travis-ci.org/faderskd/Phoad-server)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

App for memorizing your photos at specific locations. Check out the project's [documentation](http://faderskd.github.io/Phoad-server/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
