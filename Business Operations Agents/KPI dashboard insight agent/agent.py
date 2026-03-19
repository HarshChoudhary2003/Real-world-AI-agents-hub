import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly sophisticated, multi-dimensional KPI Dashboard Insight Agent (InsightCore AI).
 
Rules:
- Interpret raw KPIs within the provided business context
- Deconstruct performance into meaningful trends, anomalies, and underlying causality
- Explicitly look for correlations: e.g., how an increase in support tickets might correlate with recent product updates
- Identify "Silent Risks": things that look okay but might indicate future friction
- Identify "Untapped Growth Levers": based on current momentum
- Maintain a balanced, high-impact executive tone
 
Return ONLY valid JSON with this schema. No markdown wrapping:
 
{
  "executive_summary": "High-level strategic takeaway (1-2 sentences)",
  "detailed_analysis": "Deep dive into the narrative behind the numbers",
  "key_trends": ["List of identified directional signals"],
  "causality_mapping": ["Explanations of WHY certain metrics moved based on context"],
  "risks": ["Potential negative outcomes or early warning signs"],
  "opportunities": ["Growth levers or areas for optimization"],
  "focus_areas": ["Critical areas requiring management attention for the next 30 days"]
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
    """Generates advanced insights using LiteLLM."""
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
 
        f.write(f"Executive Summary: {data.get('executive_summary', 'N/A')}\n\n")
        
        f.write("Deep Analysis:\n")
        f.write(data.get("detailed_analysis", "N/A") + "\n\n")
 
        f.write("Key Trends:\n")
        for t in data.get("key_trends", []):
            f.write(f"- {t}\n")
            
        f.write("\nCausality Mapping:\n")
        for c in data.get("causality_mapping", []):
            f.write(f"- {c}\n")
 
        f.write("\nStrategic Risks:\n")
        for r in data.get("risks", []):
            f.write(f"- {r}\n")
 
        f.write("\nGrowth Opportunities:\n")
        for o in data.get("opportunities", []):
            f.write(f"- {o}\n")
 
        f.write("\nFocus Areas (30d):\n")
        for f_area in data.get("focus_areas", []):
            f.write(f"- {f_area}\n")
 
def main():
    prompt_text = read_input()
    insights = generate_insights(prompt_text)
    save_outputs(insights)
    print("KPI dashboard insights generated successfully.")
 
if __name__ == "__main__":
    main()
