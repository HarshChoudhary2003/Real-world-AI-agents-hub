import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are an API Documentation Agent.

Rules:
- Generate clear, structured API documentation
- Use precise technical language
- Include examples and error references
- Do NOT invent endpoints

Return ONLY valid JSON with this schema:
{
  "endpoint": "POST /users or relevant route",
  "overview": "Clear description of the API functionality",
  "request": {"field_name": "type and description"},
  "response": {"field_name": "type and description"},
  "examples": ["json string representation of example request/response"],
  "errors": ["400: Bad Request"]
}
"""

def read_spec(path: str = "api_spec.txt") -> str:
    if not os.path.exists(path):
        content = "Endpoint: POST /users\nDescription: Create a new user\nAuthentication: Bearer token\n\nRequest Body:\n- name (string, required)\n- email (string, required)\n\nResponse:\n- id (string)\n- name (string)\n- email (string)\n\nErrors:\n- 400 Bad Request\n- 401 Unauthorized\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_json(content_raw: str) -> dict:
    content = str(content_raw)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        start_idx = int(content.find("{"))
        end_idx = int(content.rfind("}")) + 1
        content = content[start_idx:end_idx]
    return json.loads(content)

def generate_docs(spec_text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating API Docs via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": spec_text}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    with open("api_docs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("api_docs.md", "w", encoding="utf-8") as f:
        f.write("# API Documentation\n\n")
        f.write(f"## {data.get('endpoint', 'Unknown Endpoint')}\n\n")
        f.write(f"{data.get('overview', 'No overview provided.')}\n\n")

        f.write("### Request Context\n")
        for k, v in data.get("request", {}).items():
            f.write(f"- **{k}**: {v}\n")

        f.write("\n### Response Architecture\n")
        for k, v in data.get("response", {}).items():
            f.write(f"- **{k}**: {v}\n")

        examples = data.get("examples", [])
        if examples:
            f.write("\n### Usage Examples\n")
            for ex in examples:
                f.write(f"```json\n{ex}\n```\n")

        errors = data.get("errors", [])
        if errors:
            f.write("\n### Error Contracts\n")
            for e in errors:
                f.write(f"- {e}\n")

def main():
    print("🚀 API Documentation Agent: Parsing specifications...")
    try:
        spec_text = read_spec()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        docs = generate_docs(spec_text, model=model)
        save_outputs(docs)
        
        print("✅ API documentation formulated successfully.")
        print("📁 Outputs: api_docs.json, api_docs.md")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
