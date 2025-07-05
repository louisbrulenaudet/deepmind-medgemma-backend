FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTE=1
ENV UV_LINK_MODE=copy

# Change the working directory to the `app` directory
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY ./pyproject.toml ./uv.lock /app/

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy the project into the image
COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
