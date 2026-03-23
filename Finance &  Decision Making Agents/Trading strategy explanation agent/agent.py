import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Trading Strategy Explanation Agent (StrategyLens AI).

Rules:
- Explain trading strategies clearly, logically, and neutrally.
- Highlight the core 'Why' behind the strategy mechanism.
- Enumerate specific 'Buy' and 'Sell' conditions as discrete logic steps.
- Explicitly identify environments where the strategy performs 'Well' and 'Poorly' (e.g., Trending vs. Ranging).
- Detail specific risks: slippage, whipsaws, systemic risk, etc.
- Do NOT provide trading advice, buy/sell signals, or price targets. No financial promotion.

Return ONLY valid JSON with this schema:

{
  "strategy_name": "Standardized Name",
  "strategy_overview": "High-level summary of the approach",
  "mechanics_audit": [
    { "step": "Logic Step Name", "description": "What happens in the system" }
  ],
  "optimal_market_state": "Description of when it performs best",
  "fail_market_state": "Description of common failure zones (e.g., sideways markets)",
  "risk_matrix": [
    { "risk_type": "Label", "impact": "Low/Medium/High", "mitigation_strategy": "Best practice to reduce risk" }
  ],
  "educational_summary": "Final synthesis for understanding the strategy's role in a portfolio"
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

def explain_strategy(text, model_name="gpt-4o"):
    """Audits a trading strategy using multi-model intelligence via LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.2
    }
    
    if "gpt-" in model_name or "o1-" in model_name:
        kwargs["response_format"] = {"type": "json_object"}
    
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    with open("strategy_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("strategy_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"TRADING STRATEGY SYSTEM AUDIT ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"📝 STRATEGY: {data.get('strategy_name', 'N/A')}\n")
        f.write(f"OVERVIEW: {data.get('strategy_overview', 'N/A')}\n\n")
        
        f.write("⚙️ MECHANICS AUDIT\n")
        for m in data.get('mechanics_audit', []):
            f.write(f"- [{m.get('step')}]: {m.get('description')}\n")
            
        f.write(f"\n✅ OPTIMAL STATE: {data.get('optimal_market_state', 'N/A')}\n")
        f.write(f"❌ FAIL STATE: {data.get('fail_market_state', 'N/A')}\n\n")
        
        f.write("⚠️ RISK MATRIX\n")
        for r in data.get('risk_matrix', []):
            f.write(f"- {r.get('risk_type')} ({r.get('impact')}%): {r.get('mitigation_strategy')}\n")
            
        f.write("\n🎓 EDUCATIONAL SYNTHESIS\n" + data.get("educational_summary", "N/A") + "\n")

if __name__ == "__main__":
    with open("strategy_input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    if input_text:
        explanation = explain_strategy(input_text)
        save_outputs(explanation)
        print("Trading strategy explained successfully.")
