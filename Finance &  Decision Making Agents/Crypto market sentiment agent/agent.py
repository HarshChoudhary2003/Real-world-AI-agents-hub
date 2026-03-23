import os
import json
import litellm
import re
from datetime import date
from dotenv import load_dotenv

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Crypto Market Sentiment Agent (SentimentCore AI).

Rules:
- Synthesize qualitative news, social media, and technical signals into a single sentiment profile
- Identify specific 'Signals of Divergence' (e.g., News is Bullish, Social is Bearish)
- Use a 'Sentiment Score' (0-100, where 0 is Extreme Fear and 100 is Extreme Greed)
- Always classify 'Trend Direction' (Accumulation / Distribution / Consolidation)
- Provide a confidence level based on source diversity
- Do NOT provide trading, legal, or investment advice. No price predictions.

Return ONLY valid JSON with this schema:

{
  "sentiment_score": 0-100,
  "overall_sentiment": "Fear / Neutral / Greed / Extreme Greed",
  "trend_direction": "Name of the current market state",
  "confidence_level": "Low / Medium / High",
  "supporting_signals": [
    { "source": "e.g., Social", "signal": "Bullish", "summary": "Detailed insight" }
  ],
  "divergence_notes": "Significant contradictions identified between data sources",
  "executive_summary": "Final synthesis for stakeholders"
}
"""

def extract_json(response_content):
    """Attempts to robustly parse JSON out of an LLM response."""
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", str(response_content))
        if match:
            try:
                return json.loads(match.group(1).strip())
            except:
                pass
        match = re.search(r"\{[\s\S]*\}", str(response_content))
        if match:
            try:
                return json.loads(match.group(0).strip())
            except:
                pass
    raise ValueError("Failed to extract valid JSON from the model's response.")

def analyze_sentiment(text, model_name="gpt-4o"):
    """Evaluates crypto market sentiment using multi-model intelligence via LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3
    }
    
    if "gpt-" in model_name or "o1-" in model_name:
        kwargs["response_format"] = {"type": "json_object"}
    
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    with open("crypto_sentiment.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("crypto_sentiment.txt", "w", encoding="utf-8") as f:
        f.write(f"CRYPTO MARKET SENTIMENT REPORT ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"🌐 OVERALL SENTIMENT: {data.get('overall_sentiment', 'N/A')}\n")
        f.write(f"Sentiment Score: {data.get('sentiment_score', 'N/A')}/100\n")
        f.write(f"Trend State: {data.get('trend_direction', 'N/A')}\n")
        f.write(f"Confidence: {data.get('confidence_level', 'N/A')}\n\n")
        
        f.write("🏷️ SIGNAL AUDIT\n")
        for s in data.get('supporting_signals', []):
            f.write(f"- [{s.get('source')}] {s.get('signal')}: {s.get('summary')}\n")
            
        f.write("\n⚠️ DIVERGENCE DETECTION\n" + data.get("divergence_notes", "None detected") + "\n\n")
        f.write("📝 EXECUTIVE SUMMARY\n" + data.get("executive_summary", "N/A") + "\n")

if __name__ == "__main__":
    with open("sentiment_input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()
    if input_text:
        sentiment = analyze_sentiment(input_text)
        save_outputs(sentiment)
        print("Crypto market sentiment analysis completed successfully.")
