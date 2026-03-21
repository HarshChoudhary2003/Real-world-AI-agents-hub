import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Model Comparison Agent.

Rules:
- Compare models for a specific task
- Evaluate strengths, weaknesses, and trade-offs
- Consider constraints (Cost, Accuracy, Latency, etc.)
- Provide a clear, objective recommendation

Return ONLY valid JSON with this schema:

{
  "comparison_summary": "High-level overview",
  "models": [
    {
      "model_name": "",
      "strengths": [],
      "weaknesses": [],
      "notes": "",
      "scores": {
        "accuracy": 0 to 100,
        "latency": 0 to 100,
        "cost": 0 to 100,
        "consistency": 0 to 100
      }
    }
  ],
  "recommended_model": "",
  "recommendation_rationale": ""
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Task: General chatbot comparison")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def compare_models(prompt_text, model_orchestrator="gpt-4o"):
    print(f"📡 Orchestrating comparison via {model_orchestrator}...")
    response = litellm.completion(
        model=model_orchestrator,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.3
    )
    
    content = response.choices[0].message.content
    # Robust JSON extraction
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    if "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]
        
    return json.loads(content)

def save_outputs(data):
    with open("model_comparison.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("model_comparison.txt", "w", encoding="utf-8") as f:
        f.write(f"Model Intelligence Comparison ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Summary: {data['comparison_summary']}\n\n")

        for m in data["models"]:
            f.write(f"Model: {m['model_name']}\n")
            f.write("Strengths:\n")
            for s in m["strengths"]:
                f.write(f"- {s}\n")
            f.write("Weaknesses:\n")
            for w in m["weaknesses"]:
                f.write(f"- {w}\n")
            f.write(f"Refinement Notes: {m['notes']}\n\n")

        f.write(f"🏆 Recommended Model: {data['recommended_model']}\n")
        f.write(f"Rationale: {data['recommendation_rationale']}\n")

def main():
    print("🚀 Model Comparison Agent: Initiating neural trade-off analysis...")
    try:
        prompt_text = read_input()
        orchestrator = os.getenv("DEFAULT_MODEL", "gpt-4o")
        comparison = compare_models(prompt_text, model_orchestrator=orchestrator)
        save_outputs(comparison)
        print("✅ Model comparison completed successfully.")
        print("📁 Outputs: model_comparison.json, model_comparison.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
