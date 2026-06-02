# Stage 1: Build environment
FROM --platform=linux/amd64 python:3.12-slim AS builder

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only requirements to cache dependencies layer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    fi

# Stage 2: Runtime environment
FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . user_agent/
WORKDIR /app/user_agent

EXPOSE 8088

CMD ["python", "main.py"]