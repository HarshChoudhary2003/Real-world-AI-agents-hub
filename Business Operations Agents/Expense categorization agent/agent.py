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
You are an Expense Categorization Agent for enterprise financial operations.

### Rules:
1. Analyze the transaction description, vendor name, and amount carefully.
2. Assign ONLY one of the categories explicitly provided in the input.
3. Do not invent new categories or guess when evidence is insufficient.
4. Provide a confidence level: "High", "Medium", or "Low".
5. Include flags for ambiguity, dual-purpose expenses, or policy concerns.
6. Write a brief justification (1-2 sentences) explaining your reasoning.

Return ONLY a valid JSON object matching this schema exactly:
{
  "vendor": "string",
  "description": "string",
  "amount": "string",
  "date": "string",
  "category": "string",
  "confidence": "High | Medium | Low",
  "justification": "string",
  "flags": ["string"]
}
"""

def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _extract_json(text: str) -> dict:
    """Robustly extract a JSON object from model output."""
    text = text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

def categorize_expense(prompt_text, provider="OpenAI", model=None, api_key=None):
    if provider == "OpenAI":
        return _call_openai(prompt_text, model or "gpt-4.1-mini", api_key)
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
        temperature=0.25
    )
    return json.loads(response.choices[0].message.content)

def _call_anthropic(prompt, model, api_key):
    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )
    return _extract_json(response.content[0].text)

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
            temperature=0.25
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
        temperature=0.25
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data, base_path=""):
    json_path = os.path.join(base_path, "expense_categorization.json")
    txt_path = os.path.join(base_path, "expense_categorization.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Expense Categorization Report ({date.today()})\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Vendor       : {data.get('vendor')}\n")
        f.write(f"Description  : {data.get('description')}\n")
        f.write(f"Amount       : {data.get('amount')}\n")
        f.write(f"Date         : {data.get('date')}\n")
        f.write(f"Category     : {data.get('category')}\n")
        f.write(f"Confidence   : {data.get('confidence')}\n")
        f.write(f"Justification: {data.get('justification')}\n")

        flags = data.get("flags", [])
        if flags:
            f.write("\nFlags:\n")
            for flag in flags:
                f.write(f"  ⚠ {flag}\n")
        else:
            f.write("\nFlags: None\n")

def main():
    if not os.path.exists("input.txt"):
        print("Error: input.txt not found. Please create it first.")
        return

    prompt_text = read_input()

    try:
        print("🔍 Analyzing expense transaction...")
        result = categorize_expense(prompt_text)
        save_outputs(result)
        print("✅ Expense categorized successfully.")
        print(f"   Category   : {result.get('category')}")
        print(f"   Confidence : {result.get('confidence')}")
        if result.get("flags"):
            print(f"   Flags      : {', '.join(result['flags'])}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
