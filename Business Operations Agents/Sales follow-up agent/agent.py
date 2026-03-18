import json
import os
from litellm import completion
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """
You are an Elite Sales Follow-Up Agent.

Rules:
- Reference prior interaction intelligently
- Be professional and consultative
- Include a clear next step
- Avoid pressure tactics and urgency inflation
- Ensure the tone matches the context provided

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "opening": "Professional opening greeting",
  "interaction_reference": "Reference to the previous discussion/interaction",
  "value_reinforcement": "Reiteration of value and context",
  "call_to_action": "Clear next step",
  "closing": "Professional closing"
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        return (
            "Previous Interaction:\n"
            "Demo call discussing workflow automation use cases.\n\n"
            "Prospect Role: Director of Operations\n"
            "Follow-Up Objective: Schedule next technical deep-dive\n"
            "Tone: Professional and consultative\n"
        )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_followup(prompt_text, model="openai/gpt-4o-mini", api_key=None, provider="openai"):
    """Generate follow-up message using any LLM provider via litellm."""
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
            temperature=0.35,
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

    json_path = os.path.join(base_path, "sales_followup.json")
    txt_path = os.path.join(base_path, "sales_followup.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Sales Follow-Up Draft ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"{data.get('opening', '')}\n\n")
        f.write(f"{data.get('interaction_reference', '')}\n\n")
        f.write(f"{data.get('value_reinforcement', '')}\n\n")
        f.write(f"Next Step:\n{data.get('call_to_action', '')}\n\n")
        f.write(f"{data.get('closing', '')}\n")

def main():
    print("🚀 Sales Follow-up Agent starting...")
    prompt_text = read_input()
    # Using gpt-4o-mini for efficient generation, falling back to basic litellm logic
    followup = generate_followup(prompt_text, model="openai/gpt-4o-mini")
    if followup:
        save_outputs(followup)
        print("✨ Sales follow-up generated successfully. Built `sales_followup.json` and `sales_followup.txt`.")
    else:
        print("❌ Failed to generate follow-up message.")

if __name__ == "__main__":
    main()
