import json
import re
import os
from datetime import date
from collections import Counter
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Systems Reliability & Cyber-Forensics Architect (Log-Sentinel AI v2.0).

Mission: Perform deep heuristic analysis on system logs to detect anomalies, security threats, and performance regressions.

Rules for Detection & Diagnostic:
1. **Anomaly Identification**: Detect unusual patterns, frequency spikes, or unique error signatures.
2. **Impact Calibration**: Assess the severity of incidents (Critical, High, Moderate, Low) in the context of system health.
3. **Forensic Narrative**: Connect isolated log events into a meaningful investigative story.
4. **Actionable SRE Support**: Suggest surgical investigation paths for Dev-Ops/SRE teams.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "sentinel_assessment": {
     "health_index": "0-100",
     "verdict": "Critical/Moderate/Stable",
     "diagnostic_overview": "A brief technical summary"
  },
  "detected_incidents": [
     {
       "event_type": "ERROR/WARNING/INFO",
       "signature": "Common phrase or log segment",
       "frequency": "Calculated or noted count",
       "technical_impact": "How it strains the system or architecture"
     }
  ],
  "structural_patterns": ["List of normal or abnormal repeating sequences identified"],
  "sre_blueprint": ["Strategic steps for the response team"],
  "security_alerts": ["Identification of potential intrusion or leakage patterns"]
}
"""

def read_logs(path="logs.txt"):
    """Reads raw log lines from a local text file."""
    if not os.path.exists(path):
        return ["2024-06-01 10:00 INFO System Warmup"]
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

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

def analyze_log_anomalies(log_text, model_name="gpt-4o-mini", api_key=None):
    """Deep analysis of log signals using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"LOG DATA:\n{log_text}"}
        ],
        "temperature": 0.2
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the log audit as JSON and formatted TXT."""
    with open("log_anomalies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("log_anomalies.txt", "w", encoding="utf-8") as f:
        f.write(f"Log-Sentinel AI: Forensic Health Audit ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        sa = data.get('sentinel_assessment', {})
        f.write(f"Health Index: {sa.get('health_index')}/100\n")
        f.write(f"Verdict: {sa.get('verdict')}\n")
        f.write(f"Audit: {sa.get('diagnostic_overview')}\n\n")
        
        f.write("--- 🚑 Detected Incidents ---\n")
        for incident in data.get('detected_incidents', []):
            f.write(f"[{incident.get('event_type')}] {incident.get('signature')} ({incident.get('frequency')}x)\n")
            f.write(f"Impact: {incident.get('technical_impact')}\n\n")
        
        f.write("--- 🔍 SRE Response Blueprint ---\n")
        for step in data.get('sre_blueprint', []):
            f.write(f"▶ {step}\n")

        if data.get("security_alerts"):
            f.write("\n--- 🔒 Security Threat Map ---\n")
            for alert in data.get("security_alerts", []):
                f.write(f"⚠️ {alert}\n")

def main():
    print("🚀 Log-Sentinel AI: Scoping System Telemetry...")
    logs = read_logs()
    log_text = "".join(logs)
    
    try:
        report = analyze_log_anomalies(log_text)
        save_outputs(report)
        print("✅ Log anomaly forensic report completed successfully.")
        print("📁 Outputs: log_anomalies.json, log_anomalies.txt")
    except Exception as e:
        print(f"❌ Telemetry Audit failed: {str(e)}")

if __name__ == "__main__":
    main()
