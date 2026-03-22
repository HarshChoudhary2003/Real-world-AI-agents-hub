import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a System Architecture Explainer Agent.

Rules:
- Explain architecture clearly
- Avoid unnecessary jargon
- Highlight component roles and data flow
- Do NOT redesign the system

Return ONLY valid JSON with this schema:
{
  "overview": "High-level summary",
  "components": ["List of component roles"],
  "data_flow": "Description of data traveling through components",
  "design_decisions": ["Implied or stated design decisions"],
  "tradeoffs": ["Potential tradeoffs of this architecture"]
}
"""

def read_architecture(path: str = "architecture.txt") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("The system consists of a web frontend, an API gateway, multiple microservices, a message queue, and a relational database.\n"
                    "The frontend communicates with the API gateway, which routes requests to services.\n"
                    "Services publish events to the queue for asynchronous processing.\n")
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
        content = str(content)[start_idx:end_idx]
    return json.loads(content)

def explain_architecture(text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Analyzing System Architecture via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    # Save JSON report
    with open("architecture_explanation.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Save TXT report
    with open("architecture_explanation.txt", "w", encoding="utf-8") as f:
        f.write(f"System Architecture Explanation ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        
        f.write("Overview:\n")
        f.write(data.get("overview", "") + "\n\n")
        
        f.write("Components:\n")
        for c in data.get("components", []):
            f.write(f"- {c}\n")
            
        f.write("\nData Flow:\n")
        f.write(data.get("data_flow", "") + "\n\n")
        
        if data.get("design_decisions"):
            f.write("Design Decisions:\n")
            for d in data.get("design_decisions", []):
                f.write(f"- {d}\n")
                
        if data.get("tradeoffs"):
            f.write("\nTrade-offs:\n")
            for t in data.get("tradeoffs", []):
                f.write(f"- {t}\n")

def main():
    print("🚀 Architecture Explainer Agent: Initiating specifications...")
    try:
        architecture_text = read_architecture()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        explanation = explain_architecture(architecture_text, model=model)
        save_outputs(explanation)
        
        print("✅ System architecture explained successfully.")
        print("📁 Outputs: architecture_explanation.json, architecture_explanation.txt")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
