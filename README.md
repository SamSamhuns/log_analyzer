# Log Summarizer

Backend with fastapi+uvicorn for log summarization with LLMs.

- [Log Summarizer](#log-summarizer)
  - [Setup](#setup)
    - [1. Create .env file](#1-create-env-file)
    - [2. Create shared volumes directory](#2-create-shared-volumes-directory)
  - [Running the summarization service](#running-the-summarization-service)
    - [i) Uvicorn server with fastapi with Docker](#i-uvicorn-server-with-fastapi-with-docker)
    - [ii) Uvicorn server with fastapi with venv](#ii-uvicorn-server-with-fastapi-with-venv)
    - [Optionally expose app through ngrok docker for sharing localhost on the internet](#optionally-expose-app-through-ngrok-docker-for-sharing-localhost-on-the-internet)
  - [Testing](#testing)
  - [TODO](#todo)

## Setup

### 1. Create .env file

Create a `.env` file with the following keys with updated values for unames and pass:

```yaml
# set to False for deployment
DEBUG=True
# http api server
API_SERVER_PORT=8080
```

### 2. Create shared volumes directory

```shell
mkdir -p volumes/log_summarizer
```

## Running the summarization service

There are two options for running the summarization service.

### i) Uvicorn server with fastapi with Docker

Build server container

```shell
bash scripts/build_docker.sh
```

Start server at HTTP port EXPOSED_HTTP_PORT

```shell
bash scripts/run_docker.sh -p EXPOSED_HTTP_PORT
```

The server will be available at <http://localhost:8080> if using the default port.

### ii) Uvicorn server with fastapi with venv

Install requirements inside venv or conda environment

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start server at HTTP port EXPOSED_HTTP_PORT. Note the host names must contain addresses when using docker microservices and the fastapi+uvicorn server outside the docker-compose environment.

```shell
python app/server.py -p EXPOSED_HTTP_PORT
```

The server will be available at <http://localhost:8080> if using the default port.

### Optionally expose app through ngrok docker for sharing localhost on the internet

WARNING: Never use for production

```bash
# start log summarizer with python
# sign up for ngrok account at https://ngrok.com/
# https://ngrok.com/docs/using-ngrok-with/docker/
docker pull ngrok/ngrok
# for linux systems
docker run --net=host -it -e NGROK_AUTHTOKEN=<NGROK_AUTHTOKEN> ngrok/ngrok:latest http <EXPOSED_HTTP_PORT>
# for MacOS and windows
docker run -it -e NGROK_AUTHTOKEN=<NGROK_AUTHTOKEN> ngrok/ngrok:latest http host.docker.internal:<EXPOSED_HTTP_PORT>
```

## Testing

Note: all the microservices must already be running with docker-compose.

Install requirements:

```shell
pip install -r tests/requirements.txt
```

Run tests:

```shell
pytest tests/
```

Generating coverage reports

```shell
coverage run -m pytest tests/
coverage report -m -i
```

## TODO

-   Fix vector database to use
-   Use redis for caching if possible
