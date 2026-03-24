import json
import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY
base_path = os.path.dirname(__file__)

SYSTEM_PROMPT = """
You are a Production-Ready Autonomous AI Agent (Apex.AI).

Rules:
- Respect ethical guardrails and mission constraints.
- Log all decisions with full transparency.
- Utilize persistent memory to inform strategic maneuvers.
- Fail safely: prioritize system stability over aggressive optimization.
- Be explainable: provide clear rationale for every decision.

Return ONLY valid JSON with this schema:

{
  "decision": "",
  "rationale": "",
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "memory_update": ""
}
"""

def load_json(path):
    """Loads a tactical JSON artifact."""
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return [] if "log" in path else {}

def save_json(path, data):
    """Persists a tactical JSON artifact."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    print("Initializing APEX Autonomous Control Matrix...")
    
    memory_path = os.path.join(base_path, "memory.json")
    log_path = os.path.join(base_path, "log.json")
    input_path = os.path.join(base_path, "input.txt")

    memory = load_json(memory_path)
    if not isinstance(memory, dict): memory = {"past_decisions": [], "learned_constraints": []}
    
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            user_input = f.read()
    except:
        print("Error: Mission input signal not detected.")
        return

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Neural Memory Context:\n{json.dumps(memory)}\n\nMission Objective:\n{user_input}"}
        ],
        response_format={ "type": "json_object" },
        temperature=0.2
    )

    result = json.loads(response.choices[0].message.content)

    # Persistence Layer Updates
    memory["past_decisions"].append(result["decision"])
    if result.get("memory_update"):
        memory["learned_constraints"].append(result["memory_update"])
    save_json(memory_path, memory)

    # Logging Layer
    log = load_json(log_path)
    if not isinstance(log, list): log = []
    log.insert(0, {
        "timestamp": datetime.utcnow().isoformat(),
        "decision": result
    })
    save_json(log_path, log[:100]) # Keep only last 100 tactical logs

    print(f"Strategic Decision Executed: {result['decision']} (Risk: {result['risk_level']})")

if __name__ == "__main__":
    main()
