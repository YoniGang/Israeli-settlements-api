FROM python:3.11-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt update && apt install -y git gcc
RUN pip install poetry==1.6.0
RUN python -m venv /venv

ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

FROM base as final

COPY --from=builder /venv /venv

ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH
ENV TZ UTC

COPY . .
CMD /venv/bin/uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-80} --reload --forwarded-allow-ips='*' --proxy-headers
