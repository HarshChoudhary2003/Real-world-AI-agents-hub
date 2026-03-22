import json
import os
import litellm
import traceback
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Risk Assessment Agent.

Rules:
- Identify and critically assess operational, legal, or technical risks based on the scenario.
- Estimate 'likelihood' and 'impact' precisely.
- Suggest highly actionable, pragmatic mitigations.
- Be realistic and balanced—do not exaggerate trivial scenarios.

Return ONLY valid JSON with this exact schema:
{
  "risks": [
    {
      "risk": "Clear description of the identified risk",
      "likelihood": "Low, Medium, or High",
      "impact": "Low, Medium, High, or Critical",
      "risk_level": "Overall risk level (Low, Medium, High, Extreme)",
      "mitigation": "Targeted mitigation strategy to reduce this risk"
    }
  ]
}
"""

def read_scenario(path: str = "scenario.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Scenario: Launching a new customer data analytics feature\nDetails:\n- Collects user behavior data\n- Integrates with third-party analytics tools\n- Targets EU customers")
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

def assess_risk(text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Risk Assessment Matrix via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("risk_assessment.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("risk_assessment.txt", "w", encoding="utf-8") as f:
        f.write(f"Risk Assessment Report ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        
        risks = data.get("risks", [])
        if not risks:
            f.write("No major risks identified within the current operational scope.\n")
            return
            
        for i, r in enumerate(risks, 1):
            f.write(f"Risk {i}: {r.get('risk')}\n")
            f.write(f" - Likelihood: {r.get('likelihood')}\n")
            f.write(f" - Impact:     {r.get('impact')}\n")
            f.write(f" - Risk Level: {r.get('risk_level')}\n")
            f.write(f" - Mitigation: {r.get('mitigation')}\n\n")

def main():
    print("🚀 Risk Assessment Agent: Initiating Forensic Protocol...")
    try:
        scenario_text = read_scenario()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        assessment = assess_risk(scenario_text, model=model)
        save_outputs(assessment)
        
        print("✅ Risk assessment completed successfully.")
        print("📁 Outputs: risk_assessment.json, risk_assessment.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
