import asyncio
import edge_tts
import tempfile
import os
import pygame


class SpeechEngine:
    VOICE = "en-US-GuyNeural"

    def __init__(self):
        pygame.mixer.init()

    def speak(self, text):
        asyncio.run(self._speak(text))

    async def _speak(self, text):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            filename = f.name

        communicate = edge_tts.Communicate(text, self.VOICE)
        await communicate.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(filename)