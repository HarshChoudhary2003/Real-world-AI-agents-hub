import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Product Marketing & GTM Strategy Agent (Launch-Pad AI v2.0).

Mission: Architect high-stakes product launch checklists that ensure zero-day failure and maximum market impact.

Rules for Strategy:
1. **Phased Architecture**: Categorize tasks into Pre-Launch (Warm-up), Launch Day (Execution), and Post-Launch (Momentum).
2. **Channel Specificity**: Provide explicit tasks for Website, Email, and Social media.
3. **Internal Alignment**: Include tasks for cross-functional alignment (Sales, Support).
4. **Actionable Ownership**: Assign clear priorities and owners.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "launch_identity": {
     "codename": "Catchy internal launch name",
     "value_hook": "Core value proposition piece"
  },
  "phases": {
     "pre_launch": [
        {"task": "Task description", "owner": "Role", "priority": "High/Med/Low"}
     ],
     "launch_day": [
        {"task": "Task description", "owner": "Role", "urgency": "High/Med/Low"}
     ],
     "post_launch": [
        {"task": "Task description", "metric_to_track": "Metric name"}
     ]
  },
  "channel_specific_tasks": {
     "website": ["List of tasks"],
     "email": ["List of tasks"],
     "social": ["List of tasks"]
  },
  "risk_mitigation": ["List of potential blockers and how to avoid them"]
}
"""

def read_input(path="input.txt"):
    """Reads input data from a local text file."""
    if not os.path.exists(path):
        return "Product: AI Tool. Launch in 2 weeks. Channels: Web, Social."
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

def generate_launch_checklist(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates advanced launch checklist using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.3
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the launch checklist as JSON and formatted TXT."""
    with open("launch_checklist.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("launch_checklist.txt", "w", encoding="utf-8") as f:
        f.write(f"Launch-Pad AI Strategy Checklist ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        li = data.get('launch_identity', {})
        f.write(f"Project Codename: {li.get('codename')}\n")
        f.write(f"Value Hook: {li.get('value_hook')}\n\n")
        
        phases = data.get('phases', {})
        
        f.write("--- 🏗️ Phase 1: Pre-Launch ---\n")
        for item in phases.get('pre_launch', []):
            f.write(f"[{item.get('priority')}] {item.get('task')} (Owner: {item.get('role', 'N/A') or item.get('owner', 'N/A')})\n")
        
        f.write("\n--- 🚀 Phase 2: Launch Day ---\n")
        for item in phases.get('launch_day', []):
            f.write(f"[{item.get('urgency', 'Med')}] {item.get('task')} (Owner: {item.get('owner', 'N/A')})\n")

        f.write("\n--- 📈 Phase 3: Post-Launch Analysis ---\n")
        for item in phases.get('post_launch', []):
            f.write(f"- {item.get('task')} (Success Metric: {item.get('metric_to_track')})\n")

        f.write("\n--- 🛡️ Risk Mitigation Strategy ---\n")
        for risk in data.get("risk_mitigation", []):
            f.write(f"- {risk}\n")

def main():
    print("🚀 Launch-Pad AI: Architecting GTM Readiness Checklist...")
    prompt_text = read_input()
    try:
        checklist = generate_launch_checklist(prompt_text)
        save_outputs(checklist)
        print("✅ Product launch checklist strategy completed successfully.")
        print("📁 Outputs: launch_checklist.json, launch_checklist.txt")
    except Exception as e:
        print(f"❌ Launch Prep failed: {str(e)}")

if __name__ == "__main__":
    main()
