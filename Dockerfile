FROM public.ecr.aws/docker/library/python:3.13-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.app:app"]

RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="DevOps-Project"
ENV NEW_RELIC_LOG="stdout"
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED="true"
ENV NEW_RELIC_LICENSE_KEY=""
ENV NEW_RELIC_LOG_LEVEL="info"

ENTRYPOINT ["newrelic-admin", "run-program"]