import asyncio
import aiohttp
from my_log import my_log
import settings
import json


def send_get(url):
    """
    Makes a async http GET request. Does not need to be awaited.
    However it must be called from a coroutine or a callback
    """
    asyncio.create_task(await_send_get(url))


async def await_send_get(url):
    """
    The same as @see send_get. But you need to await it. Unless you need to await the server parsing your request, you
    probably want to use @see send_get
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            handle_response(url, resp)


def send_post(url, data=None):
    """
    Makes a async http POST request. Does not need to be awaited.
    However it must be called from a coroutine or a callback
    """
    asyncio.create_task(await_send_post(url, data=data))


async def await_send_post(url, data=None):
    """
    The same as @see send_post. But you need to await it. Unless you need to await the server parsing your request, you
    probably want to use @see send_post
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            handle_response(url, resp)


def handle_response(url, resp):
    """
    in case there is a bad status code, this will log it (Also: debug)
    """
    if resp.status == 200:
        my_log.debug(f"request \"{url}\" finished successfully with code {resp.status}")
    else:
        my_log.error(f"request \"{url}\" failed with code {resp.status}")


async def request_effects_all_leds(effects, priority=0):
    for led_name in settings.LED_NAMES:
        asyncio.create_task(request_effects(led_name, effects, priority))


async def request_effects(led_name, effects, priority=0):
    send_post(settings.LED_WEB_ORIGIN + "effect/", data={
        "name": led_name,
        "priority": priority,
        "effects": json.dumps(flatten(effects)),
    })


def flatten(lst):
    res = list()
    for x in lst:
        if isinstance(x, list):
            res.extend(flatten(x))
        else:
            res.append(x)
    return res
