# Create container based on Python image
FROM python:2

# Grab execution arguments
ARG ENV

# Define environment variables
ENV APPSERVER /appserver
ENV APPSERVER_CFG /appconfig

# Copy required files
COPY ./src/ ${APPSERVER}/
COPY ./runtime/config/${ENV}/ ${APPSERVER_CFG}/

# Run application
RUN python ${APPSERVER}/main.py