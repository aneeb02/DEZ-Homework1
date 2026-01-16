FROM python:3.12.1-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app
COPY pyproject.toml  .python-version uv.lock ./
COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY ingest_data.py .

ENTRYPOINT ["uv", "run", "python", "ingest_data.py"]
