import json
from openai import OpenAI
from datetime import date
from dotenv import load_dotenv
import os

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

client = OpenAI()  # requires OPENAI_API_KEY
 
SYSTEM_PROMPT = """
You are a Contract Clause Explanation Agent.
 
Rules:
- Explain clauses in plain language
- Preserve original legal meaning
- Do NOT provide legal advice
- Highlight obligations and risks
 
Return ONLY valid JSON with this schema:
 
{
  "plain_language_explanation": "",
  "obligations_and_rights": [],
  "practical_implications": [],
  "risks_or_watchouts": []
}
"""
 
def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def explain_clause(prompt_text):
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
    with open("clause_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("clause_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"Contract Clause Explanation ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
 
        f.write("Explanation:\n")
        f.write(data["plain_language_explanation"] + "\n\n")
 
        f.write("Obligations & Rights:\n")
        for o in data["obligations_and_rights"]:
            f.write(f"- {o}\n")
 
        if data.get("practical_implications"):
            f.write("\nPractical Implications:\n")
            for p in data["practical_implications"]:
                f.write(f"- {p}\n")
 
        if data.get("risks_or_watchouts"):
            f.write("\nRisks / Watch-outs:\n")
            for r in data["risks_or_watchouts"]:
                f.write(f"- {r}\n")
 
def main():
    prompt_text = read_input()
    explanation = explain_clause(prompt_text)
    save_outputs(explanation)
    print("Contract clause explained successfully.")
 
if __name__ == "__main__":
    main()
