import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load local .env
load_dotenv()

def debug_code(code, error="", language="python", level="Expert", model="gpt-4o-mini"):
    """
    Analyzes code errors and returns fixed code + explanation in JSON.
    """
    
    # Constructing a rich user prompt
    user_prompt = f"""
Language: {language}
Experience Level Target: {level}

Code Snippet:
```
{code}
```

Error Message (if any):
{error if error else "Analyze for bugs and logic errors based on standard practices."}

Please fix this code and provide a line-by-line debugging guide for the most important lines.
"""

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Very precise decoding for debugging
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "message": "Debugger brain encountered an internal glitch. Verify your model settings."}
