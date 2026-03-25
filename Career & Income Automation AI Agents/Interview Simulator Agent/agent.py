import os
import json
import litellm
from dotenv import load_dotenv
from prompts import QUESTION_SYSTEM_PROMPT, get_question_prompt

# Load environment variables
load_dotenv()

# Dictionary of supported providers and their popular models
SUPPORTED_MODELS = {
    "OpenAI": [
        "gpt-4o", 
        "gpt-4o-mini", 
        "gpt-4-turbo"
    ],
    "Google (Gemini)": [
        "gemini/gemini-1.5-pro", 
        "gemini/gemini-1.5-flash"
    ],
    "Groq": [
        "groq/llama3-70b-8192", 
        "groq/llama3-8b-8192",
        "groq/mixtral-8x7b-32768"
    ],
    "Anthropic": [
        "claude-3-5-sonnet-20240620",
        "claude-3-haiku-20240307"
    ]
}

def generate_interview_question(role, level, resume_context="", model="gpt-4o-mini", api_key=None):
    """
    Generates a single interview question via LiteLLM.
    """
    # 1. Setup API keys (if provided as argument)
    if api_key:
        provider_prefix = model.split("/")[0] if "/" in model else "openai"
        key_env_map = {
            "gemini": "GEMINI_API_KEY",
            "groq": "GROQ_API_KEY",
            "claude": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY"
        }
        env_var_to_set = key_env_map.get(provider_prefix, "OPENAI_API_KEY")
        os.environ[env_var_to_set] = api_key

    # 2. Prepare Prompt
    user_prompt = get_question_prompt(role, level, resume_context)

    # 3. Call LiteLLM
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": QUESTION_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating question: {str(e)}"
