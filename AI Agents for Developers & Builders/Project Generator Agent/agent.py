import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()

def generate_project(domain, level, keywords="", model="gpt-4o-mini"):
    """
    Generates a complete, portfolio-worthy project blueprint.
    """
    keyword_instruction = f"\nKeywords / Interests to incorporate: {keywords}" if keywords.strip() else ""

    user_prompt = f"""
DOMAIN: {domain}
DIFFICULTY LEVEL: {level}
{keyword_instruction}

Generate one compelling, original, portfolio-worthy project idea with full technical blueprint.
Make it impressive enough to stand out on GitHub and LinkedIn.
"""
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.75,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {
            "error": str(e),
            "message": "Project Generator engine failure. Check API key and model availability."
        }
