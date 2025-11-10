# LuminoraCore SDK Python Docker Image - v1.1
# Includes support for memory, affinity tracking, and relationship management

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# v1.1 specific environment variables
ENV LUMINORA_VERSION=1.1.0
ENV LUMINORA_FEATURES_CONFIG=/app/config/features_production_safe.json
ENV LUMINORA_AUTO_MIGRATE=true

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install the package in development mode
RUN pip install -e .

# Create non-root user
RUN useradd --create-home --shell /bin/bash luminoracore
RUN chown -R luminoracore:luminoracore /app
USER luminoracore

# Expose port
EXPOSE 8000

# Create directories for v1.1 features
RUN mkdir -p /app/data /app/logs /app/config /app/snapshots

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import luminoracore_sdk; print('OK')" || exit 1

# Run migrations on startup (if enabled)
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Default command
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "luminoracore_sdk.server:app", "--host", "0.0.0.0", "--port", "8000"]
