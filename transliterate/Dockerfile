# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a working directory inside the container
WORKDIR /app

# Install build dependencies needed for fairseq and other libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

# Upgrade pip to version 22.x
RUN python -m pip install --upgrade pip==22.*

# Copy the requirements to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model download script to the container
COPY download_model.py .

# Download the models (this will be cached in the Docker image)
RUN python download_model.py

# Copy the rest of the application code
COPY . .

# Expose the new port (6000) for Flask
EXPOSE 6000

# Set the entry point to run the Flask app
CMD ["python", "app.py"]
