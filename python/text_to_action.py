"""
For the voice assistant. Receives some text and executes the programmed action for it
"""
import settings
import effect
from utils import send_post, request_effects_all_leds


async def light_on(text):
    await request_effects_all_leds([effect.RESTORE_PREVIOUS])


async def light_off(text):
    await request_effects_all_leds([effect.RESTORE_PREVIOUS_OFF])


# TODO: Think about a actions model
ACTIONS = [
    [["licht an", "hell", "licht", "es werde licht"], light_on],
    [["licht aus", "dunkel"], light_off],
]


def get_action(text, confidence):
    global ACTIONS

    for action in ACTIONS:
        if any([text.lower() in phrase.lower() for phrase in action[0]]):
            return action
    return None


def text_has_action(text, confidence):
    """
    If a given text has an action, or if no action is related to that text
    """
    return get_action(text, confidence) is not None


async def text_execute_action(text, confidence):
    """
    executes an action for the text. If no action matches, a not found action will be executed
    """
    action = get_action(text, confidence)
    if action is not None:
        await action[1](text)
    else:
        send_post(settings.BRAIN_WEB_ORIGIN + "say", {"text": settings.SAY_DONT_UNDERSTAND})
