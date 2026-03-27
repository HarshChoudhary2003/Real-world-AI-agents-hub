import os
import json
import litellm
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, get_planner_prompt

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

def generate_plan(goals, hours, model="gpt-4o-mini", api_key=None):
    """
    Generates a structured daily plan via LiteLLM.
    """
    if not goals or not hours:
        return {"error": "Wait! Both goals and available hours are required."}

    # Setup API keys (if provided as argument)
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

    # Prepare Prompt
    user_prompt = get_planner_prompt(goals, hours)

    # Call LiteLLM
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.5
        )
        # Parse Result
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"error": f"Plan Generation Failed: {str(e)}"}
