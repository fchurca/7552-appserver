#!/bin/bash

if [ -z "$2" ]; then
	echo "Usage: $0 SHAREDSERVER_TOKEN FCM_API_KEY" >&2
	exit 1
fi

docker rm appserver.taller > /dev/null 2>&1

docker run -it --net taller --name appserver.taller -e SHAREDSERVER_TOKEN="$1" -e FCM_API_KEY="$2" -p 8080:8080 -v $(pwd)/src:/appserver fiuba/appserver:dev

