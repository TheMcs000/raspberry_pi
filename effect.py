DEFAULT_DURATION = 5_000
DEFAULT_SPEED = 100

SWEEP_DURATION = 1000
SWEEP_SPEED = 50

# ----------

RESTORE_PREVIOUS = {
    "effectType": "previous",
    "color": "previous",
    "duration": DEFAULT_DURATION,
    "speed": DEFAULT_SPEED
}

# returns the previous state and turns the LED off
RESTORE_PREVIOUS_OFF = {
    "effectType": "previous",
    "color": "previous",
    "duration": DEFAULT_DURATION,
    "speed": DEFAULT_SPEED,
    "power": False
}

# duration: 30 seconds
RESTORE_PREVIOUS_DARKEN_30 = {
    "effectType": "previous",
    "color": "previousDarken",
    "duration": 30_000,
    "speed": DEFAULT_SPEED
}

# afterwards RESTORE_PREVIOUS should come
ERROR_SWEEP = {
    "effectType": "sweep",
    "color": "rgb",
    "duration": SWEEP_DURATION,
    "speed": SWEEP_SPEED,
    "rgb": [255, 0, 0]
}

PREVIOUS_SWEEP = {
    "effectType": "sweep",
    "color": "previous",
    "duration": SWEEP_DURATION,
    "speed": SWEEP_SPEED,
}
