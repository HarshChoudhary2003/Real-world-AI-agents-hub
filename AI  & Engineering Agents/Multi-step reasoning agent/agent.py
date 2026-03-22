import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are an advanced Multi-Step Reasoning Agent.

Rules:
- Decompose the problem into clear, numbered logical steps
- Show intermediate calculations and conclusions per step
- Validate constraints at each step
- Do NOT skip reasoning shortcuts
- Explicitly state all assumptions made

Return ONLY valid JSON with this schema:
{
  "problem_type": "math | logic | strategy | analysis | mixed",
  "steps": [
    {
      "step_number": 1,
      "title": "Short step title",
      "reasoning": "Detailed explanation",
      "interim_result": "Intermediate value or conclusion"
    }
  ],
  "final_answer": "Clear, complete answer",
  "confidence": 0.0 to 1.0,
  "assumptions": ["List of assumptions made"]
}
"""

def read_problem(path="problem.txt"):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("A company has a budget of $120,000. If each feature costs $8,000, how many features can they build?")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_json(content: str) -> dict:
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]
    return json.loads(content)

def solve_problem(problem: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Orchestrating reasoning via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": problem}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("reasoning_result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("reasoning_result.txt", "w", encoding="utf-8") as f:
        f.write(f"ThinkForge AI: Multi-Step Reasoning Report ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Problem Type: {data.get('problem_type', 'N/A').upper()}\n")
        f.write(f"Confidence: {int(data.get('confidence', 0) * 100)}%\n\n")
        f.write("Reasoning Chain:\n")
        for s in data.get("steps", []):
            f.write(f"\nStep {s['step_number']}: {s['title']}\n")
            f.write(f"  → {s['reasoning']}\n")
            f.write(f"  Result: {s['interim_result']}\n")
        f.write(f"\nFinal Answer:\n{data['final_answer']}\n")
        if data.get("assumptions"):
            f.write("\nAssumptions:\n")
            for a in data["assumptions"]:
                f.write(f"- {a}\n")

def main():
    print("🚀 ThinkForge AI: Initiating multi-step reasoning chain...")
    try:
        problem = read_problem()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        result = solve_problem(problem, model=model)
        save_outputs(result)
        print("✅ Multi-step reasoning completed successfully.")
        print("📁 Outputs: reasoning_result.json, reasoning_result.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
