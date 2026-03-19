import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly creative and strategic Ad Copy Generator Agent.
 
Rules:
- Focus on tangible benefits and outcomes, not just technical features
- Match the copy specifically to the target platform (e.g., character limits, tone) and audience persona
- Provide multiple high-impact variations (A/B testing ready)
- Include clear, compelling calls-to-action (CTAs)
- Ensure the tone remains consistent with the brand's voice
 
Return ONLY valid JSON with this schema. No markdown wrapping, no extra text:
 
{
  "headlines": ["List of 3-5 punchy headlines"],
  "primary_copy_variations": [
    {
      "variation_name": "e.g., Benefit-Driven, Problem-Solution, Social Proof",
      "text": "The full ad copy text"
    }
  ],
  "calls_to_action": ["List of 3-5 distinct CTAs"]
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

def generate_ad_copy(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates ad copy variations using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.5
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)
 
def save_outputs(data):
    with open("ad_copy.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("ad_copy.txt", "w", encoding="utf-8") as f:
        f.write(f"Ad Copy Variations ({date.today()})\n")
        f.write("=" * 50 + "\n\n")
 
        f.write("Headlines:\n")
        for h in data.get("headlines", []):
            f.write(f"- {h}\n")
 
        f.write("\nPrimary Copy Variations:\n")
        for p in data.get("primary_copy_variations", []):
            f.write(f"[{p.get('variation_name')}]\n{p.get('text')}\n\n")
 
        f.write("Calls to Action:\n")
        for c in data.get("calls_to_action", []):
            f.write(f"- {c}\n")
 
def main():
    prompt_text = read_input()
    ad_copy = generate_ad_copy(prompt_text)
    save_outputs(ad_copy)
    print("Ad copy generated successfully.")
 
if __name__ == "__main__":
    main()
