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
You are an Elite Enterprise Product Description Architect.

Rules:
- Write clear, incredibly persuasive, benefit-driven product descriptions.
- Expertly map every provided feature to a tangible real-world outcome.
- Avoid all hype, exaggerations, or unsupported claims.
- Adapt your tone perfectly to the target audience.
- Make the reading experience highly scannable and professional.

Return ONLY valid JSON with this exact schema (no markdown blocks around it):

{
  "analysis": "A brief internal thought on how to correctly map these features to the target audience's pain points.",
  "product_name": "The Product Name",
  "description": "A compelling 2-3 paragraph primary product description.",
  "key_benefits": ["Benefit 1", "Benefit 2"],
  "ideal_for": "A clear description of the ideal customer.",
  "cta": "A powerful Call to Action."
}
"""

def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_description(prompt_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.4,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("product_description.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("product_description.txt", "w", encoding="utf-8") as f:
        f.write(f"{data['product_name']}\n")
        f.write("=" * len(data["product_name"]) + "\n\n")
        
        f.write(f"🧠 Strategy: {data.get('analysis', '')}\n\n")
        f.write(data["description"] + "\n\n")

        f.write("🎯 Key Benefits:\n")
        for b in data.get("key_benefits", []):
            f.write(f"- {b}\n")

        f.write(f"\n👤 Ideal For:\n{data.get('ideal_for', '')}\n")
        f.write(f"\n⚡ Call to Action:\n{data.get('cta', '')}\n")

def main():
    print("🚀 Initializing Product Description generation...")
    prompt_text = read_input()
    product = generate_description(prompt_text)
    save_outputs(product)
    print(f"✨ Product description generated successfully for '{product.get('product_name', 'Unknown')}'.")

if __name__ == "__main__":
    main()
