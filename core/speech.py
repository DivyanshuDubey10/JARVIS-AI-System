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

        self.stop_requested = False
        self.listening_for_stop = True

        # Start background interrupt listener
        self.stop_thread = threading.Thread(
            target=self._listen_for_stop,
            daemon=True
        )

        self.stop_thread.start()

        try:
            asyncio.run(self._speak(text))

        finally:
            self.listening_for_stop = False

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

            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True

            while self.listening_for_stop:

                try:
                    audio = recognizer.listen(
                        source,
                        timeout=1,
                        phrase_time_limit=2
                    )

                    text = (
                        recognizer
                        .recognize_google(audio)
                        .lower()
                        .strip()
                    )

                    print(f"Interrupt listener: {text}")

                    if text in STOP_WORDS:

                        print("Interrupt detected!")

                        self.stop()

                        break

                except sr.WaitTimeoutError:
                    continue

                except sr.UnknownValueError:
                    continue

                except sr.RequestError:
                    continue

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

    def stop(self):

        print("Stopping speech...")

        self.stop_requested = True
        self.listening_for_stop = False

        pygame.mixer.music.stop()