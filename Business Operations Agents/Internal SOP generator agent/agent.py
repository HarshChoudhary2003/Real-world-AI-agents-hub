import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly efficient Internal SOP (Standard Operating Procedure) Generator Agent.
 
Rules:
- Generate clear, step-by-step SOPs that are easy to follow
- Do NOT invent or hallucinate processes; stay strictly within provided data
- Use neutral, objective instructional language (imperative mood)
- Explicitly define Roles, Scope, and verification checks
 
Return ONLY valid JSON with this schema. No markdown wrapping, no extra text:
 
{
  "title": "Clear process name",
  "purpose": "Why this process exists",
  "scope": "What this procedure covers and what it does not",
  "roles_and_responsibilities": ["List of roles and what they do"],
  "procedure_steps": ["Step 1 description", "Step 2 description with check"],
  "review_notes": "Structural observations or potential areas for improvement"
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

def generate_sop(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates an SOP using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.25
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)
 
def save_outputs(data):
    with open("sop.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("sop.txt", "w", encoding="utf-8") as f:
        f.write(f"SOP Document ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
 
        f.write(f"Title: {data.get('title', 'N/A')}\n\n")
        f.write(f"Purpose:\n{data.get('purpose', 'N/A')}\n\n")
        f.write(f"Scope:\n{data.get('scope', 'N/A')}\n\n")
 
        f.write("Roles & Responsibilities:\n")
        for r in data.get("roles_and_responsibilities", []):
            f.write(f"- {r}\n")
 
        f.write("\nProcedure Steps:\n")
        for i, step in enumerate(data.get("procedure_steps", []), start=1):
            f.write(f"{i}. {step}\n")
 
        f.write(f"\nReview Notes:\n{data.get('review_notes', 'N/A')}\n")
 
def main():
    prompt_text = read_input()
    sop = generate_sop(prompt_text)
    save_outputs(sop)
    print("Internal SOP generated successfully.")
 
if __name__ == "__main__":
    main()
