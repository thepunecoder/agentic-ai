import os
from dotenv import load_dotenv
from groq import Groq

from tools import save_code, explain, debug
from parser import parse_llm_response

load_dotenv()

# Configuration
MODEL = "llama-3.1-8b-instant"
SYSTEM_PROMPT = """You are an AI data engineering agent.

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
"""

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Tool registry
TOOLS = {
    "save_code": save_code,
    "explain": explain,
    "debug": debug
}

def get_llm_response(user_input):
    """Get response from LLM for user input."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content


def execute_tool(tool_name, tool_input):
    """Execute a tool and return the result."""
    if tool_name not in TOOLS:
        print(f"❌ Unknown tool: {tool_name}")
        return None
    
    result = TOOLS[tool_name](tool_input)
    if result:
        print(f"⚡ Action: {result}")
    return result


def chat():
    """Main chat loop for the AI agent."""
    print("AI Agent started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response_text = get_llm_response(user_input)
        parsed = parse_llm_response(response_text)

        tool_name = parsed.get("tool")
        tool_input = parsed.get("input")

        execute_tool(tool_name, tool_input)
        print("-" * 50)

if __name__ == "__main__":
    chat()  # run chat if script is executed directly