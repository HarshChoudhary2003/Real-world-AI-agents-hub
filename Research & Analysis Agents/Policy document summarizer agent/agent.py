import json
from openai import OpenAI
from datetime import date
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
# Requires OPENAI_API_KEY in .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a Policy Document Summarizer Agent.

Rules:
- Summarize policies clearly and neutrally.
- Preserve legal and regulatory intent without adding interpretation.
- Avoid offering advice or subjective opinions.
- Highlight the scope of the policy and specific obligations mentioned.
- Identify any potential limitations or ambiguities in the text.

Return ONLY valid JSON with this schema:
{
  "overview": "A high-level summary of the policy's purpose",
  "scope": "Who and what the policy applies to",
  "key_requirements": ["Requirement 1", "Requirement 2"],
  "implications": ["Implication 1", "Implication 2"],
  "limitations_or_ambiguities": ["Limitation 1", "Ambiguity 2"]
}
"""

def read_input(path="input.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No policy text found. Please provide an input.txt file."

def summarize_policy(prompt_text):
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.25,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    # Save JSON output
    with open("policy_summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Save Text output
    with open("policy_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Policy Summary ({date.today()})\n")
        f.write("=" * 55 + "\n\n")

        f.write("Overview:\n")
        f.write(data["overview"] + "\n\n")

        f.write("Scope:\n")
        f.write(data["scope"] + "\n\n")

        f.write("Key Requirements:\n")
        for r in data["key_requirements"]:
            f.write(f"- {r}\n")

        if data.get("implications"):
            f.write("\nImplications:\n")
            for i in data["implications"]:
                f.write(f"- {i}\n")

        if data.get("limitations_or_ambiguities"):
            f.write("\nLimitations / Ambiguities:\n")
            for l in data["limitations_or_ambiguities"]:
                f.write(f"- {l}\n")

def main():
    print("Reading policy input...")
    prompt_text = read_input()
    
    if prompt_text.startswith("No policy text"):
        print(prompt_text)
        return

    try:
        print("Summarizing policy...")
        summary = summarize_policy(prompt_text)
        
        print("Saving outputs...")
        save_outputs(summary)
        print("Policy document summary generated successfully.")
        print("Outputs saved to policy_summary.json and policy_summary.txt")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
