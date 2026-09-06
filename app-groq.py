import os
from dotenv import load_dotenv
from groq import Groq
from tools import save_code, explain, debug, final_answer
from parser import parse_llm_response

load_dotenv()

# Configuration
MODEL = "openai/gpt-oss-120b"
SYSTEM_PROMPT = """You are an AI data engineering agent.

You MUST always respond in valid JSON.

Available tools:
1. save_code → for generating code
2. explain → for explaining concepts
3. debug → for troubleshooting issues
4. final_answer → for providing final answers

Response format:
{
"tool": "<tool_name>",
"input": "<content>"
}

STRICT RULES:
- You can call tools multiple times
- If the task is not complete → choose another tool
- If the task is complete → use "final_answer"
- Do NOT stop until final_answer is used
- Do NOT return anything outside JSON

CRITICAL RULE:
- You MUST return ONLY ONE JSON object at a time
- Do NOT return multiple tool calls in one response
- First decide ONE action
- Wait for tool result before next step
"""

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Tool registry
TOOLS = {
    "save_code": save_code,
    "explain": explain,
    "debug": debug,
    "final_answer": final_answer
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

    MAX_STEPS = 5  # prevent infinite loops

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # ✅ Initialize memory
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]

        for step in range(MAX_STEPS):
            print(f"\n🧠 Step {step+1}")

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )

            response_text = response.choices[0].message.content
            print("RAW:", response_text)

            parsed = parse_llm_response(response_text)

            tool_name = parsed.get("tool")
            tool_input = parsed.get("input")

            if tool_name not in TOOLS:
                print("❌ Unknown tool:", tool_name)
                break

            # ✅ Execute tool
            result = execute_tool(tool_name, tool_input)

            # ✅ Add to memory
            messages.append({
                "role": "assistant",
                "content": response_text
            })

            messages.append({
                "role": "assistant",
                "content": f"Tool result: {result}"
                })

            # ✅ STOP CONDITION
            if tool_name == "final_answer":
                print("\n🎯 Task Completed")
                break

        print("-" * 50)

if __name__ == "__main__":
    chat()  # run chat if script is executed directly