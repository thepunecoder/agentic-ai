import json
import re

def parse_llm_response(response_text: str) -> dict:
    """
    Robust parser for LLM responses
    """

    # 🔥 Clean markdown
    response_text = response_text.replace("```", "").strip()

    # 🔥 Extract JSON block
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    json_text = match.group() if match else response_text

    try:
        # Try direct parsing
        return json.loads(json_text)

    except Exception:
        print("⚠️ JSON parsing failed, applying fallback...")

        parsed = {}

        # 🔥 Extract tool
        tool_match = re.search(r'"tool"\s*:\s*"([^"]+)"', json_text)

        # 🔥 Extract input (multiline safe)
        input_match = re.search(r'"input"\s*:\s*"(.*)"\s*}', json_text, re.DOTALL)

        parsed["tool"] = tool_match.group(1) if tool_match else None

        raw_input = input_match.group(1).strip() if input_match else ""

        # 🔥 Clean "python" prefix
        if raw_input.startswith("python"):
            raw_input = raw_input.replace("python", "", 1).strip()

        parsed["input"] = raw_input.encode().decode("unicode_escape")

        print("\n🛠️ Fallback Parsed:\n", parsed)

        return parsed