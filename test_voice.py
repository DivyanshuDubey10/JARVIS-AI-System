from voice.listener import VoiceListener

listener = VoiceListener()

while True:
    text = listener.listen()

    if text:
        print("RESULT:", text)

    if text == "exit":
        break