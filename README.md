# Python Application Server
Python application server for subject Taller de Programación 2 (Programming Workshop 2) of the University of Buenos Aires

## Deploy for Development
Install Docker and execute the wrapper script inside the root of the project's directory:
```
appserver$ chmod u+x ./build-run-dev.sh && ./build-run-dev.sh
```
May need to be executed as root if Docker installation requires elevated privileges. As of now, the Docker container brings up a web server mapped to port 8080 of the host.
