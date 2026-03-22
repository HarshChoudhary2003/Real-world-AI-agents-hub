import json
import os
import litellm
import traceback
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are an Enterprise Training Content Generator Agent.

Rules:
- Generate clear, highly structured, modular training content based on the target audience.
- Align tightly with specified macro learning objectives.
- Use accessible, engaging language suitable for corporate enablement.
- Do NOT include assessments unless requested.

Return ONLY valid JSON with this exact schema:
{
  "learning_objectives": ["Objective 1", "Objective 2"],
  "modules": [
    {
      "title": "Module Title",
      "key_points": ["Point 1", "Point 2", "Point 3"]
    }
  ]
}
"""

def read_input(path: str = "training_input.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("Topic: Data Security Awareness\nAudience: New employees\nObjective: Understand basic data security responsibilities")
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

def generate_training(text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Enablement Modules via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Training Brief:\n{text}"}
        ],
        temperature=0.3
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("training_content.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("training_content.txt", "w", encoding="utf-8") as f:
        f.write(f"Corporate Training Content Index ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        
        f.write("--- LEARNING OBJECTIVES ---\n")
        for o in data.get("learning_objectives", []):
            f.write(f"- {o}\n")
            
        f.write("\n--- TRAINING MODULES ---\n")
        for m in data.get("modules", []):
            f.write(f"\n[MODULE]: {m.get('title', 'Unknown')}\n")
            for p in m.get("key_points", []):
                f.write(f"  * {p}\n")

def main():
    print("🚀 Training Content Generator Agent: Initiating Enablement Core...")
    try:
        input_text = read_input()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        training = generate_training(input_text, model=model)
        save_outputs(training)
        
        print("✅ Training content generated successfully.")
        print("📁 Outputs: training_content.json, training_content.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
