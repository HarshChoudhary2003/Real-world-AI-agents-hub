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
You are an Email Summarization Agent.
 
Your job:
1. Summarize the email in 2–3 sentences
2. Extract key points
3. Extract action items (who should do what)
4. Identify deadlines
5. Classify urgency: Low, Medium, or High
 
Return ONLY valid JSON with this schema format (no markdown):
 
{
  "summary": "",
  "key_points": [],
  "action_items": [],
  "deadlines": [],
  "urgency": ""
}
"""

def read_email(path="email.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def summarize_email(email_text):
    # Using 'gpt-4o-mini' as the current standard mini model instead of 'gpt-4.1-mini'
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": email_text}
        ],
        temperature=0.2,
        response_format={"type": "json_object"} # added for safer JSON extraction
    )
    # Strip markdown if any was returned despite instructions
    content = response.choices[0].message.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return json.loads(content)

def save_outputs(data):
    with open("summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Email Summary ({date.today()})\n")
        f.write("=" * 40 + "\n\n")
        f.write("SUMMARY:\n")
        f.write(data.get("summary", "") + "\n\n")
 
        f.write("KEY POINTS:\n")
        for p in data.get("key_points", []):
            f.write(f"- {p}\n")
 
        f.write("\nACTION ITEMS:\n")
        for a in data.get("action_items", []):
            f.write(f"- {a}\n")
 
        f.write("\nDEADLINES:\n")
        for d in data.get("deadlines", []):
            f.write(f"- {d}\n")
 
        f.write(f"\nURGENCY: {data.get('urgency', '')}\n")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set in your environment.")
        
    print("Reading email...")
    email_text = read_email()
    
    print("Summarizing with AI...")
    result = summarize_email(email_text)
    
    save_outputs(result)
    print("Email summarized successfully.")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
