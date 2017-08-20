# Python Application Server

## Deploy Container for Local Development

From the root of the project directory, execute
```
appserver$ docker build --build-arg MONGO=true -t fiuba/appserver:dev .
```
Since Docker will install Python environment and MongoDB, the first build will most likely take a while.
After the build is done, launch a container as follows:
```
appserver$ docker run -p 8080:8080 -it fiuba/appserver:dev
```
