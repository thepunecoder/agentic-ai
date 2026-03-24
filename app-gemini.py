import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"api_version": "v1"}
)

def chat():
    print("AI Agent started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"You are a smart data engineering assistant.\nUser: {user_input}"
        )

        print("\nAI:", response.text)
        print("-" * 50)

if __name__ == "__main__":
    chat()