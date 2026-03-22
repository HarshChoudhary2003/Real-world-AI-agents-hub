import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Candidate Screening Agent.

Rules:
- Screen candidates against job requirements
- Be fair and transparent
- Avoid biased or protected attributes
- Do NOT make hiring decisions

Return ONLY valid JSON with this schema:
{
  "qualification_score": "Score out of 100",
  "matched_requirements": ["list of skills candidate met"],
  "missing_requirements": ["list of required skills candidate lacks"],
  "screening_summary": "Objective overview of the alignment"
}
"""

def read_file(path: str) -> str:
    if not os.path.exists(path):
        return ""
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

def screen_candidate(job_text: str, resume_text: str, model: str = "gpt-4o") -> dict:
    prompt = f"Job Description:\n{job_text}\n\nCandidate Resume:\n{resume_text}\n"
    print(f"📡 Screening Candidate via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("screening_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("screening_results.txt", "w", encoding="utf-8") as f:
        f.write(f"Candidate Screening Results ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Qualification Score: {data.get('qualification_score', 'N/A')}\n\n")
        
        f.write("Matched Requirements:\n")
        for m in data.get("matched_requirements", []):
            f.write(f"- {m}\n")
            
        f.write("\nMissing Requirements:\n")
        for m in data.get("missing_requirements", []):
            f.write(f"- {m}\n")
            
        f.write("\nSummary:\n")
        f.write(data.get("screening_summary", "") + "\n")

def main():
    print("🚀 Candidate Screening Agent: Initiating specifications...")
    try:
        job_text = read_file("job.txt")
        resume_text = read_file("resume.txt")
        
        if not job_text or not resume_text:
            print("❌ Error: Missing job.txt or resume.txt")
            return
            
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        result = screen_candidate(job_text, resume_text, model=model)
        save_outputs(result)
        
        print("✅ Candidate screening completed successfully.")
        print("📁 Outputs: screening_results.json, screening_results.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
