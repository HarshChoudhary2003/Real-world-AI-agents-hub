import json
import os
import litellm
import traceback
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are an Enterprise Audit Preparation Agent.

Rules:
- Assess strict audit readiness based on the input payload (e.g., SOC 2, ISO 27001).
- Identify distinct gaps and pinpoint missing operational evidence.
- Prioritize risks based on past findings.
- Recommend strictly actionable, compliance-oriented remediation steps.
- Maintain a cold, professional, objective auditing tone.

Return ONLY valid JSON with this exact schema:
{
  "readiness_summary": "High-level realistic overview of current state",
  "evidence_checklist": ["Required Log 1", "Required Document 2"],
  "identified_gaps": ["Critical Gap 1", "Warning 1"],
  "remediation_actions": ["Specific Fix 1", "Specific Fix 2"]
}
"""

def read_input(path: str = "audit_input.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Audit Type: SOC 2\nScope: Data security and access controls\nPast Findings:\n- Incomplete access review documentation\n- Delayed incident response reporting")
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

def prepare_audit(text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Audit Readiness Telemetry via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Audit Context:\n{text}"}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("audit_readiness.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("audit_readiness.txt", "w", encoding="utf-8") as f:
        f.write(f"Corporate Audit Readiness Matrix ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        
        f.write("--- READINESS SUMMARY ---\n")
        f.write(data.get("readiness_summary", "No summary extracted.") + "\n\n")
        
        f.write("--- REQUIRED EVIDENCE CHECKLIST ---\n")
        for e in data.get("evidence_checklist", []):
            f.write(f"[ ] {e}\n")
            
        f.write("\n--- IDENTIFIED DELTAS & GAPS ---\n")
        for g in data.get("identified_gaps", []):
            f.write(f"! {g}\n")
            
        f.write("\n--- REMEDIATION DIRECTIVES ---\n")
        for r in data.get("remediation_actions", []):
            f.write(f"-> {r}\n")

def main():
    print("🚀 Audit Preparation Agent: Initiating Regulatory Sweep...")
    try:
        input_text = read_input()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        readiness = prepare_audit(input_text, model=model)
        save_outputs(readiness)
        
        print("✅ Audit preparation telemetry compiled successfully.")
        print("📁 Outputs: audit_readiness.json, audit_readiness.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
