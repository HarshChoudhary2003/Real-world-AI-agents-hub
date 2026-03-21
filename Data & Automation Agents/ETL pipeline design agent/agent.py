import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Data Engineering & Cloud Data Architect (Pipeline-Forge AI v2.0).

Mission: Architect high-performance, scalable ETL (Extract, Transform, Load) pipelines for mission-critical data systems.

Rules for Architecture:
1. **Stage Separation**: Explicitly define the logic for Extract (Ingestion), Transform (Processing), and Load (Persistence).
2. **Scalability Diagnostics**: Design for the specified volume (Batch or Streaming) using resilient methods (e.g., Change Data Capture, Delta loading).
3. **Resilience & Fault Tolerance**: Architect retry logic, validation checkpoints, and monitoring strategies.
4. **Data Integrity**: Include steps for deduplication, schema enforcement, and lineage.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "pipeline_blueprint": {
     "architecture_style": "Batch / Streaming / Lambda",
     "complexity_level": "Level #",
     "strategic_overview": "A brief summary of the design approach"
  },
  "extraction_protocol": [
     {"component": "...", "strategy": "...", "risk_mitigation": "..."}
  ],
  "transformation_logic": [
     {"operation": "...", "purpose": "...", "performance_logic": "..."}
  ],
  "loading_strategy": [
     {"target": "...", "method": "...", "partitioning": "..."}
  ],
  "monitoring_and_slas": {
     "observability": "...",
     "alerting_rules": "...",
     "recovery_objective": "..."
  },
  "architect_pro_tips": ["Expert advice for production-grade reliability"]
}
"""

def read_input(path="input.txt"):
    """Reads ETL requirements from a local text file."""
    if not os.path.exists(path):
        return "Source: Local DB. Target: Cloud. Volume: 1M."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_json(response_content):
    """Robustly parse JSON out of an LLM response."""
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", str(response_content))
        if match:
            try: return json.loads(match.group(1).strip())
            except: pass
        match = re.search(r"\{[\s\S]*\}", str(response_content))
        if match:
            try: return json.loads(match.group(0).strip())
            except: pass
    raise ValueError("Failed to extract pipeline JSON.")

def design_etl_pipeline(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Architects a structured ETL design using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.3
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the ETL design as JSON and formatted TXT."""
    with open("etl_design.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("etl_design.txt", "w", encoding="utf-8") as f:
        f.write(f"Pipeline-Forge AI: ETL Architecture Plan ({date.today()})\n")
        f.write("=" * 65 + "\n\n")

        pb = data.get('pipeline_blueprint', {})
        f.write(f"Architecture: {pb.get('architecture_style')}\n")
        f.write(f"Complexity: {pb.get('complexity_level')}\n")
        f.write(f"Overview: {pb.get('strategic_overview')}\n\n")
        
        f.write("--- 📡 EXTRACTION PROTOCOL ---\n")
        for stage in data.get('extraction_protocol', []):
            f.write(f"▶ {stage.get('component')}: {stage.get('strategy')}\n")
            f.write(f"  Mitigation: {stage.get('risk_mitigation')}\n\n")
        
        f.write("--- 🧬 TRANSFORMATION LOGIC ---\n")
        for logic in data.get('transformation_logic', []):
            f.write(f"• {logic.get('operation')}: {logic.get('purpose')}\n")
            f.write(f"  Perf: {logic.get('performance_logic')}\n\n")

        f.write("--- 💾 LOADING STRATEGY ---\n")
        for load in data.get('loading_strategy', []):
            f.write(f"▶ {load.get('target')}: {load.get('method')}\n")
            f.write(f"  Partition: {load.get('partitioning')}\n\n")

        f.write("--- 📊 SRE & OPS --- \n")
        sla = data.get('monitoring_and_slas', {})
        f.write(f"Observability: {sla.get('observability')}\n")
        f.write(f"Recovery: {sla.get('recovery_objective')}\n\n")

        f.write("--- 🛠️ ARCHITECT PRO-TIPS --- \n")
        for tip in data.get('architect_pro_tips', []):
            f.write(f"- {tip}\n")

def main():
    print("🚀 Pipeline-Forge AI: Architecting Data Flow...")
    prompt_text = read_input()
    try:
        design = design_etl_pipeline(prompt_text)
        save_outputs(design)
        print("✅ ETL pipeline architecture completed successfully.")
        print("📁 Outputs: etl_design.json, etl_design.txt")
    except Exception as e:
        print(f"❌ Architectural failure: {str(e)}")

if __name__ == "__main__":
    main()
