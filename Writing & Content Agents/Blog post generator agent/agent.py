import json
from datetime import date
from openai import OpenAI
import anthropic
import google.generativeai as genai
import os

SYSTEM_PROMPT = """
You are an Elite SEO-Optimized Blog Post Generator Agent.

Your job:
- Generate a powerful, highly engaging, well-structured blog post.
- Adapt tone and depth to the target audience with absolute precision.
- Optimize the content for search engines (SEO) using the provided target keywords.
- Use strong, clear section headers and advanced formatting (e.g., bullet points, bold text).
- Include an attention-grabbing hook, a compelling introduction, and a strong call-to-action (CTA).
- Provide a brief social media promo post.
- Keep writing highly readable, avoiding fluff, jargon, or repetition.

Return ONLY valid JSON with this exact schema:

{
  "seoTitle": "Optimized title under 60 chars",
  "slug": "url-friendly-slug",
  "metaDescription": "Optimized description under 160 chars",
  "keywords": ["key1", "key2"],
  "title": "Engaging display title",
  "hook": "An attention grabbing first sentence",
  "introduction": "Introductory paragraphs",
  "sections": [
    {
      "header": "Section Header",
      "content": "Rich markdown content including lists or bold text where applicable. Min 150 words per section."
    }
  ],
  "conclusion": "Summary and final thoughts",
  "callToAction": "A strong CTA for the audience",
  "socialMediaPost": "A concise post for Twitter/LinkedIn with emojis and hashtags"
}
"""

def read_blog_input(path="blog.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_blog(blog_instructions, model="gpt-4o-mini", temperature=0.7):
    if model.startswith("gpt-") or model.startswith("o1-") or model.startswith("o3-"):
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # O-series models don't support temperature or system roles in the same way, but standard GPTs do
        # We will keep temperature standard for GPT models. Note: o-series models might ignore it.
        params = {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": blog_instructions}
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
                {"role": "user", "content": blog_instructions}
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
        response = genai_model.generate_content(blog_instructions)
        return json.loads(response.text)
    else:
        raise ValueError(f"Unsupported model: {model}")

def save_outputs(blog):
    with open("blog.json", "w", encoding="utf-8") as f:
        json.dump(blog, f, indent=2)

    with open("blog.txt", "w", encoding="utf-8") as f:
        f.write(f"SEO Title: {blog.get('seoTitle', '')}\n")
        f.write(f"Slug: {blog.get('slug', '')}\n")
        f.write(f"Meta Description: {blog.get('metaDescription', '')}\n")
        f.write(f"Keywords: {', '.join(blog.get('keywords', []))}\n")
        f.write("=" * 40 + "\n\n")
        
        f.write(f"{blog.get('title', '')}\n")
        f.write("=" * len(blog.get("title", "")) + "\n\n")

        f.write(f"{blog.get('hook', '')}\n\n")
        f.write(f"{blog.get('introduction', '')}\n\n")

        for s in blog.get("sections", []):
            f.write(f"## {s.get('header', '')}\n")
            f.write(f"{s.get('content', '')}\n\n")

        f.write("## Conclusion\n")
        f.write(f"{blog.get('conclusion', '')}\n\n")
        
        f.write("## Call to Action\n")
        f.write(f"{blog.get('callToAction', '')}\n\n")
        
        f.write("--- Social Media Promo ---\n")
        f.write(f"{blog.get('socialMediaPost', '')}\n")

def main():
    instructions = read_blog_input()
    blog = generate_blog(instructions)
    save_outputs(blog)
    print("Blog post generated successfully.")
    print(blog["title"])

if __name__ == "__main__":
    main()
