import json
import os
from datetime import date
from dotenv import load_dotenv

# Optional imports based on provider
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

SYSTEM_PROMPT = """
You are a Senior Strategic Growth Consultant and SWOT Analysis Expert.
Your goal is to provide a deep, actionable, and data-driven SWOT analysis.

### Rules:
1. Internal Factors (Strengths & Weaknesses): Focus on resources and competencies.
2. External Factors (Opportunities & Threats): Focus on market trends and competition.
3. Impact Assessment: Categorize every factor with Impact: High, Medium, or Low.
4. TOWS Matrix: Suggest specific SO, WO, ST, and WT strategies.

Return ONLY a valid JSON object:
{
  "strengths": [{"factor": "string", "impact": "High/Medium/Low", "description": "string"}],
  "weaknesses": [{"factor": "string", "impact": "High/Medium/Low", "description": "string"}],
  "opportunities": [{"factor": "string", "impact": "High/Medium/Low", "description": "string"}],
  "threats": [{"factor": "string", "impact": "High/Medium/Low", "description": "string"}],
  "tows_strategies": {
    "so_strategies": [],
    "wo_strategies": [],
    "st_strategies": [],
    "wt_strategies": []
  },
  "strategic_observations": []
}
"""

def generate_swot(prompt_text, provider="OpenAI", model=None, api_key=None):
    if provider == "OpenAI":
        return _call_openai(prompt_text, model or "gpt-4o-mini", api_key)
    elif provider == "Anthropic":
        return _call_anthropic(prompt_text, model or "claude-3-5-sonnet-20240620", api_key)
    elif provider == "Gemini":
        return _call_gemini(prompt_text, model or "gemini-1.5-flash", api_key)
    elif provider == "Groq":
        return _call_groq(prompt_text, model or "llama-3.1-70b-versatile", api_key)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def _call_openai(prompt, model, api_key):
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)

def _call_anthropic(prompt, model, api_key):
    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    # Anthropic requires system prompt in top-level
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return json.loads(response.content[0].text)

def _call_gemini(prompt, model, api_key):
    genai.configure(api_key=api_key or os.getenv("GEMINI_API_KEY"))
    model_instance = genai.GenerativeModel(
        model_name=model,
        system_instruction=SYSTEM_PROMPT
    )
    response = model_instance.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.3
        )
    )
    return json.loads(response.text)

def _call_groq(prompt, model, api_key):
    client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data, base_path=""):
    json_path = os.path.join(base_path, "swot_analysis.json")
    txt_path = os.path.join(base_path, "swot_analysis.txt")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"ADVANCED SWOT ANALYSIS REPORT ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        for section in ["strengths", "weaknesses", "opportunities", "threats"]:
            f.write(f"### {section.upper()}\n")
            for item in data[section]:
                f.write(f"- [{item['impact']}] {item['factor']}: {item['description']}\n")
            f.write("\n")
        f.write("### STRATEGIC OBSERVATIONS\n")
        for so in data["strategic_observations"]:
            f.write(f"- {so}\n")

def read_input(path="input.txt"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Entity: Startup\nIndustry: Tech"

def main():
    print("Multi-Model SWOT Agent")
    context = read_input()
    # Default to OpenAI for CLI
    try:
        swot = generate_swot(context)
        save_outputs(swot)
        print("Success! Outputs saved.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
