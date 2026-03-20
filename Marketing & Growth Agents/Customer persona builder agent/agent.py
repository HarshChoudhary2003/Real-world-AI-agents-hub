import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Customer Research & Persona Strategy Agent (Persona-Forge AI v2.0).

Mission: Transform market data into deep, actionable customer personas that drive high-conversion marketing.

Rules for Strategy:
1. **Deeper Inference**: From "Manual workflows", infer "Cognitive Load" and "Decision Fatigue".
2. **Psychographic Depth**: Identify the core motivation (e.g., Security, Efficiency, Status).
3. **Actionable Hooks**: Provide messaging cues including specific power words and trust signals.
4. **Professional & Empathic**: Be data-driven but deeply empathetic to the user's struggle.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "persona_name": "Memorable, catchy persona name",
  "overview": "High-level summary of the persona's core identity",
  "archetype": "The market archetype (e.g., The Efficiency Chaser)",
  "demographics_and_role": "Detailed context on their role and background",
  "core_motivations": ["The 2-3 deep-seated drivers"],
  "fears_and_anxieties": ["What keeps them up at night?"],
  "goals": ["Strategic results they must achieve"],
  "pain_points": ["Specific friction points and blockers"],
  "messaging_strategy": {
    "hooks": ["Viral/Attention hooks"],
    "power_words": ["Specific vocabulary they resonate with"],
    "trust_signals": ["What they need for proof (e.g., case studies, security audits)"]
  },
  "buying_objections": ["3-5 reasons they might say NO and how to counter them"]
}
"""

def read_input(path="input.txt"):
    """Reads input data from a local text file."""
    if not os.path.exists(path):
        return "Product: Generic SaaS\nTarget: Mid-level managers\nData: High workload, low visibility."
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

def build_persona(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Synthesizes a customer persona using LiteLLM."""
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
    """Saves the persona data as JSON and formatted TXT."""
    with open("customer_persona.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("customer_persona.txt", "w", encoding="utf-8") as f:
        f.write(f"Advanced Customer Persona Strategy ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Persona Name: {data.get('persona_name')}\n")
        f.write(f"Archetype: {data.get('archetype', 'N/A')}\n\n")
        
        f.write(f"Overview:\n{data.get('overview')}\n\n")
        f.write(f"Context & Role:\n{data.get('demographics_and_role')}\n\n")

        f.write("Core Motivations:\n")
        for m in data.get("core_motivations", []):
            f.write(f"- {m}\n")

        f.write("\nGoals:\n")
        for g in data.get("goals", []):
            f.write(f"- {g}\n")

        f.write("\nPain Points & Friction:\n")
        for p in data.get("pain_points", []):
            f.write(f"- {p}\n")

        f.write("\nFears & Anxieties:\n")
        for f_ in data.get("fears_and_anxieties", []):
            f.write(f"- {f_}\n")

        f.write("\n--- Messaging Strategy ---\n")
        ms = data.get("messaging_strategy", {})
        f.write(f"Hooks: {', '.join(ms.get('hooks', []))}\n")
        f.write(f"Power Words: {', '.join(ms.get('power_words', []))}\n")
        f.write(f"Trust Signals: {', '.join(ms.get('trust_signals', []))}\n\n")

        f.write("Buying Objections:\n")
        for obj in data.get("buying_objections", []):
            f.write(f"- {obj}\n")

def main():
    print("🚀 Persona-Forge AI: Initializing Customer Persona Synthesis...")
    prompt_text = read_input()
    try:
        persona = build_persona(prompt_text)
        save_outputs(persona)
        print("✅ Customer persona architecture generated successfully.")
        print("📁 Outputs: customer_persona.json, customer_persona.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
