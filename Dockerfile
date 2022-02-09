FROM python:3.10.2-slim as base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.1.12 \
    PYSETUP_PATH="/opt/srv" \
    VENV_PATH="/opt/srv/.venv"
ENV PYTHONPATH="$PYSETUP_PATH/app"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base AS test
RUN echo "running TEST commands"

FROM base as builder
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml .//README.md ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

FROM base as development
ENV FASTAPI_ENV=development

# Copying poetry and venv into image
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
COPY ./app ./app
# Install CLI globally
# note, editable does not work
RUN pip install .

WORKDIR $PYTHONPATH
CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "routes:app"]
