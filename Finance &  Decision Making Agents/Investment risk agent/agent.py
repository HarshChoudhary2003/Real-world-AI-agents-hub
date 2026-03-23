import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are an Investment Risk Agent (RiskVault AI).

Rules:
- Identify and meticulously assess investment risks (Market, Tech, Financial, Operative)
- Evaluate likelihood (1-10) and impact (Low/Med/High) with clear rationale
- Be neutral, analytical, and highly realistic; simulate a professional VC risk committee
- Provide an 'Overall Risk Profile' (e.g., Aggressive, Balanced, Conservative) with a weighted risk score
- Do NOT provide definitive investment advice or financial recommendations

Return ONLY valid JSON with this schema:

{
  "risk_score": "Weighted score out of 100",
  "risk_profile": "Overall Risk Profile category",
  "risks": [
    {
      "risk": "Name of the risk",
      "likelihood": "1-10",
      "impact": "Low/Med/High",
      "category": "E.g., Market, Tech, Legal",
      "mitigation_potential": "Ease of solving this risk",
      "notes": "Detailed analysis"
    }
  ],
  "overall_summary": "Comprehensive risk summary for stakeholders"
}
"""

def extract_json(response_content):
    """Attempts to robustly parse JSON out of an LLM response."""
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", str(response_content))
        if match:
            try:
                return json.loads(match.group(1).strip())
            except:
                pass
        match = re.search(r"\{[\s\S]*\}", str(response_content))
        if match:
            try:
                return json.loads(match.group(0).strip())
            except:
                pass
    raise ValueError("Failed to extract valid JSON from the model's response.")

def assess_risk(text, model_name="gpt-4o"):
    """Evaluates investment risks using multi-model intelligence via LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3
    }
    
    if "gpt-" in model_name or "o1-" in model_name:
        kwargs["response_format"] = {"type": "json_object"}
    
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    with open("investment_risk.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("investment_risk.txt", "w", encoding="utf-8") as f:
        f.write(f"INVESTMENT RISK ASSESSMENT REPORT ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"📊 OVERALL RISK PROFILE: {data.get('risk_profile', 'N/A')}\n")
        f.write(f"Weighted Risk Score: {data.get('risk_score', 'N/A')}/100\n\n")
        
        f.write("🏷️ RISK REGISTRY\n")
        for r in data.get("risks", []):
            f.write(f"[{r.get('category', 'General')}] {r.get('risk')}\n")
            f.write(f"Likelihood: {r.get('likelihood')}/10 | Impact: {r.get('impact')}\n")
            f.write(f"Mitigation: {r.get('mitigation_potential')}\n")
            f.write(f"Notes: {r.get('notes')}\n\n")
            
        f.write("\n📝 EXECUTIVE SUMMARY\n" + data.get("overall_summary", "N/A") + "\n")

if __name__ == "__main__":
    with open("investment_input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    if input_text:
        assessment = assess_risk(input_text)
        save_outputs(assessment)
        print("Investment risk assessment completed successfully.")
