# Based on Ubuntu Xenial 16.04
FROM ubuntu:xenial

# Define environment variables
ENV INSTALL /tmp
ENV APPSERVER /appserver
ENV APPSERVER_CFG /appconfig

# Copy MongoDB installation script to some temporary location
COPY ./mongodb-install.sh $INSTALL

# Determine from build arguments whether MongoDB should be installed or not
ARG MONGO=false

# Make MongoDB script executable and install MongoDB for development usage
RUN if $MONGO; then chmod u+x $INSTALL/mongodb-install.sh; \
                              $INSTALL/mongodb-install.sh; fi

# Install Python environment
RUN apt-get update && apt-get install -y python python-pip

# Copy requirements.txt to some temporary location
COPY ./requirements.txt ${INSTALL}

# Install Python dependencies
RUN pip install -r ${INSTALL}/requirements.txt

# Take target environment argument
ARG ENV=dev

# Copy source and runtime files to container
COPY ./src/ ${APPSERVER}
COPY ./runtime/config/${ENV}/ $APPSERVER_CFG

# Move into application directory
WORKDIR ${APPSERVER}

# Open ports
EXPOSE 8080

# Execute application
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=4", "main:app"]