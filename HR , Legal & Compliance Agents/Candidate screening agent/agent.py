import json
import os
import litellm
import glob
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are an Advanced Candidate Screening Agent (ATS Intelligence).

Rules:
- Conduct an objective, multi-dimensional forensic analysis of the resume against the job description.
- Never make final hiring decisions, act purely as an analytical engine.
- Identify both explicit skill matches and implicit trajectory matches.
- Highlight specific "red flags" (e.g., gaps in employment, missing critical certifications, mismatched seniority).
- Provide specific, tailored follow-up interview questions to probe the candidate's exact weaknesses.
- Remain neutral and avoid protected attribute bias.

Return ONLY valid JSON with this exact schema:
{
  "scores": {
    "technical_alignment": "Score out of 100",
    "experience_alignment": "Score out of 100",
    "overall_score": "Score out of 100"
  },
  "matched_requirements": ["Strong skill or experience matches"],
  "missing_requirements": ["Critical requirements not found"],
  "red_flags_or_concerns": ["Job gaps, overqualification, underqualification, missing degrees"],
  "custom_interview_probes": ["Question targeting missing requirement 1", "Question targeting red flag 1"],
  "screening_summary": "Objective 2-3 sentence executive summary"
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
    print(f"📡 Advanced ATS Screening via {model}...")
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
    # Save JSON report
    with open("advanced_screening_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Save TXT report
    with open("advanced_screening_results.txt", "w", encoding="utf-8") as f:
        f.write(f"Advanced Candidate Screening Report ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        
        scores = data.get("scores", {})
        f.write("--- INTELLIGENCE SCORES ---\n")
        f.write(f"Overall Match:      {scores.get('overall_score', 'N/A')}/100\n")
        f.write(f"Technical Affinity: {scores.get('technical_alignment', 'N/A')}/100\n")
        f.write(f"Experience Rating:  {scores.get('experience_alignment', 'N/A')}/100\n\n")
        
        f.write("--- EXECUTIVE SUMMARY ---\n")
        f.write(data.get("screening_summary", "") + "\n\n")

        f.write("--- MATCHED REQUIREMENTS ---\n")
        for m in data.get("matched_requirements", []):
            f.write(f"✅ {m}\n")
            
        f.write("\n--- MISSING REQUIREMENTS ---\n")
        for m in data.get("missing_requirements", []):
            f.write(f"❌ {m}\n")
            
        f.write("\n--- RED FLAGS / CONCERNS ---\n")
        flags = data.get("red_flags_or_concerns", [])
        if not flags:
            f.write("None detected.\n")
        for fg in flags:
            f.write(f"⚠️ {fg}\n")
            
        f.write("\n--- RECOMMENDED INTERVIEW PROBES ---\n")
        for q in data.get("custom_interview_probes", []):
            f.write(f"🎤 {q}\n")

def main():
    print("🚀 Advanced Candidate Screening Agent: Initiating Deep Scan...")
    try:
        job_text = read_file("job.txt")
        resume_text = read_file("resume.txt")
        
        if not job_text or not resume_text:
            print("❌ Error: Missing job.txt or resume.txt")
            return
            
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        result = screen_candidate(job_text, resume_text, model=model)
        save_outputs(result)
        
        print("✅ Advanced candidate screening completed successfully.")
        print("📁 Outputs: advanced_screening_results.json, advanced_screening_results.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Added capability to process an entire folder of resumes
def batch_process(job_text: str, resumes_folder: str = "resumes", model: str = "gpt-4o"):
    if not os.path.exists(resumes_folder):
        print(f"Directory {resumes_folder} not found for batch processing.")
        return
        
    resume_files = glob.glob(f"{resumes_folder}/*.txt")
    if not resume_files:
        print("No resumes found in the target directory.")
        return
        
    batch_results = []
    print(f"Found {len(resume_files)} resumes. Commencing BATCH ATS Scan...")
    
    for rp in resume_files:
        c_text = read_file(rp)
        res = screen_candidate(job_text, c_text, model)
        res["candidate_file"] = os.path.basename(rp)
        batch_results.append(res)
        
    with open("batch_screening_results.json", "w", encoding="utf-8") as f:
        json.dump(batch_results, f, indent=2)
    print(f"✅ Batch processed {len(resume_files)} candidates. Results in batch_screening_results.json")

if __name__ == "__main__":
    main()
