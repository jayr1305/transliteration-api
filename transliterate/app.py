from flask import Flask, jsonify, request, Response
import json
from ai4bharat.transliteration import XlitEngine
from datetime import datetime
from download_model import get_engines
import pytz

app = Flask(__name__)


# #############################################################
# #############################################################

# INPUT

# GET /tl/{lang}/{word}?k={optional_topk_value}
# E.g. GET /tl/hi/namaste?k=5

# #############################################################


# OUPUT 

# {
#     "at": "2024-09-18T13:15:31.682491845+05:30",
#     "error": "",
#     "input": "namaste",
#     "result": ["नमस्ते", "नमास्थे", "नमस्थे", "नामस्थे", "नमस्थें"],
#     "success": true
# }

# #############################################################
# #############################################################


engines = get_engines()

# Pre-load models by transliterating a word in both languages

engines["hi"].translit_word("namaste", topk=1)
engines["mr"].translit_word("namaste", topk=1)

@app.route('/tl/<string:lang>/<string:word>', methods=['GET'])
def transliterate(lang, word):
    try:
        # Get the optional topk value, default to 5 if not provided
        topk = request.args.get('k', default=5, type=int)

        # Input validation
        if lang not in engines:
            raise ValueError(f"Unsupported language code: {lang}. Supported languages are 'hi' and 'mr'.")

        # Perform transliteration
        result = engines[lang].translit_word(word, topk=topk)[lang]

        response = {
            "at": datetime.now(pytz.timezone("Asia/Kolkata")).isoformat(),
            "error": "",
            "input": word,
            "result": result,
            "success": True
        }

        return Response(
            json.dumps(response, ensure_ascii=False),  # Ensure non-ASCII characters are not escaped
            mimetype='application/json; charset=utf-8'
        )


    except Exception as e:
        response = {
            "at": datetime.now(pytz.timezone("Asia/Kolkata")).isoformat(),
            "error": str(e),
            "input": word,
            "result": [],
            "success": False
        }
        return Response(
            json.dumps(response, ensure_ascii=False),  # Ensure non-ASCII characters are not escaped
            mimetype='application/json; charset=utf-8'
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
