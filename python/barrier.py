import asyncio
import RPi.GPIO as GPIO
from my_log import my_log
import settings
from utils import send_get
import datetime

LAST_BROKEN = -1
LAST_BROKEN_TIME = datetime.datetime(2000, 1, 1)
LAST_TIME_SENT = datetime.datetime(2000, 1, 1)


# region === why is this so complicate? ===
# usually async is easy, because you may use loop.create_task in order to
# call from a sync context something async without having to wait.
#
# However the RPi callback is on another thread.
# Therefore we first have to get on the main thread using loop.call_soon_threadsafe
# endregion --- why is this so complicate? ---


def other_thread_handle(channel):
    global loop
    global LAST_BROKEN
    global LAST_BROKEN_TIME
    # because scheduling a call to the main thread may switch up the order, the calculation is done here.
    # Then a call to the main thread will execute the request (async)
    channel_active = GPIO.input(channel)
    my_log.debug(f"channel {channel} is now {channel_active}")
    if channel_active:
        now = datetime.datetime.now()
        if LAST_BROKEN_TIME + settings.LAST_BROKEN_TIMEOUT > now and \
                LAST_BROKEN >= 0 and LAST_BROKEN != channel:
            send_barrier_movement(now, "in" if channel == settings.BARRIER_PIN_1 else "out")
            LAST_BROKEN = -1
        else:
            LAST_BROKEN = channel
        LAST_BROKEN_TIME = now


def send_barrier_movement(now, direction):
    global LAST_TIME_SENT

    my_log.debug(f"Barrier {direction}")
    # this function is called by the callback, which is on another thread. Therefore call_soon_threadsafe
    # has to be called. With that callback function we are on the main thread and use createTask
    if LAST_TIME_SENT + settings.LAST_SENT_TIME < now:
        loop.call_soon_threadsafe(send_get, settings.BRAIN_WEB_ORIGIN + f"barrier/{direction}")
        LAST_TIME_SENT = now


if __name__ == "__main__":
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(settings.BARRIER_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(settings.BARRIER_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(settings.BARRIER_PIN_1, GPIO.BOTH, callback=other_thread_handle, bouncetime=50)
    GPIO.add_event_detect(settings.BARRIER_PIN_2, GPIO.BOTH, callback=other_thread_handle, bouncetime=50)

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Exiting gracefully...")
        loop.close()

    GPIO.cleanup()
