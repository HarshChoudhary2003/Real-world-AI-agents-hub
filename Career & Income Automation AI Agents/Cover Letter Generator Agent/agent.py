import os
import litellm
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Dictionary of supported providers and their popular models
# Format: { "Display Name": ["model_identifier", ...] }
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

def generate_cover_letter(resume, job_description, model="gpt-4o-mini", company="the company", tone="Professional", focus="Overall Fit", variation_index=1, api_key=None):
    """
    Generates a personalized cover letter using LiteLLM for multi-provider support.
    """
    
    # Configure API key based on provider
    # LiteLLM automatically uses environment variables (OPENAI_API_KEY, GEMINI_API_KEY, GROQ_API_KEY)
    # But we allow passing an explicit key for the UI users.
    
    # Extract provider for key routing if explicit key is provided
    provider_prefix = model.split("/")[0] if "/" in model else "openai"
    
    # Map display names to LiteLLM env var names
    key_env_map = {
        "gemini": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY"
    }
    
    env_var_to_set = key_env_map.get(provider_prefix, "OPENAI_API_KEY")
    
    # If the user provides a key in the UI, we temporarily set it for the session
    if api_key:
        os.environ[env_var_to_set] = api_key

    user_prompt = f"""
        ### INSTRUCTIONS:
        - Generate a {tone} cover letter.
        - Primary Focus: {focus}.
        - Role context: Applying to {company}.
        - Variation: {variation_index} (Provide a unique angle relative to other versions).
        
        ### USER RESUME DATA:
        {resume}
        
        ### JOB DESCRIPTION DATA:
        {job_description}
        
        ### FINAL CHECK:
        - Ensure it bridges the resume's experience with the job's needs.
        - Focus on {focus} and use a {tone} tone.
    """

    try:
        response = litellm.completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7 + (variation_index * 0.1),
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"
