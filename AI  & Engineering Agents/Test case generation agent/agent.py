import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a Test Case Generation Agent.

Rules:
- Generate meaningful test cases
- Cover normal and edge cases
- Align with Python unittest style
- Do NOT invent behavior

Return ONLY valid JSON with this schema:
{
  "test_cases": [
    {
      "description": "Short description of the case",
      "inputs": {"a": 10, "b": 2},
      "expected": "5.0 or Exception"
    }
  ]
}
"""

def read_code(path: str = "source_code.py") -> str:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("def divide(a, b):\n    if b == 0:\n        raise ValueError(\"Division by zero\")\n    return a / b\n")
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
        content = str(content)[start_idx:end_idx]
    return json.loads(content)

def generate_tests(code_text: str, model: str = "gpt-4o") -> dict:
    print(f"📡 Generating Test Cases via {model}...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": code_text}
        ],
        temperature=0.2
    )
    return extract_json(response.choices[0].message.content)

def save_outputs(data: dict):
    # Save JSON report
    report = {
        "date": str(date.today()),
        "tests": data.get("test_cases", [])
    }

    with open("test_cases_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Save Python test file
    with open("generated_tests.py", "w", encoding="utf-8") as f:
        f.write("import unittest\n\n")
        # In a real dynamic context we might not know the exact filename or method name generically
        # But this is formatted for the current code context based on the example.
        f.write("# NOTE: You may need to adjust the import depending on your actual file and function names\n")
        f.write("from source_code import divide\n\n")
        f.write("class TestGeneratedCode(unittest.TestCase):\n")
        for i, t in enumerate(data.get("test_cases", []), 1):
            f.write(f"    def test_case_{i}(self):\n")
            f.write(f"        \"\"\"{t.get('description', '')}\"\"\"\n")
            
            expected = str(t.get('expected', ''))
            inputs = t.get('inputs', {})
            
            if "Exception" in expected or "Error" in expected:
                f.write(
                    f"        with self.assertRaises(ValueError):\n"
                    f"            divide(**{inputs})\n\n"
                )
            else:
                f.write(
                    f"        self.assertEqual(divide(**{inputs}), {expected})\n\n"
                )

def main():
    print("🚀 Test Case Generation Agent: Initiating specifications...")
    try:
        code_text = read_code()
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
        
        tests = generate_tests(code_text, model=model)
        save_outputs(tests)
        
        print("✅ Test cases generated successfully.")
        print("📁 Outputs: generated_tests.py, test_cases_report.json")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
