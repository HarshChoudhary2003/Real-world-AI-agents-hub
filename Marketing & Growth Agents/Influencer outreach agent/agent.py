import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Influencer Relations & Outreach Agent (Influence-Core AI v2.0).

Mission: Architect highly personalized, relationship-first outreach strategies for high-impact influencers.

Rules for Outreach Logic:
1. **Value-First Reciprocity**: Focus on what's in it for the influencer and their community. Avoid transactional or entitled language.
2. **Platform Context**: Tailor the style and length to the platform (e.g., professional/longer for LinkedIn, punchy/visual for IG/X).
3. **Low-Friction CTA**: Always suggest a "low-stakes" first interaction (e.g., a 10m introductory chat or simply a "Does this sound interesting?" query).
4. **Authenticity Anchors**: Identify specific areas for personalization based on the influencer's focus area.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "subject_line": "For email/LinkedIn subject",
  "outreach_strategy": {
     "platform_style_description": "Explanation of the platform tailoring",
     "reciprocity_angle": "The unique value proposition (UVP) for the influencer"
  },
  "messages": [
     {
       "variant_name": "Full Professional Outreach",
       "composition": {
          "greeting": "Personalized greeting",
          "opening": "The personalization hook",
          "value_proposition": "The brand context and mutual value",
          "proposal": "The collaboration idea",
          "call_to_action": "The specific next step",
          "closing": "Sign-off"
       }
     },
     {
       "variant_name": "Concise/Direct Message",
       "full_text": "A punchier, shortened version for chat-based platforms"
     }
  ],
  "follow_up_logic": "Strategy for when and how to follow up if no response",
  "psychological_anchors": ["List of hooks used (e.g., Social Proof, Authority, Reciprocity)"]
}
"""

def read_input(path="input.txt"):
    """Reads input data from a local text file."""
    if not os.path.exists(path):
        return "Brand: AI Platform. Goal: Promotion. Influencer: Ops Specialist. Platform: LinkedIn."
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

def generate_outreach_strategy(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates influencer outreach strategy and messages using LiteLLM."""
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
    """Saves the outreach strategy as JSON and formatted TXT."""
    with open("influencer_outreach.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("influencer_outreach.txt", "w", encoding="utf-8") as f:
        f.write(f"Influence-Core v2.0 Outreach Strategy ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Subject Line: {data.get('subject_line')}\n")
        
        f.write("\n--- Strategic Foundation ---\n")
        f.write(f"Style: {data.get('outreach_strategy', {}).get('platform_style_description')}\n")
        f.write(f"Value Angle: {data.get('outreach_strategy', {}).get('reciprocity_angle')}\n\n")

        for variant in data.get("messages", []):
            f.write(f"[{variant.get('variant_name')}]\n")
            if 'composition' in variant:
                comp = variant.get('composition')
                f.write(f"{comp.get('greeting')}\n\n")
                f.write(f"{comp.get('opening')}\n\n")
                f.write(f"{comp.get('value_proposition')}\n\n")
                f.write(f"{comp.get('proposal')}\n\n")
                f.write(f"{comp.get('call_to_action')}\n\n")
                f.write(f"{comp.get('closing')}\n\n")
            else:
                f.write(f"{variant.get('full_text')}\n\n")

        f.write(f"Follow-up Logic:\n{data.get('follow_up_logic')}\n\n")
        f.write(f"Hooks Leveraged: {', '.join(data.get('psychological_anchors', []))}")

def main():
    print("🚀 Influence-Core AI: Architecting Relationship Strategy...")
    prompt_text = read_input()
    try:
        strategy = generate_outreach_strategy(prompt_text)
        save_outputs(strategy)
        print("✅ Influencer outreach architecture completed successfully.")
        print("📁 Outputs: influencer_outreach.json, influencer_outreach.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
