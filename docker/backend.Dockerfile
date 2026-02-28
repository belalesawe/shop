FROM python:3.12-slim AS base

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Set Python path to include src
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Expose the default port
EXPOSE 8000

# Run alembic migrations and start the server
CMD ["sh", "-c", "alembic upgrade head && uvicorn ecommerce.main:app --host 0.0.0.0 --port 8000"]
