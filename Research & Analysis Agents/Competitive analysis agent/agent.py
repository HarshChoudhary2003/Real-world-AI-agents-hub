import json
import os
import argparse
from datetime import date
from openai import OpenAI
import anthropic
import groq
import google.generativeai as genai

SYSTEM_PROMPT = """
You are an elite Competitive Analysis Agent.

Rules:
- Compare competitors objectively and rigorously.
- Identify specific strengths, weaknesses, and market positioning.
- Avoid subjective or promotional language; remain neutral and analytical.
- Focus on strategic, actionable insights for market differentiation.

Return ONLY valid JSON with this schema (do not wrap in markdown):

{
  "overview": "High-level summary of the competitive landscape",
  "competitors": [
    {
      "name": "Competitor Name",
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "positioning": "Strategic market positioning description"
    }
  ],
  "gaps_and_opportunities": ["Opportunity 1", "Gap 2"]
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_competition(api_provider, model, prompt_text):
    print(f"Executing competitive analysis via {api_provider} ({model})...")
    
    if api_provider == "openai":
        client = OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.35,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    # Add other providers similarly if needed for CLI version
    # ... (omitted for brevity in CLI, fully present in app.py)
    return {}

def save_outputs(data):
    with open("competitive_analysis.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("competitive_analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"Competitive Analysis Report ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        f.write("MARKET OVERVIEW:\n")
        f.write(data.get("overview", "") + "\n\n")

        for c in data.get("competitors", []):
            f.write(f"COMPETITOR: {c.get('name', 'N/A')}\n")
            f.write("-" * 30 + "\n")
            f.write("Strengths:\n")
            for s in c.get("strengths", []):
                f.write(f"  - {s}\n")
            f.write("Weaknesses:\n")
            for w in c.get("weaknesses", []):
                f.write(f"  - {w}\n")
            f.write(f"Positioning Strategy:\n{c.get('positioning', 'N/A')}\n\n")

        f.write("STRATEGIC GAPS & OPPORTUNITIES:\n")
        for g in data.get("gaps_and_opportunities", []):
            f.write(f"  - {g}\n")
            
    print("Intelligence successfully exported to competitive_analysis.json and competitive_analysis.txt.")

def main():
    parser = argparse.ArgumentParser(description="Competitive Analysis Agent")
    parser.add_argument("--provider", type=str, default="openai", choices=["openai", "anthropic", "groq", "gemini"])
    parser.add_argument("--model", type=str, default="gpt-4o")
    args = parser.parse_args()

    input_data = read_input()
    if not input_data:
        print("Error: input.txt is empty or missing.")
        return

    try:
        analysis = analyze_competition(args.provider, args.model, input_data)
        save_outputs(analysis)
        print("Analysis cycle complete.")
    except Exception as e:
        print(f"Strategic analysis failed: {str(e)}")

if __name__ == "__main__":
    main()
