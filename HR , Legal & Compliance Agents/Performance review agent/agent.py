import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Performance Review Agent.

Rules:
- Generate balanced, evidence-based reviews
- Use professional, constructive language
- Avoid biased or inflammatory phrasing
- Do NOT assign compensation decisions

Return ONLY valid JSON with this schema:
{
  "summary": "High level overview of performance",
  "strengths": ["List of strengths"],
  "areas_for_improvement": ["Constructive feedback points"],
  "development_recommendations": ["Actionable next steps"]
}
"""

def read_input(path: str = "review_input.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Employee Role: Software Engineer\nReview Period: Q2\nGoals:\n- Deliver authentication feature\n- Improve code quality\nManager Notes:\n- Delivered feature on time\n- Improved test coverage\n- Occasionally missed documentation updates")
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

def generate_review(input_text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Performance Review via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input_text}
        ],
        temperature=0.3
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("performance_review.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("performance_review.txt", "w", encoding="utf-8") as f:
        f.write(f"Performance Review ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        
        f.write("Summary:\n")
        f.write(data.get("summary", "") + "\n\n")
        
        f.write("Strengths:\n")
        for s in data.get("strengths", []):
            f.write(f"- {s}\n")
            
        f.write("\nAreas for Improvement:\n")
        for a in data.get("areas_for_improvement", []):
            f.write(f"- {a}\n")
            
        f.write("\nDevelopment Recommendations:\n")
        for d in data.get("development_recommendations", []):
            f.write(f"- {d}\n")

def main():
    print("🚀 Performance Review Agent: Initiating specifications...")
    try:
        input_text = read_input()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        review = generate_review(input_text, model=model)
        save_outputs(review)
        
        print("✅ Performance review generated successfully.")
        print("📁 Outputs: performance_review.json, performance_review.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
