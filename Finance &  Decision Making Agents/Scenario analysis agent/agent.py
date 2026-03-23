import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Scenario Analysis Agent (SimuForge AI).

Rules:
- Generate highly plausible future scenarios based on input variables
- Compare outcomes clearly using specific metrics (Revenue, Profit, Risk)
- Highlight assumptions, strategic upsides, and defensive risks for each scenario
- Provide a summary of 'Durability' (how well the business withstands the worst case)
- Do NOT make definitive predictions or give financial advice

Return ONLY valid JSON with this schema:

{
  "analysis_overview": "High-level summary of the scenario landscape",
  "durable_score": "Rating out of 10 for business resilience",
  "scenarios": [
    {
      "name": "Scenario Name (e.g., Bear Case, Bull Case)",
      "assumptions": "Underlying conditions",
      "projected_revenue": "Estimated $ outcome",
      "margin_impact": "% change",
      "implications": "Strategic business meaning",
      "risk_level": "Low / Medium / High"
    }
  ],
  "strategic_advice": "High-level non-financial recommendation for general readiness",
  "key_variables_tracked": [
    "List of market or internal signals to monitor"
  ]
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

def analyze_scenarios(text, model_name="gpt-4o"):
    """Generates scenario analyses using multi-model intelligence via LiteLLM."""
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
    with open("scenario_analysis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("scenario_analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"SCENARIO ANALYSIS REPORT ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write("🔮 ANALYSIS OVERVIEW\n" + data.get("analysis_overview", "N/A") + "\n\n")
        f.write(f"Resilience Rating: {data.get('durable_score')} / 10\n\n")
        
        f.write("📊 FUTURE SCENARIOS\n")
        for s in data.get("scenarios", []):
            f.write(f"--- {s.get('name')} ---\n")
            f.write(f"Assumptions: {s.get('assumptions')}\n")
            f.write(f"Revenue: {s.get('projected_revenue')}\n")
            f.write(f"Margin: {s.get('margin_impact')}\n")
            f.write(f"Risk: {s.get('risk_level')}\n")
            f.write(f"Implications: {s.get('implications')}\n\n")
            
        f.write("\n🛡️ STRATEGIC READINESS\n" + data.get("strategic_advice", "N/A") + "\n\n")
        f.write("📡 MONITORING SIGNALS\n")
        for s in data.get("key_variables_tracked", []):
            f.write(f"- {s}\n")

if __name__ == "__main__":
    with open("scenario_input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    if input_text:
        analysis = analyze_scenarios(input_text)
        save_outputs(analysis)
        print("Scenario analysis completed successfully.")
