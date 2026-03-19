import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly analytical and objective Vendor Comparison Agent.
 
Rules:
- Compare vendors across provided criteria objectively
- Use consistent criteria for every vendor analyzed
- Highlight specific strengths, weaknesses, and structural trade-offs
- Avoid making final recommendations; provide the data for the user to decide
 
Return ONLY valid JSON with this schema. No markdown wrapping, no extra text:
 
{
  "summary": "High-level executive overview of the vendor landscape",
  "vendors": [
    {
      "name": "Vendor Name",
      "strengths": ["list", "of", "strengths"],
      "weaknesses": ["list", "of", "weaknesses"],
      "notes": "Specific observations or context"
    }
  ],
  "key_tradeoffs": ["List of core business trade-offs identified"]
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

def compare_vendors(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Analyzes the vendor data using LiteLLM."""
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
    with open("vendor_comparison.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("vendor_comparison.txt", "w", encoding="utf-8") as f:
        f.write(f"Vendor Comparison ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
 
        f.write("Summary:\n")
        f.write(data.get("summary", "N/A") + "\n\n")
 
        for v in data.get("vendors", []):
            f.write(f"Vendor: {v.get('name', 'N/A')}\n")
            f.write("Strengths:\n")
            for s in v.get("strengths", []):
                f.write(f"- {s}\n")
            f.write("Weaknesses:\n")
            for w in v.get("weaknesses", []):
                f.write(f"- {w}\n")
            f.write(f"Notes:\n{v.get('notes', 'N/A')}\n\n")
 
        f.write("Key Trade-offs:\n")
        for t in data.get("key_tradeoffs", []):
            f.write(f"- {t}\n")
 
def main():
    prompt_text = read_input()
    comparison = compare_vendors(prompt_text)
    save_outputs(comparison)
    print("Vendor comparison completed successfully.")
 
if __name__ == "__main__":
    main()
