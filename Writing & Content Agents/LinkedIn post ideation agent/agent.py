import json
import os
from datetime import date
from openai import OpenAI
import anthropic
import google.generativeai as genai

SYSTEM_PROMPT = """
You are an Elite LinkedIn Viral Post Architect and Ideation Agent.

Your job is to generate 5 completely distinct, high-impact LinkedIn post strategies.
For each concept, you must:
- Use proven content frameworks (e.g., Problem-Agitate-Solve, AIDA, Story-Lesson-Action).
- Write a scroll-stopping, psychological hook.
- Draft the ACTUAL full post, perfectly formatted for LinkedIn (short paragraphs, punchy sentences, appropriate emojis).
- Provide a strong, discussion-oriented Call To Action (CTA).
- Suggest a visual asset (Image, Chart, Carousel, or Text-only).
- Assign an estimated engagement potential score.

Return ONLY valid JSON exactly matching this schema:

{
  "ideas": [
    {
      "title": "A short descriptive title for the strategy",
      "framework": "The psychological or content framework used",
      "hook": "The specific hook line",
      "core_message": "A summary of the central insight",
      "full_post_draft": "The entire ready-to-publish LinkedIn post, including formatting",
      "visual_suggestion": "Description of the ideal accompanying media",
      "estimated_engagement_score": "e.g., 94/100",
      "cta": "The specific provocative question or action at the end",
      "hashtags": ["#tag1", "#tag2"]
    }
  ]
}
"""

def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_ideas(prompt_text, model="gpt-4o-mini", temperature=0.7):
    if model.startswith("gpt-") or model.startswith("o1-") or model.startswith("o3-"):
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        params = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ]
        }
        if not (model.startswith("o1-") or model.startswith("o3-")):
            params["temperature"] = temperature
            
        response = client.chat.completions.create(**params)
        
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
        
    elif model.startswith("claude-"):
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=model,
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            temperature=temperature
        )
        text = response.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
        
    elif model.startswith("gemini-"):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        generation_config = {"temperature": temperature, "response_mime_type": "application/json"}
        genai_model = genai.GenerativeModel(model_name=model, system_instruction=SYSTEM_PROMPT, generation_config=generation_config)
        response = genai_model.generate_content(prompt_text)
        return json.loads(response.text)
        
    else:
        raise ValueError(f"Unsupported model: {model}")

def save_outputs(data):
    # Save the raw JSON data
    with open("ideas.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Save a readable text version
    with open("ideas.txt", "w", encoding="utf-8") as f:
        f.write(f"Elite LinkedIn Post Ideation ({date.today()})\n")
        f.write("=" * 50 + "\n\n")
        for i, idea in enumerate(data.get("ideas", []), 1):
            f.write(f"IDEA #{i}: {idea.get('title', '')}\n")
            f.write(f"[{idea.get('estimated_engagement_score', '')} Potential | Framework: {idea.get('framework', '')}]\n")
            f.write("-" * 50 + "\n")
            f.write(f"HOOK: {idea.get('hook', '')}\n")
            f.write(f"CORE MESSAGE: {idea.get('core_message', '')}\n")
            f.write(f"VISUAL: {idea.get('visual_suggestion', '')}\n\n")
            
            f.write(f"--- FULL POST DRAFT ---\n")
            f.write(f"{idea.get('full_post_draft', '')}\n")
            f.write(f"-----------------------\n\n")
            
            f.write(f"CTA: {idea.get('cta', '')}\n")
            if idea.get("hashtags"):
                f.write(f"HASHTAGS: {' '.join(idea.get('hashtags', []))}\n")
            f.write("\n" + "="*50 + "\n\n")

def main():
    prompt_text = read_input()
    # Provide a default model (e.g. gpt-4o-mini) and let it error if no api key found for CLI usage
    # If the user is missing a key, it will raise standard openai errors just like original.
    ideas = generate_ideas(prompt_text)
    save_outputs(ideas)
    print("LinkedIn post ideas generated successfully.")
    print(f"Ideas generated: {len(ideas.get('ideas', []))}")

if __name__ == "__main__":
    main()
