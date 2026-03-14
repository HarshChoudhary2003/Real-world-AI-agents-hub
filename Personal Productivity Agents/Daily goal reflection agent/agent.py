import json
from datetime import date
from openai import OpenAI
import os

client = None
if os.getenv("OPENAI_API_KEY"):
    try:
        client = OpenAI()
    except Exception:
        pass

SYSTEM_PROMPT = """
You are a Daily Goal Reflection Agent.
 
Your task:
- Compare planned goals with actual outcomes
- Identify what was completed and what was missed
- Analyze reasons for misses
- Extract insights and lessons
- Provide 2–3 actionable suggestions for tomorrow
 
Return ONLY valid JSON with this exact schema:
 
{
  "summary": "",
  "completed_goals": [],
  "missed_goals": [],
  "insights": [],
  "lessons_learned": [],
  "tomorrow_suggestions": []
}
"""

def read_day(path="day.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def reflect(day_text):
    if client is None:
        raise ValueError("OpenAI client not initialized.")
        
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": day_text}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return json.loads(content)

def save_outputs(data):
    with open("reflection.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("reflection.txt", "w", encoding="utf-8") as f:
        f.write(f"Daily Reflection ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
 
        f.write("SUMMARY:\n")
        f.write(data.get("summary", "") + "\n\n")
 
        f.write("COMPLETED GOALS:\n")
        for g in data.get("completed_goals", []):
            f.write(f"- {g}\n")
 
        f.write("\nMISSED GOALS:\n")
        for g in data.get("missed_goals", []):
            f.write(f"- {g}\n")
 
        f.write("\nINSIGHTS:\n")
        for i in data.get("insights", []):
            f.write(f"- {i}\n")
 
        f.write("\nLESSONS LEARNED:\n")
        for l in data.get("lessons_learned", []):
            f.write(f"- {l}\n")
 
        f.write("\nSUGGESTIONS FOR TOMORROW:\n")
        for s in data.get("tomorrow_suggestions", []):
            f.write(f"- {s}\n")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set.")
        
    print("Reading daily notes...")
    day_text = read_day()
    
    print("Generating reflection...")
    try:
        reflection = reflect(day_text)
        save_outputs(reflection)
        print("Daily reflection generated successfully.")
        print(json.dumps(reflection, indent=2))
    except Exception as e:
        print(f"Error during reflection: {e}")

if __name__ == "__main__":
    main()
