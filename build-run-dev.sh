#!/bin/bash

export APPSERVER_TARGET_ENV_CFG=./runtime/config/dev/

docker build -t fiuba/pyappserver:dev .
docker run -p 8080:8080 -it fiuba/pyappserver:dev