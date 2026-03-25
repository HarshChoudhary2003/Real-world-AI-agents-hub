import os
import requests
import litellm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    Uses AI to calculate a match percentage between a resume and a job description.
    """
    if not resume or not job_description:
        return 0, "No data to compare."

    # Set API key for LiteLLM if provided manually
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    prompt = f"""
    You are an expert AI Career Matchmaker. 
    Compare the following Resume and Job Description.
    
    ### Resume:
    {resume[:2000]} # Limit for token safety
    
    ### Job Description:
    {job_description[:2000]}
    
    Analyze the skill overlap, experience relevance, and cultural fit.
    
    RETURN ONLY A JSON OBJECT with these keys:
    - score: (Integer between 0 and 100)
    - analysis: (A one-sentence punchy summary of the match)
    """

    try:
        # We use litellm for universal routing (gpt-4o-mini as default)
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        import json
        result = json.loads(response.choices[0].message.content)
        return result.get("score", 0), result.get("analysis", "No analysis provided.")
    except Exception as e:
        return 0, f"Error calculating match: {str(e)}"
