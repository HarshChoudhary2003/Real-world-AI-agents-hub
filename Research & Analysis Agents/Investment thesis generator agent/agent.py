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
You are an Investment Thesis Generator Agent.

Rules:
- Build structured, balanced, and evidence-driven investment theses.
- Clearly separate rationale, assumptions, and catalysts.
- Explicitly surface risks and potential failure modes.
- Avoid hype, speculative predictions, or financial advice.
- Maintain a professional, analytical tone.

Return ONLY valid JSON with this schema:
{
  "thesis_summary": "High-level summary of the investment core idea",
  "rationale": "Detailed logical explanation for the investment",
  "catalysts": ["Catalyst 1", "Catalyst 2"],
  "risks": ["Risk 1", "Risk 2"],
  "conclusion": "Final synthesis aligning with the investment horizon"
}
"""

def read_input(path="input.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Asset: NVIDIA\nSector: Technology\nHorizon: 5 years\nRisk: High"

def generate_thesis(prompt_text):
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    # Save JSON output
    with open("investment_thesis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Save Text output
    with open("investment_thesis.txt", "w", encoding="utf-8") as f:
        f.write(f"Investment Thesis ({date.today()})\n")
        f.write("=" * 55 + "\n\n")

        f.write("Thesis Summary:\n")
        f.write(data["thesis_summary"] + "\n\n")

        f.write("Rationale:\n")
        f.write(data["rationale"] + "\n\n")

        f.write("Key Catalysts:\n")
        for c in data["catalysts"]:
            f.write(f"- {c}\n")

        f.write("\nKey Risks:\n")
        for r in data["risks"]:
            f.write(f"- {r}\n")

        f.write("\nConclusion:\n")
        f.write(data["conclusion"] + "\n")

def main():
    print("Reading investment context...")
    prompt_text = read_input()
    
    try:
        print("Generating investment thesis...")
        thesis = generate_thesis(prompt_text)
        
        print("Saving outputs...")
        save_outputs(thesis)
        print("Investment thesis generated successfully.")
        print("Outputs saved to investment_thesis.json and investment_thesis.txt")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
