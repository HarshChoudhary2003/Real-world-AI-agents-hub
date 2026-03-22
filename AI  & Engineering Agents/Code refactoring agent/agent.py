import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Code Refactoring Agent.

Rules:
- Improve readability and structure
- Preserve behavior exactly
- Follow Python best practices
- Explain changes clearly

Return ONLY valid JSON with this schema:
{
  "refactored_code": "string with the new python code",
  "changes_summary": ["string change 1", "string change 2"],
  "behavior_preserved": true
}
"""

def read_code(path="original_code.py"):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("def calc(a, b):\n    x = a * b\n    y = a * b\n    return x + y\n")
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

def refactor_code(code_text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Orchestrating Code Refactoring via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": code_text}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("refactored_code.py", "w", encoding="utf-8") as f:
        f.write(data.get("refactored_code", ""))

    report = {
        "date": str(date.today()),
        "changes_summary": data.get("changes_summary", []),
        "behavior_preserved": data.get("behavior_preserved", False)
    }

    with open("refactoring_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    with open("refactoring_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Refactoring Report ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Behavior Preserved: {report['behavior_preserved']}\n\n")
        f.write("Changes Summary:\n")
        for change in report["changes_summary"]:
            f.write(f"- {change}\n")

def main():
    print("🚀 Code Refactoring Agent: Initiating process...")
    try:
        code_text = read_code()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        result = refactor_code(code_text, model=model)
        save_outputs(result)
        print("✅ Code refactoring completed successfully.")
        print("📁 Outputs: refactored_code.py, refactoring_report.json, refactoring_report.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
