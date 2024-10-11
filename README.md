# Transliteration API

This project is a Flask-based API for transliterating text from English to Indian languages using [AI4Bharat's](https://ai4bharat.iitm.ac.in/areas/xlit)  `ai4bharat-transliteration` library. The API allows users to input a word and receive the corresponding transliteration for the requested language.

## Table of Contents

- [Features](#features)
- [Tooling](#tooling)
- [Setup on local machine](#setup-on-local-machine)
- [Deployment Steps](#deployment-steps)
- [Deployment Notes](#deployment-notes)
- [API Documentation](#api-documentation)

## Features

- **Transliteration Support**: Converts English text into Hindi (`hi`) or Marathi (`mr`).
- **Customizable Top-K Results**: Users can specify the number of transliterations they want in the response.
- **Dockerized**: Easy to build and deploy using Docker.

## Tooling

### Stack

- `flask` - for web framework
- `gunicorn` - for ASGI webserver
- [docker](https://docs.docker.com/engine/install/) - for containerization

### Python tooling

- `poetry` - for dependency management
- `pyenv` - for managing python versions
- `black` - for formatting
- `flake8` - for linting
- `isort` - for import sorting

## Setup on local machine

1. Clone the project git repository

    ```bash
    git clone git@github.com:jayr1305/transliteration-api.git
    cd transliteration-api
    ```

2. Install required python version using [`pyenv`](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

    ```bash
    # Install pyenv
    curl https://pyenv.run | bash

    # Add pyenv to path

    # Install python
    pyenv install $(cat .python-version)
    pyenv local $(cat .python-version)
    ```

3. Install dependencies with [`poetry`](https://python-poetry.org/docs/#installation/)

    ```bash
    # Install poetry
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Configure poetry
    export PATH="$HOME/.local/bin:$PATH"
    source ~/.zshrc
    poetry config virtualenvs.in-project true

    # Install dependencies
    poetry install
    ```

4. Start server

     ```bash
    poetry run python src/app.py
    ```

## Deployment Steps

1. Clone the repository and navigate to the project directory.
2. Build the Docker image:

    ```bash
    docker build -t transliteration-api .
    ```

3. Run the docker container

    ```bash
    docker run -p 6000:6000 transliteration-api
    ```

    The API will be available at `http://localhost:6000`.

4. Test the API using `curl`, Postman, or directly from your browser.

    ```bash
    curl "http://localhost:6000/tl/hi/namaste?k=5"
    ```

## Deployment Notes

- **Model Loading**: On the first API call, the models for Hindi and Marathi are loaded into memory. This may take some time initially but will be faster on subsequent calls.
  
- **Docker Configuration**: The Dockerfile ensures that the necessary models are downloaded and cached during the image build process, reducing the time needed during the first request after deployment.

## API Documentation

1. `GET /tl/{lang}/{word}?k={topk}`

- `lang`: The language code for transliteration (`hi` for Hindi, `mr` for Marathi).
- `word`: The English word you want to transliterate.
- `topk`: (Optional) The number of top-k transliterations to return (default is 5).

Here is the list of [Languagues supported](https://pypi.org/project/ai4bharat-transliteration/).

Example Request:

```
GET /tl/hi/namaste?k=3
```

Example Response:

```json
{
    "at": "2024-09-18T13:15:31.682491845+05:30",
    "error": "",
    "input": "namaste",
    "result": ["नमस्ते", "नमास्थे", "नमस्थे"],
    "success": true
}
```

Example Error Response:

```json
{
    "at": "2024-09-18T13:15:31.682491845+05:30",
    "error": "Unsupported language code: fr. Supported languages are 'hi' and 'mr'.",
    "input": "bonjour",
    "result": [],
    "success": false
}
```

## Files in this Project

- `app.py`: The main Flask application that handles API requests.
- `download_model.py`: Script to download and preload the transliteration models.
