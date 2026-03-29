import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

def review_code_advanced(code, language="python", style_guide="Clean Code / Standard", model="gpt-4o-mini"):
    """
    Performs a deep technical review and returns fixed implementation + analysis JSON.
    """
    
    user_prompt = f"""
Language: {language}
Style Guide: {style_guide}

Code:
```
{code}
```

As a senior engineer, perform a pull request (PR) style review.
Identify issues, risks, and provide a full refactored version that follows {style_guide} standards.
"""

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3, # Stable but creative for refactoring
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "message": "Failed to perform review. Please check your credentials or model."}
