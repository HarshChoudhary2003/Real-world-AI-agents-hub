import json
import os
from openai import OpenAI
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY
base_path = os.path.dirname(__file__)

SYSTEM_PROMPT = """
You are an Ethics & Guardrails Agent.

Rules:
- Rigorously evaluate proposed actions against the defined policies.
- Classify potential risks and potential for harm.
- Decision options: ALLOW, BLOCK, or ESCALATE.
- Provide a detailed rationale and audit notes.

Return ONLY valid JSON with this schema:

{
  "ethical_assessment": "",
  "applied_policies": [],
  "final_decision": "ALLOW|BLOCK|ESCALATE",
  "audit_notes": ""
}
"""

def main():
    print("Initializing Ethical Governance Protocol...")
    
    policies_path = os.path.join(base_path, "policies.txt")
    action_path = os.path.join(base_path, "ethics_input.txt")
    output_json = os.path.join(base_path, "ethics_output.json")
    output_txt = os.path.join(base_path, "ethics_output.txt")

    try:
        with open(policies_path, "r", encoding="utf-8") as f:
            policies = f.read()
        with open(action_path, "r", encoding="utf-8") as f:
            proposed_action = f.read()
    except FileNotFoundError as e:
        print(f"Error: Required file not found: {e.filename}")
        return

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Neural Ethical Framework / Policies:\n{policies}\n\nProposed Autonomous Action:\n{proposed_action}"
            }
        ],
        response_format={ "type": "json_object" },
        temperature=0.0
    )

    result = json.loads(response.choices[0].message.content)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(f"Neural Ethics Audit Record ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Strategic Assessment: {result['ethical_assessment']}\n\n")
        f.write("Governance Policies Applied:\n")
        for p in result["applied_policies"]:
            f.write(f" [√] {p}\n")
        f.write("\nFinal Decision: " + result["final_decision"] + "\n\n")
        f.write("Immutable Audit Notes:\n")
        f.write(result["audit_notes"] + "\n")

    print(f"Ethics evaluation complete. Result: {result['final_decision']}.")

if __name__ == "__main__":
    main()
