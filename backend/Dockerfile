# ---- Base ----
FROM python:3.11-slim AS base

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# ---- Dependencies ----
FROM base AS deps

# Copy dependency files (lockfile ensures reproducible fast installs)
COPY pyproject.toml uv.lock* ./

# Install dependencies only (not the project itself)
RUN uv venv .venv && \
    uv sync --frozen --no-install-project --no-dev

# ---- Final ----
FROM base AS final

WORKDIR /app

# Copy venv from deps stage
COPY --from=deps /app/.venv .venv

# Copy source code
COPY src/ ./src/

# Make venv binaries available
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# Hugging Face Spaces requires port 7860
EXPOSE 7860

CMD ["uvicorn", "main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "7860"]
