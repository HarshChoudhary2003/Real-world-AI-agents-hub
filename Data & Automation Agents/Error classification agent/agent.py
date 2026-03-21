import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Reliability Engineer & Systems Forensic Architect (Error-Forensics AI v2.0).

Mission: Perform deep linguistic and logical analysis on system errors to identify root causes, calculate impact severity, and architect surgical code-level remediations.

Rules for Classification:
1. **Multi-Vector Auditing**: Classify the error across three vectors: Category (Network, Schema, Auth, Logic), Severity (Critical, High, Moderate, Low), and Impact (End-User vs. Backend).
2. **Technical Forensic**: Explain the "Mechanical Reason" for the error (e.g., protocol timeout, deadlocks, circular deps).
3. **Actionable Remediation**: Provide both an "Immediate Fix" (patch) and a "Structural Fix" (long-term resilience).
4. **Resilience Advice**: Suggest monitoring strategies to detect or prevent this specific error in the future.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "audit_report": {
     "severity": "Critical/High/Moderate/Low",
     "primary_category": "Network/Database/Auth/Logic",
     "logical_gist": "Short executive summary"
  },
  "forensic_breakdown": {
     "root_cause_explanation": "Technical why an error occurred",
     "impact_assessment": "How this affects users/upstream services",
     "recognized_patterns": ["List of repeating incident signatures"]
  },
  "surgical_remediation": [
     {"action": "...", "remediation_blueprint": "Step-by-step fix guide"}
  ],
  "monitoring_guidelines": ["How to detect this error in systems like Datadog or Sentry"],
  "sre_expert_tips": ["Strategic advice for reliability teams"]
}
"""

def read_error_data(path="error.txt"):
    """Reads raw error message from a local text file."""
    if not os.path.exists(path):
        return "GenericError: Unknown incident"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_json(response_content):
    """Robustly parse JSON out of an LLM response."""
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", str(response_content))
        if match:
            try: return json.loads(match.group(1).strip())
            except: pass
        match = re.search(r"\{[\s\S]*\}", str(response_content))
        if match:
            try: return json.loads(match.group(0).strip())
            except: pass
    raise ValueError("Linguistic forensic extraction failed.")

def classify_error_signals(error_text, model_name="gpt-4o-mini", api_key=None):
    """Performs neural classification of the error using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": error_text}
        ],
        "temperature": 0.2
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the error classification as JSON and formatted TXT."""
    with open("error_classification.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("error_classification.txt", "w", encoding="utf-8") as f:
        f.write(f"Error-Forensics AI: Incident Diagnosis Report ({date.today()})\n")
        f.write("=" * 65 + "\n\n")

        ar = data.get('audit_report', {})
        f.write(f"Severity: {ar.get('severity')}\n")
        f.write(f"Category: {ar.get('primary_category')}\n")
        f.write(f"Audit: {ar.get('logical_gist')}\n\n")
        
        fb = data.get('forensic_breakdown', {})
        f.write("--- 🚑 FORENSIC DEEP-DIVE ---\n")
        f.write(f"Root Cause: {fb.get('root_cause_explanation')}\n")
        f.write(f"Impact: {fb.get('impact_assessment')}\n\n")
        
        f.write("--- 🛡️ SURGICAL REMEDIATION ---\n")
        for fix in data.get('surgical_remediation', []):
            f.write(f"▶ {fix.get('action')}\n")
            f.write(f"  Guide: {fix.get('remediation_blueprint')}\n\n")

        f.write("--- ⚡ LOGGING & MONITORING ---\n")
        for tip in data.get("monitoring_guidelines", []):
            f.write(f"• {tip}\n")

def main():
    print("🚀 Error-Forensics AI: Diagnosing Incident Criticality...")
    error_text = read_error_data()
    try:
        report = classify_error_signals(error_text)
        save_outputs(report)
        print("✅ Error classification completed successfully.")
        print("📁 Outputs: error_classification.json, error_classification.txt")
    except Exception as e:
        print(f"❌ Diagnostic failure: {str(e)}")

if __name__ == "__main__":
    main()
