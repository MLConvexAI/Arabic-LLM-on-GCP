# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set the HF_HOME environment variable to avoid the deprecation warning
ENV HF_HOME=/app/.cache/huggingface

# Suppress specific warnings
ENV PYTHONWARNINGS="ignore::FutureWarning:transformers.utils.hub"

WORKDIR /app

# Create a non-root user and group with a specific UID and GID
RUN adduser --disabled-password --gecos "" --home "/app" --shell "/bin/bash" appuser \
    && mkdir -p cache /app/.cache \
    && chown -R appuser:appuser cache /app/.cache  # Grant write permissions to /app/.cache

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-root user
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]