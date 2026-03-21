import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Prompt Optimization Agent.

Rules:
- Improve clarity and intent
- Add structure and constraints
- Avoid unnecessary verbosity
- Do NOT change task intent

Return ONLY valid JSON with this schema:

{
  "optimized_prompt": "",
  "improvements": [],
  "usage_notes": []
}
"""

def read_prompt(path="input_prompt.txt"):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Analyze market trends for AI agents.")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def optimize_prompt(prompt_text, model_name="gpt-4o-mini"):
    print(f"📡 Dispatching to model: {model_name}...")
    response = litellm.completion(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.3
    )
    # Handle potential markdown wrapping in response
    content = response.choices[0].message.content
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]
        
    return json.loads(content)

def save_outputs(data):
    with open("optimized_prompt.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("optimized_prompt.txt", "w", encoding="utf-8") as f:
        f.write(f"Optimized Prompt ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write("Optimized Prompt:\n")
        f.write(data["optimized_prompt"] + "\n\n")
        f.write("Improvements:\n")
        for i in data["improvements"]:
            f.write(f"- {i}\n")
        if data["usage_notes"]:
            f.write("\nUsage Notes:\n")
            for u in data["usage_notes"]:
                f.write(f"- {u}\n")

def main():
    print("🚀 PromptForge AI CLI: Refining your intent...")
    try:
        prompt_text = read_prompt()
        # Default to gpt-4o-mini, but litellm allows any model via env vars
        model_to_use = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
        optimized = optimize_prompt(prompt_text, model_name=model_to_use)
        save_outputs(optimized)
        print(f"✅ Prompt optimized successfully via {model_to_use}.")
        print("📁 Outputs: optimized_prompt.json, optimized_prompt.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
