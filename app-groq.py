import os  # import os for environment variable access
from dotenv import load_dotenv  # import load_dotenv to read .env file
from groq import Groq  # import Groq client class from groq SDK

load_dotenv()  # load environment variables from .env into os.environ

client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # create Groq client with API key from env

def chat():
    print("AI Agent started (type 'exit' to quit)\n")  # startup message

    while True:
        user_input = input("You: ")  # read user input

        if user_input.lower() == "exit":
            print("Goodbye!")  # goodbye message
            break  # exit loop and function

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # model name
            messages=[
                {"role": "system", "content": "You are a smart data engineering assistant who helps with Spark, SQL, and data pipelines."},  # system prompt
                {"role": "user", "content": user_input}  # user prompt
            ]
        )

        print("\nAI:", response.choices[0].message.content)  # show AI reply
        print("-" * 50)  # separator line

if __name__ == "__main__":
    chat()  # run chat if script is executed directly