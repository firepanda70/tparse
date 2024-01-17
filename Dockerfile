FROM python:3.12

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN pip install poetry==1.7.1

WORKDIR /app
COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi