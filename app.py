import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

print("DEBUG KEY:", os.getenv("OPENAI_API_KEY"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat():
    print("AI Agent started (type 'exit' to quit)\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart data engineering assistant who helps with Spark, SQL, and data pipelines."},
                {"role": "user", "content": user_input}
            ]
        )

        print("\nAI:", response.choices[0].message.content)
        print("-" * 50)

if __name__ == "__main__":
    chat()