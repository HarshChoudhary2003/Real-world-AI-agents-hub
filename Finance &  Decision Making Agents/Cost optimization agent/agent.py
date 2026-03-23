import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Cost Optimization Agent (OptiForge AI).

Rules:
- Identify realistic, high-impact cost optimization opportunities
- Estimate month-on-month savings and overall business impact
- Avoid recommending harmful cuts that affect product velocity or core infrastructure
- Align recommendations with business priorities (e.g., uptime, development speed)
- Do NOT give legal or financial advice

Return ONLY valid JSON with this schema:

{
  "optimization_summary": "High-level overview of total potential savings",
  "priority_focus": "The first area that should be addressed immediately",
  "opportunity_list": [
    {
      "area": "E.g., Cloud Infrastructure, SaaS Portfolio",
      "estimated_savings": "$Amount or %",
      "effort_level": "Low, Medium, High",
      "impact": "Description of operational impact",
      "recommendation": "Specific actionable steps to optimize"
    }
  ],
  "efficiency_metrics": {
    "total_potential_reduction": "$Amount",
    "burn_rate_improvement": "% Percentage",
    "roi_period": "Expected time to see full impact"
  },
  "risk_mitigation": [
    "Precautions to take when implementing these cuts"
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

def optimize_costs(text, model_name="gpt-4o"):
    """Generates cost optimization strategies using multi-model intelligence via LiteLLM."""
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
    with open("cost_optimization.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("cost_optimization.txt", "w", encoding="utf-8") as f:
        f.write(f"COST OPTIMIZATION AUDIT ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write("🏷️ OPTIMIZATION SUMMARY\n" + data.get("optimization_summary", "N/A") + "\n\n")
        f.write(f"Immediate Priority: {data.get('priority_focus')}\n\n")
        
        f.write("⚡ OPPORTUNITIES\n")
        for o in data.get("opportunity_list", []):
            f.write(f"--- {o.get('area')} ---\n")
            f.write(f"Savings: {o.get('estimated_savings')}\n")
            f.write(f"Effort: {o.get('effort_level')}\n")
            f.write(f"Impact: {o.get('impact')}\n")
            f.write(f"Recommendation: {o.get('recommendation')}\n\n")
            
        f.write("\n📊 EFFICIENCY METRICS\n")
        metrics = data.get("efficiency_metrics", {})
        f.write(f"- Total Reduction: {metrics.get('total_potential_reduction')}\n")
        f.write(f"- Burn Rate Improvement: {metrics.get('burn_rate_improvement')}\n")
        f.write(f"- ROI Period: {metrics.get('roi_period')}\n")

        f.write("\n🛡️ RISK MITIGATION\n")
        for risk in data.get("risk_mitigation", []):
            f.write(f"- {risk}\n")

if __name__ == "__main__":
    with open("cost_input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    if input_text:
        optimization = optimize_costs(input_text)
        save_outputs(optimization)
        print("Cost optimization analysis completed successfully.")
