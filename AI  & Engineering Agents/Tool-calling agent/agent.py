import json
import os
import math
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# =============================================================================
# TOOL REGISTRY
# =============================================================================
def calculator(quantity: float, price: float, tax_rate: float) -> float:
    """Computes total cost including tax."""
    subtotal = quantity * price
    return round(subtotal * (1 + tax_rate), 2)

def unit_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Handles basic unit conversions (km<->miles, kg<->lbs, C<->F)."""
    conversions = {
        ("km", "miles"): lambda v: round(v * 0.621371, 4),
        ("miles", "km"): lambda v: round(v * 1.60934, 4),
        ("kg", "lbs"): lambda v: round(v * 2.20462, 4),
        ("lbs", "kg"): lambda v: round(v / 2.20462, 4),
        ("celsius", "fahrenheit"): lambda v: round((v * 9/5) + 32, 2),
        ("fahrenheit", "celsius"): lambda v: round((v - 32) * 5/9, 2),
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        return conversions[key](value)
    raise ValueError(f"Unsupported conversion: {from_unit} → {to_unit}")

def percentage_calculator(base: float, rate: float) -> float:
    """Calculates a percentage value."""
    return round(base * (rate / 100), 2)

TOOL_MAP = {
    "calculator": calculator,
    "unit_converter": unit_converter,
    "percentage_calculator": percentage_calculator,
}

SYSTEM_PROMPT = """
You are an advanced Tool-Calling Agent with access to the following tools:

1. calculator(quantity, price, tax_rate) — Computes purchase totals with tax
2. unit_converter(value, from_unit, to_unit) — Converts between units (km, miles, kg, lbs, celsius, fahrenheit)
3. percentage_calculator(base, rate) — Computes a percentage of a value

Rules:
- Analyze the task carefully to select the correct tool
- Extract exact parameters with correct data types (numbers must be floats)
- tax_rate must be a decimal (e.g., 8% = 0.08, not 8)
- Do NOT change task intent

Return ONLY valid JSON with this schema:
{
  "reasoning": "Short explanation of why this tool was selected",
  "tool_used": "tool_name",
  "inputs": { ...parameters... },
  "result": null,
  "final_answer": ""
}
"""

def read_task(path="task.txt"):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Calculate the total cost if 3 items cost $49 each, including 8% tax.")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_json(content: str) -> dict:
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]
    return json.loads(content)

def run_agent(task: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Orchestrating agent via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task}
        ],
        temperature=0.2
    )
    decision = extract_json(response.choices[0].message.content)

    tool_name = decision.get("tool_used", "")
    if tool_name in TOOL_MAP:
        result = TOOL_MAP[tool_name](**decision["inputs"])
        decision["result"] = result
        decision["final_answer"] = f"✅ {tool_name} completed successfully. Result: {result}"
    else:
        decision["result"] = "N/A"
        decision["final_answer"] = "No matching tool was invoked."

    return decision

def save_outputs(data: dict):
    with open("tool_call_result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("tool_call_result.txt", "w", encoding="utf-8") as f:
        f.write(f"ToolForge AI: Tool-Call Execution Report ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Reasoning: {data.get('reasoning', 'N/A')}\n\n")
        f.write(f"Tool Used: {data['tool_used']}\n")
        f.write(f"Inputs: {json.dumps(data['inputs'], indent=2)}\n")
        f.write(f"Result: {data['result']}\n\n")
        f.write(f"Final Answer: {data['final_answer']}\n")

def main():
    print("🚀 ToolForge AI: Initiating autonomous tool-call logic...")
    try:
        task = read_task()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        result = run_agent(task, model=model)
        save_outputs(result)
        print("✅ Tool-calling agent executed successfully.")
        print("📁 Outputs: tool_call_result.json, tool_call_result.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
