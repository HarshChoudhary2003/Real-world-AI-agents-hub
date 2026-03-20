import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Direct-Response Copywriting Agent (Email-Mind AI v3.0).

Mission: Generate high-conversion email marketing copy using psychological triggers and industry-standard frameworks (AIDA, PAS).

Copywriting Rules:
1. **Psychic Hooks**: Subject lines should leverage curiosity, scarcity, or high-value benefits.
2. **Contextual Fluency**: Tailor the tone of voice precisely to the campaign goal and audience segment.
3. **Structured Flow**: Use clear headers, bullet points, and high-impact CTAs.
4. **Behavioral Triggers**: Suggest specific behavioral triggers for automated sequences (e.g., 'Trigger on link click').

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "subject_line_options": [
     {"type": "Curiosity/Gap", "text": "Subject line text"},
     {"type": "Benefit-Driven", "text": "Subject line text"},
     {"type": "Scarcity/Urgency", "text": "Subject line text"}
  ],
  "preview_text": "Engaging snippet for inbox preview",
  "email_content": {
     "salutation": "Salutation line",
     "body": "The core body copy (Markdown-formatted)",
     "footer": "Sign-off and footer text"
  },
  "call_to_action": {
     "text": "The specific button/link text",
     "logic": "The strategic reason for this specific CTA"
  },
  "copywriting_framework_used": "e.g., PAS (Problem-Agitation-Solution)",
  "psychological_triggers": ["List of triggers leveraged"]
}
"""

def read_input(path="input.txt"):
    """Reads input data from a local text file."""
    if not os.path.exists(path):
        return "Goal: Re-engage users. Audience: Inactive trial users. Offer: New templates."
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

def generate_email_strategy(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates advanced email strategy and copy using LiteLLM."""
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
    """Saves the email strategy as JSON and formatted TXT."""
    with open("email_marketing.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("email_marketing.txt", "w", encoding="utf-8") as f:
        f.write(f"Advanced Email Marketing Strategy ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        f.write("Subject Line Options:\n")
        for s in data.get("subject_line_options", []):
            f.write(f"[{s.get('type')}]: {s.get('text')}\n")
        
        f.write(f"\nPreview Text: {data.get('preview_text')}\n\n")

        ec = data.get("email_content", {})
        f.write(f"--- Email Body Content ---\n")
        f.write(f"{ec.get('salutation')}\n\n")
        f.write(f"{ec.get('body')}\n\n")
        f.write(f"{ec.get('footer')}\n\n")

        cta = data.get("call_to_action", {})
        f.write(f"Call to Action: {cta.get('text')}\n")
        f.write(f"Strategy: {cta.get('logic')}\n\n")

        f.write(f"Framework: {data.get('copywriting_framework_used')}\n")
        f.write(f"Triggers: {', '.join(data.get('psychological_triggers', []))}")

def main():
    print("🚀 Email-Mind AI: Synthesizing High-Conversion Copy...")
    prompt_text = read_input()
    try:
        strategy = generate_email_strategy(prompt_text)
        save_outputs(strategy)
        print("✅ Email marketing architecture completed successfully.")
        print("📁 Outputs: email_marketing.json, email_marketing.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
