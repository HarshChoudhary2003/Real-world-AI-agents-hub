import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Automation Architect & Business Process Strategist (Auto-Strategist AI v2.0).

Mission: Perform deep process-mining logic on manual workflows to identify high-ROI automation candidates.

Rules for Strategy:
1. **ROI Analysis**: Evaluate each candidate based on Complexity (Technical difficulty) vs. Impact (Time/Value saved).
2. **Technical Blueprint**: Suggest specific automation tools (RPA, AI Agents, Python scripts, SaaS platforms) for each candidate.
3. **Quantifiable Benefits**: Provide concrete expected outcomes (e.g., 'Eliminate 95% of manual errors').
4. **Architectural Foresight**: Anticipate data-entry risks or structural bottlenecks in the automation path.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "strategic_assessment": {
     "readiness_score": "0-100",
     "total_potential_identified": #,
     "executive_summary": "Process architecture gist"
  },
  "automation_roadmap": [
    {
      "candidate": "Process name",
      "priority": "Critical/High/Standard",
      "impact_rating": "Scale 1-10",
      "strategic_rationale": "Why this is a target",
      "expected_outcomes": ["Benefit A", "Benefit B"],
      "tech_stack_suggestion": ["Tool 1", "Tool 2"],
      "pre_requisites": ["Prereq 1", "Prereq 2"]
    }
  ],
  "structural_risks": ["Potential bottlenecks"],
  "transformation_pro_tips": ["Strategic advice for architects"]
}
"""

def read_workflow_data(path="workflows.txt"):
    """Reads raw workflow descriptions from a local text file."""
    if not os.path.exists(path):
        return "Process: Default Flow. Tasks: Step A, B, C."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_json(response_content):
    """Robustly parse JSON out of an LLM response."""
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", str(response_content))
        if match:
            try: return json.loads(match.group(1).strip())
            except: pass
        match = re.search(r"\{[\s\S]*\}", str(response_content))
        if match:
            try: return json.loads(match.group(0).strip())
            except: pass
    raise ValueError("Failed to extract strategic JSON.")

def generate_automation_strategy(workflow_text, model_name="gpt-4o-mini", api_key=None):
    """Generates the automation roadmap using neural process mining in LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": workflow_text}
        ],
        "temperature": 0.3
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the automation strategy as JSON and formatted TXT."""
    with open("automation_recommendations.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("automation_recommendations.txt", "w", encoding="utf-8") as f:
        f.write(f"Auto-Strategist AI: Neural Process Roadmap ({date.today()})\n")
        f.write("=" * 65 + "\n\n")

        sa = data.get('strategic_assessment', {})
        f.write(f"Readiness Score: {sa.get('readiness_score')}/100\n")
        f.write(f"Potential Count: {sa.get('total_potential_identified')}\n")
        f.write(f"Summary: {sa.get('executive_summary')}\n\n")
        
        f.write("--- 🏗️ AUTOMATION ROADMAP ---\n")
        for item in data.get('automation_roadmap', []):
            f.write(f"▶ CANDIDATE: {item.get('candidate')} [{item.get('priority')}]\n")
            f.write(f"  Rationale: {item.get('strategic_rationale')}\n")
            f.write(f"  Impact: {item.get('impact_rating')}/10) | Tech: {item.get('tech_stack_suggestion')}\n")
            f.write(f"  Outcomes: {item.get('expected_outcomes')}\n\n")
        
        f.write("--- 🧬 ARCHITECT PRO-TIPS ---\n")
        for tip in data.get("transformation_pro_tips", []):
            f.write(f"- {tip}\n")

def main():
    print("🚀 Auto-Strategist AI: Scoping Transformation Potential...")
    flows = read_workflow_data()
    try:
        strategy = generate_automation_strategy(flows)
        save_outputs(strategy)
        print("✅ Automation roadmap generated successfully.")
        print("📁 Outputs: automation_recommendations.json, automation_recommendations.txt")
    except Exception as e:
        print(f"❌ Strategy fail: {str(e)}")

if __name__ == "__main__":
    main()
