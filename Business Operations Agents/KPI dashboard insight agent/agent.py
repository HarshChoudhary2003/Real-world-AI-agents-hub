import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly sophisticated KPI Dashboard Insight Agent.
 
Rules:
- Interpret raw KPIs within the provided business context
- Deconstruct performance into meaningful trends and anomalies
- Distinguish between correlated events and causal signals
- Highlight risks and opportunities without prescribing prescriptive decisions
- Maintain a balanced, objective, and executive tone
 
Return ONLY valid JSON with this schema. No markdown wrapping, no extra text:
 
{
  "executive_summary": "High-level strategic takeaway",
  "key_trends": ["List of identified directional signals"],
  "risks": ["Potential negative outcomes identified from the data"],
  "opportunities": ["Positive areas for growth or optimization"],
  "focus_areas": ["Critical areas requiring management attention"]
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

def generate_insights(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates insights using LiteLLM."""
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
 
def save_outputs(data):
    with open("kpi_insights.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("kpi_insights.txt", "w", encoding="utf-8") as f:
        f.write(f"KPI Dashboard Insights ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
 
        f.write("Executive Summary:\n")
        f.write(data.get("executive_summary", "N/A") + "\n\n")
 
        f.write("Key Trends:\n")
        for t in data.get("key_trends", []):
            f.write(f"- {t}\n")
 
        if data.get("risks"):
            f.write("\nRisks:\n")
            for r in data["risks"]:
                f.write(f"- {r}\n")
 
        if data.get("opportunities"):
            f.write("\nOpportunities:\n")
            for o in data["opportunities"]:
                f.write(f"- {o}\n")
 
        if data.get("focus_areas"):
            f.write("\nFocus Areas:\n")
            for f_area in data["focus_areas"]:
                f.write(f"- {f_area}\n")
 
def main():
    prompt_text = read_input()
    insights = generate_insights(prompt_text)
    save_outputs(insights)
    print("KPI dashboard insights generated successfully.")
 
if __name__ == "__main__":
    main()
