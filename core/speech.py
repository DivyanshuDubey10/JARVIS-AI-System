import asyncio
import edge_tts
import tempfile
import os
import pygame
import re
import threading
import speech_recognition as sr


class SpeechEngine:

    VOICE = "en-US-GuyNeural"

    def __init__(self):
        pygame.mixer.init()

        self.stop_requested = False
        self.listening_for_stop = False
        self.stop_thread = None
        self.speech_lock = threading.Lock()
        
        
    def clean_text(self, text):
        # Remove asterisks / Markdown formatting
        text = re.sub(r'\*+', '', text)

        # Remove Markdown headings
        text = re.sub(r'#+\s*', '', text)

        # Remove bullet points
        text = re.sub(
            r'^\s*[-•]\s+',
            '',
            text,
            flags=re.MULTILINE
        )

        # Remove code backticks
        text = text.replace("`", "")

        # Convert Markdown links to normal text
        text = re.sub(
            r'\[([^\]]+)\]\([^)]+\)',
            r'\1',
            text
        )

        # Remove excessive spaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def speak(self, text):

        text = self.clean_text(text)

        if not text:
            return

        with self.speech_lock:

            self.stop_requested = False
            self.listening_for_stop = True

            self.stop_thread = threading.Thread(
                target=self._listen_for_stop,
                daemon=True
            )

            self.stop_thread.start()

            try:
                asyncio.run(self._speak(text))

            finally:
                self.listening_for_stop = False

                if self.stop_thread and self.stop_thread.is_alive():
                    self.stop_thread.join(timeout=1.5)

                self.stop_thread = None

    async def _speak(self, text):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as f:
            filename = f.name

        try:

            communicate = edge_tts.Communicate(
                text,
                self.VOICE
            )

            await communicate.save(filename)

            if self.stop_requested:
                return

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():

                if self.stop_requested:
                    pygame.mixer.music.stop()
                    break

                await asyncio.sleep(0.05)

            pygame.mixer.music.unload()

        finally:

            if os.path.exists(filename):
                os.remove(filename)

    def _listen_for_stop(self):

        recognizer = sr.Recognizer()

        STOP_WORDS = {
            "stop",
            "cancel",
            "quiet",
            "shut up",
            "be quiet"
        }

        with sr.Microphone() as source:

            recognizer.pause_threshold = 1.0
            recognizer.phrase_threshold = 0.3
            recognizer.non_speaking_duration = 0.5
            recognizer.energy_threshold = 100
            recognizer.dynamic_energy_threshold = False

            while self.listening_for_stop:

                try:

                    audio = recognizer.listen(
                        source,
                        timeout=0.5,
                        phrase_time_limit=1
                    )

                    text = (
                        recognizer
                        .recognize_google(audio)
                        .lower()
                        .strip()
                    )

                    if text in STOP_WORDS:

                        self.stop()

                        break

                except sr.WaitTimeoutError:
                    continue

                except sr.UnknownValueError:
                    continue

                except sr.RequestError:
                    continue

    def stop(self):

        self.stop_requested = True
        self.listening_for_stop = False

        pygame.mixer.music.stop()