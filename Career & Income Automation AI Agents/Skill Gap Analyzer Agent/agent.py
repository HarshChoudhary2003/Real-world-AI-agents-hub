import os
import json
import litellm
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, get_analysis_prompt

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

def analyze_skill_gap(resume, job_desc, model="gpt-4o-mini", api_key=None):
    """
    Analyzes the gap between a resume and a job description via LiteLLM.
    """
    if not resume or not job_desc:
        return {"error": "Wait! Both a resume and a job description are required for a quality analysis."}

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
    user_prompt = get_analysis_prompt(resume, job_desc)

    # Call LiteLLM
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.3
        )
        # Parse Result
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"error": f"Gap Analysis Failed: {str(e)}"}
