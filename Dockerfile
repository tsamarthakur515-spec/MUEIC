# Use slim image
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        curl \
        git \
        build-essential \
        ffmpeg \
        aria2 \
        ca-certificates \
        wget \
        gnupg && \
    rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Downloads folder
RUN mkdir -p /app/downloads

# Run bot
CMD ["python", "main.py"]
