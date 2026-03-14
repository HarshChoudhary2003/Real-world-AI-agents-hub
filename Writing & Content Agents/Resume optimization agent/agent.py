import json
from openai import OpenAI
from datetime import date

client = OpenAI()  # requires OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a Resume Optimization Agent.

Your goals:
- Rewrite resume bullets to emphasize measurable impact
- Align content with the target role
- Preserve factual accuracy (do not invent experience)
- Keep language ATS-friendly and concise

Return ONLY valid JSON with this schema:

{
  "optimized_experience": [],
  "optimized_skills": [],
  "summary_suggestion": ""
}
"""

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def optimize_resume(resume_text, job_text):
    prompt = f"""
RESUME:
{resume_text}

TARGET ROLE:
{job_text}
"""
    # using gpt-4o-mini instead of gpt-4.1-mini for OpenAI compatibility
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("resume_optimized.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("resume_optimized.txt", "w", encoding="utf-8") as f:
        f.write(f"Optimized Resume Output ({date.today()})\n")
        f.write("=" * 45 + "\n\n")

        f.write("Optimized Experience:\n")
        for b in data.get("optimized_experience", []):
            f.write(f"- {b}\n")

        f.write("\nOptimized Skills:\n")
        for s in data.get("optimized_skills", []):
            f.write(f"- {s}\n")

        f.write("\nSummary Suggestion:\n")
        f.write(data.get("summary_suggestion", "") + "\n")

def main():
    resume_text = read_file("resume.txt")
    job_text = read_file("job.txt")
    optimized = optimize_resume(resume_text, job_text)
    save_outputs(optimized)
    print("Resume optimization complete.")

if __name__ == "__main__":
    main()
