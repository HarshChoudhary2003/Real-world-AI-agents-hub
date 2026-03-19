import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly sophisticated Campaign Strategic Intelligence Engine (AdIntel AI v2.0).
 
Rules:
- Perform deep-dive attribution analysis (First-click, Last-click, and Multi-touch simulations)
- Calculate Spend Velocity: project end-of-month spend and conversion volume based on current run-rate
- Identity anomalies in the data (e.g., high CTR but low conversion may indicate landing page friction)
- Provide a "Creative Fatigue Index" if ad duration or creative metrics are provided
- Audit budget allocation: suggest rebalancing between high-performing and low-performing segments
- Maintain an objective, high-stakes diagnostic tone
 
Return ONLY valid JSON with this schema. No markdown wrapping:
 
{
  "executive_summary": "Diagnostic brief (1-2 sentences)",
  "efficiency_score": 0-100,
  "spend_velocity": {
    "projected_eom_spend": "$Amt",
    "projected_eom_conversions": 0,
    "pacing_status": "Over-pacing / Under-pacing / On-track"
  },
  "attribution_insights": [
    {
      "model": "Model Name",
      "interpretation": "How performance looks under this lens"
    }
  ],
  "anomaly_detection": [
    {
      "metric": "e.g., CVR",
      "observation": "What is unusual",
      "root_cause_hypothesis": "The most likely reason why"
    }
  ],
  "leaky_bucket_audit": ["Critical budget leaks"],
  "rebalancing_suggestions": ["Where to move funds for max ROI"],
  "benchmark_analysis": "Contextual comparison to industry norms"
}
"""
 
def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def extract_json(response_content):
    """Attempts to robustly parse JSON out of an LLM response."""
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

def analyze_campaign_advanced(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates advanced strategic intelligence audit using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.3
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)
 
def save_outputs_advanced(data):
    with open("campaign_analysis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("campaign_analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"Advanced Strategic Performance Intelligence ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
 
        f.write(f"Executive Summary: {data.get('executive_summary', 'N/A')}\n")
        f.write(f"Efficiency Score: {data.get('efficiency_score', 'N/A')}/100\n\n")
 
        v = data.get('spend_velocity', {})
        f.write(f"Spend Pacing & Forecasting:\n")
        f.write(f"- Status: {v.get('pacing_status')}\n")
        f.write(f"- Projected EOM Spend: {v.get('projected_eom_spend')}\n")
        f.write(f"- Projected EOM Conversions: {v.get('projected_eom_conversions')}\n\n")
 
        f.write("Anomaly & Root Cause Analysis:\n")
        for a in data.get("anomaly_detection", []):
            f.write(f"- {a.get('metric')}: {a.get('observation')} (Hypothesis: {a.get('root_cause_hypothesis')})\n")
 
        f.write("\nBudget Rebalancing Suggestions:\n")
        for r in data.get("rebalancing_suggestions", []):
            f.write(f"- {r}\n")
            
        f.write("\nLeaky Bucket Audit:\n")
        for l in data.get("leaky_bucket_audit", []):
            f.write(f"- {l}\n")
 
def main():
    prompt_text = read_input()
    analysis = analyze_campaign_advanced(prompt_text)
    save_outputs_advanced(analysis)
    print("Strategic intelligence audit v2.0 finalized.")
 
if __name__ == "__main__":
    main()
