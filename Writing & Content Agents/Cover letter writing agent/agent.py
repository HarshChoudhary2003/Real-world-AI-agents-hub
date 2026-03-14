import json
from datetime import date
from openai import OpenAI

client = OpenAI()  # requires OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a Cover Letter Writing Agent.

Your goals:
- Write a concise, role-specific cover letter
- Align experience with the job requirements
- Preserve factual accuracy (do not invent experience)
- Maintain a professional, human tone
- Keep length to 3-4 short paragraphs

Return ONLY valid JSON with this schema:

{
  "company": "",
  "role": "",
  "cover_letter": ""
}
"""

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_cover_letter(resume_text, job_text):
    prompt = f"""
RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}
"""
    # Using gpt-4o-mini instead of gpt-4.1-mini
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.35
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("cover_letter.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("cover_letter.txt", "w", encoding="utf-8") as f:
        f.write(f"Cover Letter — {data.get('role', 'Role')} at {data.get('company', 'Company')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(data.get("cover_letter", "") + "\n")

def main():
    resume_text = read_file("resume.txt")
    job_text = read_file("job.txt")
    letter = generate_cover_letter(resume_text, job_text)
    save_outputs(letter)
    print("Cover letter generated successfully.")

if __name__ == "__main__":
    main()
