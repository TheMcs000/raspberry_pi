import asyncio
import RPi.GPIO as GPIO
from my_log import my_log
import settings
from utils import send_async

LAST_BROKEN = -1


# region === why is this so complicate? ===
# usually async is easy, because you may use loop.create_task in order to
# call from a sync context something async without having to wait.
#
# However the RPi callback is on another thread.
# Therefore we first have to get on the main thread using loop.call_soon_threadsafe
# endregion --- why is this so complicate? ---


async def break_beam_handle(channel, channel_active):
    global LAST_BROKEN

    my_log.debug(f"channel {channel} is now {channel_active}")
    if channel_active:
        if LAST_BROKEN >= 0 and LAST_BROKEN != channel:
            if channel == settings.BARRIER_PIN_1:
                my_log.debug("Barrier in")
                coro = send_async(settings.WEB_ORIGIN + "barrier/in")
            else:
                my_log.debug("Barrier out")
                coro = send_async(settings.WEB_ORIGIN + "barrier/out")
            LAST_BROKEN = -1
            await coro
        else:
            LAST_BROKEN = channel


def call_async(channel, channel_active):
    global loop
    # create_task will run the task without waiting for it
    loop.create_task(break_beam_handle(channel, channel_active))


def schedule_main_thread(channel):
    """
    used to go from the callback thread to the main thread
    :param channel:
    :return:
    """
    global loop
    # this function is called by the callback, which is on another thread. Therefore call_soon_threadsafe has to be
    # called. With that callback function we are on the main thread and use createTask
    loop.call_soon_threadsafe(call_async, channel, GPIO.input(channel))


if __name__ == "__main__":
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(settings.BARRIER_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(settings.BARRIER_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(settings.BARRIER_PIN_1, GPIO.BOTH, callback=schedule_main_thread, bouncetime=50)
    GPIO.add_event_detect(settings.BARRIER_PIN_2, GPIO.BOTH, callback=schedule_main_thread, bouncetime=50)

    try:
        loop = asyncio.get_event_loop()
        loop.run_forever()
        loop.close()
    except KeyboardInterrupt:
        print("Exiting gracefully...")

    GPIO.cleanup()
