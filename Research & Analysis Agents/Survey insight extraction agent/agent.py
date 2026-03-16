import json
import os
from datetime import date
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from groq import Groq

SYSTEM_PROMPT = """
You are a Survey Insight Extraction Agent.

Rules:
- Identify themes and sentiment from survey responses
- Preserve nuance and representative voice
- Avoid bias or interpretation
- Highlight both majority and minority signals

Return ONLY valid JSON with this schema:

{
  "summary": "",
  "themes": [
    {
      "theme": "",
      "sentiment": "",
      "examples": []
    }
  ],
  "outliers": [],
  "suggested_follow_ups": []
}
"""

def clean_json_response(text):
    """Strips markdown code blocks and whitespace from AI JSON response."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def analyze_with_openai(model, api_key, prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def analyze_with_anthropic(model, api_key, prompt):
    client = Anthropic(api_key=api_key)
    # Anthropic requires the system prompt in the top-level
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    # Extract JSON from response
    content = response.content[0].text
    return json.loads(clean_json_response(content))

def analyze_with_gemini(model, api_key, prompt):
    genai.configure(api_key=api_key)
    client = genai.GenerativeModel(
        model_name=model,
        generation_config={"response_mime_type": "application/json"}
    )
    full_prompt = f"{SYSTEM_PROMPT}\n\nAnalyze this survey data:\n{prompt}"
    response = client.generate_content(full_prompt)
    return json.loads(clean_json_response(response.text))

def analyze_with_groq(model, api_key, prompt):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def run_multi_model_analysis(provider, model, api_key, input_text):
    """Router for multi-provider survey analysis."""
    if not api_key:
        raise ValueError(f"API Key for {provider} is missing.")
    
    if provider == "OpenAI":
        return analyze_with_openai(model, api_key, input_text)
    elif provider == "Anthropic":
        return analyze_with_anthropic(model, api_key, input_text)
    elif provider == "Google Gemini":
        return analyze_with_gemini(model, api_key, input_text)
    elif provider == "Groq":
        return analyze_with_groq(model, api_key, input_text)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def save_outputs(data):
    """Save analysis results to disk."""
    with open("survey_insights.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("survey_insights.txt", "w", encoding="utf-8") as f:
        f.write(f"Survey Insights ({date.today()})\n")
        f.write("=" * 50 + "\n\n")
        f.write("Summary:\n")
        f.write(data.get("summary", "") + "\n\n")

        for t in data.get("themes", []):
            f.write(f"Theme: {t['theme']}\n")
            f.write(f"Sentiment: {t['sentiment']}\n")
            f.write("Examples:\n")
            for e in t['examples']:
                f.write(f"- {e}\n")
            f.write("\n")

        if data.get("outliers"):
            f.write("Outliers:\n")
            for o in data["outliers"]:
                f.write(f"- {o}\n")
            f.write("\n")

        if data.get("suggested_follow_ups"):
            f.write("Suggested Follow-Up Questions:\n")
            for q in data["suggested_follow_ups"]:
                f.write(f"- {q}\n")

if __name__ == "__main__":
    # Standard CLI fallback
    print("Multi-Model Survey Agent (CLI)")
    # Defaults for local testing
    try:
        with open("input.txt", "r") as f:
            text = f.read()
        # Expecting OpenAI by default for CLI
        key = os.getenv("OPENAI_API_KEY")
        if key:
            results = run_multi_model_analysis("OpenAI", "gpt-4o-mini", key, text)
            save_outputs(results)
            print("Successfully analyzed and saved to survey_insights.json/txt")
        else:
            print("Set OPENAI_API_KEY environment variable to use CLI.")
    except Exception as e:
        print(f"CLI Error: {e}")
