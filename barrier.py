import asyncio
import RPi.GPIO as GPIO
from my_log import my_log
import settings
from utils import send_sync

LAST_BROKEN = -1


def break_beam_handle(channel, channel_active):
    global LAST_BROKEN

    my_log.debug(f"channel {channel} is now {channel_active}")
    if channel_active:
        if LAST_BROKEN >= 0 and LAST_BROKEN != channel:
            if channel == settings.BARRIER_PIN_1:
                my_log.debug("Barrier in")
                # unfortunately i cant async here, because its called from sync callback
                send_sync(settings.WEB_ORIGIN + "barrier/in")
            else:
                my_log.debug("Barrier out")
                # unfortunately i cant async here, because its called from sync callback
                send_sync(settings.WEB_ORIGIN + "barrier/out")
            LAST_BROKEN = -1
        else:
            LAST_BROKEN = channel


def break_beam_callback(channel):
    """
    This just tells asyncio to start the async function above
    :param channel:
    :return:
    """
    global loop
    loop.call_soon_threadsafe(break_beam_handle, channel, GPIO.input(channel))


if __name__ == "__main__":
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(settings.BARRIER_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(settings.BARRIER_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(settings.BARRIER_PIN_1, GPIO.BOTH, callback=break_beam_callback, bouncetime=50)
    GPIO.add_event_detect(settings.BARRIER_PIN_2, GPIO.BOTH, callback=break_beam_callback, bouncetime=50)

    try:
        loop = asyncio.get_event_loop()
        loop.run_forever()
        loop.close()
    except KeyboardInterrupt:
        print("Exiting gracefully...")

GPIO.cleanup()
