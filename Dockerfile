FROM python:3.10

WORKDIR /websocket-server
ENV POETRY_VERSION=1.1.13

RUN pip install gunicorn "poetry==$POETRY_VERSION"
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes -f requirements.txt | pip install -r /dev/stdin

EXPOSE 8000/tcp
ENV LOG_LEVEL="debug"

COPY . .
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--timeout", "300", "main:app"]
