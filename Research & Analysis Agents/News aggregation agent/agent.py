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
You are a News Aggregation Agent.

Rules:
- Aggregate and synthesize news objectively
- Group related stories by theme
- Avoid sensationalism or opinion
- Focus on relevance and clarity

Return ONLY valid JSON with this schema:

{
  "summary": "",
  "themes": [
    {
      "theme": "",
      "key_developments": []
    }
  ]
}
"""

def read_input(path="input.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Topics: AI, AI Ethics, Future of Work\nTime Window: Daily\nGeography: Global"

def aggregate_news(prompt_text):
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
    with open("news_digest.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("news_digest.txt", "w", encoding="utf-8") as f:
        f.write(f"News Digest ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        f.write("Summary:\n")
        f.write(data["summary"] + "\n\n")

        for t in data["themes"]:
            f.write(f"Theme: {t['theme']}\n")
            for d in t["key_developments"]:
                f.write(f"- {d}\n")
            f.write("\n")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    print("Reading input.txt...")
    prompt_text = read_input()
    
    print("Generating news digest...")
    digest = aggregate_news(prompt_text)
    
    print("Saving outputs...")
    save_outputs(digest)
    print("News aggregation completed successfully.")

if __name__ == "__main__":
    main()
