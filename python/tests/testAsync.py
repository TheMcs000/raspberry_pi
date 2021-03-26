import asyncio


async def handle():
    print("HANDLE")
    await asyncio.sleep(1)
    print("HANDLE DONE")


def sync():
    global loop

    loop.create_task(handle())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for i in range(10):
        sync()
    loop.run_forever()
    loop.close()
