#!/bin/bash

docker rm mongo.taller > /dev/null 2>&1

docker run -it --net taller --name mongo.taller -p 27017:27017 mongo
