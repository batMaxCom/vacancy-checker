ARG PYTHON_VERSION=3.12
ARG UV_VERSION=0.8.0

# =====================================================
# Base
# =====================================================
FROM python:${PYTHON_VERSION}-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_PATH=/app \
    VIRTUAL_ENV=/app/.venv

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# =====================================================
# UV
# =====================================================
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-bin

# =====================================================
# Builder
# =====================================================
FROM python-base AS builder

ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_HTTP_TIMEOUT=120 \
    UV_PROJECT_ENVIRONMENT=$VIRTUAL_ENV

COPY --from=uv-bin /uv /uvx /usr/local/bin/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        librdkafka-dev \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN uv venv $VIRTUAL_ENV

WORKDIR $APP_PATH

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
        --frozen \
        --no-dev \
        --no-editable \
        --no-install-project

COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv build --wheel && \
    uv pip install --no-deps dist/*.whl

# =====================================================
# Runtime
# =====================================================
FROM python-base AS web-runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        librdkafka1 \
        curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd \
        --system \
        --create-home \
        --shell /usr/sbin/nologin \
        appuser

WORKDIR $APP_PATH

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

USER appuser