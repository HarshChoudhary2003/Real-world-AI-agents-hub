import json
import os
from litellm import completion
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """
You are an Elite Customer Support Response Agent for Enterprise Teams.

Rules:
- Craft highly professional, empathetic, and clear customer support responses.
- Analyze the customer's tone, urgency, and core issue before responding.
- Match the appropriate tone (formal, friendly, apologetic, solution-focused).
- Provide actionable next steps and resolution paths.
- Include escalation recommendations when appropriate.
- Never use generic filler language or robotic templates.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "ticket_analysis": {
    "core_issue": "The primary customer problem",
    "sentiment": "Customer sentiment (frustrated, confused, urgent, neutral, positive)",
    "priority": "low | medium | high | critical",
    "category": "Category of the support ticket"
  },
  "response": {
    "subject_line": "Professional email subject line",
    "greeting": "Personalized opening",
    "body": "The main response body with empathy, acknowledgment, and solution",
    "next_steps": ["Array of concrete next steps"],
    "closing": "Professional closing statement"
  },
  "internal_notes": {
    "escalation_needed": false,
    "escalation_reason": "Why escalation is or isn't needed",
    "follow_up_date": "Suggested follow-up timeframe",
    "knowledge_base_tags": ["Tags for internal categorization"]
  }
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        return (
            "Customer: John Smith\n"
            "Email: john@example.com\n"
            "Subject: Billing issue — charged twice\n"
            "Message: Hi, I noticed I was charged twice for my subscription this month. "
            "I've been a loyal customer for 2 years and this is really frustrating. "
            "Can you please fix this ASAP? I need a refund for the duplicate charge.\n"
            "Product: Premium SaaS Platform\n"
            "Account Tier: Enterprise"
        )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_response(prompt_text, model="openai/gpt-4o-mini", api_key=None, provider="openai"):
    """Generate customer support response using any LLM provider via litellm."""
    try:
        if api_key:
            env_map = {
                "openai": "OPENAI_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "google": "GEMINI_API_KEY",
                "groq": "GROQ_API_KEY",
            }
            env_var = env_map.get(provider)
            if env_var:
                os.environ[env_var] = api_key

        response = completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.3,
            response_format={"type": "json_object"} if provider == "openai" else None
        )

        content = response.choices[0].message.content

        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif "```" in content:
            content = content.split("```")[1].replace("json", "").strip()

        return json.loads(content)
    except Exception as e:
        print(f"Error calling {model}: {e}")
        return None

def save_outputs(data, base_path="."):
    if not data:
        print("No data to save.")
        return

    json_path = os.path.join(base_path, "support_response.json")
    txt_path = os.path.join(base_path, "support_response.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Customer Support Response ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        analysis = data.get("ticket_analysis", {})
        f.write(f"Issue: {analysis.get('core_issue', 'N/A')}\n")
        f.write(f"Sentiment: {analysis.get('sentiment', 'N/A')}\n")
        f.write(f"Priority: {analysis.get('priority', 'N/A')}\n")
        f.write(f"Category: {analysis.get('category', 'N/A')}\n\n")

        resp = data.get("response", {})
        f.write(f"Subject: {resp.get('subject_line', '')}\n\n")
        f.write(f"{resp.get('greeting', '')}\n\n")
        f.write(f"{resp.get('body', '')}\n\n")

        f.write("Next Steps:\n")
        for step in resp.get("next_steps", []):
            f.write(f"  - {step}\n")

        f.write(f"\n{resp.get('closing', '')}\n\n")

        notes = data.get("internal_notes", {})
        f.write("--- Internal Notes ---\n")
        f.write(f"Escalation Needed: {notes.get('escalation_needed', False)}\n")
        f.write(f"Reason: {notes.get('escalation_reason', 'N/A')}\n")
        f.write(f"Follow-up: {notes.get('follow_up_date', 'N/A')}\n")
        f.write(f"Tags: {', '.join(notes.get('knowledge_base_tags', []))}\n")

def main():
    print("🚀 Customer Support Response Agent starting...")
    prompt_text = read_input()
    result = generate_response(prompt_text, model="openai/gpt-4o-mini")
    if result:
        save_outputs(result)
        analysis = result.get("ticket_analysis", {})
        print("✨ Response generated. Built `support_response.json` and `support_response.txt`.")
        print(f"\n🎯 Issue: {analysis.get('core_issue', '')}")
        print(f"⚡ Priority: {analysis.get('priority', '')}")
        print(f"💬 Sentiment: {analysis.get('sentiment', '')}")
    else:
        print("❌ Failed to generate support response.")

if __name__ == "__main__":
    main()
