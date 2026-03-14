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
You are a Meeting Agenda Generator Agent.
 
Your job is to generate a clear, time-boxed meeting agenda.
 
Rules:
- Agenda must fit within the provided duration
- Focus on the meeting objective
- Include time allocation for each item
- Identify decision points where applicable
- Auto-assign owners from the participant list context
- Return ONLY valid JSON with this exact schema:
 
{
  "meeting_title": "",
  "objective": "",
  "total_duration_minutes": 0,
  "agenda": [
    {
      "topic": "",
      "time_minutes": 0,
      "owner": "",
      "outcome": ""
    }
  ]
}
"""

def read_input(path="meeting.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_agenda(meeting_text):
    if client is None:
        raise ValueError("OpenAI client not initialized. Set OPENAI_API_KEY.")
        
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": meeting_text}
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
    with open("agenda.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("agenda.txt", "w", encoding="utf-8") as f:
        f.write(f"Meeting Agenda ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Title: {data.get('meeting_title', 'Untitled')}\n")
        f.write(f"Objective: {data.get('objective', '')}\n")
        f.write(f"Duration: {data.get('total_duration_minutes', 0)} minutes\n\n")
 
        for i, item in enumerate(data.get("agenda", []), 1):
            f.write(f"{i}. {item.get('topic', '')} ({item.get('time_minutes', 0)} min)\n")
            f.write(f"   Owner: {item.get('owner', 'Unassigned')}\n")
            f.write(f"   Outcome: {item.get('outcome', '')}\n\n")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set in your environment.")
        # But we still try reading just so the user knows
        
    print("Reading meeting context...")
    meeting_text = read_input()
    
    print("Generating intelligent agenda...")
    agenda = generate_agenda(meeting_text)
    
    save_outputs(agenda)
    print("Meeting agenda generated successfully.")
    print(json.dumps(agenda, indent=2))

if __name__ == "__main__":
    main()
