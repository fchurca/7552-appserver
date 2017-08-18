# python-appserver
Python application server for subject Taller de Programación 2 (Programming Workshop 2) of the University of Buenos Aires

## Deploy

```
# Building and deploying development environment
appserver$ docker build -f Dockerfile.dev -t fiuba/appserver:dev .
appserver$ docker run -p 8080:8080 -it fiuba/pyappserver:dev

# Building production environment
appserver$ docker build -f Dockerfile.prod -t fiuba/pyappserver:prod .
```
