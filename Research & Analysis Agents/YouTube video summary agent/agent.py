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
You are a YouTube Video Summary Agent.

Rules:
- Summarize video content clearly and faithfully
- Remove filler and repetition
- Preserve key ideas and structure
- Avoid personal interpretation

Return ONLY valid JSON with this schema:
{
  "overview": "",
  "key_points": [],
  "examples_or_insights": [],
  "final_takeaway": ""
}
"""

def read_input(path="input.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Video Title: Introduction to AI Agents\nTranscript: AI agents are systems that can act autonomously toward goals."

def summarize_video(prompt_text):
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
    with open("video_summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("video_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"YouTube Video Summary ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        f.write("Overview:\n")
        f.write(data["overview"] + "\n\n")

        f.write("Key Points:\n")
        for p in data["key_points"]:
            f.write(f"- {p}\n")

        if data["examples_or_insights"]:
            f.write("\nExamples / Insights:\n")
            for e in data["examples_or_insights"]:
                f.write(f"- {e}\n")

        f.write("\nFinal Takeaway:\n")
        f.write(data["final_takeaway"] + "\n")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    print("Reading input.txt...")
    prompt_text = read_input()
    
    print("Generating summary...")
    summary = summarize_video(prompt_text)
    
    print("Saving outputs...")
    save_outputs(summary)
    print("YouTube video summary generated successfully.")

if __name__ == "__main__":
    main()
