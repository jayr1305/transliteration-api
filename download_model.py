# download_models.py
from ai4bharat.transliteration import XlitEngine

# Initialize engines
engines = {
    "hi": XlitEngine("hi", beam_width=10, rescore=True),
    "mr": XlitEngine("mr", beam_width=10, rescore=True)
}

def get_engines():
    return engines
