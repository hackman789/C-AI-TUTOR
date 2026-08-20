from dotenv import load_dotenv
from google import genai
import os


def create_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    return genai.Client(api_key=api_key)


def create_chat(client):
    return client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": """
You are a friendly C++ tutor.

Rules:
- Explain concepts in simple language.
- Assume the student is a beginner.
- Give small examples when helpful.
- Explain difficult terminology.
- Use practical programming examples.
- Encourage the student to understand the concept rather than just memorize code.
"""
        }
    )


def run_chatbot(client, chat):
    print("===================================")
    print("       C++ AI Tutor Chatbot")
    print("===================================")
    print("Type /help for commands.")
    print("Type /exit to quit.\n")

    while True:

        question = input("You: ").strip()

        # Empty input
        if not question:
            print("AI: Please enter a question.\n")
            continue

        # Exit command
        if question.lower() == "/exit":
            print("AI: Goodbye! 👋")
            break

        # Help command
        if question.lower() == "/help":
            print("\nAvailable commands:")
            print("/help  - Show available commands")
            print("/clear - Clear conversation memory")
            print("/exit  - Exit the chatbot\n")
            continue

        # Clear conversation
        if question.lower() == "/clear":
            chat = create_chat(client)
            print("AI: Conversation cleared.\n")
            continue

        # Send message to Gemini
        try:
            response = chat.send_message(question)

            print("\nAI:", response.text)
            print()

        except Exception as e:
            print("\nAI: Sorry, something went wrong.")
            print("Error:", e)
            print()


def main():
    client = create_client()

    chat = create_chat(client)

    run_chatbot(client, chat)


if __name__ == "__main__":
    main()