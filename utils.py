import aiohttp
import requests


async def send_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url):
            # html = await response.text()
            pass


def send_sync(url):
    """
    Only use this, if absolutely necessary, because it blocks a thread
    :param url:
    :return:
    """
    requests.get(url)
