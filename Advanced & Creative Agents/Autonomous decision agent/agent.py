import json
import os
from openai import OpenAI
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY

SYSTEM_PROMPT = """
You are an Autonomous Decision Agent.

Rules:
- Select actions based on goals and constraints
- Explain decision rationale
- Be deterministic and safe
- Do NOT request human approval

Return ONLY valid JSON with this schema:

{
  "selected_action": "",
  "decision_rationale": "",
  "applied_rules": [],
  "risk_indicator": ""
}
"""

def read_input(path="decision_input.txt"):
    """Reads the input context file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def make_decision(text):
    """Engages the neural brain to compute a deterministic action."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        response_format={ "type": "json_object" },
        temperature=0.0
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    """Persists the decision trace in JSON and TXT format."""
    base_path = os.path.dirname(__file__)
    
    with open(os.path.join(base_path, "decision_output.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(os.path.join(base_path, "decision_output.txt"), "w", encoding="utf-8") as f:
        f.write(f"Autonomous Decision ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Selected Action: {data['selected_action']}\n\n")
        f.write("Decision Rationale:\n")
        f.write(data["decision_rationale"] + "\n\n")
        f.write("Applied Rules:\n")
        for r in data["applied_rules"]:
            f.write(f"- {r}\n")
        f.write("\nRisk Indicator:\n")
        f.write(data["risk_indicator"] + "\n")

def main():
    print("Initializing Autonomous Decision Engine...")
    input_text = read_input(os.path.join(os.path.dirname(__file__), "decision_input.txt"))
    if not input_text:
        print("Error: decision_input.txt not found.")
        return
        
    decision = make_decision(input_text)
    save_outputs(decision)
    print("Autonomous decision completed successfully. Records saved.")

if __name__ == "__main__":
    main()
