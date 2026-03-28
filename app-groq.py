from json import tool
import os
import re  # import os for environment variable access
from dotenv import load_dotenv  # import load_dotenv to read .env file
from groq import Groq  # import Groq client class from groq SDK
import json  # import json for handling JSON data
from tools import save_code_to_file  # import helper function to save code to file
from parser import parse_llm_response  # import helper function to parse LLM response
import time  # import time for timestamping filenames
from tools import save_code, explain, debug

load_dotenv()  # load environment variables from .env into os.environ

client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # create Groq client with API key from env

tools = {
    "save_code": save_code,
    "explain": explain,
    "debug": debug
}

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

                You MUST always respond in valid JSON.

                Available tools:
                1. save_code → for generating code
                2. explain → for explaining concepts
                3. debug → for troubleshooting issues

                Response format:
                {
                "tool": "<tool_name>",
                "input": "<content>"
                }

                STRICT RULES:
                - If user asks for code → use "save_code"
                - If user asks for explanation → use "explain"
                - If user asks about issues/errors → use "debug"
                - Do NOT return anything outside JSON
                - Do NOT include markdown or backticks
                """ },  # system prompt
                {"role": "user", 
                 "content": user_input}  # user prompt
            ]
        )

        #print("\nAI:", response.choices[0].message.content)  # show AI reply
        response_text = response.choices[0].message.content
        parsed = parse_llm_response(response_text)  # parse AI response
        
        tool_name = parsed.get("tool")
        tool_input = parsed.get("input")

        if tool_name in tools:
            result = tools[tool_name](tool_input)
            
            if result:
                print("⚡ Action:", result)
        else:
            print("❌ Unknown tool:", tool_name)
        
        print("-" * 50)  # separator line

if __name__ == "__main__":
    chat()  # run chat if script is executed directly