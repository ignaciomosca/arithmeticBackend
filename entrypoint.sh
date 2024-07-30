#!/bin/sh

# Run Alembic migrations
poetry run alembic upgrade head

# Start the application
poetry run uvicorn main:app --host 0.0.0.0 --port 8000