# Python Application Server

## Build Docker Image
From the root of the project, where the build scripts are located, execute:
```
appserver$ ./appserver.build.sh
```
Depending on how Docker was installed, this may require root privileges.

## Deploy Container for Local Development

First create a Docker network for Mongo and server containers:
```
appserver$ docker network create taller
```

Launch now a MongoDB container:
```
appserver$ ./mongo.run.sh
```
After the MongoDB is up, run:
```
appserver$ ./appserver.run.sh
```
