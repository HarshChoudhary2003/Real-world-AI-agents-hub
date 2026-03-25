import os
import requests
import litellm
import json
from dotenv import load_dotenv

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

def fetch_jobs(role, location, api_key=None, num_jobs=10):
    """
    Fetches job listings from RapidAPI JSearch.
    """
    url = "https://jsearch.p.rapidapi.com/search"

    # Use specified key or fallback to environment variable
    rapid_api_key = api_key or os.getenv("RAPIDAPI_KEY")
    
    if not rapid_api_key:
        return {"error": "RapidAPI Key not found. Please provide one in the sidebar."}

    querystring = {
        "query": f"{role} in {location}",
        "num_pages": "1",
        "date_posted": "week", # Focus on recent jobs
        "remote_jobs_only": "false"
    }

    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        response.raise_for_status()
        data = response.json()

        jobs = []
        for job in data.get("data", [])[:num_jobs]:
            jobs.append({
                "id": job.get("job_id"),
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "logo": job.get("employer_logo"),
                "location": f"{job.get('job_city', '')}, {job.get('job_country', '')}",
                "link": job.get("job_apply_link"),
                "description": job.get("job_description"),
                "posted_at": job.get("job_posted_at_datetime_utc", "")[:10]
            })

        return jobs
    except Exception as e:
        return {"error": f"Failed to fetch jobs: {str(e)}"}

def calculate_match_score(resume, job_description, model="gpt-4o-mini", api_key=None):
    """
    Uses AI via LiteLLM to calculate a match percentage between a resume and a job description.
    """
    if not resume or not job_description:
        return 0, "No data to compare."

    # Configure API key based on provider
    provider_prefix = model.split("/")[0] if "/" in model else "openai"
    key_env_map = {
        "gemini": "GEMINI_API_KEY",
        "groq": "GROQ_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY"
    }
    env_var_to_set = key_env_map.get(provider_prefix, "OPENAI_API_KEY")
    
    # Temporarily set key for session
    if api_key:
        os.environ[env_var_to_set] = api_key

    prompt = f"""
    You are an expert AI Career Matchmaker. 
    Compare the following Resume and Job Description.
    
    Resume Summary:
    {resume[:1500]} 

    Job Description:
    {job_description[:1500]}
    
    Analyze the skill overlap, experience relevance, and cultural fit.
    
    Return a JSON object with: 
    - score: integer (0-100)
    - analysis: one-sentence summary.
    """

    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("score", 0), result.get("analysis", "No analysis provided.")
    except Exception as e:
        return 0, f"Error: {str(e)}"
