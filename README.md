# Transliteration API

This project is a Flask-based API for transliterating text from English to Indian languages (currently supporting Hindi and Marathi) using the `ai4bharat-transliteration` library. The API allows users to input a word and get the corresponding transliteration for the requested language.

## Features
- **Transliteration Support**: Converts English text into Hindi (`hi`) or Marathi (`mr`).
- **Customizable Top-K Results**: Users can specify the number of transliterations (top-k) they want in the response.
- **Dockerized**: Easy to build and deploy using Docker.

## Requirements
- Docker installed on your machine

## Input and Output

### API Endpoint

**Format:**
```
GET /tl/{lang}/{word}?k={optional_topk_value}
```

- `lang`: The language code for transliteration (`hi` for Hindi, `mr` for Marathi).
- `word`: The English word you want to transliterate.
- `k`: (Optional) The number of top-k transliterations to return (default is 5).

### Example Request
```
GET /tl/hi/namaste?k=3
```

### Example Response
```json
{
    "at": "2024-09-18T13:15:31.682491845+05:30",
    "error": "",
    "input": "namaste",
    "result": ["नमस्ते", "नमास्थे", "नमस्थे"],
    "success": true
}
```

### Error Response
If an unsupported language code is provided or any other error occurs:
```json
{
    "at": "2024-09-18T13:15:31.682491845+05:30",
    "error": "Unsupported language code: fr. Supported languages are 'hi' and 'mr'.",
    "input": "bonjour",
    "result": [],
    "success": false
}
```

## How to Build and Run the Docker Container

### Step 1: Build the Docker Image
First, clone the repository and navigate to the project directory. Then run the following command to build the Docker image:

```bash
docker build -t transliteration-api .
```

### Step 2: Run the Docker Container
Once the image is built, run the container using:

```bash
docker run -p 6000:6000 transliteration-api
```

The API will be available at `http://localhost:6000`.

### Step 3: Test the API
You can test the API using `curl`, Postman, or directly from your browser.

Example using `curl`:
```bash
curl "http://localhost:6000/tl/hi/namaste?k=5"
```

## Development Notes

- **Model Loading**: On the first API call, the models for Hindi and Marathi are loaded into memory. This may take some time initially but will be faster on subsequent calls.
  
- **Docker Configuration**: The Dockerfile ensures that the necessary models are downloaded and cached during the image build process, reducing the time needed during the first request after deployment.

## Files in this Project

- `Dockerfile`: Docker configuration for building the API image.
- `app.py`: The main Flask application that handles API requests.
- `download_model.py`: Script to download and preload the transliteration models.
- `requirements.txt`: Dependencies for the project, including `Flask` and `ai4bharat-transliteration`.
