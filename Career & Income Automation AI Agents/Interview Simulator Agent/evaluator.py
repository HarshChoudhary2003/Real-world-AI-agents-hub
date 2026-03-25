import os
import json
import litellm
from dotenv import load_dotenv
from prompts import EVALUATION_SYSTEM_PROMPT, get_evaluation_prompt

# Load environment variables
load_dotenv()

def evaluate_interview_answer(question, answer, model="gpt-4o-mini", api_key=None):
    """
    Evaluates an interview answer using a Lead Hiring Decision Maker's mindset.
    Returns a critical JSON analysis.
    """
    if not answer:
        return {"error": "Wait, don't submit an empty answer! Take a deep breath and give it your best shot."}

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
    user_prompt = get_evaluation_prompt(question, answer)

    # Call LiteLLM
    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={ "type": "json_object" },
            temperature=0.3
        )
        # Parse Result
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"error": f"Evaluation crashed: {str(e)}"}
