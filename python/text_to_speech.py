"""
This module is using google text to speech (gTTS) and caches results.
gTTS abuses the google translation API
"""
import asyncio
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


async def say(executor, text):
    """
    caching text to speech
    :param executor: a thread pool to execute the say
    :param text: the text that should be said
    :return: bool: If it was successful, or not. If not successful, it will say that error out loud
    """
    global CACHE

    def save_audio_and_cache():
        audio = gTTS(text=text, lang=settings.TTS_LANGUAGE, slow=False)
        audio.save(os.path.join(settings.TTS_DIR, file_id))
        with open(settings.TTS_CACHE_FILE, "w") as f:
            f.write(json.dumps(CACHE))

    def say_downloaded_file():
        os.system(f"mpg321 {quote(os.path.join(settings.TTS_DIR, file_id))}")

    loop = asyncio.get_running_loop()
    if text in CACHE:
        file_id = CACHE[text]
    else:
        try:
            file_id = f"{len(CACHE)}.mp3"
            CACHE[text] = file_id  # this has to be on the main thread in order to prevent downloading the same twice
            await loop.run_in_executor(executor, save_audio_and_cache)
        except Exception:
            del CACHE[text]
            raise Exception(f"Could not download {text}")
    await loop.run_in_executor(executor, say_downloaded_file)
