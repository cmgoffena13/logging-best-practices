FROM python:3.12-slim-bookworm
ENV PYTHONBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    apt-get upgrade -y openssl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"
ENV UV_LINK_MODE=copy

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --compile-bytecode && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Make sure to expose for OpenTelemetry gRPC port
EXPOSE 4137

CMD ["uv", "run", "--", "python", "-m", "src.main"]
