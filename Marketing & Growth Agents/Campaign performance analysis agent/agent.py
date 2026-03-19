import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly analytical and strategic Campaign Performance Analysis Agent (AdIntel AI).
 
Rules:
- Interpret metrics in strict relation to stated campaign goals and benchmarks
- Deconstruct performance into meaningful trends, causal signals, and anomalies
- Explicitly identify "Leaky Buckets" (where budget is being wasted)
- Identify "High-Momentum Channels" or segments
- Provide an Efficiency Score (1-100) based on conversion vs spend
- Maintain an objective, executive-level diagnostic tone
- Avoid making final prescriptive decisions; provide the evidence for the user
 
Return ONLY valid JSON with this schema. No markdown wrapping:
 
{
  "executive_summary": "High-level diagnostic overview (1-2 sentences)",
  "efficiency_score": 85,
  "key_performance_insights": ["List of significant data-driven observations"],
  "budget_utilization_audit": "One paragraph auditing the spend efficiency",
  "risks_and_leaky_buckets": ["Areas of concern or wasted spend"],
  "strategic_opportunities": ["Areas for scaled growth or tactical pivots"],
  "benchmark_comparison": "How this period compares to the previous period or targets"
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

def analyze_campaign(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates advanced campaign analysis using LiteLLM."""
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
    with open("campaign_analysis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("campaign_analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"Campaign Strategic Intelligence ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
 
        f.write(f"Executive Summary: {data.get('executive_summary', 'N/A')}\n")
        f.write(f"Efficiency Score: {data.get('efficiency_score', 'N/A')}/100\n\n")
 
        f.write("Key Performance Insights:\n")
        for i in data.get("key_performance_insights", []):
            f.write(f"- {i}\n")
 
        f.write(f"\nBudget Utilization Audit:\n{data.get('budget_utilization_audit', 'N/A')}\n\n")
 
        f.write("Risks & Leaky Buckets:\n")
        for r in data.get("risks_and_leaky_buckets", []):
            f.write(f"- {r}\n")
 
        f.write("\nStrategic Opportunities:\n")
        for o in data.get("strategic_opportunities", []):
            f.write(f"- {o}\n")
            
        f.write(f"\nBenchmark vs Previous:\n{data.get('benchmark_comparison', 'N/A')}\n")
 
def main():
    prompt_text = read_input()
    analysis = analyze_campaign(prompt_text)
    save_outputs(analysis)
    print("Campaign performance analysis generated successfully.")
 
if __name__ == "__main__":
    main()
