#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 SHAREDSERVER_TOKEN" >&2
	exit 1
fi

docker rm appserver.taller > /dev/null 2>&1

docker run -it --net taller --name appserver.taller -e SHAREDSERVER_TOKEN="$1" -p 8080:8080 -v $(pwd)/src:/appserver fiuba/appserver:dev

