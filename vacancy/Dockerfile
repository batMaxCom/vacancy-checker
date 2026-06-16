ARG PYTHON_VERSION
ARG UV_VERSION
# ---------------- Base -----------------------
FROM docker.io/library/python:${PYTHON_VERSION:-3.12}-alpine AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    APP_PATH="/app"
ENV VIRTUAL_ENV="$APP_PATH/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# ----------------------------------------------
# ------------------ Uv Stage ------------------
FROM ghcr.io/astral-sh/uv:${UV_VERSION:-0.8.0} AS uv-bin
# ----------------------------------------------
# --------------- Base Builder -----------------
FROM python-base AS base-builder
ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_HTTP_TIMEOUT=100 \
    UV_PROJECT_ENVIRONMENT=$VIRTUAL_ENV
COPY --link --from=uv-bin /uv /uvx /usr/local/bin/
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev
RUN uv venv $VIRTUAL_ENV
WORKDIR $APP_PATH
# ----------------------------------------------
# ----------------- Base Runtime ---------------
FROM python-base AS base-runtime
RUN apk add --no-cache \
    curl \
    libstdc++
RUN adduser --system --no-create-home appuser
# ----------------------------------------------
# =================== Web ======================
FROM base-builder AS web-builder
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-editable --no-install-project
COPY ./src ./src
COPY ./pyproject.toml ./uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv build --wheel && \
    uv pip install --no-deps dist/*.whl

FROM base-runtime AS web-runtime
COPY --from=web-builder $VIRTUAL_ENV $VIRTUAL_ENV
USER appuser
# ==============================================