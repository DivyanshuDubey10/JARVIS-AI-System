import speech_recognition as sr


class VoiceListener:

    def __init__(self):
        self.recognizer = sr.Recognizer()

        # Give the user time to pause naturally.
        self.recognizer.pause_threshold = 1.5
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.8

        # Prevent excessive sensitivity to background noise.
        self.recognizer.dynamic_energy_threshold = True

        with sr.Microphone() as source:
            print("Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print(
                f"Energy threshold: "
                f"{self.recognizer.energy_threshold:.2f}"
            )

    def listen(self):

        with sr.Microphone() as source:
            print("Listening...")

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=20
                )

            except sr.WaitTimeoutError:
                return ""

        try:
            text = self.recognizer.recognize_google(audio)

            text = text.lower().strip()

            if text:
                print(f"You: {text}")

            return text

        except sr.UnknownValueError:
            return ""

        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return ""