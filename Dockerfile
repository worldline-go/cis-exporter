FROM python:3.12-alpine3.20

# Author of the image
LABEL maintainer="#wordline-devops"

# Main variables
ARG APP_FOLDER="/usr/src/app" \
    USER="cisexporter"

# Refresh the rpm repos and then create the app user
RUN apk update \
    && apk add curl \
    && addgroup -S exporter && adduser -S $USER -G exporter

# Set the working directory
WORKDIR $APP_FOLDER

# Copy related files in image
COPY app $APP_FOLDER
COPY requirements.txt $APP_FOLDER

# Expose the Prometheus metric port
EXPOSE 9091

# Install any required Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Run application with non-root user
USER $USER

# Health checking in container for default service port
# Generate non-expensive GET request on fail-fast mode.
HEALTHCHECK --interval=5s --timeout=3s \
  CMD curl -I -X GET -f http://localhost:9091/metrics

# Default entrypoint for exporter
ENTRYPOINT ["python", "cis_exporter.py"]
