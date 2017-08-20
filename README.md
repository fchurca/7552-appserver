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
The script launches the image fiuba/appserver:dev inside a container. The container is configured as follows:

* Port 8080 of the container is mapped to port 8080 of the host.

* Container is placed inside network `taller`, with name `appserver.taller`.

* The project's source code directory in the host is mapped to the directory where gunicorn looks for the application scripts. Since gunicorn is executed with live reload, local live edits to the application code will be instantly reloaded by gunicorn without having to build the image and reload the container once again.
