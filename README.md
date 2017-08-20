# Python Application Server

## Build Docker Image
From the root of the project, where the build scripts are located, execute:
```
appserver$ ./appserver.build.sh
```
This script builds a Docker image from the Dockerfile in the root of the project's tree. The image will be called fiuba/appserver:dev, and this is the name that the execution scripts will later use.

## Deploy Container for Local Development

First create a Docker network for Mongo and server containers:
```
appserver$ docker network create taller
```

Launch now a MongoDB container:
```
appserver$ ./mongo.run.sh
```
After Mongo is up, run in another terminal:
```
appserver$ ./appserver.run.sh
```
