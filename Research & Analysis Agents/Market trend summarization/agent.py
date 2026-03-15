import json
import os
from litellm import completion
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """
You are a Market Trend Summarization Agent.

Rules:
- Identify meaningful market trends
- Distinguish trends from isolated events
- Avoid speculation and hype
- Highlight implications and uncertainty

Return ONLY valid JSON with this schema:

{
  "overview": "A concise summary of the market landscape",
  "trends": [
    {
      "trend": "Name of the trend",
      "description": "Detailed explanation of what is happening",
      "implications": "What this means for stakeholders"
    }
  ],
  "risks_and_uncertainties": ["Array of potential risks or unknown factors"]
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        return "Market: General AI\nTime Horizon: Short-term\nSources: General News\nGeography: Global"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def summarize_trends(prompt_text, model="gpt-4o-mini", api_key=None, provider="openai"):
    """
    Summarize trends using any LLM provider via litellm.
    """
    try:
        # litellm uses environment variables by default, but we can pass keys explicitly
        if api_key:
            if provider == "openai":
                os.environ["OPENAI_API_KEY"] = api_key
            elif provider == "anthropic":
                os.environ["ANTHROPIC_API_KEY"] = api_key
            elif provider == "google":
                os.environ["GEMINI_API_KEY"] = api_key
            elif provider == "groq":
                os.environ["GROQ_API_KEY"] = api_key

        response = completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.35,
            response_format={ "type": "json_object" } if provider == "openai" else None
        )
        
        content = response.choices[0].message.content
        
        # Clean up markdown if not in JSON mode
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
            
        return json.loads(content)
    except Exception as e:
        print(f"Error calling {model}: {e}")
        return None

def save_outputs(data, base_path="."):
    if not data:
        print("No data to save.")
        return

    json_path = os.path.join(base_path, "market_trends.json")
    txt_path = os.path.join(base_path, "market_trends.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Market Trend Summary ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        f.write("Overview:\n")
        f.write(data.get("overview", "N/A") + "\n\n")

        f.write("Key Trends:\n")
        for t in data.get("trends", []):
            f.write(f"- {t.get('trend', 'Unknown Trend')}\n")
            f.write(f"  {t.get('description', '')}\n")
            f.write(f"  Implications: {t.get('implications', '')}\n\n")

        f.write("Risks & Uncertainties:\n")
        for r in data.get("risks_and_uncertainties", []):
            f.write(f"- {r}\n")

def main():
    print("Market Trend Summarization Agent starting...")
    prompt_text = read_input()
    # Defaulting to gpt-4o-mini for CLI, but can be changed
    trends = summarize_trends(prompt_text, model="openai/gpt-4o-mini")
    if trends:
        save_outputs(trends)
        print("Market trend summarization completed successfully.")
    else:
        print("Failed to generate trends.")

if __name__ == "__main__":
    main()
