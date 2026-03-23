import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Cash Flow Forecasting Agent (FlowForge AI).

Rules:
- Generate realistic, structured cash flow projections
- Highlight potential liquidity gaps and funding risks
- Align projections with user-stated burn rates and growth goals
- Highlight trade-offs and suggest optimization points
- Do NOT give financial advice

Return ONLY valid JSON with this schema:

{
  "forecasting_summary": "Overall summary of the cash flow projection",
  "starting_balance": "$Amount",
  "projected_ending_balance": "$Amount",
  "inflows": [
    {
      "source": "Source name",
      "amount": "$Amount",
      "timing": "When expected",
      "certainty": "Expected probability (e.g., High, Medium, Low)"
    }
  ],
  "outflows": [
    {
      "category": "Category name",
      "amount": "$Amount",
      "timing": "When expected",
      "priority": "Priority level (e.g., Critical, Flexible)"
    }
  ],
  "liquidity_metrics": {
    "burn_rate": "$Monthly burn",
    "runway_months": "Estimated months of runway",
    "reserve_status": "Status vs reserve goal"
  },
  "risk_assessment": [
    "Potential risk factors identified in the data"
  ]
}
"""

def read_input(path="cash_flow_input.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return None

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

def generate_forecast(text, model_name="gpt-4o"):
    """Generates cash flow forecast using selected provider via LiteLLM."""
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
    with open("cash_flow_forecast.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("cash_flow_forecast.txt", "w", encoding="utf-8") as f:
        f.write(f"CASH FLOW FORECAST REPORT ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write("📊 SUMMARY\n" + data.get("forecasting_summary", "N/A") + "\n\n")
        f.write(f"Starting Balance: {data.get('starting_balance')}\n")
        f.write(f"Projected Ending Balance: {data.get('projected_ending_balance')}\n\n")
        
        f.write("📈 PROJECTED INFLOWS\n")
        for inflow in data.get("inflows", []):
            f.write(f"- {inflow.get('source')}: {inflow.get('amount')} (Certainty: {inflow.get('certainty')})\n")
        
        f.write("\n📉 PROJECTED OUTFLOWS\n")
        for outflow in data.get("outflows", []):
            f.write(f"- {outflow.get('category')}: {outflow.get('amount')} (Priority: {outflow.get('priority')})\n")
            
        f.write("\n💡 LIQUIDITY METRICS\n")
        metrics = data.get("liquidity_metrics", {})
        f.write(f"- Burn Rate: {metrics.get('burn_rate')}\n")
        f.write(f"- Runway: {metrics.get('runway_months')} months\n")
        f.write(f"- Reserve Status: {metrics.get('reserve_status')}\n")
        
        f.write("\n⚠️ RISK ASSESSMENT\n")
        for risk in data.get("risk_assessment", []):
            f.write(f"- {risk}\n")

if __name__ == "__main__":
    input_text = read_input()
    if input_text:
        forecast = generate_forecast(input_text)
        save_outputs(forecast)
        print("Cash flow forecast generated successfully.")
