"""
This module is using google text to speech (gTTS) and caches results.
gTTS abuses the google translation API
"""
from gtts import gTTS
import os
import json
from shlex import quote
import settings

if os.path.exists(settings.TTS_CACHE_FILE):
    with open(settings.TTS_CACHE_FILE, "r") as file:
        CACHE = json.load(file)
else:
    CACHE = dict()


# todo: async?
def say(text):
    """
    caching text to speech
    :param text: the text that should be said
    :return: bool: If it was successful, or not. If not successful, it will say that error out loud
    """
    file_id = get_or_download(text)
    code = os.system(f"mpg321 {quote(os.path.join(settings.TTS_DIR, file_id))}")
    if code != 0:
        raise SystemError("Could not say")


def get_or_download(text):
    global CACHE

    if text in CACHE:
        file_id = CACHE[text]
    else:
        file_id = f"{len(CACHE)}.mp3"
        audio = gTTS(text=text, lang=settings.TTS_LANGUAGE, slow=False)
        audio.save(os.path.join(settings.TTS_DIR, file_id))
        CACHE[text] = file_id
        with open(settings.TTS_CACHE_FILE, "w") as f:
            f.write(json.dumps(CACHE))
    return file_id


get_or_download(settings.SAY_SAY_ERROR)  # always make sure that this one is cached
