# Use Python 3.9 base image
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for building fairseq and other libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy only the Poetry configuration first (for better caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies with Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Download models for caching in the image
COPY src/download_model.py .
RUN poetry run python download_model.py

# Copy the rest of the application code
COPY src/ .

# Expose the port on which the app will run
EXPOSE 6000

# Run the application using Poetry
CMD ["poetry", "run", "python", "app.py"]
