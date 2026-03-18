import json
import os
from litellm import completion
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """
You are an Elite CRM Data Enrichment Agent for Enterprise Sales Teams.

Rules:
- Analyze the provided company/contact information and enrich it with actionable intelligence.
- Generate industry classification, company size estimates, technology stack guesses, and buying signals.
- Identify potential decision-makers' roles and engagement strategies.
- Provide concrete, data-driven enrichment — avoid vague or generic insights.
- Score the lead readiness from 1-10.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "enriched_profile": {
    "company_name": "Name of the company",
    "industry": "Classified industry vertical",
    "estimated_size": "Employee range estimate",
    "tech_stack_signals": ["Likely technologies used"],
    "buying_signals": ["Observed or inferred buying intent signals"],
    "pain_points": ["Likely business challenges"],
    "recommended_approach": "Tailored outreach strategy"
  },
  "decision_makers": [
    {
      "role": "Title/Role",
      "engagement_tip": "How to engage this persona"
    }
  ],
  "lead_score": 7,
  "enrichment_summary": "Brief strategic summary of findings"
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        return (
            "Company: Acme Corp\n"
            "Website: acmecorp.io\n"
            "Contact: Jane Doe, VP of Engineering\n"
            "Source: LinkedIn Inbound\n"
            "Notes: Expressed interest in AI automation tools"
        )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def enrich_crm(prompt_text, model="openai/gpt-4o-mini", api_key=None, provider="openai"):
    """Enrich CRM data using any LLM provider via litellm."""
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

    json_path = os.path.join(base_path, "crm_enrichment.json")
    txt_path = os.path.join(base_path, "crm_enrichment.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"CRM Data Enrichment Report ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        profile = data.get("enriched_profile", {})
        f.write(f"Company: {profile.get('company_name', 'N/A')}\n")
        f.write(f"Industry: {profile.get('industry', 'N/A')}\n")
        f.write(f"Size: {profile.get('estimated_size', 'N/A')}\n\n")

        f.write("Tech Stack Signals:\n")
        for tech in profile.get("tech_stack_signals", []):
            f.write(f"  - {tech}\n")

        f.write("\nBuying Signals:\n")
        for signal in profile.get("buying_signals", []):
            f.write(f"  - {signal}\n")

        f.write("\nPain Points:\n")
        for pain in profile.get("pain_points", []):
            f.write(f"  - {pain}\n")

        f.write(f"\nRecommended Approach:\n  {profile.get('recommended_approach', 'N/A')}\n\n")

        f.write("Decision Makers:\n")
        for dm in data.get("decision_makers", []):
            f.write(f"  - {dm.get('role', 'Unknown')}: {dm.get('engagement_tip', '')}\n")

        f.write(f"\nLead Score: {data.get('lead_score', 'N/A')}/10\n")
        f.write(f"\nSummary: {data.get('enrichment_summary', 'N/A')}\n")

def main():
    print("🚀 CRM Data Enrichment Agent starting...")
    prompt_text = read_input()
    result = enrich_crm(prompt_text, model="openai/gpt-4o-mini")
    if result:
        save_outputs(result)
        print("✨ CRM enrichment complete. Built `crm_enrichment.json` and `crm_enrichment.txt`.")
        print(f"\n📊 Lead Score: {result.get('lead_score', 'N/A')}/10")
        print(f"📋 Summary: {result.get('enrichment_summary', '')}")
    else:
        print("❌ Failed to enrich CRM data.")

if __name__ == "__main__":
    main()
