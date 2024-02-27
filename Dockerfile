FROM python:3.11.8-bookworm as base

ENV PKGS_DIR=/install \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

FROM base as builder
RUN apt update
RUN apt install -y gcc g++
RUN pip install --upgrade pip
RUN pip install poetry

RUN mkdir $PKGS_DIR
RUN mkdir /code

WORKDIR /code

COPY poetry.lock pyproject.toml /code/
# Generate requirements.txt from poetry files
RUN poetry export --without-hashes -f requirements.txt --output ./requirements.txt

# Install dependencies to local folder
RUN pip install --target=$PKGS_DIR -r ./requirements.txt
RUN pip install --target=$PKGS_DIR gunicorn

# Main image with service
FROM base
ARG SRC_PATH=./devops_demo

ENV PYTHONPATH=/usr/local
COPY --from=builder /install /usr/local

RUN mkdir -p /app/

COPY $SRC_PATH /app/
WORKDIR /app

ENV SERVICE_DEBUG=False
ENV SERVICE_DB_PATH=/data
ENV SERVICE_HOST="0.0.0.0"
ENV SERVICE_PORT=8000

# Run service
CMD python manage.py migrate && gunicorn --workers=1 --bind $SERVICE_HOST:$SERVICE_PORT devops_demo.wsgi
