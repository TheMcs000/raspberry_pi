from aiohttp import web
import settings
from my_log import my_log


def save_say(text):
    from text_to_speech import say
    try:
        say(text)
    except Exception as e:
        my_log.error("text to speech failed saying")
        my_log.exception(e)
        print("TODO: LIGHT SHOW ERROR")  # todo: light show error
        say(settings.SAY_SAY_ERROR)


async def handle_index(request):
    return web.Response(text="This is the index page")


async def handle_barrier(request):
    name = request.match_info.get('direction', "in")  # possible values: in, out
    direction_is_in = name == "in"
    if direction_is_in:
        print("TODO: DIRECTION IN")  # todo: direction in
    else:  # direction is out
        save_say(settings.SAY_SHOULD_TURN_LIGHT_OFF)
    return web.Response(text="OK")


app = web.Application()
app.add_routes([web.get('/', handle_index),
                web.get('/barrier/{direction}', handle_barrier),  # possible values: in, out
                ])

if __name__ == '__main__':
    web.run_app(app)
