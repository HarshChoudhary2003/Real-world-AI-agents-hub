import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Revenue Breakdown Agent (RevForge AI).

Rules:
- Break down revenue structure with high precision (Product, Channel, Geography)
- Highlight contribution and concentration risk (Pareto effects)
- Identify actionable key insights and growth opportunities
- Do NOT provide legal or financial advice

Return ONLY valid JSON with this schema:

{
  "revenue_summary": "High-level overview of the revenue state",
  "breakdown": [
    {
       "category": "E.g., Product A, North America",
       "amount": "$Amount",
       "percentage": "% contribution",
       "status": "Growth / Stable / Declined"
    }
  ],
  "contribution_percentages": [
    "List of key percentage highlights"
  ],
  "key_insights": [
    "Strategic conclusions from the data"
  ],
  "risks_and_opportunities": [
    "Specific competitive or economic factors"
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

def analyze_revenue(text, model_name="gpt-4o"):
    """Generates revenue breakdown reports using multi-model intelligence via LiteLLM."""
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
    with open("revenue_breakdown.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("revenue_breakdown.txt", "w", encoding="utf-8") as f:
        f.write(f"REVENUE BREAKDOWN AUDIT ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write("💰 REVENUE SUMMARY\n" + data.get("revenue_summary", "N/A") + "\n\n")
        
        f.write("📈 BREAKDOWN DATA\n")
        for b in data.get("breakdown", []):
            f.write(f"- {b.get('category')}: {b.get('amount')} ({b.get('percentage')}) | Status: {b.get('status')}\n")
            
        f.write("\n📊 CONTRIBUTION HIGHLIGHTS\n")
        for c in data.get("contribution_percentages", []):
            f.write(f"- {c}\n")
            
        f.write("\n💡 KEY INSIGHTS\n")
        for k in data.get("key_insights", []):
            f.write(f"- {k}\n")

        f.write("\n🛡️ RISKS & OPPORTUNITIES\n")
        for r in data.get("risks_and_opportunities", []):
            f.write(f"- {r}\n")

if __name__ == "__main__":
    with open("revenue_input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    if input_text:
        breakdown = analyze_revenue(input_text)
        save_outputs(breakdown)
        print("Revenue breakdown analysis completed successfully.")
