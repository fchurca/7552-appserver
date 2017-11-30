# Llevame AppServer
An application server for Llevame written in Python

* [![Build Status](https://travis-ci.org/fchurca/7552-appserver.svg?branch=master)](https://travis-ci.org/fchurca/7552-appserver)
* [![Coverage Status](https://coveralls.io/repos/github/fchurca/7552-appserver/badge.svg)](https://coveralls.io/github/fchurca/7552-appserver)

## Associated Acts
* Heroku Dashboard: https://dashboard.heroku.com/teams/tallerii-7552-20172-g3 (you are logged in, aren't you?)

* Master repositories
    * Android client: https://github.com/smaraggi/HG-android-client/network
    * AppServer (this repo): https://github.com/fchurca/7552-appserver
    * SharedServer: https://github.com/florrup/sharedserver

## Useful links
* Subject site: http://7552.fi.uba.ar/
* Assignment: https://github.com/taller-de-programacion-2/taller-de-programacion-2.github.io/blob/master/trabajo-practico/enunciados/2017/2/llevame.md

## Interfaces
* An Android client will connect to this server
* A MongoDB instance for persistence. Means for configuring a development instance are included in this repo.
* SharedServer for storing user data, final trip data, and all that jazz.
* Firebase Cloud Messaging for pushing notifications to Android clients.
* USIG for determining street addresses from user locations inside Buenos Aires City.

## Dependencies
For a Docker server on Debian:
https://docs.docker.com/engine/installation/linux/docker-ce/debian/

## Building Docker Image
From the root of the project, where the build scripts are located, execute:
```
./appserver.build.sh
```
This script builds a Docker image from the Dockerfile in the root of the project's tree. The image will be called fiuba/appserver:dev, and this is the name that the execution scripts will later use.

## Deploying Containers for Local Development

First create a Docker network for Mongo and server containers:
```
docker network create taller
```
Launch now a MongoDB container:
```
./mongo.run.sh
```
After Mongo is up, run in another terminal:
```
./appserver.run.sh
```

The script launches the image fiuba/appserver:dev inside a container. The container is configured as follows:
* Port 8080 of the container is mapped to port 8080 of the host
* AppServer container is placed inside network `taller`, with name `appserver.taller`
* The project's source code directory in the host is mapped to the directory where gunicorn looks for the application scripts. Since gunicorn is executed with live reload, local live edits to the application code will be instantly reloaded by gunicorn without having to build the image and reload the container once again.
* MongoDB container is placed inside network `taller`, with name `mongodb.taller`
* By default, the container will try to contact the SharedServer at `sharedserver.taller`
More elaborate setups may arise. In that case, refer to the following sections.

## Deploying to Heroku
To deploy to Heroku simply push the contents of the source directory into the Heroku repository.
For details and specifics, goto https://devcenter.heroku.com/articles/git
We have found it useful to use pipelines and Github Sync: https://devcenter.heroku.com/articles/pipelines

## Configuration
The following environment variables need to be set:
* `APPSERVER_CFG` Location for configuration files, relative to the root of the project.
* `SHAREDSERVER_URL` SharedServer URL (default, variable name in `$APPSERVER_CFG/sharedserver.ini`)
* `SHAREDSERVER_TOKEN` Initial SharedServer token
* `MONGODB_URI` MongoDB URI (default, variable name in `$APPSERVER_CFG/mongo.ini`)
* `FCM_API_KEY` Firebase Cloud Messaging key

### SharedServer
The variable that defines the URL of the SharedServer instance is defined in `$APPSERVER_CFG/sharedserver.ini`:
```
[Connection]
sharedservervar=SHAREDSERVER_URL
```
Alternatively, the URL itself can be defined in the configuration file:
```
[Connection]
url=http://sharedserver.taller:5000/api/
```
In both cases, the token will be defined as the environment variable `SHAREDSERVER_TOKEN`.

### MongoDB
The variable that defines the connection string to some MongoDB instance can be defined in `$APPSERVER_CFG/mongo.ini`:
```
[Connection]
mongovar=MONGODB_URI
database=db
```
Then, in this case, the connection string is equal to the value of the variable `MONGODB_URI`. Alternatively, the connection string can be placed directly inside the configuration file as follows:
```
[Connection]
uri=<connection string>
database=db
```
For security reasons, however, this may not be desirable.

### Logging
Logging is configured in `$APPSERVER_CFG/mongo.ini`. Example:
```
[Logging]
level=DEBUG
format=[%%(asctime)s] [%%(process)d] [%%(levelname)s] %%(name)s - %%(message)s
```
For more information regarding Python 3 logging and logging formats, see: https://docs.python.org/3/library/logging.html


## Building Redistributable Package
First install Python dependency setuptools:
```
pip install setuptools
```
Then execute from the root of the project directory
```
python setup.py sdist
```
This should generate a redistributable archive file under a newly created dist directory. 

## Installing and Executing Redistributable Package
To install the package, execute the following:
```
pip install <path to archive file>
```
Application server can then be executed using gunicorn:
```
pip install gunicorn
gunicorn --workers 4 appserver:app
```

## Future improvements
In order to make this daemon bulletproof, several improvements can be made. Namely:
* Use of USIG can be replaced by calls to Google or OpenStreetMap in order to infer street addresses outside of Buenos Aires.
* A back office module can be implemented, or an administration API to be exposed to the SharedServer backoffice.
* The position of the passenger is tracked during the trip in order to calculate distance. However, the raw positions as informed by the passenger are used. This can result in unexpectedly high costs if the positions jump around. The datapoints can be smoothed out with LOESS and outlier filtering, either by local variance or by position error. Or with LOWESS weighted by (π/2)-arctan(error). Or some nonlinear regression algorithm or other. Or something.
* The deployment methods described use a static number of worker processes. Means to ensure an on-demand elastic deployment of daemons can be realised.
* Even more testing. There's never enough testing.

## Generating Doxygen Documentation
```
apt-get install doxygen graphviz
doxygen
```
HTML documentation will be placed inside the docs/generated directory.

## Troubleshooting
### Mongo complains about `No space left on device: "/data/db/journal"`
Dangling stale volumes may still be laying around after an untidy exit, such as a power loss.
The following commands for listing and removing volumes may require root permissions.
In that case, use `su` or `sudo` with the usual precautions. You know what you doing.
```
# list
docker volume ls -qf dangling=true
# remove
docker volume rm $(docker volume ls -qf dangling=true)
```
### An invisible man sitting in your bed
Call `555-2368`

