# Copyright (c) 2025 Alogram Inc.
# The official Alogram PayRisk Local Emulator.
# Generated from Payments Risk API v0.1.6

FROM python:3.12-slim

WORKDIR /app

# 1. Install system dependencies for build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy the self-contained server source and metadata
COPY src /app/src
COPY pyproject.toml /app/
# Use wildcard to make copy optional if file is missing
COPY requirements.txt* /app/

# 3. Install the server and its dependencies
RUN pip install --no-cache-dir .

# 4. Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8080
ENV DEBUG=true

# 5. Launch the emulator
EXPOSE 8080
CMD ["uvicorn", "payrisk_base_server.main:app", "--host", "0.0.0.0", "--port", "8080"]