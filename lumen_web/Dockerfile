# =======================================
# DOCKERFILE: LUMEN WEB FLASK APPLICATION
# =======================================
# Purpose:
# Build and run a lightweight Python-based container for the Lumen Flask web app.
# Designed to work both locally and on Render with minimal dependencies.
# ---------------------------------------
# Base image:
# Using python:3.11-slim for reduced image size and faster build times.
# ---------------------------------------

FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list and install all requirements first
# This layer is cached unless requirements.txt changes
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose Flask/Gunicorn port
EXPOSE 5000

# Default startup command (runs Gunicorn via run_start.sh)
CMD ["bash", "./run_start.sh"]
