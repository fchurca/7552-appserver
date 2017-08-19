#!/bin/bash

docker build --build-arg ENV=prod -t fiuba/appserver:prod .