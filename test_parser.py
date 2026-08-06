from core.parser import CommandParser

parser = CommandParser()

while True:
    text = input("Command: ")

    if text.lower() == "exit":
        break

    command = parser.parse(text)

    print("\n----- Parsed Command -----")
    print("Raw    :", command.raw_text)
    print("Action :", command.action)
    print("Target :", command.target)
    print("Query  :", command.query)
    print("--------------------------\n")