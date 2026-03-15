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
You are an Elite Presentation and Slide Architect.

Rules:
- Convert the provided script into a highly polished, professional slide outline.
- Strictly allocate ONE main idea per slide to prevent cognitive overload.
- Keep bullets extremely concise (6 words or fewer per bullet if possible).
- Do NOT include full sentences unless absolutely necessary.
- Optimize the flow for a visual presentation.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "analysis": "A brief internal thought on pacing, narrative arc, and how to chunk the text visually.",
  "slides": [
    {
      "slide_number": 1,
      "title": "Clear Slide Title",
      "bullets": ["Punchy bullet 1", "Punchy bullet 2"]
    }
  ]
}
"""

def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_slides(script_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": script_text}
        ],
        temperature=0.35,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("slides.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("slides.txt", "w", encoding="utf-8") as f:
        f.write(f"Slide Outline ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"🧠 Strategy: {data.get('analysis', '')}\n\n")
        
        for slide in data.get("slides", []):
            f.write(f"Slide {slide.get('slide_number', '?')}: {slide.get('title', '')}\n")
            for b in slide.get("bullets", []):
                f.write(f"- {b}\n")
            f.write("\n")

def main():
    print("🚀 Initializing Slide Architecture engine...")
    script = read_input()
    slides = generate_slides(script)
    save_outputs(slides)
    print("✨ Slide outline generated successfully. Check `slides.txt` and `slides.json`.")
    print(f"\n🧠 Strategy: {slides.get('analysis', '')}")

if __name__ == "__main__":
    main()
