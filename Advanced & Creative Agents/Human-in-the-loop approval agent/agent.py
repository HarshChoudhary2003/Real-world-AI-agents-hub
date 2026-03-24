import json
import os
from openai import OpenAI
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a Human-in-the-Loop Approval Agent.

Rules:
- Determine if approval is required
- Generate approval request
- Capture human decision
- Enforce outcome
- Maintain audit trail

Return ONLY valid JSON with this schema:

{
  "approval_required": true,
  "approval_request": "",
  "human_decision": "",
  "final_status": "",
  "audit_notes": ""
}
"""

def read_input(path="approval_input.txt"):
    """Reads the proposed action context."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def generate_request(text):
    """Engages the neural brain to formulate a formal approval request."""
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
    """Persists the approval record in JSON and TXT format."""
    base_path = os.path.dirname(__file__)
    
    with open(os.path.join(base_path, "approval_output.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(os.path.join(base_path, "approval_output.txt"), "w", encoding="utf-8") as f:
        f.write(f"Approval Record ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Approval Required: {data['approval_required']}\n\n")
        f.write("Approval Request:\n")
        f.write(data["approval_request"] + "\n\n")
        f.write("Human Decision:\n")
        f.write(data["human_decision"] or "PENDING" + "\n\n")
        f.write("Final Status:\n")
        f.write(data["final_status"] or "WAITING FOR REVIEW" + "\n\n")
        f.write("Audit Notes:\n")
        f.write(data["audit_notes"] + "\n")

def main():
    print("Initializing Human-in-the-Loop Protocol...")
    input_text = read_input(os.path.join(os.path.dirname(__file__), "approval_input.txt"))
    if not input_text:
        print("Error: approval_input.txt not found.")
        return
        
    approval = generate_request(input_text)
    save_outputs(approval)
    print("Human-in-the-loop approval record generated. Awaiting human input.")

if __name__ == "__main__":
    main()
