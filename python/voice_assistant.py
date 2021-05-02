import os
import struct
from threading import Thread
import pvporcupine
import pyaudio
from text_to_action import text_has_action, text_execute_action
from utils import send_get
import asyncio
from my_log import my_log
import settings
from MicrophoneStream import MicrophoneStream
from google.cloud import speech
import datetime

GOOGLE_RUNNING = False
GOOGLE_ABORT_ID = 0


def start_google():
    global GOOGLE_RUNNING

    if not GOOGLE_RUNNING:
        GOOGLE_RUNNING = True
        loop.call_soon_threadsafe(send_get, settings.BRAIN_WEB_ORIGIN + "voice/listening/start")
        start_timestamp = datetime.datetime.now()
        loop.call_soon_threadsafe(call_abort, start_timestamp)
        googleT.start()
        my_log.debug("Start google")
    else:
        raise Exception("Can't start google because it's already running")


def stop_google():
    global googleT
    global GOOGLE_RUNNING

    if GOOGLE_RUNNING:
        googleT.stop()
        googleT = GoogleSpeech(audio)
        my_log.debug("Stop google")
        GOOGLE_RUNNING = False

        # after trying to stop in order for me to recognize if something goes wrong
        loop.call_soon_threadsafe(send_get, settings.BRAIN_WEB_ORIGIN + "voice/listening/done")
    else:
        raise Exception("Can't stop google because it's not running")


async def abort_google_after_timeout(start_timestamp):
    global GOOGLE_ABORT_ID

    abort_id = GOOGLE_ABORT_ID = GOOGLE_ABORT_ID + 1
    now = datetime.datetime.now()
    await asyncio.sleep(settings.GOOGLE_TIMEOUT - (now - start_timestamp).total_seconds())
    if abort_id == GOOGLE_ABORT_ID and GOOGLE_RUNNING:
        my_log.debug("Aborting Google after Timeout")
        stop_google()


def call_abort(start_timestamp):
    """
    This function is needed because we first need to the main thread and then call async functions from there
    """
    asyncio.create_task(abort_google_after_timeout(start_timestamp))


def call_text_execute_action(text, confidence):
    """
    This function is needed because we first need to the main thread and then call async functions from there
    """
    asyncio.create_task(text_execute_action(text, confidence))


def porcupine_heard(keyword):
    global GOOGLE_RUNNING

    if GOOGLE_RUNNING:
        stop_google()
    else:
        start_google()


class PorcupineRecognizer(Thread):
    def __init__(self, audio_interface):
        super(PorcupineRecognizer, self).__init__()
        self.should_stop = False
        self._audio_interface = audio_interface

        self._keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in settings.WAKE_WORDS]

        # could be altered per wake_word if required. Determines the required confidence to recognize the wake word
        self._sensitivities = [0.8] * len(self._keyword_paths)

    def run(self):
        """
        Creates an input audio stream, instantiates an instance of Porcupine object, and monitors the audio stream for
        occurrences of the wake word(s). It prints the time of detection for each occurrence and the wake word.
        """
        keywords = list()
        for x in self._keyword_paths:
            keywords.append(os.path.basename(x).replace('.ppn', '').split('_')[0])

        porcupine = None
        try:
            porcupine = pvporcupine.create(
                library_path=pvporcupine.LIBRARY_PATH,
                model_path=pvporcupine.MODEL_PATH,
                keyword_paths=self._keyword_paths,
                sensitivities=self._sensitivities)

            my_log.debug(f"listening on keywords {keywords}")

            with MicrophoneStream(self._audio_interface, porcupine.sample_rate, porcupine.frame_length) as stream:
                audio_generator = stream.generator()
                for x in audio_generator:
                    if self.should_stop:
                        raise SystemExit("should_stop")
                    pcm = struct.unpack_from("h" * porcupine.frame_length, x)
                    result = porcupine.process(pcm)
                    if result >= 0:
                        my_log.debug(f"Detected {keywords[result]}")
                        porcupine_heard(keywords[result])
        except Exception as e:
            if type(e) != SystemExit:
                my_log.exception(e)
        finally:
            if porcupine is not None:
                porcupine.delete()


class GoogleSpeech(Thread):
    def __init__(self, audio_interface):
        super(GoogleSpeech, self).__init__()
        self._microphone_stream = None
        self._audio_interface = audio_interface

        # Audio recording parameters
        self._rate = 16000
        self._chunk = int(self._rate / 10)  # 100ms

        language_code = "de-DE"  # a BCP-47 language tag

        self._client = speech.SpeechClient.from_service_account_json(settings.SPEECH_GOOGLE_CREDENTIALS)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self._rate,
            language_code=language_code,
            max_alternatives=settings.MAX_ALTERNATIVES,
            model="command_and_search",
        )
        self._streaming_config = speech.StreamingRecognitionConfig(
            config=config, interim_results=True
        )

    def run(self):
        with MicrophoneStream(self._audio_interface, self._rate, self._chunk) as stream:
            self._microphone_stream = stream
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = self._client.streaming_recognize(self._streaming_config, requests)

            for response in responses:
                for result in response.results:
                    my_log.info(result)
                    for alternative in result.alternatives:
                        transcript = alternative.transcript
                        confidence = alternative.confidence if "confidence" in alternative else 0.01

                        if "is_final" in result and result.is_final:  # todo: Muss der text bei den is_final aneinander gehängt werden? testen!
                            if text_has_action(transcript, confidence):
                                stop_google()
                                self._microphone_stream = None  # must be after stop_google()
                                loop.call_soon_threadsafe(call_text_execute_action, transcript, confidence)
                                return

                        if any([word.lower() in transcript.lower() for word in settings.ABORT_WORDS]):
                            my_log.debug(f"Google aborted because abort word in '{transcript}' was heard")
                            stop_google()
                            self._microphone_stream = None  # must be after stop_google()
                            return

        # for loop did not react: Not understood
        loop.call_soon_threadsafe(call_text_execute_action, "", 1)
        self._microphone_stream = None

    def stop(self):
        if self._microphone_stream is None:
            raise Exception("No microphone stream to stop")
        else:
            self._microphone_stream.__exit__(None, None, None)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    audio = pyaudio.PyAudio()

    googleT = GoogleSpeech(audio)

    porcupineT = PorcupineRecognizer(audio)
    porcupineT.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Exiting gracefully...")
        loop.close()

        porcupineT.should_stop = True
        porcupineT.join()

        audio.terminate()
