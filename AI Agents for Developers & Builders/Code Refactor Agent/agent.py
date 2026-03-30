import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()

def refactor_code(code, style_guide="PEP8 (Python)", model="gpt-4o-mini"):
    """
    Transforms messy code into clean, production-grade implementation.
    Returns refactored code, diffs, performance gains, and style notes.
    """
    user_prompt = f"""
SOURCE CODE TO REFACTOR:
{code}

STYLE GUIDE TO APPLY: {style_guide}

Perform a comprehensive refactoring pass:
- Fix all style violations
- Improve naming, structure, and modularity
- Optimize time/space complexity where possible
- Generate a before/after diff for every major change
Return all results in the required JSON format.
"""
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {
            "error": str(e),
            "message": "Refactor engine failure. Check API key and model availability."
        }
