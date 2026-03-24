import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY
base_path = os.path.dirname(__file__)

SYSTEM_PROMPT = """
You are a Self-Improving Agent.

Rules:
- Strictly evaluate past performance based on provided feedback.
- Apply small, controlled, and verifiable improvements to the next iteration.
- Respect all mission constraints.
- Do NOT modify your core purpose or governance rules.

Return ONLY valid JSON with this schema:

{
  "output": "",
  "improvements_applied": [],
  "performance_notes": ""
}
"""

def main():
    print("Initializing Neural Self-Improvement Protocol...")
    
    # Path setup
    task_path = os.path.join(base_path, "task_input.txt")
    feedback_path = os.path.join(base_path, "feedback.json")
    output_path = os.path.join(base_path, "output.json")

    try:
        with open(task_path, "r", encoding="utf-8") as f:
            task = f.read()
        with open(feedback_path, "r", encoding="utf-8") as f:
            feedback = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Missing or corrupt input files: {e}")
        return

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Neural Task Definition:\n{task}\n\nHistorical Feedback Matrix:\n{json.dumps(feedback, indent=2)}"
            }
        ],
        response_format={ "type": "json_object" },
        temperature=0.3
    )

    result = json.loads(response.choices[0].message.content)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Self-improvement cycle complete. Applied {len(result.get('improvements_applied', []))} optimizations.")

if __name__ == "__main__":
    main()
