DEFAULT_DURATION = 5_000
DEFAULT_SPEED = 100

SWEEP_DURATION = 30_000
SWEEP_SPEED = 92

BLINK_DURATION = 500

# ----------

RESTORE_PREVIOUS = {
    "effectType": "previous",
    "color": "previous",
    "duration": DEFAULT_DURATION,
    "speed": DEFAULT_SPEED
}

# returns the previous state and turns the LED off
RESTORE_PREVIOUS_OFF = [
    {
        "effectType": "previous",
        "color": "previous",
        "duration": 501,  # we need to wait here because the LED animates the color change and would loose it otherwise
        "speed": DEFAULT_SPEED,
    },
    {
        "effectType": "previous",
        "color": "previous",
        "duration": DEFAULT_DURATION,
        "speed": DEFAULT_SPEED,
        "power": False
    },
]

# duration: 30 seconds
DARKEN_30 = {
    "effectType": "previous",
    "color": "previousDarken",
    "duration": 30_000,
    "speed": DEFAULT_SPEED
}

# duration: 30 seconds (30 seconds is the timeout. Should never get that far)
VOICE_SWEEP_300 = [
    {
        "effectType": "sweep",
        "color": "rgb",
        "duration": 300_000,
        "speed": SWEEP_SPEED,
        "rgb": [0, 0, 255]
    },
    RESTORE_PREVIOUS
]

# Does RESTORE_PREVIOUS
BLINK = [
    {
        "effectType": "static",
        "color": "previousDarken",
        "duration": BLINK_DURATION,
        "speed": DEFAULT_SPEED,
    },
    RESTORE_PREVIOUS
]

# afterwards RESTORE_PREVIOUS should come
ERROR_BLINK = [
    {
        "effectType": "static",
        "color": "rgb",
        "duration": BLINK_DURATION,
        "speed": DEFAULT_SPEED,
        "rgb": [255, 0, 0]
    },
    {
        "effectType": "static",
        "color": "rgb",
        "duration": BLINK_DURATION,
        "speed": DEFAULT_SPEED,
        "rgb": [50, 0, 0]
    },
    {
        "effectType": "static",
        "color": "rgb",
        "duration": BLINK_DURATION,
        "speed": DEFAULT_SPEED,
        "rgb": [255, 0, 0]
    },
]
