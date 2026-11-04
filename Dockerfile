# ==============================================================================
# Dockerfile for Healthy Relationships API & Web App
# ==============================================================================

# Use official, lightweight Python 3.12 slim base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000

# Set the working directory inside the container
WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY relationship_messages.py .
COPY app.py .
COPY README.md .

# Create a non-privileged user for security compliance (avoid running as root)
RUN useradd -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the API server port
EXPOSE 8000

# Container healthcheck to verify the server is responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/categories')" || exit 1

# Command to start the application
CMD ["python3", "app.py"]

