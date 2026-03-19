import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a highly sophisticated, multi-dimensional Ad Copy Strategy Agent (AdForge AI v2.0).
 
Rules:
- Generate copy that leverages deep consumer psychology (e.g., Loss Aversion, Social Proof, Curiosity Gaps)
- Tailor copy specifically for the stated platform's technical constraints and cultural nuances
- Provide multiple strategic variations ranging from "Direct Response" to "Story-Driven"
- Perform "Buyer Persona Simulations": predict how specific target roles will react to the copy
- Include high-impact Viral Hooks and clear, multi-stage CTAs
 
Return ONLY valid JSON with this schema. No markdown wrapping:
 
{
  "headlines": ["3-5 high-engagement headlines"],
  "primary_copy_variations": [
    {
      "variation_name": "Strategic Angle (e.g., Problem-Agitate-Solve)",
      "text": "Full ad text",
      "viral_hook": "The specific opening hook meant to stop the scroll"
    }
  ],
  "persona_simulations": [
    {
      "persona": "Target Role/Persona Name",
      "likely_reaction": "How they might perceive the ad",
      "perceived_value": "The specific core benefit they will latch onto"
    }
  ],
  "calls_to_action": ["List of 3-5 distinct CTAs"],
  "image_text_overlays": ["Text ideas for accompanying visuals"]
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
    """Generates advanced ad copy strategy using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.6
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
        f.write(f"Advanced Ad Identity Strategy ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
 
        f.write("Headlines:\n")
        for h in data.get("headlines", []):
            f.write(f"- {h}\n")
 
        f.write("\nStrategic Identity Variants:\n")
        for p in data.get("primary_copy_variations", []):
            f.write(f"[{p.get('variation_name')}]\nHook: {p.get('viral_hook')}\n{p.get('text')}\n\n")
 
        f.write("Persona Feedback Simulations:\n")
        for ps in data.get("persona_simulations", []):
            f.write(f"- {ps.get('persona')}: {ps.get('likely_reaction')} (Value: {ps.get('perceived_value')})\n")
            
        f.write("\nCalls to Action:\n")
        for c in data.get("calls_to_action", []):
            f.write(f"- {c}\n")
        
        f.write("\nVisual Overlays:\n")
        for v in data.get("image_text_overlays", []):
            f.write(f"- {v}\n")
 
def main():
    prompt_text = read_input()
    ad_copy = generate_ad_copy(prompt_text)
    save_outputs(ad_copy)
    print("Advanced ad copy architecture completed successfully.")
 
if __name__ == "__main__":
    main()
