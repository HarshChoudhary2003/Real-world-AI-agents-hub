import json
import litellm
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables (OPENAI_API_KEY, etc.)
load_dotenv()

def generate_code_multi_file(idea, tech_stack, model="gpt-4o-mini"):
    """
    Generate clean, multi-file code for a project idea.
    """
    
    # We want to encourage a clean structure, so we include it in the user prompt
    user_prompt = f"""
Project Idea:
{idea}

Technical Stack:
{tech_stack}

Please generate a high-performance, modular implementation for this project.
Include all necessary files (e.g., app.py, requirements.txt, .gitignore, etc.).
"""

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3, # Lower temperature for stable code generation
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "message": "Neural generation failed. Check API key or model availability."}

def save_generated_project(result, base_dir="output"):
    """
    Utility to save the generated files to a local directory (useful for 'Run Code' or local export).
    """
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    for file_info in result.get("files", []):
        file_path = os.path.join(base_dir, file_info["file_path"])
        # Handle subdirectories
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_info["content"])
    
    return base_dir
