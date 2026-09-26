import sys

from core.assistant import Assistant


def main():

    jarvis = Assistant()

    initial_command = None

    if len(sys.argv) > 1:

        if sys.argv[1] == "--wake":
            initial_command = ""

        else:
            initial_command = " ".join(sys.argv[1:])

    jarvis.run(initial_command)


if __name__ == "__main__":
    main()