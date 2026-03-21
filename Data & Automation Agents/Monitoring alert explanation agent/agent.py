import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class SRE Observability Expert & Neural Alert Interpreter (Alert-Insight AI v2.0).

Mission: Translate cryptic system alerts from Datadog, Prometheus, Sentry, or CloudWatch into plain-English root causes and remediation blueprints.

Rules for Interpretation:
1. **Plain-English Translation**: Convert technical tags (env:prod, service:X) and threshold values into a concise, readable summary.
2. **Root Cause Heuristic**: Identify the most likely mechanical cause inferred from logs or error symbols (e.g., Handshake -> TLS/Network).
3. **Surgical Remediation**: Architect a step-by-step fix guide for the responder (Immediate action vs. Structural fix).
4. **Resilience Strategy**: Suggest how to optimize the alert threshold to reduce noise or improve detection.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "alert_briefing": {
     "criticality": "Critical/Moderate/Info",
     "incident_title": "Short descriptive name",
     "executive_summary": "Plain English gist of the issue"
  },
  "diagnostic_deep_dive": {
     "likely_cause": "The core reason for the breach",
     "impacted_services": ["Affected services or regions"],
     "technical_explanation": "Technical depth on why the threshold was bypassed"
  },
  "remediation_roadmap": [
     {"action": "...", "strategy": "Detailed fix steps"}
  ],
  "alert_optimization": ["How to silence or fine-tune this monitor"],
  "sre_expert_tips": ["Strategic advice for observability teams"]
}
"""

def read_alert_data(path="alert.txt"):
    """Reads raw alert message from a local text file."""
    if not os.path.exists(path):
        return "Alert: Metric CPU > 90%"
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
    raise ValueError("Linguistic alert interpretation failed.")

def interpret_alert_signals(alert_text, model_name="gpt-4o-mini", api_key=None):
    """Performs neural interpretation of the alert signals using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": alert_text}
        ],
        "temperature": 0.2
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the alert interpretation as JSON and formatted TXT."""
    with open("alert_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("alert_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"Alert-Insight AI: Incident Briefing Report ({date.today()})\n")
        f.write("=" * 65 + "\n\n")

        ab = data.get('alert_briefing', {})
        f.write(f"Criticality: {ab.get('criticality')}\n")
        f.write(f"Title: {ab.get('incident_title')}\n")
        f.write(f"Summary: {ab.get('executive_summary')}\n\n")
        
        dd = data.get('diagnostic_deep_dive', {})
        f.write("--- 🚑 DIAGNOSTIC DEEP-DIVE ---\n")
        f.write(f"Likely Cause: {dd.get('likely_cause')}\n")
        f.write(f"Technical: {dd.get('technical_explanation')}\n\n")
        
        f.write("--- 🛡️ REMEDIATION ROADMAP ---\n")
        for fix in data.get('remediation_roadmap', []):
            f.write(f"▶ {fix.get('action')}\n")
            f.write(f"  Strategy: {fix.get('strategy')}\n\n")

        f.write("--- ⚡ MONITOR OPTIMIZATION ---\n")
        for tip in data.get("alert_optimization", []):
            f.write(f"• {tip}\n")

def main():
    print("🚀 Alert-Insight AI: Interpreting Monitoring Signals...")
    alert_text = read_alert_data()
    try:
        report = interpret_alert_signals(alert_text)
        save_outputs(report)
        print("✅ Alert interpretation completed successfully.")
        print("📁 Outputs: alert_explanation.json, alert_explanation.txt")
    except Exception as e:
        print(f"❌ Interpret fail: {str(e)}")

if __name__ == "__main__":
    main()
