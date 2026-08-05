from voice.listener import VoiceListener

listener = VoiceListener()

while True:

    command = listener.listen()

    if command:
        print(command)

    if command == "exit":
        break