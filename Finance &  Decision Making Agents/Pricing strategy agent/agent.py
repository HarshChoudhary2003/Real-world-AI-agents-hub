import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Pricing Strategy Agent (PriceForge AI).

Rules:
- Generate multiple, high-fidelity pricing strategy options
- Explain the rationale, economic trade-offs, and perceived market value
- Align all strategies with user objectives and cost structures
- Highlight risks and competitive positioning for each option
- Do NOT give legal or financial advice

Return ONLY valid JSON with this schema:

{
  "pricing_summary": "Overall market positioning and strategy overview",
  "starting_recommendation": "The most aggressive yet sustainable first move",
  "pricing_options": [
    {
      "name": "Strategy Name (e.g., Market Penetration, Premium Skimming)",
      "price": "$Amount / billing cycle",
      "target_segment": "Who this is for",
      "rationale": "Economic and competitive reasoning",
      "risks": "Potential downsides or competitor reactions",
      "margin_impact": "Estimated impact on profitability"
    }
  ],
  "value_drivers": [
    "Key features justifying the price points"
  ],
  "competitive_moat": "How this pricing strategy creates a long-term advantage"
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

def generate_pricing(text, model_name="gpt-4o"):
    """Generates pricing strategies using multi-model intelligence via LiteLLM."""
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
    with open("pricing_strategy.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("pricing_strategy.txt", "w", encoding="utf-8") as f:
        f.write(f"PRICING STRATEGY REPORT ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write("🏷️ PRICING SUMMARY\n" + data.get("pricing_summary", "N/A") + "\n\n")
        f.write(f"Primary Recommendation: {data.get('starting_recommendation')}\n\n")
        
        f.write("🚀 PRICING OPTIONS\n")
        for p in data.get("pricing_options", []):
            f.write(f"--- {p.get('name')} ---\n")
            f.write(f"Price: {p.get('price')}\n")
            f.write(f"Segment: {p.get('target_segment')}\n")
            f.write(f"Rationale: {p.get('rationale')}\n")
            f.write(f"Risks: {p.get('risks')}\n")
            f.write(f"Margin: {p.get('margin_impact')}\n\n")
            
        f.write("\n💎 VALUE DRIVERS\n")
        for driver in data.get("value_drivers", []):
            f.write(f"- {driver}\n")
        
        f.write(f"\n🏰 COMPETITIVE MOAT\n{data.get('competitive_moat')}\n")

if __name__ == "__main__":
    with open("pricing_input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    if input_text:
        strategy = generate_pricing(input_text)
        save_outputs(strategy)
        print("Pricing strategy generated successfully.")
