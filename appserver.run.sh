docker rm appserver.taller > /dev/null 2>&1

docker run -it --net taller --name appserver.taller -p 8080:8080 fiuba/appserver:dev