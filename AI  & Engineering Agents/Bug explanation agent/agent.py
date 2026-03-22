import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Bug Explanation Agent.

Rules:
- Explain bugs clearly
- Identify root cause
- Reference code where relevant
- Do NOT provide a full fix

Return ONLY valid JSON with this schema:
{
  "explanation": "Clear explanation of the error",
  "root_cause": "The specific reason it failed",
  "affected_code": ["code lines or components affected"],
  "debugging_focus": ["where to look next or what to check"]
}
"""

def read_file(path: str) -> str:
    if not os.path.exists(path):
        if "error.txt" in path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("TypeError: unsupported operand type(s) for +: 'int' and 'str'\n")
        elif "code_snippet.py" in path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("def add_values(a, b):\n    return a + b\n\nresult = add_values(5, \"10\")\n")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_json(content_raw: str) -> dict:
    content = str(content_raw)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        start_idx = content.find("{")
        end_idx = content.rfind("}") + 1
        content = content[start_idx:end_idx]
    return json.loads(content)

def explain_bug(error_text: str, code_text: str, model: str = "gpt-4o") -> dict:
    prompt = f"Error:\n{error_text}\n\nCode:\n{code_text}"
    print(f"📡 Analyzing Bug via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("bug_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("bug_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"Bug Explanation ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write("Explanation:\n")
        f.write(data.get("explanation", "N/A") + "\n\n")
        f.write("Root Cause:\n")
        f.write(data.get("root_cause", "N/A") + "\n\n")
        
        affected = data.get("affected_code", [])
        if affected:
            f.write("Affected Code Areas:\n")
            for a in affected:
                f.write(f"- {a}\n")
                
        focus = data.get("debugging_focus", [])
        if focus:
            f.write("\nDebugging Focus:\n")
            for d in focus:
                f.write(f"- {d}\n")

def main():
    print("🚀 Bug Explanation Agent: Initiating process...")
    try:
        error_text = read_file("error.txt")
        code_text = read_file("code_snippet.py")
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        explanation = explain_bug(error_text, code_text, model=model)
        save_outputs(explanation)
        
        print("✅ Bug explanation generated successfully.")
        print("📁 Outputs: bug_explanation.json, bug_explanation.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
