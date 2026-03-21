import json
import re
import os
from datetime import date
from collections import deque
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Workflow Architect & Systems Orchestrator (Orchestra-Core AI v2.0).

Mission: Analyze complex multi-step workflows to calculate optimal execution paths, resolve dependencies, and identify circularities.

Rules for Orchestration logic:
1. **Topological Purity**: Resolve the absolute execution order based on strict dependencies.
2. **Parallel potential**: Identify steps that can be run concurrently to minimize latency.
3. **Failure Scenarios**: Anticipate potential break points (API timeouts, DB locks) for each step and suggest granular recovery.
4. **Efficiency Metrics**: Score the workflow's architecture based on dependency depth and bottleneck possibility.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "orchestra_assessment": {
     "efficiency_score": "0-100",
     "verdict": "Optimized/Sub-optimal/Broken",
     "diagnostic_overview": "Strategic summary"
  },
  "execution_blueprint": [
     {
       "step_id": "...",
       "priority_level": #,
       "parallel_group": "Group A/B/...",
       "action_intent": "Description of the operation"
     }
  ],
  "dependency_diagnostics": {
     "circular_nodes": ["List of any recursive dependency loops"],
     "bottleneck_nodes": ["Steps that block multiple downstream updates"]
  },
  "recovery_blueprints": [
     {"step_id": "...", "incident_type": "...", "surgical_remediation": "..."}
  ],
  "pro_architect_tips": ["Strategic advice for system performance"]
}
"""

def read_workflow(path="workflow.json"):
    """Reads raw workflow JSON from a local file."""
    if not os.path.exists(path):
        return {"workflow_name": "Default", "steps": [{"id": "init", "depends_on": []}]}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

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

def architect_execution_path(workflow_data, model_name="gpt-4o-mini", api_key=None):
    """Deep orchestration analysis of the workflow using LiteLLM."""
    prompt = f"ARCHITECT WORKFLOW:\n{json.dumps(workflow_data, indent=2)}"
    
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the orchestration audit as JSON and formatted TXT."""
    with open("workflow_run.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("workflow_run.txt", "w", encoding="utf-8") as f:
        f.write(f"Orchestra-Core AI: Workflow Execution Architecture ({date.today()})\n")
        f.write("=" * 65 + "\n\n")

        oa = data.get('orchestra_assessment', {})
        f.write(f"Efficiency Score: {oa.get('efficiency_score')}/100\n")
        f.write(f"Verdict: {oa.get('verdict')}\n")
        f.write(f"Audit: {oa.get('diagnostic_overview')}\n\n")
        
        f.write("--- 🚀 OPTIMIZED EXECUTION BLUEPRINT ---\n")
        for step in data.get('execution_blueprint', []):
            f.write(f"Priority {step.get('priority_level')} | Group {step.get('parallel_group')}: {step.get('step_id')}\n")
            f.write(f"Intent: {step.get('action_intent')}\n\n")
        
        f.write("--- 🛡️ RECOVERY BLUEPRINTS ---\n")
        for rec in data.get('recovery_blueprints', []):
            f.write(f"[{rec.get('step_id')}] Incident: {rec.get('incident_type')}\n")
            f.write(f"Remediation: {rec.get('surgical_remediation')}\n\n")

        f.write("--- 🧬 PRO TIPS ---\n")
        for tip in data.get("pro_architect_tips", []):
            f.write(f"- {tip}\n")

def main():
    print("🚀 Orchestra-Core AI: Architecting Execution Path...")
    workflow = read_workflow()
    
    try:
        blueprint = architect_execution_path(workflow)
        save_outputs(blueprint)
        print("✅ Workflow orchestration architecture completed successfully.")
        print("📁 Outputs: workflow_run.json, workflow_run.txt")
    except Exception as e:
        print(f"❌ Logical failure: {str(e)}")

if __name__ == "__main__":
    main()
