import json
from openai import OpenAI
from datetime import date
import os

# Use environment variable or default to OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an Academic Paper Explainer Agent.

Rules:
- Explain academic research clearly and accurately
- Preserve meaning, nuance, and limitations
- Avoid speculation or exaggeration
- Adapt explanation to non-expert readers

Return ONLY valid JSON with this schema:

{
  "summary": "",
  "research_question": "",
  "methodology": "",
  "key_findings": [],
  "implications": [],
  "limitations": []
}
"""

def read_input(path="input.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Paper Title: Example Research on AI Agents\nAbstract: This paper investigates the use of autonomous AI agents in enterprise workflows."

def explain_paper(prompt_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini", # Corrected from gpt-4.1-mini
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("paper_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("paper_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"Academic Paper Explanation ({date.today()})\n")
        f.write("=" * 55 + "\n\n")

        f.write("Summary:\n")
        f.write(data["summary"] + "\n\n")

        f.write("Research Question:\n")
        f.write(data["research_question"] + "\n\n")

        f.write("Methodology:\n")
        f.write(data["methodology"] + "\n\n")

        f.write("Key Findings:\n")
        for k in data["key_findings"]:
            f.write(f"- {k}\n")

        f.write("\nImplications:\n")
        for i in data["implications"]:
            f.write(f"- {i}\n")

        f.write("\nLimitations:\n")
        for l in data["limitations"]:
            f.write(f"- {l}\n")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    print("Reading input.txt...")
    prompt_text = read_input()
    
    print("Generating explanation...")
    explanation = explain_paper(prompt_text)
    
    print("Saving outputs...")
    save_outputs(explanation)
    print("Academic paper explanation generated successfully.")

if __name__ == "__main__":
    main()
