import json
import os
import argparse
from datetime import date

# Import API Clients
from openai import OpenAI
import anthropic
import groq
import google.generativeai as genai

SYSTEM_PROMPT = """
You are an elite, enterprise-grade Web Research Expert Agent.

Rules:
- Synthesize complex information from diverse web domains and knowledge sources.
- Focus strictly on high relevance, absolute factual accuracy, and credibility.
- Do NOT copy text verbatim; synthesize and paraphrase professionally.
- Clearly separate established facts, emerging trends, and unresolved questions.
- Provide actionable, executive-level insights.

Return ONLY valid JSON strictly matching this schema (do not wrap in markdown tags like ```json):

{
  "summary": "High-level executive summary (2-3 paragraphs)",
  "key_findings": ["Actionable finding 1", "Actionable finding 2"],
  "trends": ["Emerging trend 1", "Emerging trend 2"],
  "open_questions": ["Critical unknown 1", "Critical unknown 2"]
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        default_input = (
            "Topic: AI Agents in Enterprise Productivity\n"
            "Scope: High-level executive overview\n"
            "Focus Areas: Automation, ROI, Security risks\n"
            "Timeframe: Last 12 months"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(default_input)
        return default_input

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def conduct_research(api_provider, model, prompt_text):
    print(f"Initiating autonomous intelligence gathering using {api_provider} ({model})...")
    
    if api_provider == "openai":
        client = OpenAI() # Requires OPENAI_API_KEY environment variable
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.3,
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)

    elif api_provider == "anthropic":
        client = anthropic.Anthropic() # Requires ANTHROPIC_API_KEY
        response = client.messages.create(
            model=model,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        content = response.content[0].text
        start = content.find('{')
        end = content.rfind('}') + 1
        return json.loads(content[start:end])

    elif api_provider == "groq":
        client = groq.Groq() # Requires GROQ_API_KEY
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    elif api_provider == "gemini":
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY")) # Requires GEMINI_API_KEY
        model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction=SYSTEM_PROMPT,
            generation_config={"temperature": 0.3, "response_mime_type": "application/json"}
        )
        response = model_instance.generate_content(prompt_text)
        return json.loads(response.text)
    
    else:
        raise ValueError("Unsupported AI Provider")

def save_outputs(data):
    with open("research.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("research.txt", "w", encoding="utf-8") as f:
        f.write(f"Executive Intelligence Report ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        f.write("Summary:\n")
        f.write(data.get("summary", "") + "\n\n")

        f.write("Key Findings:\n")
        for k in data.get("key_findings", []):
            f.write(f"- {k}\n")

        f.write("\nTrends:\n")
        for t in data.get("trends", []):
            f.write(f"- {t}\n")

        f.write("\nOpen Questions:\n")
        for q in data.get("open_questions", []):
            f.write(f"- {q}\n")
            
    print(f"Intelligence successfully written to research.json and research.txt.")

def main():
    parser = argparse.ArgumentParser(description="Multi-Model Enterprise Web Research Agent")
    parser.add_argument("--provider", type=str, choices=["openai", "anthropic", "groq", "gemini"], default="openai", help="The AI Provider to use.")
    parser.add_argument("--model", type=str, help="Specific model to use (e.g., gpt-4o, claude-3-5-sonnet-20240620).", default=None)
    args = parser.parse_args()

    # Default models fallback
    if not args.model:
        defaults = {
            "openai": "gpt-4o",
            "anthropic": "claude-3-5-sonnet-20240620",
            "groq": "llama3-70b-8192",
            "gemini": "gemini-1.5-pro"
        }
        args.model = defaults[args.provider]

    prompt_text = read_input()
    print(f"Loaded Research Parameters from input.txt:\n{prompt_text}\n")
    
    try:
        research = conduct_research(args.provider, args.model, prompt_text)
        save_outputs(research)
        print("Web research agent deployment completed successfully.")
    except Exception as e:
        print(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()