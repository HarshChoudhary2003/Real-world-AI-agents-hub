import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Financial Report Explainer Agent (FinLens Pro).

Rules:
- Explain complex financial statements using clear, professional, yet understandable narrative
- Highlight key metrics, hidden trends, and structural risks
- Translate raw numbers into strategic business implications
- Maintain a neutral, analytical tone (JARVIS-like intelligence)
- Do NOT provide legal or financial advice

Return ONLY valid JSON with this schema:

{
  "summary": "Executive summary of the report in 2-3 sentences",
  "key_metrics": [
     { "label": "Metric Name", "value": "Current Value", "context": "Comparison or Trend" }
  ],
  "notable_changes": [
    "List of significant shifts in the data"
  ],
  "business_implications": [
    "What the data means for future strategy/operations"
  ],
  "risk_assessment": "The most critical financial vulnerability identified"
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

def explain_report(text, model_name="gpt-4o"):
    """Generates financial report explanations using multi-model intelligence via LiteLLM."""
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
    with open("financial_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("financial_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"FINANCIAL REPORT EXPLANATION ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write("📖 SUMMARY\n" + data.get("summary", "N/A") + "\n\n")
        
        f.write("📊 KEY METRICS\n")
        for k in data.get("key_metrics", []):
            f.write(f"- {k.get('label')}: {k.get('value')} ({k.get('context')})\n")
            
        f.write("\n🔄 NOTABLE CHANGES\n")
        for n in data.get("notable_changes", []):
            f.write(f"- {n}\n")
            
        f.write("\n💡 BUSINESS IMPLICATIONS\n")
        for b in data.get("business_implications", []):
            f.write(f"- {b}\n")

        f.write("\n🛡️ RISK ASSESSMENT\n" + data.get("risk_assessment", "N/A") + "\n")

if __name__ == "__main__":
    with open("report_input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    if input_text:
        explanation = explain_report(input_text)
        save_outputs(explanation)
        print("Financial report explained successfully.")
