import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Funnel Optimization & Growth Strategy Agent (Funnel-Force AI v4.0).

Your mission is to perform professional, behavioral diagnostics on conversion funnels to identify exactly where and WHY friction exists.

Optimization Rules for Analysis:
1. **Behavioral Diagnostics**: Don't just identify drop-offs; explain the psychological friction (e.g., "Decision Fatigue at Selection" or "High-Friction Data Fields").
2. **Efficiency Mapping**: Calculate conversion percentages at each stage.
3. **Strategic Scaling**: Analyze based on the specific acquisition segment (e.g., Organic trust gaps vs Paid ad expectations).
4. **Professional & Empathic**: Be analytical but deeply empathetic to the user's friction.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "summary": "Professional overview of the funnel health",
  "conversion_metrics": {
    "overall": "The overall CR from the top to the bottom",
    "at_each_stage": {
       "Stage 1 -> Stage 2": "X%",
       "Stage 2 -> Stage 3": "Y%"
    }
  },
  "drop_off_stages": [
    {
       "stage": "The stage experiencing the drop-off",
       "drop_off_pct": "Calculation of the users lost",
       "psychological_reason": "Why are they leaving here?"
    }
  ],
  "observed_patterns": ["Top thematic insights based on the segment"],
  "prioritized_actions": [
     {
       "priority": "High/Med/Low",
       "focus_area": "The specific area needing optimization",
       "potential_impact": "Expected conversion lift if resolved",
       "suggested_counter_bias": "Bias to use (e.g., Social Proof, Scarcity, Reciprocity)"
     }
  ]
}
"""

def read_input(path="input.txt"):
    """Reads input data from a local text file."""
    if not os.path.exists(path):
        return "Landing: 1000\nSignup: 200\nLead: 50\nGoal: Increase Lead."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

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

def analyze_funnel(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Performs advanced funnel analysis using LiteLLM."""
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

def save_outputs(data):
    """Saves the funnel insights as JSON and formatted TXT."""
    with open("funnel_insights.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("funnel_insights.txt", "w", encoding="utf-8") as f:
        f.write(f"Advanced Funnel Optimization Strategy ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Executive Summary:\n{data.get('summary')}\n\n")
        
        f.write("--- Conversion Efficiency ---\n")
        f.write(f"Overall CR: {data.get('conversion_metrics', {}).get('overall')}\n")
        for stage, cr in data.get('conversion_metrics', {}).get('at_each_stage', {}).items():
            f.write(f"- {stage}: {cr}\n")
        
        f.write("\n--- Critical Drop-off Diagnostics ---\n")
        for drop in data.get("drop_off_stages", []):
            f.write(f"- {drop.get('stage')}: {drop.get('drop_off_pct')} lost\n")
            f.write(f"  Reason: {drop.get('psychological_reason')}\n")

        f.write("\nObserved Behavioral Patterns:\n")
        for pattern in data.get("observed_patterns", []):
            f.write(f"- {pattern}\n")

        f.write("\n--- Prioritized Growth Roadmap ---\n")
        for action in data.get("prioritized_actions", []):
            f.write(f"[{action.get('priority')}] {action.get('focus_area')}\n")
            f.write(f"Impact: {action.get('potential_impact')}\n")
            f.write(f"Strategic Bias: {action.get('suggested_counter_bias')}\n\n")

def main():
    print("🚀 Funnel-Force AI: Initializing Performance Diagnostics...")
    prompt_text = read_input()
    try:
        insights = analyze_funnel(prompt_text)
        save_outputs(insights)
        print("✅ Funnel optimization strategy generated successfully.")
        print("📁 Outputs: funnel_insights.json, funnel_insights.txt")
    except Exception as e:
        print(f"❌ Diagnostic failed: {str(e)}")

if __name__ == "__main__":
    main()
