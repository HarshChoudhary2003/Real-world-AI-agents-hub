import json
import os
from litellm import completion
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """
You are an Elite Lead Qualification Agent for Enterprise Sales Teams.

Rules:
- Analyze the provided lead information and qualify them using the BANT framework (Budget, Authority, Need, Timeline).
- Score each lead on a 1-100 scale based on qualification strength.
- Classify leads as: Hot (80-100), Warm (50-79), Cool (25-49), or Cold (0-24).
- Identify red flags and green flags in the lead data.
- Provide a tailored next-action recommendation for the sales team.
- Be brutally honest — false positives waste sales resources.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "qualification": {
    "lead_name": "Lead contact name",
    "company": "Company name",
    "score": 75,
    "classification": "Hot | Warm | Cool | Cold",
    "bant": {
      "budget": {"score": 8, "assessment": "Budget assessment details"},
      "authority": {"score": 7, "assessment": "Authority assessment details"},
      "need": {"score": 9, "assessment": "Need assessment details"},
      "timeline": {"score": 6, "assessment": "Timeline assessment details"}
    }
  },
  "green_flags": ["Positive indicators"],
  "red_flags": ["Warning signals or concerns"],
  "recommended_action": "Specific next step for the sales team",
  "talking_points": ["Key discussion points for the next call"],
  "disqualification_risks": ["Factors that could disqualify this lead"],
  "summary": "Executive summary of the qualification"
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        return (
            "Lead: Sarah Chen, Director of Operations\n"
            "Company: GrowthTech Solutions (Series B, 150 employees)\n"
            "Source: Demo Request Form\n"
            "Budget: Mentioned they have $50K-$100K allocated for automation tools\n"
            "Notes: Urgently looking to reduce manual data entry. "
            "Currently evaluates 3 vendors. Decision expected within 6 weeks. "
            "Has authority to sign contracts up to $75K. "
            "Team of 25 operations staff who would use the tool daily."
        )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def qualify_lead(prompt_text, model="openai/gpt-4o-mini", api_key=None, provider="openai"):
    """Qualify a lead using any LLM provider via litellm."""
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
            temperature=0.25,
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

    json_path = os.path.join(base_path, "lead_qualification.json")
    txt_path = os.path.join(base_path, "lead_qualification.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Lead Qualification Report ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        qual = data.get("qualification", {})
        f.write(f"Lead: {qual.get('lead_name', 'N/A')}\n")
        f.write(f"Company: {qual.get('company', 'N/A')}\n")
        f.write(f"Score: {qual.get('score', 0)}/100\n")
        f.write(f"Classification: {qual.get('classification', 'N/A')}\n\n")

        bant = qual.get("bant", {})
        f.write("BANT Analysis:\n")
        for key in ["budget", "authority", "need", "timeline"]:
            item = bant.get(key, {})
            f.write(f"  {key.upper()} ({item.get('score', 'N/A')}/10): {item.get('assessment', '')}\n")

        f.write("\nGreen Flags:\n")
        for flag in data.get("green_flags", []):
            f.write(f"  ✅ {flag}\n")

        f.write("\nRed Flags:\n")
        for flag in data.get("red_flags", []):
            f.write(f"  🔴 {flag}\n")

        f.write(f"\nRecommended Action:\n  {data.get('recommended_action', 'N/A')}\n")

        f.write("\nTalking Points:\n")
        for tp in data.get("talking_points", []):
            f.write(f"  • {tp}\n")

        f.write(f"\nSummary: {data.get('summary', 'N/A')}\n")

def main():
    print("🚀 Lead Qualification Agent starting...")
    prompt_text = read_input()
    result = qualify_lead(prompt_text, model="openai/gpt-4o-mini")
    if result:
        save_outputs(result)
        qual = result.get("qualification", {})
        print("✨ Qualification complete. Built `lead_qualification.json` and `lead_qualification.txt`.")
        print(f"\n🎯 Score: {qual.get('score', 0)}/100")
        print(f"🏷️ Classification: {qual.get('classification', 'N/A')}")
        print(f"📋 Summary: {result.get('summary', '')}")
    else:
        print("❌ Failed to qualify lead.")

if __name__ == "__main__":
    main()
