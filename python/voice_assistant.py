import os
import struct
from threading import Thread
import pvporcupine
import pyaudio

import speech_recognition as sr

from my_log import my_log
import settings


def speech_to_text(recognizer, source):
    audio = recognizer.listen(source)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # with open("microphone-results.wav", "wb") as f:
    #     f.write(audio.get_wav_data())


class PorcupineDemo(Thread):
    def __init__(self):
        super(PorcupineDemo, self).__init__()

        self._keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in settings.WAKE_WORDS]

        # could be altered per wake_word if required. Determines the required confidence to recognize the wake word
        self._sensitivities = [0.5] * len(self._keyword_paths)

        # region === recognizer ===
        self._recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            # listen for 1 second to calibrate  the energy threshold for ambient noise levels
            self._recognizer.adjust_for_ambient_noise(source)
        # endregion --- recognizer ---

    def run(self):
        """
         Creates an input audio stream, instantiates an instance of Porcupine object, and monitors the audio stream for
         occurrences of the wake word(s). It prints the time of detection for each occurrence and the wake word.
         """

        keywords = list()
        for x in self._keyword_paths:
            keywords.append(os.path.basename(x).replace('.ppn', '').split('_')[0])

        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = pvporcupine.create(
                library_path=pvporcupine.LIBRARY_PATH,
                model_path=pvporcupine.MODEL_PATH,
                keyword_paths=self._keyword_paths,
                sensitivities=self._sensitivities)

            pa = pyaudio.PyAudio()

            # input device could be changed here if required. list all device indices:
            # for i in range(pa.get_device_count()):
            #     info = pa.get_device_info_by_index(i)
            input_device_index = None

            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=input_device_index)

            my_log.debug(f"listening on keywords {keywords}")

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                result = porcupine.process(pcm)
                if result >= 0:
                    my_log.debug(f"Detected {keywords[result]}")
                    with sr.Microphone() as source:
                        speech_to_text(self._recognizer, source)

        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()


if __name__ == '__main__':
    PorcupineDemo().run()
