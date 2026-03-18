import json
from openai import OpenAI
from datetime import date
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an Advanced Policy Intelligence Agent. Your goal is to deconstruct complex regulatory frameworks and enterprise policies into high-fidelity, actionable intelligence.

Rules:
1. Neutrality: Maintain absolute objectivity. Do not offer legal advice or subjective interpretations.
2. Precision: Preserve the exact legal and regulatory intent.
3. Transparency: Highlight sections that are intentionally or unintentionally vague.
4. Schema: You must return ONLY valid JSON matching the specified schema.

Analysis Schema:
{
  "metadata": {
    "policy_title": "Official title or descriptive name",
    "jurisdiction": "Governing law or geographic scope",
    "effective_date": "Date of enforcement",
    "issuer": "Organization or Regulatory Body"
  },
  "summary": {
    "executive_overview": "High-level summary for leadership",
    "detailed_scope": "Comprehensive definition of applicable entities/data"
  },
  "compliance_framework": {
    "core_obligations": ["Requirement 1", "Requirement 2"],
    "primary_stakeholders": ["Who is affected", "Department roles"],
    "critical_deadlines": ["Dates", "Milestones"]
  },
  "risk_intelligence": {
    "perceived_risk_level": "Low | Medium | High",
    "quantified_risk_score": 0-100,
    "operational_threats": ["Risks of non-compliance", "Conflict areas"],
    "ambiguity_index": ["Sections that require legal clarification"]
  },
  "strategic_implications": ["Impact on culture", "Cost of compliance", "Long-term outlook"]
}
"""

def read_input(path="input.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

def analyze_policy(text):
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY missing.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    # Save JSON
    with open("policy_intelligence.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Save Text Report
    with open("policy_intelligence.txt", "w", encoding="utf-8") as f:
        m = data["metadata"]
        f.write(f"ADVANCED POLICY INTELLIGENCE REPORT: {m['policy_title']}\n")
        f.write("=" * 60 + "\n")
        f.write(f"Issuer: {m['issuer']} | Jurisdiction: {m['jurisdiction']}\n")
        f.write(f"Effective Date: {m['effective_date']} | Generated: {date.today()}\n\n")

        f.write("EXECUTIVE SUMMARY\n" + "-"*17 + "\n")
        f.write(data["summary"]["executive_overview"] + "\n\n")

        f.write("COMPLIANCE OBLIGATIONS\n" + "-"*22 + "\n")
        for req in data["compliance_framework"]["core_obligations"]:
            f.write(f"• {req}\n")
        f.write("\n")

        f.write("RISK PROFILE\n" + "-"*12 + "\n")
        f.write(f"Level: {data['risk_intelligence']['perceived_risk_level']} (Score: {data['risk_intelligence']['quantified_risk_score']}/100)\n")
        for threat in data["risk_intelligence"]["operational_threats"]:
            f.write(f"- {threat}\n")
        
        if data["risk_intelligence"]["ambiguity_index"]:
            f.write("\nAmbiguities Identified:\n")
            for amb in data["risk_intelligence"]["ambiguity_index"]:
                f.write(f"- {amb}\n")

def main():
    print("Initializing Intelligence Agent...")
    text = read_input()
    if not text:
        print("Error: input.txt not found.")
        return

    try:
        print("Synthesizing policy data...")
        intelligence = analyze_policy(text)
        save_outputs(intelligence)
        print("Intelligence extraction complete. Check policy_intelligence.json/txt")
    except Exception as e:
        print(f"Agent Fault: {str(e)}")

if __name__ == "__main__":
    main()
