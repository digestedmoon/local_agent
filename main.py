import yaml

from agent import SYSTEM_PROMPT, Agent,get_current_time, do_division, get_date,get_weather
from models import Message
from utils import create_session, list_sessions, save_session, load_session, delete_session 

with open("./data/config.yaml", "r") as file:
    config = yaml.safe_load(file)

models = config["model"]["name"]

print("\nAvailable models: ")
for index, model  in enumerate (models, start = 1):
    print(f"{index}. Model: {model}") 

choice = int(input("Enter the model you want to use: "))

if choice == 1:
    MODEL = "qwen3:8B"
elif choice == 2:
    MODEL = "hhao/qwen2.5-coder-tools:latest"
elif choice == 3:
    MODEL = "qwen3:4b"    
elif choice == 4:
    MODEL = "qwen3-vl:4b"
elif choice == 5:
    MODEL = "qwen2.5-coder:7b"
else:
    raise ValueError("Invalid choice")

tool = {
    "get_current_time": get_current_time,
    "do_division": do_division,
    "get_date": get_date,
    "get_weather": get_weather,
}


def create_agent(session):
    return Agent(
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
        messages=session.messages,
        tools=tool,
    )


def new_session():
    session = create_session(MODEL)

    session.messages = [
        Message(
            role="system",
            content=SYSTEM_PROMPT,
        )
    ]

    return session


def choose_session():
    session_list = list_sessions()

    print("\n1. New Session")
    print("2. Load Session")

    choice = int(input("\nEnter the Session: "))

    if choice == 1:
        return new_session()

    if choice == 2:
        if not session_list:
            print("\nNo saved sessions found.")
            print("Creating new session.")
            return new_session()

        print("\nAvailable sessions:")

        for index, session_id in enumerate(session_list, start=1):
            print(f"{index}. {session_id}")

        selection = int(input("\nSelect the session: "))

        session_id = session_list[selection - 1]

        return load_session(session_id)

    raise ValueError("Invalid choice")


def main():

    session = choose_session()

    agent = create_agent(session)

    print(f"\nSession: {session.session_id}")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in {"exit", "quit", "bye"}:
            break

        response = agent.run(user_input)

        print(f"\nAgent: {response}")

        session.messages = agent.messages

        save_session(session)


if __name__ == "__main__":
    main()