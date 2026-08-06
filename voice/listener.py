import speech_recognition as sr

class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.3
        
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=4)
            
        try: 
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower()
        
        except sr.UnknownValueError:
            return ""
        
        except sr.RequestError:
            return ""