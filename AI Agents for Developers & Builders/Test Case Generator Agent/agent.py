import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

def generate_quality_tests(code, framework="pytest", model="gpt-4o-mini"):
    """
    Architects high-fidelity unit tests and quality assessments for the provided code.
    """
    
    user_prompt = f"""
SOURCE CODE:
{code}

TARGET FRAMEWORK: {framework}

Perform a deep architectural review and generate a complete test suite.
Identify edge cases, bugs to watch, and a strategic coverage plan.
Return everything in the requested JSON format.
"""

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Lower temperature for precision
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {
            "error": str(e), 
            "message": "SDET Logic failure. Please verify your Neural API connectivity."
        }
