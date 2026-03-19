import json
import re
from datetime import date
from dotenv import load_dotenv
import os
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly advanced, enterprise-grade Contract Clause Explanation Agent.
 
Rules:
- Explain clauses in sophisticated yet plain language
- Diligently preserve the original legal meaning
- Do NOT provide formal legal advice, only structural translation
- Highlight latent obligations, implicit rights, and hidden risks
 
Output your response STRICTLY as a valid JSON object matching this schema. NO markdown wrapping, NO additional text before or after:
 
{
  "plain_language_explanation": "String explaining the core mechanics",
  "obligations_and_rights": ["List of strings detailing obligations/rights"],
  "practical_implications": ["List of strings detailing real-world outcomes"],
  "risks_or_watchouts": ["List of strings detailing risks or pitfalls"]
}
"""
 
def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def extract_json(response_content):
    """Attempts to robustly parse JSON out of an LLM response."""
    try:
        # Direct parse
        return json.loads(response_content)
    except json.JSONDecodeError:
        # Try stripping markdown blocks
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", response_content)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except:
                pass
        
        # Try finding anything between braces
        match = re.search(r"\{[\s\S]*\}", response_content)
        if match:
            try:
                return json.loads(match.group(0).strip())
            except:
                pass
        
    raise ValueError("Failed to extract valid JSON from the model's response.")

def explain_clause(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """
    Analyzes the contract clause using the specified LiteLLM model.
    Models supported: gpt-4o, claude-3-5-sonnet-20240620, gemini/gemini-1.5-pro, groq/llama3-70b-8192, etc.
    """
    # Use litellm.completion to dynamically route to the correct provider
    # Some providers may require strict structural prompting, so we rely on the robust JSON extractor.
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.25,
    }
    
    # If explicitly passed, override the environment variables cleanly
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)
 
def save_outputs(data):
    with open("clause_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("clause_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"Contract Clause Explanation ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
 
        f.write("Explanation:\n")
        f.write(data.get("plain_language_explanation", "") + "\n\n")
 
        f.write("Obligations & Rights:\n")
        for o in data.get("obligations_and_rights", []):
            f.write(f"- {o}\n")
 
        if data.get("practical_implications"):
            f.write("\nPractical Implications:\n")
            for p in data["practical_implications"]:
                f.write(f"- {p}\n")
 
        if data.get("risks_or_watchouts"):
            f.write("\nRisks / Watch-outs:\n")
            for r in data["risks_or_watchouts"]:
                f.write(f"- {r}\n")
 
def main():
    prompt_text = read_input()
    explanation = explain_clause(prompt_text)
    save_outputs(explanation)
    print("Contract clause explained successfully.")
 
if __name__ == "__main__":
    main()
