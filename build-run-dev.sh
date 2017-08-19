#!/bin/bash

docker build --build-arg ENV=dev -t fiuba/pyappserver:dev .
docker run -p 8080:8080 -it fiuba/pyappserver:dev