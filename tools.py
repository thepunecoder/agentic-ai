import os
import time
import json

def save_code_to_file(code: str, filename: str):
    with open(filename, "w") as f:
        f.write(code)
    return f"Code saved to {filename}"

def save_code(input_text):
    if not input_text or not input_text.strip():
        return "❌ No code provided"

    os.makedirs("generated", exist_ok=True)
    filename = f"generated/generated_{int(time.time())}.py"

    return save_code_to_file(input_text, filename)

def explain(input_text):
    try:
        data = json.loads(input_text)

        if isinstance(data, dict):
            formatted = "\n📘 Explanation:\n\n"

            for key, value in data.items():
                formatted += f"🔹 {key.capitalize()}:\n"

                if isinstance(value, list):
                    for item in value:
                        formatted += f"- {item}\n"
                else:
                    formatted += f"{value}\n"

                formatted += "\n"

            return formatted

        return f"\n📘 Explanation:\n{input_text}"

    except Exception:
        return f"\n📘 Explanation:\n{input_text}"

def debug(input_text):
    if not input_text:
        return "❌ No debug info provided"
    return f"\n🐞 Debug Info:\n{input_text}"