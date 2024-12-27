# Use the official Python 3.10 slim image as the base
FROM python:3.10-slim

# Environment variables to prevent Python from buffering output and creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for building and PostgreSQL interaction
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt into the container
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project into the container (including entrypoint.sh)
COPY . .

# Set PYTHONPATH to /app to recognize the 'app' package
ENV PYTHONPATH=/app

# Ensure entrypoint.sh has executable permissions inside the container
RUN chmod +x /app/entrypoint.sh

# Entrypoint will run the script that waits for the DB, runs migrations, populates the DB, and starts the server
ENTRYPOINT ["/app/entrypoint.sh"]