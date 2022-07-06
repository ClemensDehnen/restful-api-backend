FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# install gcc so wheels can be installed. Not included in fastapi docker image yet.
RUN apt-get update && apt-get install gcc -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/pip-tmp/

RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt && rm -rf /tmp/pip-tmp