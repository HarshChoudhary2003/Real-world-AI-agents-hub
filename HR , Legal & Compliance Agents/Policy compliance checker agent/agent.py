import json
import os
import litellm
import traceback
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Policy Compliance Checker Agent.

Rules:
- Evaluate the provided content strictly against the provided policy rules.
- Identify violations directly tied to explicit policies.
- Classify the severity of each violation (e.g., Low, Medium, High, Critical).
- Explain findings transparently and impartially.
- If completely compliant, clearly state that.

Return ONLY valid JSON with this exact schema:
{
  "compliance_status": "Compliant, Partial, or Non-Compliant",
  "violations": [
    {
      "rule": "The specific policy rule that was violated",
      "severity": "Low, Medium, High, Critical",
      "explanation": "Why this content violates the rule"
    }
  ],
  "guidance": ["Steps to remediate and achieve full compliance"]
}
"""

def read_file(path: str) -> str:
    if not os.path.exists(path):
        return ""
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

def check_compliance(policy_text: str, content_text: str, model: str = "gpt-4o") -> dict:
    prompt = f"Policy Elements:\n{policy_text}\n\nContent to Audit:\n{content_text}\n"
    print(f"📡 Auditing Compliance against Policy via {model}...")
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
    with open("compliance_report.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("compliance_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Policy Compliance Audit Report ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        
        status = data.get("compliance_status", "N/A")
        f.write(f"Compliance Status: {status}\n\n")
        
        violations = data.get("violations", [])
        if violations:
            f.write("--- VIOLATIONS & INFRACTIONS ---\n")
            for idx, v in enumerate(violations, 1):
                f.write(f"{idx}. Rule: {v.get('rule')}\n")
                f.write(f"   Severity: {v.get('severity')}\n")
                f.write(f"   Issue Log: {v.get('explanation')}\n\n")
        else:
            f.write("--- VIOLATIONS & INFRACTIONS ---\nNone detected.\n\n")
            
        f.write("--- REMEDIATION GUIDANCE ---\n")
        for g in data.get("guidance", []):
            f.write(f"- {g}\n")

def main():
    print("🚀 Policy Compliance Checker Agent: Initiating Audit Protocol...")
    try:
        policy_text = read_file("policy.txt")
        content_text = read_file("content.txt")
        
        if not policy_text or not content_text:
            print("❌ Error: Missing policy.txt or content.txt - Both are required.")
            return

        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        report = check_compliance(policy_text, content_text, model=model)
        save_outputs(report)
        
        print("✅ Policy compliance audit completed successfully.")
        print("📁 Outputs: compliance_report.json, compliance_report.txt")
    except Exception as e:
        print(f"❌ Critical Validation Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
