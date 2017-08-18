#!/bin/bash

export APPSERVER_TARGET_ENV_CFG=./runtime/config/prod/

docker build -t fiuba/appserver:prod .