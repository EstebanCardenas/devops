FROM public.ecr.aws/docker/library/python:3.13-slim

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install newrelic

ENV PYTHONPATH=/app
EXPOSE 5000

# New Relic vars
ENV NEW_RELIC_APP_NAME="DevOps-Project"
ENV NEW_RELIC_LOG="stdout"
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED="true"
# NEW_RELIC_LICENSE_KEY is provided via ECS task definition (secrets or environment)
ENV NEW_RELIC_LOG_LEVEL="info"

# Log forwarding
ENV NEW_RELIC_APPLICATION_LOGGING_ENABLED="true"
ENV NEW_RELIC_APPLICATION_LOGGING_FORWARDING_ENABLED="true"

# Error capturing
ENV NEW_RELIC_ERROR_COLLECTOR_CAPTURE_EVENTS=true
ENV NEW_RELIC_ERROR_COLLECTOR_IGNORE_STATUS_CODES=""


# Entry point para que newrelic-admin ejecute gunicorn
ENTRYPOINT ["newrelic-admin", "run-program"]

# Gunicorn logs to stdout for NR
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "src.app:app"]
