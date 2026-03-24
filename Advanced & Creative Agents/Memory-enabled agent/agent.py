import json
import os
from openai import OpenAI
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY
base_path = os.path.dirname(__file__)
MEMORY_FILE = os.path.join(base_path, "memory.json")

SYSTEM_PROMPT = """
You are a Memory-Enabled Agent.

Rules:
- Use stored memory when relevant to provide personalized responses.
- Update memory selectively with new facts or interaction summaries.
- DO NOT store sensitive personal data (passwords, PII, etc.).
- Be concise and efficient.

Return ONLY valid JSON with this schema:

{
  "response": "",
  "memory_used": [],
  "memory_updates": []
}
"""

def load_memory():
    """Loads the neural memory store."""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"facts": [], "interactions": []}

def save_memory(memory):
    """Persists the updated neural memory."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def main():
    print("Engaging Neural Memory Module...")
    memory = load_memory()

    input_path = os.path.join(base_path, "input.txt")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            user_input = f.read()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Neural Memory Context: {json.dumps(memory)}\n\nUser Input: {user_input}"}
        ],
        response_format={ "type": "json_object" },
        temperature=0.3
    )

    result = json.loads(response.choices[0].message.content)

    # Core Memory Update Logic
    if result.get("memory_updates"):
        memory["interactions"].extend(result["memory_updates"])
        # Keep only last 20 interactions for efficiency
        memory["interactions"] = memory["interactions"][-20:]
        save_memory(memory)

    output_path = os.path.join(base_path, "output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("Memory-enabled interaction completed successfully. Context updated.")

if __name__ == "__main__":
    main()
