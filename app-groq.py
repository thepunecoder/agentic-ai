import os  # import os for environment variable access
from dotenv import load_dotenv  # import load_dotenv to read .env file
from groq import Groq  # import Groq client class from groq SDK
import json  # import json for handling JSON data

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
            {
                "role": "system",
                "content": """
                You are an AI data engineering agent.

                You MUST always respond in valid JSON format.

                Response format:
                {
                "type": "concept | code | debug",
                "topic": "string",
                "explanation": "string",
                "code": "string"
                }

                STRICT RULES:
                - If question asks "why", "error", "slow", "issue" → type = "debug"
                - If question asks "write", "code", "example" → type = "code"
                - Otherwise → type = "concept"
                - Never misclassify
                - Always return valid JSON only
                """ },  # system prompt
                {"role": "user", 
                 "content": user_input}  # user prompt
            ]
        )

        #print("\nAI:", response.choices[0].message.content)  # show AI reply
        response_text = response.choices[0].message.content
        try:
            parsed = json.loads(response_text)  # parse AI response as JSON
            if parsed["type"] not in ["concept", "code", "debug"]:
                parsed["type"] = "concept"  # fallback
            if parsed["type"] == "code":
                print("💻 Generating Code...")
            elif parsed["type"] == "concept":
                print("📘 Explaining Concept...")
            elif parsed["type"] == "debug":
                print("🐞 Debugging Issue...")
            print("\nParsed Response:\n", parsed)  # show parsed JSON
        except:
            print("\nRaw Response:\n", response_text)  # show raw response if JSON parsing fails
        
        print("-" * 50)  # separator line

if __name__ == "__main__":
    chat()  # run chat if script is executed directly