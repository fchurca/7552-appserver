# Create container based on Python image
FROM python:2

# Define environment variables
ENV APPSERVER /appserver
ENV APPSERVER_CFG ${APPSERVER}/config

# Copy required files
COPY ./src/ ${APPSERVER}
COPY ${APPSERVER_TARGET_ENV_CFG}/ ${APPSERVER_CFG}

# Run application
RUN python ${APPSERVER}/main.py