import json
import os
import sys
from openai import OpenAI
from datetime import date

# Safely initialize client
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("❌ Error: OPENAI_API_KEY environment variable not found.")
    print('Please set your OPENAI_API_KEY.')
    print('Example: $env:OPENAI_API_KEY="your-key-here" (PowerShell) or set OPENAI_API_KEY="your-key" (CMD)')
    sys.exit(1)

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are an Elite FAQ Generation Agent for Enterprise Products.

Rules:
- Generate extraordinarily clear, relevant FAQs based on the provided product and audience.
- Focus strictly on real user concerns and objections.
- Completely avoid fluffy marketing language and sales hype.
- Keep answers concise, honest, and direct.
- Structure and format the language to sound deeply professional and reassuring.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "analysis": "A brief internal thought on how to correctly answer the known concerns honestly but reassuringly.",
  "faqs": [
    {
      "question": "Clear user concern formatted as a question",
      "answer": "Direct, honest, and helpful answer"
    }
  ]
}
"""

def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_faqs(prompt_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.35,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("faq.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("faq.txt", "w", encoding="utf-8") as f:
        f.write(f"Frequently Asked Questions ({date.today()})\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"🧠 Strategy: {data.get('analysis', '')}\n\n")
        
        for faq in data.get("faqs", []):
            f.write(f"Q: {faq.get('question', '')}\n")
            f.write(f"A: {faq.get('answer', '')}\n\n")

def main():
    print("🚀 Initializing FAQ extraction...")
    prompt_text = read_input()
    faqs = generate_faqs(prompt_text)
    save_outputs(faqs)
    print("✨ FAQ generation complete. Built `faq.json` and `faq.txt`.")
    print(f"\n🧠 Strategy: {faqs.get('analysis', '')}")

if __name__ == "__main__":
    main()
