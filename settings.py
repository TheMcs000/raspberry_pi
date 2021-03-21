import os

# region === brain web ===
BRAIN_WEB_ORIGIN = "http://localhost:8080/"  # must have trailing slashes!
# endregion --- brain web ---

# region === LEDS ===
LED_WEB_ORIGIN = "http://localhost:3000/"  # must have trailing slashes!
LED_NAMES = ["tisch", "bett"]
# endregion === LEDS ===

# region === text to speech ===
TTS_LANGUAGE = "de"
TTS_DIR = "tts/"
TTS_CACHE_FILE = os.path.join(TTS_DIR, "cache.txt")
# endregion === text to speech ===

# region === say sentences ===
SAY_SHOULD_TURN_LIGHT_OFF = "Soll ich das licht aus machen?"
SAY_SAY_ERROR = "Es ist ein Fehler beim sprechen passiert!"
# endregion --- say sentences ---

# region === barrier ===
BARRIER_PIN_1 = 17
BARRIER_PIN_2 = 22
# endregion --- barrier ---
