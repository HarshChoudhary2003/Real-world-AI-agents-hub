import json
import os
import sys
from openai import OpenAI
from datetime import date

# Safely initialize client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("❌ Error: OPENAI_API_KEY environment variable not found.")
    print('Please set your OPENAI_API_KEY.')
    print('Example: $env:OPENAI_API_KEY="your-key-here" (PowerShell) or set OPENAI_API_KEY="your-key" (CMD)')
    sys.exit(1)

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are an Elite Enterprise SEO Keyword Expansion Agent. Your sole purpose is to transform a seed keyword into a powerful, comprehensive list of SEO target phrases based on the user's specific content context.

Rules:
- Expand the seed keyword into highly relevant SEO terms.
- Group keywords logically by intent and purpose.
- Avoid keyword stuffing or spammy variations completely.
- Focus strictly on search relevance, clarity, and the provided content intent/audience.

Return ONLY valid JSON with this exact schema:

{
  "analysis": "A brief 1-sentence strategic summary on how you derived these keywords for the target audience.",
  "primary_keywords": ["keyword 1", "keyword 2"],
  "supporting_keywords": ["keyword 1", "keyword 2"],
  "long_tail_keywords": ["keyword 1", "keyword 2"],
  "question_keywords": ["question 1", "question 2"]
}
"""

def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def expand_keywords(prompt_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.4,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("keywords.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("keywords.txt", "w", encoding="utf-8") as f:
        f.write(f"SEO Keyword Expansion ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        
        analysis = data.pop("analysis", "No AI analysis provided.")
        f.write(f"🧠 AI Strategy Analysis:\n{analysis}\n\n")

        for section, items in data.items():
            f.write(section.replace("_", " ").title() + ":\n")
            for k in items:
                f.write(f"- {k}\n")
            f.write("\n")

def main():
    print("🚀 Initializing SEO Keyword Expansion generation...")
    prompt_text = read_input()
    keywords = expand_keywords(prompt_text)
    save_outputs(keywords)
    print("✨ SEO keyword expansion complete. Built `keywords.json` and `keywords.txt`.")
    print("\n🧠 Strategy:", keywords.get("analysis", ""))
    print("\n🌟 Primary Keywords:", ", ".join(keywords.get("primary_keywords", [])))

if __name__ == "__main__":
    main()
