from ai4bharat.transliteration import XlitEngine
from config import supported_languages

cached_engines = {}


def initialize_engines():
    for lang in supported_languages:
        cached_engines[lang] = XlitEngine(lang, beam_width=10, rescore=True)


def get_engines():
    return cached_engines


if __name__ == "__main__":
    initialize_engines()
