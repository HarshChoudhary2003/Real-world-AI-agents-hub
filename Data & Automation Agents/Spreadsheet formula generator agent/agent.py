import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Spreadsheet & Data Architect (Sheet-Logic AI v2.0).

Mission: Architect high-performance, complex formulas across multiple platforms (Excel, Google Sheets, Airtable, Notion).

Rules for Logic Architecture:
1. **Platform Strictness**: Ensure the exact syntax for the requested platform (e.g., ArrayFormula for Google Sheets, absolute vs. relative references).
2. **Efficiency First**: Choose the most performant functions available (e.g., SUMIFS/XLOOKUP over heavy nested IFs).
3. **Logic Breakdown**: Provide a human-readable, step-by-step technical explanation of the formula's calculation path.
4. **Boundary Detection**: Highlight potential error points (e.g., handling #N/A, zero division, or empty cells).

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "project_meta": {
     "platform": "Excel/Google Sheets/etc.",
     "complexity_level": "Basic/Intermediate/Advanced",
     "best_suited_for": "Use-case description"
  },
  "primary_formula": "The final result formula",
  "technical_breakdown": [
     {"step": "Component of the formula", "explanation": "Why this function is used and what it does"}
  ],
  "validation_rules": ["Assumptions made about the data structure"],
  "alternative_methods": [
     {"name": "e.g., Pivot Table approach", "formula_or_method": "Draft formula or high-level steps"}
  ],
  "pro_tips": ["Advice for implementation (e.g., performance impact)"]
}
"""

def read_input(path="input.txt"):
    """Reads spreadsheet formula request from a local text file."""
    if not os.path.exists(path):
        return "Platform: Excel. Request: Sum column C if B is 'Paid'."
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

def generate_sheet_logic(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates advanced spreadsheet logic and formulas using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.2
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the formula logic as JSON and formatted TXT."""
    with open("formula_output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("formula_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Sheet-Logic AI Formula Architecture ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Platform: {data.get('project_meta', {}).get('platform')}\n")
        f.write(f"Complexity: {data.get('project_meta', {}).get('complexity_level')}\n\n")
        
        f.write("--- 🚀 PRIMARY FORMULA ---\n")
        f.write(f"{data.get('primary_formula')}\n\n")
        
        f.write("--- 📉 TECHNICAL BREAKDOWN ---\n")
        for step in data.get('technical_breakdown', []):
            f.write(f"▶ {step.get('step')}: {step.get('explanation')}\n")
        
        f.write("\n--- 🛡️ VALIDATION RULES ---\n")
        for rule in data.get('validation_rules', []):
            f.write(f"• {rule}\n")

        f.write("\n---💡 PRO TIPS ---\n")
        for tip in data.get('pro_tips', []):
            f.write(f"- {tip}\n")

def main():
    print("🚀 Sheet-Logic AI: Architecting Data Formula...")
    prompt_text = read_input()
    try:
        logic = generate_sheet_logic(prompt_text)
        save_outputs(logic)
        print("✅ Spreadsheet formula architecture completed successfully.")
        print("📁 Outputs: formula_output.json, formula_output.txt")
    except Exception as e:
        print(f"❌ Logical failure: {str(e)}")

if __name__ == "__main__":
    main()
