# Based on Ubuntu Xenial 16.04
FROM ubuntu:xenial

# Define environment variables
ENV INSTALL /tmp
ENV APPSERVER /appserver
ENV APPSERVER_CFG /appconfig

# Install Python environment
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy requirements.txt to some temporary location
COPY ./requirements.txt ${INSTALL}

# Install Python dependencies
RUN pip3 install -r ${INSTALL}/requirements.txt

# Take target environment argument
ARG ENV=dev

# Copy source and runtime files to container
COPY ./runtime/config/${ENV}/ ${APPSERVER_CFG}

# Move into application directory
WORKDIR ${APPSERVER}

# Open ports
EXPOSE 8080

# Execute application
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=4", "--reload", "main:app"]