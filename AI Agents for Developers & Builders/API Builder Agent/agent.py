import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

def build_api_advanced(feature, framework="FastAPI", database="PostgreSQL", auth="JWT", model="gpt-4o-mini"):
    """
    Builds a full-featured backend API and returns a full ecosystem JSON (Code, Docker, Auth, etc.).
    """
    
    user_prompt = f"""
API Feature Request:
{feature}

Technical Constraints:
Framework: {framework}
Database: {database}
Authentication: {auth if auth else "None"}

Please build a high-performance, production-ready API for this requirement.
Include all necessary models, routes, auth logic, and containerization configs.
"""

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3, # Low temperature for structured implementation
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "message": "The backend architect is currently debugging an incident. Please retry or check your keys."}
