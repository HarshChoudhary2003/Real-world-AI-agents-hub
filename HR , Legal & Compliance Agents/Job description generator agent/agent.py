import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Job Description Generator Agent.

Rules:
- Generate clear, inclusive job descriptions
- Avoid biased language
- Structure content professionally
- Do NOT invent unrealistic requirements

Return ONLY valid JSON with this schema:

{
  "role_overview": "",
  "responsibilities": [],
  "required_qualifications": [],
  "preferred_qualifications": [],
  "benefits": []
}
"""

def read_role(path: str = "role.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Role: AI Product Manager\nTeam: Enterprise AI Platform\nSeniority: Senior\nLocation: Remote\nResponsibilities:\n- Define AI product roadmap\n- Collaborate with engineering and stakeholders\n- Drive product delivery\nRequired Skills:\n- Product management experience\n- AI/ML fundamentals\n")
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

def generate_job_description(role_text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Job Description via {model}...")
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
    with open("job_description.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("job_description.txt", "w", encoding="utf-8") as f:
        f.write(f"Job Description ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write("Role Overview:\n")
        f.write(data.get("role_overview", "") + "\n\n")
        
        f.write("Responsibilities:\n")
        for r in data.get("responsibilities", []):
            f.write(f"- {r}\n")
            
        f.write("\nRequired Qualifications:\n")
        for q in data.get("required_qualifications", []):
            f.write(f"- {q}\n")
            
        if data.get("preferred_qualifications"):
            f.write("\nPreferred Qualifications:\n")
            for p in data.get("preferred_qualifications", []):
                f.write(f"- {p}\n")
                
        if data.get("benefits"):
            f.write("\nBenefits:\n")
            for b in data.get("benefits", []):
                f.write(f"- {b}\n")

def main():
    print("🚀 Job Description Generator Agent: Initiating specifications...")
    try:
        role_text = read_role()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        jd = generate_job_description(role_text, model=model)
        save_outputs(jd)
        
        print("✅ Job description generated successfully.")
        print("📁 Outputs: job_description.json, job_description.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
