import json
import os
import litellm
import traceback
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Data Privacy Explanation Agent.

Rules:
- Explain specific privacy regulations and concepts clearly based on the provided scenario.
- Preserve the exact regulatory intent (e.g., GDPR, CCPA, HIPAA).
- Do NOT provide binding legal advice; always act as a compliance explainer.
- Focus strictly on practical understanding, obligations, and individual rights.

Return ONLY valid JSON with this exact schema:
{
  "explanation": "Clear, plain-English explanation of how the regulation applies to the scenario",
  "key_obligations": ["List of what the company must do to comply"],
  "individual_rights": ["List of what rights the end-user has in this scenario"],
  "practical_implications": ["Actionable engineering or business steps required"]
}
"""

def read_input(path: str = "privacy_input.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Scenario: Collecting email addresses for a marketing newsletter from EU users.\nRegulation: GDPR")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_json(content_raw: str) -> dict:
    content = str(content_raw)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        start_idx = int(content.find("{"))
        end_idx = int(content.rfind("}")) + 1
        content_str = str(content)
        content = content_str[start_idx:end_idx]
    return json.loads(content)

def explain_privacy(text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Privacy Ordinance Explanation via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("privacy_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("privacy_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"Data Privacy Explanation Matrix ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        
        f.write("--- REGULATORY EXPLANATION ---\n")
        f.write(data.get("explanation", "No explanation extracted.") + "\n\n")
        
        f.write("--- KEY CORPORATE OBLIGATIONS ---\n")
        for o in data.get("key_obligations", []):
            f.write(f"- {o}\n")
            
        f.write("\n--- INDIVIDUAL USER RIGHTS ---\n")
        for r in data.get("individual_rights", []):
            f.write(f"- {r}\n")
            
        f.write("\n--- PRACTICAL IMPLICATIONS ---\n")
        for p in data.get("practical_implications", []):
            f.write(f"- {p}\n")

def main():
    print("🚀 Data Privacy Explanation Agent: Initiating Regulatory Core...")
    try:
        input_text = read_input()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        explanation = explain_privacy(input_text, model=model)
        save_outputs(explanation)
        
        print("✅ Data privacy explanation generated successfully.")
        print("📁 Outputs: privacy_explanation.json, privacy_explanation.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
