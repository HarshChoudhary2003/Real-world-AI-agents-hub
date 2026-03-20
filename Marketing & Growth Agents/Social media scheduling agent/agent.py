import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Social Media Strategy & Scheduling Agent (Social-Sync AI v2.0).

Mission: Architect high-impact, platform-optimized posting schedules that maximize reach and engagement.

Rules for Strategy:
1. **Platform Diversity**: Tailor content style specifically for the platform (e.g., professional for LinkedIn, punchy/viral for X).
2. **Engagement Windows**: Suggest times in the provided timezone (EST) based on peak audience engagement patterns.
3. **Cohesive Narrative**: Ensure the scheduled posts follow a logical storytelling loop (Awareness -> Value -> Trust).
4. **Strategic Metadata**: Include high-relevance hashtags and meta-tags for each post.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "project_overview": {
     "campaign_identity": "Catchy campaign name",
     "primary_goal": "The main objective of the schedule"
  },
  "posts": [
     {
       "day_index": "Day 1, 2, 3...",
       "platform": "LinkedIn/X/etc.",
       "scheduled_time_est": "e.g., 9:15 AM EST",
       "content_hook": "A brief draft or hook of the post content",
       "strategic_rationale": "Why this time and this content?",
       "visual_recommendation": "Advice on image or video type",
       "hashtags": ["#Tag1", "#Tag2"]
     }
  ],
  "platform_best_practices": ["Advice for thread structure on X or LinkedIn algorithms"]
}
"""

def read_input(path="input.txt"):
    """Reads input data from a local text file."""
    if not os.path.exists(path):
        return "Platforms: LinkedIn, Twitter. Timezone: EST. Goal: Product Awareness."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_json(response_content):
    """Robustly parse JSON out of an LLM response."""
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        # Try stripping markdown blocks
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", str(response_content))
        if match:
            try:
                return json.loads(match.group(1).strip())
            except:
                pass
        
        # Try finding anything between braces
        match = re.search(r"\{[\s\S]*\}", str(response_content))
        if match:
            try:
                return json.loads(match.group(0).strip())
            except:
                pass
    raise ValueError("Failed to extract valid JSON from the model's response.")

def generate_social_schedule(prompt_text, model_name="gpt-4o-mini", api_key=None):
    """Generates advanced social schedule using LiteLLM."""
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.4
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the social schedule as JSON and formatted TXT."""
    with open("social_schedule.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("social_schedule.txt", "w", encoding="utf-8") as f:
        f.write(f"Social-Sync AI Strategy Schedule ({date.today()})\n")
        f.write("=" * 60 + "\n\n")

        po = data.get('project_overview', {})
        f.write(f"Campaign: {po.get('campaign_identity')}\n")
        f.write(f"Objective: {po.get('primary_goal')}\n\n")
        
        posts = data.get('posts', [])
        for post in posts:
            f.write(f"--- {post.get('day_index')} | {post.get('platform')} ---\n")
            f.write(f"Time: {post.get('scheduled_time_est')}\n")
            f.write(f"Content Hook: {post.get('content_hook')}\n")
            f.write(f"Strategy: {post.get('strategic_rationale')}\n")
            f.write(f"Visual: {post.get('visual_recommendation')}\n")
            f.write(f"Tags: {', '.join(post.get('hashtags', []))}\n\n")

        f.write("--- 📜 Platform Mastery Tips ---\n")
        for tip in data.get("platform_best_practices", []):
            f.write(f"- {tip}\n")

def main():
    print("🚀 Social-Sync AI: Architecting Cross-Platform Schedule...")
    prompt_text = read_input()
    try:
        schedule = generate_social_schedule(prompt_text)
        save_outputs(schedule)
        print("✅ Social media schedule strategy completed successfully.")
        print("📁 Outputs: social_schedule.json, social_schedule.txt")
    except Exception as e:
        print(f"❌ Schedule Prep failed: {str(e)}")

if __name__ == "__main__":
    main()
