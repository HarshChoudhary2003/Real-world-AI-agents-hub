import json
from datetime import date
from openai import OpenAI

client = OpenAI()  # requires OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a Grammar Correction Agent.

Rules:
- Correct grammar, spelling, and punctuation
- Improve clarity while preserving original meaning
- Do NOT rewrite content or change tone
- Do NOT add new information
- Keep edits minimal

Return ONLY valid JSON with this schema:

{
  "corrected_text": "",
  "notes": []
}
"""

def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def correct_text(raw_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.1
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("corrected.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("corrected.txt", "w", encoding="utf-8") as f:
        f.write(f"Corrected Text ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write(data.get("corrected_text", "") + "\n")

    # Save notes if any
    if "notes" in data and data["notes"]:
        with open("corrected.txt", "a", encoding="utf-8") as f:
            f.write("\n\nCorrection Notes:\n")
            for note in data["notes"]:
                 f.write(f"- {note}\n")


def main():
    raw_text = read_input()
    corrected = correct_text(raw_text)
    save_outputs(corrected)
    print("Grammar correction complete.")
    print(corrected.get("corrected_text", ""))

if __name__ == "__main__":
    main()
