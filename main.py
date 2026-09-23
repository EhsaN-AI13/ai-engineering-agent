from agent.agent import EhsaNAgent


def main():
    agent = EhsaNAgent()

    print(f"{agent.name} AI Agent")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("EhsaN: Goodbye!")
            break

        response = agent.run(user_input)
        print(f"EhsaN: {response}")


if __name__ == "__main__":
    main()