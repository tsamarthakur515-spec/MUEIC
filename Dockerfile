# Use Python 3.10 slim
FROM python:3.10-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies (git, ffmpeg, build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        ffmpeg \
        build-essential \
        curl \
        wget \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Create downloads folder
RUN mkdir -p /app/downloads

# Run bot
CMD ["python", "main.py"]
