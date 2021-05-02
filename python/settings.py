import os
import datetime

# region === brain web ===
BRAIN_WEB_ORIGIN = "http://localhost:8080/"  # must have trailing slashes!
# endregion --- brain web ---

# region === LEDS ===
LED_WEB_ORIGIN = "http://localhost:3000/"  # must have trailing slashes!
LED_NAMES = ["tisch", "bett"]
# endregion --- LEDS ---

# region === text to speech ===
TTS_LANGUAGE = "de"
TTS_DIR = "tts/"
TTS_CACHE_FILE = os.path.join(TTS_DIR, "cache.txt")
# endregion --- text to speech ---

# region === speech to text ===
# available wake_words: pvporcupine.KEYWORDS (needs import pvporcupine). On 2021-04-10 available:
#     {'blueberry', 'porcupine', 'alexa', 'pico clock', 'bumblebee', 'computer', 'jarvis', 'americano', 'hey google',
#     'hey siri', 'terminator', 'grapefruit', 'grasshopper', 'ok google', 'picovoice'}
WAKE_WORDS = ["jarvis", "bumblebee", "computer", "terminator", "picovoice"]
SPEECH_GOOGLE_CREDENTIALS = "credentials/speech_google_credentials.json"
GOOGLE_TIMEOUT = 14  # After how many seconds Google should definitely be terminated. in seconds
ABORT_WORDS = ["abbrechen", "stop"]  # if word is heard, abort immediately
MAX_ALTERNATIVES = 5  # how many alternative transcripts google may give maximum
# endregion --- speech to text ---

# region === say sentences ===
SAY_SHOULD_TURN_LIGHT_OFF = "Soll ich das licht aus machen?"
SAY_SAY_ERROR = "Es ist ein Fehler beim sprechen passiert!"
SAY_DONT_UNDERSTAND = "Das habe ich nicht verstanden."
# endregion --- say sentences ---

# region === barrier ===
BARRIER_PIN_1 = 22
BARRIER_PIN_2 = 17
LAST_BROKEN_TIMEOUT = datetime.timedelta(seconds=2)  # timedelta after a barrier signal is invalidated
LAST_SENT_TIME = datetime.timedelta(seconds=3)  # how long ago the last send must have been
# endregion --- barrier ---
