import json
import logging
import os
import uuid
from datetime import datetime
from time import time
from typing import Any, Dict

import pytz
from flask import Flask, Response, g, request

from config import supported_languages
from download_model import get_engines

app = Flask(__name__)

# Pre-load models by transliterating a word in both languages
engines: Dict[str, Any] = get_engines()
for lang in supported_languages:
    engines[lang].translit_word("namaste world", topk=1)


@app.before_request
def start_request() -> None:
    request_id: str = str(uuid.uuid4())

    g.request_id = request_id  # Attach to Flask's global object for this request
    g.start_time = time()

    logging.info(
        f"Request {g.request_id} - START - {request.method} {request.path} - Params: {request.args}"
    )


@app.after_request
def log_response(response: Response) -> Response:
    response_time: float = time() - g.start_time
    response.headers["X-Request-ID"] = g.request_id

    logging.info(
        f"Request {g.request_id} - END - {request.method} {request.path} - Response Code: {response.status_code} - Response Time: {response_time:.4f}s"
    )

    return response


@app.route("/tl/<string:lang>/<string:word>", methods=["GET"])
def transliterate(lang: str, word: str) -> Response:
    """
    Transliterate a word from Latin script into Indic script.

    Args:
        lang (str): The language code ('hi' for Hindi, 'mr' for Marathi).
        word (str): The word to be transliterated.

    Query Params:
        k (int, optional): The number of top transliterations to return (default is 5).

    Returns:
        Response (JSON): A JSON object containing the transliteration results.
    """

    topk: int = request.args.get("k", default=5, type=int)

    if lang not in supported_languages:
        raise ValueError(
            f"Unsupported language code: {lang}. Supported languages are {', '.join(supported_languages)}"
        )

    result: list[str] = engines[lang].translit_word(word, topk=topk)[lang]

    response: Dict[str, Any] = {
        "at": datetime.now(pytz.timezone("Asia/Kolkata")).isoformat(),
        "error": "",
        "input": word,
        "result": result,
        "success": True,
    }

    return Response(json.dumps(response, ensure_ascii=False))


@app.errorhandler(Exception)
def handle_exception(e: Exception) -> Response:
    logging.error(f"Request {g.request_id} - ERROR - {str(e)}")

    response: Dict[str, Any] = {
        "at": datetime.now(pytz.timezone("Asia/Kolkata")).isoformat(),
        "error": (
            str(e)
            if isinstance(e, ValueError)
            else "An unexpected error occurred. Please try again later."
        ),
        "input": request.view_args.get("word", ""),
        "result": [],
        "success": False,
    }

    return Response(json.dumps(response, ensure_ascii=False))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=6000,
        debug=os.getenv("FLASK_DEBUG", "False").lower() == "true",
    )
