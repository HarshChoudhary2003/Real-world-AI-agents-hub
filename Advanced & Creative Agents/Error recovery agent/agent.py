import json
import os
from openai import OpenAI
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY

SYSTEM_PROMPT = """
You are an Error Recovery Agent.

Rules:
- Classify errors correctly
- Select safe recovery actions
- Avoid infinite retries
- Escalate when necessary

Return ONLY valid JSON with this schema:

{
  "error_classification": "",
  "recovery_actions": [],
  "recovery_status": "",
  "escalation_required": true
}
"""

def read_input(path="error_input.txt"):
    """Reads the failed process context."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def process_recovery(text):
    """Engages the neural brain to compute recovery maneuvers."""
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
    """Persists the recovery record in JSON and TXT format."""
    base_path = os.path.dirname(__file__)
    
    with open(os.path.join(base_path, "recovery_output.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(os.path.join(base_path, "recovery_output.txt"), "w", encoding="utf-8") as f:
        f.write(f"Error Recovery Report ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Error Classification: {data['error_classification']}\n\n")
        f.write("Recovery Actions:\n")
        for a in data["recovery_actions"]:
            f.write(f"- {a}\n")
        f.write("\nRecovery Status:\n")
        f.write(data["recovery_status"] + "\n\n")
        f.write("Escalation Required:\n")
        f.write(str(data["escalation_required"]) + "\n")

def main():
    print("Initializing Error Recovery Protocol...")
    input_text = read_input(os.path.join(os.path.dirname(__file__), "error_input.txt"))
    if not input_text:
        print("Error: error_input.txt not found.")
        return
        
    recovery = process_recovery(input_text)
    save_outputs(recovery)
    print("Error recovery process completed. Records logged.")

if __name__ == "__main__":
    main()
