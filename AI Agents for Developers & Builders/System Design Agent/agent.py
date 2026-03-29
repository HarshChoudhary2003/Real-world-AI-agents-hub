import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

def design_system_advanced(idea, scale, model="gpt-4o-mini"):
    """
    Designs a high-scale system architecture and returns a full blueprint JSON.
    """
    
    user_prompt = f"""
System Idea:
{idea}

Scale Complexity:
{scale} (1K, 100K, or 1M+ users)

Please provide a detailed architecture, data flow, tech stack, and scaling strategy.
Include a Mermaid.js diagram and estimated cloud infrastructure costs.
"""

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4, # Balanced for structural consistency
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "message": "The system architect is currently in a meeting. Please try again or check your keys."}
