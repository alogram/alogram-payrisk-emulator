# Copyright (c) 2025 Alogram Inc.
# The official Alogram PayRisk Local Emulator.
# Generated from Payments Risk API v0.3.1

FROM python:3.12-slim-bookworm

WORKDIR /app

# 1. Patch OS vulnerabilities (glibc, systemd) and install build deps
RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -f /usr/lib/x86_64-linux-gnu/gconv/IBM1390.so /usr/lib/x86_64-linux-gnu/gconv/IBM1399.so \
    && rm -rf /var/lib/apt/lists/*

# 2. Upgrade pip to fix CVE-2025-8869 and copy source
RUN pip install --no-cache-dir --upgrade pip
COPY src /app/src
COPY pyproject.toml /app/
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
