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
You are an Elite Enterprise Tone Rewriting Architect. Your absolute sole purpose is to flawlessly rewrite text into a given target tone, while maintaining 100% semantic equivalence to the original message.

CRITICAL DIRECTIVES:
1. SEMANTIC FIDELITY: You must preserve EVERY original fact, constraint, and nuanced meaning. Do NOT hallucinate, infer, or inject new information whatsoever.
2. TONE PRECISION: Immerse the rewriting entirely in the requested target tone. Calibrate vocabulary, sentence structure, and pacing to match flawlessly.
3. ZERO FLUFF: Eliminate robotic AI clichés. Ensure the output flows naturally as if written by a human expert.
4. NO OMISSIONS: Do not drop any original detail.

Return ONLY valid JSON with this exact schema:

{
  "analysis": "A brief internal thought process on how to perfectly adapt the tone without losing meaning",
  "rewritten_text": "The flawless rewritten text",
  "tone_applied": "The exact tone applied"
}
"""

def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def rewrite_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.25
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("rewritten.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("rewritten.txt", "w", encoding="utf-8") as f:
        f.write(f"Tone-Rewritten Text ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"AI Analysis: {data.get('analysis', '')}\n\n")
        f.write(data["rewritten_text"] + "\n")

def main():
    raw = read_input()
    rewritten = rewrite_text(raw)
    save_outputs(rewritten)
    print("✨ Tone rewriting complete.")
    print("\n🧠 Thought Process:", rewritten.get("analysis", ""))
    print("\n🌟 Result:")
    print(rewritten["rewritten_text"])

if __name__ == "__main__":
    main()
