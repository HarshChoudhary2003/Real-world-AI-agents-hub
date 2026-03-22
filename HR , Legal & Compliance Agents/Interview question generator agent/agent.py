import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are an Interview Question Generator Agent.

Rules:
- Generate fair, role-relevant questions
- Avoid illegal or biased topics
- Include behavioral and technical questions
- Do NOT provide answers

Return ONLY valid JSON with this schema:
{
  "behavioral_questions": ["question 1", "question 2"],
  "technical_questions": ["question 1", "question 2"],
  "scenario_questions": ["question 1", "question 2"]
}
"""

def read_role(path: str = "role.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Role: Backend Software Engineer\nSeniority: Mid-level\nKey Skills:\n- Python\n- APIs\n- Databases\n- System design")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_json(content_raw: str) -> dict:
    content = str(content_raw)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        start_idx = int(content.find("{"))
        end_idx = int(content.rfind("}")) + 1
        content_str = str(content)
        content = content_str[start_idx:end_idx]
    return json.loads(content)

def generate_questions(role_text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Questions via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": role_text}
        ],
        temperature=0.3
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("interview_questions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("interview_questions.txt", "w", encoding="utf-8") as f:
        f.write(f"Interview Questions ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        
        f.write("Behavioral Questions:\n")
        for q in data.get("behavioral_questions", []):
            f.write(f"- {q}\n")
            
        f.write("\nTechnical Questions:\n")
        for q in data.get("technical_questions", []):
            f.write(f"- {q}\n")
            
        f.write("\nScenario-Based Questions:\n")
        for q in data.get("scenario_questions", []):
            f.write(f"- {q}\n")

def main():
    print("🚀 Interview Question Generator Agent: Initiating specifications...")
    try:
        role_text = read_role()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        questions = generate_questions(role_text, model=model)
        save_outputs(questions)
        
        print("✅ Interview questions generated successfully.")
        print("📁 Outputs: interview_questions.json, interview_questions.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
