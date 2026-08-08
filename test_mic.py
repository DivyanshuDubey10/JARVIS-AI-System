import speech_recognition as sr
import audioop

recognizer = sr.Recognizer()

with sr.Microphone() as source:

    print("Stay completely silent.")
    print("Measuring microphone energy...")

    for i in range(50):

        audio = recognizer.record(source, duration=0.1)

        energy = audioop.rms(
            audio.frame_data,
            audio.sample_width
        )

        print(f"{energy}")

print("Finished.")