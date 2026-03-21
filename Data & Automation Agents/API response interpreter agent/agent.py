import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class API Diagnostic & Systems Architect (API-Insight AI v2.0).

Mission: Perform deep forensic analysis on raw API responses. Translate cryptic payloads and status codes into actionable developer intelligence.

Rules for Interpretation:
1. **Developer-Facing Logic**: Explain the response for a mid-level engineer (not just a basic summary).
2. **Payload Mapping**: Identify critical data nodes and their structural significance.
3. **Forensic Error Analysis**: Identify the precise root cause of failures (protocol, schema, auth, or logic).
4. **Actionable Remediation**: Suggest surgical fixes (retry strategy, payload correction, or header updates).

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "audit_report": {
     "http_status_intent": "Interpretation of the status code (e.g., Client Side Fault)",
     "severity": "Low/Medium/High/Critical",
     "brief_executive_summary": "1-sentence gist"
  },
  "payload_nodes": [
     {"field": "...", "intent": "Description", "value_type": "...", "status": "Valid/Empty/Error"}
  ],
  "root_cause_forensics": [
     {
       "error_code": "...",
       "mechanical_reason": "Technical why",
       "fix_blueprint": "How to resolve in code"
     }
  ],
  "security_observations": ["Is PII exposed? Vulnerable stack trace?"],
  "ops_next_actions": ["Strategic steps for the system architects"]
}
"""

def read_response(path="response.json"):
    """Reads raw API response from a local JSON file."""
    if not os.path.exists(path):
        return '{"status": 200, "msg": "API is healthy"}'
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_json(response_content):
    """Robustly parse JSON out of an LLM response."""
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        # Try stripping markdown blocks
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", str(response_content))
        if match:
            try:
                return json.loads(match.group(1).strip())
            except:
                pass
        
        # Try finding anything between braces
        match = re.search(r"\{[\s\S]*\}", str(response_content))
        if match:
            try:
                return json.loads(match.group(0).strip())
            except:
                pass
    raise ValueError("Failed to extract valid JSON from the model's response.")

def interpret_api_response(raw_text, model_name="gpt-4o-mini", api_key=None):
    """Interprets raw API response using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text}
        ],
        "temperature": 0.2
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the API interpretation as JSON and formatted TXT."""
    with open("api_interpretation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("api_interpretation.txt", "w", encoding="utf-8") as f:
        f.write(f"API-Insight AI Forensic Report ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        ar = data.get('audit_report', {})
        f.write(f"Status Intent: {ar.get('http_status_intent')}\n")
        f.write(f"Severity: {ar.get('severity')}\n")
        f.write(f"Summary: {ar.get('brief_executive_summary')}\n\n")
        
        f.write("--- 🏗️ Payload Node Mapping ---\n")
        for node in data.get('payload_nodes', []):
            f.write(f"[{node.get('status')}] {node.get('field')} ({node.get('value_type')}): {node.get('intent')}\n")
        
        f.write("\n--- 🚨 Error Forensics & Remediation ---\n")
        for err in data.get('root_cause_forensics', []):
            f.write(f"Issue: {err.get('error_code')} - {err.get('mechanical_reason')}\n")
            f.write(f"Blueprint Fix: {err.get('fix_blueprint')}\n\n")

        f.write("--- 🛡️ Security Posture ---\n")
        for signal in data.get("security_observations", []):
            f.write(f"- {signal}\n")
        
        f.write("\n--- ⚡ Developer Next Actions ---\n")
        for action in data.get("ops_next_actions", []):
            f.write(f"▶ {action}\n")

def main():
    print("🚀 API-Insight AI: Interpreting Payload Integrity...")
    raw_text = read_response()
    try:
        interpretation = interpret_api_response(raw_text)
        save_outputs(interpretation)
        print("✅ API response forensic audit completed successfully.")
        print("📁 Outputs: api_interpretation.json, api_interpretation.txt")
    except Exception as e:
        print(f"❌ Diagnostic failure: {str(e)}")

if __name__ == "__main__":
    main()
