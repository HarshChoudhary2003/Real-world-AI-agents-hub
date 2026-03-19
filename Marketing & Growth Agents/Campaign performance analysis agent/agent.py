import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a high-tier Campaign Intelligence Architect (AdIntel AI v3.0).
 
Rules:
- Perform deep-dive attribution analysis and Spend Velocity forecasting.
- Conduct a "Creative Performance Pivot": based on the metrics, suggest specific visual or copy shifts.
- Map "Strategic Next Actions" with urgency levels (Critical / High / Medium).
- Provide a "Market Context Matrix": compare these metrics against estimated industry benchmarks for the platform.
- Evaluate "Diminishing Returns": project at what spend level the CPA may start to climb.
- Maintain a highly sophisticated, tactical, and strategic growth tone.
 
Return ONLY valid JSON with this schema. No markdown wrapping:
 
{
  "executive_summary": "High-level strategic diagnostic",
  "efficiency_score": 0-100,
  "forecasting_projection": {
    "projected_eom_spend": "$Amt",
    "projected_eom_conversions": 0,
    "pacing_status": "Status"
  },
  "creative_pivot_roadmap": [
    {
      "dimension": "e.g., Creative Angle / Format",
      "current_state": "What is being used",
      "pivot_suggestion": "The suggested change",
      "rationale": "Why this will work"
    }
  ],
  "strategic_next_actions": [
    {
      "action": "Task description",
      "urgency": "Priority level",
      "expected_impact": "High/Medium/Low"
    }
  ],
  "diminishing_returns_audit": "An analysis of current scaling limits",
  "leaky_bucket_audit": ["Specific budget leakages"],
  "industry_benchmark_context": "Comparative performance mapping"
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

def analyze_campaign_v3(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates next-level strategic intelligence audit using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.4
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)
 
def save_outputs_v3(data):
    with open("campaign_analysis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("campaign_analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"Advanced Neural Growth Intelligence Audit ({date.today()})\n")
        f.write("=" * 70 + "\n\n")
 
        f.write(f"Executive Summary: {data.get('executive_summary', 'N/A')}\n")
        f.write(f"Efficiency Score: {data.get('efficiency_score', 'N/A')}/100\n\n")
 
        v = data.get('forecasting_projection', {})
        f.write(f"Neural Forecasting Matrix:\n")
        f.write(f"- Pacing: {v.get('pacing_status')}\n")
        f.write(f"- Projected EOM Spend: {v.get('projected_eom_spend')}\n")
        f.write(f"- Projected EOM Conversions: {v.get('projected_eom_conversions')}\n\n")
 
        f.write("Creative Pivot Roadmap:\n")
        for cp in data.get("creative_pivot_roadmap", []):
            f.write(f"- {cp.get('dimension')}: {cp.get('pivot_suggestion')} (Why: {cp.get('rationale')})\n")
 
        f.write("\nStrategic Next Actions:\n")
        for sa in data.get("strategic_next_actions", []):
            f.write(f"- [{sa.get('urgency')}] {sa.get('action')} (Impact: {sa.get('expected_impact')})\n")
            
        f.write(f"\nScaling & Diminishing Returns Audit:\n{data.get('diminishing_returns_audit', 'N/A')}\n\n")
        f.write(f"Leaky Bucket Audit: {', '.join(data.get('leaky_bucket_audit', []))}\n")
 
def main():
    prompt_text = read_input()
    analysis = analyze_campaign_v3(prompt_text)
    save_outputs_v3(analysis)
    print("Next-generation intelligence audit v3.0 finalized.")
 
if __name__ == "__main__":
    main()
