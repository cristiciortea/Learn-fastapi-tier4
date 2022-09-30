FROM python:3.10.7-bullseye

# System variables
ARG ENV_STATE
ARG POETRY_VERSION

ENV ENV_STATE=${ENV_STATE} \
    # poetry:
    POETRY_VERSION=${POETRY_VERSION} \
    # debug:
    PYTHONUNBUFFERED=1

# Initialize bash shell
SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Install system dependencies
RUN pip install --upgrade pip
RUN pip install "poetry==${POETRY_VERSION}"
# Official installation when the above method doesn't work
#RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 -

# Working on /app folder
WORKDIR /app

# Copy only requirements to cache them in docker layer
COPY "poetry.lock" "pyproject.toml" /app/

# Project initialization.
# poetry tries to create a virtualenv, we do not need it in docker. It is already isolated.
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction $(test "${ENV_STATE}" == "prod" && echo "--no-dev")

# Creating folders, and files for project
COPY . /app/

# Expose the application port
EXPOSE 8000
