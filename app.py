import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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


#Difference between OpenAI, Gemini, Groq?
#OpenAI, Gemini, and Groq are all companies that provide AI models and services, but they have different focuses and offerings:
#1. OpenAI: OpenAI is a leading AI research organization that has developed several influential AI models, including the GPT series (like GPT-3 and GPT-4). OpenAI's models are widely used for natural language processing tasks, and they offer an API for developers to integrate their models into applications.
#2. Gemini: Gemini is a product from Google that provides AI models and services. It is designed to offer powerful AI capabilities, and it includes models like Gemini-2.0-flash
#3. Groq: Groq is a company that focuses on building AI hardware and software solutions. They provide AI models and services, and they have their own API for developers to access their models. Groq's offerings are designed to be efficient and scalable for various AI applications.
