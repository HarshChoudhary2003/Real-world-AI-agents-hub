import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()

def explain_code(code, difficulty="Intermediate", interview_mode=False, model="gpt-4o-mini"):
    """
    Produces a deep, structured explanation of the provided code.
    """
    mode_instruction = ""
    if interview_mode:
        mode_instruction = "\n\nIMPORTANT: The user is in INTERVIEW MODE. Make the 'simple_explanation' and 'interview_answer' fields crisp, confident, and structured like a senior engineer answering in a technical interview."

    difficulty_instruction = f"\nEXPLANATION DEPTH: {difficulty}. Calibrate your vocabulary and depth accordingly."

    user_prompt = f"""
SOURCE CODE:
{code}
{difficulty_instruction}
{mode_instruction}

Perform a deep analysis and return the full JSON explanation.
"""

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {
            "error": str(e),
            "message": "Code Explainer neural engine failure. Check your API key and model availability."
        }
