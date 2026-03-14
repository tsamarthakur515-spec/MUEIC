FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    wget \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Upgrade pip and install Python deps
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Create downloads folder
RUN mkdir -p /app/downloads

CMD ["python", "main.py"]
