import json
from datetime import date
try:
    from openai import OpenAI
    client = OpenAI()  # requires OPENAI_API_KEY
except Exception:
    pass

SYSTEM_PROMPT = """
You are a Note-to-Action Item Agent.

Your job:
- Extract ONLY actionable tasks from the notes
- Ignore ideas, opinions, or decisions without actions
- Identify owner if mentioned; otherwise use "Unassigned"
- Suggest a deadline if implied; otherwise "Not specified"
- Assign priority: Low, Medium, or High

Return ONLY valid JSON with this schema:

{
  "actions": [
    {
      "action": "",
      "owner": "",
      "deadline": "",
      "priority": "",
      "source_context": ""
    }
  ]
}
"""

def read_notes(path="notes.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_actions(notes_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": notes_text}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content.strip()
    return json.loads(content)

def save_outputs(data):
    with open("actions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("actions.txt", "w", encoding="utf-8") as f:
        f.write(f"Extracted Action Items ({date.today()})\n")
        f.write("=" * 45 + "\n\n")

        for i, a in enumerate(data.get("actions", []), 1):
            f.write(f"{i}. {a.get('action', '')}\n")
            f.write(f"   Owner: {a.get('owner', '')}\n")
            f.write(f"   Deadline: {a.get('deadline', '')}\n")
            f.write(f"   Priority: {a.get('priority', '')}\n")
            f.write(f"   Source: {a.get('source_context', '')}\n\n")

def main():
    try:
        notes_text = read_notes()
    except FileNotFoundError:
        print("notes.txt not found.")
        return
        
    try:
        actions = extract_actions(notes_text)
        save_outputs(actions)
        print("Action items extracted successfully.")
        print(json.dumps(actions, indent=2))
    except Exception as e:
        print(f"Error extracting actions: {e}. Check API key.")

if __name__ == "__main__":
    main()
