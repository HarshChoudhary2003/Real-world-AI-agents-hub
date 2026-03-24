import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI()  # requires OPENAI_API_KEY
base_path = os.path.dirname(__file__)

SYSTEM_PROMPT = """
You are a Persona-Driven Agent.

Rules:
- Strictly adhere to the provided persona in all responses.
- Maintain consistent tone, values, and constraints as defined.
- Do NOT express personal opinions or deviate from the role.
- Be precise and professional.

Return ONLY valid JSON with this schema:

{
  "persona_response": "",
  "persona_used": ""
}
"""

def main():
    print("Initiating Persona-Driven Interaction...")
    
    # Path setup
    persona_path = os.path.join(base_path, "persona.txt")
    input_path = os.path.join(base_path, "input.txt")
    output_path = os.path.join(base_path, "output.json")

    try:
        with open(persona_path, "r", encoding="utf-8") as f:
            persona = f.read()
        with open(input_path, "r", encoding="utf-8") as f:
            user_input = f.read()
    except FileNotFoundError as e:
        print(f"Error: Required file not found: {e.filename}")
        return

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Neural Persona Definition:\n{persona}\n\nClient Request:\n{user_input}"}
        ],
        response_format={ "type": "json_object" },
        temperature=0.3
    )

    result = json.loads(response.choices[0].message.content)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Persona-driven response generated for role: {result.get('persona_used', 'Unknown')}")

if __name__ == "__main__":
    main()
