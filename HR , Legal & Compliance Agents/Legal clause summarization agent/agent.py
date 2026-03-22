import json
import os
import litellm
import traceback
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Legal Clause Summarization Agent.

Rules:
- Summarize legal clauses clearly into everyday professional language.
- Preserve the exact original contractual meaning.
- Highlight crucial obligations and risks/conditions.
- Avoid providing formal legal advice (state a disclaimer if necessary).

Return ONLY valid JSON with this exact schema:
{
  "summary": "Clear, plain-English translation of the provision",
  "key_obligations": ["Obligation 1", "Obligation 2"],
  "risks_or_conditions": ["Risk factor 1", "Limitation/Condition 1"]
}
"""

def read_clause(path: str = "clause.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("The Company shall not be liable for any indirect, incidental, special, or consequential damages arising out of or related to the use of the Service, even if advised of the possibility of such damages.")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_json(content_raw: str) -> dict:
    content = str(content_raw)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        start_idx = int(content.find("{"))
        end_idx = int(content.rfind("}")) + 1
        content_str = str(content)
        content = content_str[start_idx:end_idx]
    return json.loads(content)

def summarize_clause(text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Legal Clause Summary Matrix via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Legal Clause:\n{text}"}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("legal_summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("legal_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Legal Clause Summary Record ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        
        f.write("--- EXECUTIVE SUMMARY ---\n")
        f.write(data.get("summary", "No summary provided.") + "\n\n")
        
        obs = data.get("key_obligations", [])
        f.write("--- KEY OBLIGATIONS ---\n")
        if obs:
            for o in obs:
                f.write(f"- {o}\n")
        else:
            f.write("None strictly defined by this clause.\n")
            
        f.write("\n--- RISKS / CONDITIONS ---\n")
        risks = data.get("risks_or_conditions", [])
        if risks:
            for r in risks:
                f.write(f"- {r}\n")
        else:
            f.write("No explicit conditional risks identified.\n")

def main():
    print("🚀 Legal Clause Summarization Agent: Initiating Linguistics Core...")
    try:
        clause_text = read_clause()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        summary = summarize_clause(clause_text, model=model)
        save_outputs(summary)
        
        print("✅ Legal clause summarized successfully.")
        print("📁 Outputs: legal_summary.json, legal_summary.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
