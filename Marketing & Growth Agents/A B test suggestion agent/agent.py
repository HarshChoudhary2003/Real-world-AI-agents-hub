import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly strategic and data-driven A/B Test Suggestion Agent (OptiTest AI).
 
Rules:
- Propose clear, hypothesis-driven experiments based on conversion psychology and user behavior.
- Use the ICE Scoring framework (Impact, Confidence, Ease) for all suggestions (1-10 scale).
- Ensure variables are isolated to avoid overlapping or confounding results.
- Provide a clear "Variable Control Matrix" for each test.
- Do NOT guarantee specific percentage lifts; provide probability-based estimates.
- Maintain a professional, optimization-focused tone.
 
Return ONLY valid JSON with this schema. No markdown wrapping:
 
{
  "strategic_overview": "A brief overview of the optimization strategy.",
  "tests": [
    {
      "test_id": "UT-001",
      "hypothesis": "If we [action], then [result] because [reason].",
      "element_to_change": "e.g., Hero CTA Button Text",
      "variation_details": "Description of the 'B' version",
      "success_metrics": ["Primary metric", "Secondary guardrail metrics"],
      "ice_score": {
        "impact": 0-10,
        "confidence": 0-10,
        "ease": 0-10,
        "total": 0-30
      },
      "variable_control": "How to ensure no other factors interfere.",
      "estimated_runtime_weeks": 2
    }
  ]
}
"""
 
def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def extract_json(response_content):
    """Attempts to robustly parse JSON out of an LLM response."""
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

def suggest_tests(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates advanced A/B test suggestions using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.4
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)
 
def save_outputs(data):
    with open("ab_test_suggestions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("ab_test_suggestions.txt", "w", encoding="utf-8") as f:
        f.write(f"A/B Testing Strategic Roadmap ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
 
        f.write(f"Strategic Overview: {data.get('strategic_overview', 'N/A')}\n\n")
 
        for i, test in enumerate(data.get("tests", []), start=1):
            f.write(f"--- Test {i}: {test.get('test_id')} ---\n")
            f.write(f"Hypothesis: {test.get('hypothesis')}\n")
            f.write(f"Element: {test.get('element_to_change')}\n")
            f.write(f"Variation: {test.get('variation_details')}\n")
            f.write(f"ICE Score: {test.get('ice_score', {}).get('total', 0)}/30 (I:{test.get('ice_score', {}).get('impact')} C:{test.get('ice_score', {}).get('confidence')} E:{test.get('ice_score', {}).get('ease')})\n")
            f.write(f"Success Metrics: {', '.join(test.get('success_metrics', []))}\n")
            f.write(f"Runtime: {test.get('estimated_runtime_weeks')} week(s)\n")
            f.write(f"Control: {test.get('variable_control')}\n\n")
 
def main():
    prompt_text = read_input()
    tests = suggest_tests(prompt_text)
    save_outputs(tests)
    print("A/B test suggestions generated successfully.")
 
if __name__ == "__main__":
    main()
