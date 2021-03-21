import asyncio
from aiohttp import web
import effect
import settings
from my_log import my_log
from utils import send_post, flatten
import json


async def save_say(text):
    from text_to_speech import say
    try:
        say(text)
    except Exception as e:
        my_log.error("text to speech failed saying")
        my_log.exception(e)
        await request_effects_all_leds([effect.ERROR_BLINK, effect.RESTORE_PREVIOUS], 99)
        say(settings.SAY_SAY_ERROR)


async def request_effects_all_leds(effects, priority=0):
    for led_name in settings.LED_NAMES:
        asyncio.create_task(request_effects(led_name, effects, priority))


async def request_effects(led_name, effects, priority=0):
    send_post(settings.LED_WEB_ORIGIN + "effect/", data={
        "name": led_name,
        "priority": priority,
        "effects": json.dumps(flatten(effects)),
    })


async def handle_index(request):
    return web.Response(text="This is the index page")


async def handle_barrier_in(request):
    await request_effects_all_leds([effect.BLINK], 20)
    return web.Response(text="OK")


async def handle_barrier_out(request):
    await request_effects_all_leds([effect.RESTORE_PREVIOUS_DARKEN_30, effect.RESTORE_PREVIOUS_OFF], 10)
    await save_say(settings.SAY_SHOULD_TURN_LIGHT_OFF)
    # todo: if wake_word, abort. not just after 5 seconds
    await asyncio.sleep(5)

    # this will abort the turn off and restore previous state.
    # This is working, because the effect from above is still running and with the priority it will be overwritten
    await request_effects_all_leds([effect.RESTORE_PREVIOUS], 20)
    return web.Response(text="OK")


# todo: for all handles: the same handle can't run async in parallel. Fix that maybe?
app = web.Application()
app.add_routes([web.get('/', handle_index),
                # web.get('/barrier/{direction}', handle_barrier),  # possible values: in, out
                web.get('/barrier/in', handle_barrier_in),
                web.get('/barrier/out', handle_barrier_out),
                ])

if __name__ == '__main__':
    web.run_app(app)
