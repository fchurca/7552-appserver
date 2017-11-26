#!/bin/bash

. .env

docker rm appserver.taller > /dev/null 2>&1

docker run -it --net taller --name appserver.taller -e SHAREDSERVER_TOKEN="${SHAREDSERVER_TOKEN}" -e FCM_API_KEY="${FCM_API_KEY}" -p 8080:8080 -v $(pwd)/src:/appserver fiuba/appserver:dev

