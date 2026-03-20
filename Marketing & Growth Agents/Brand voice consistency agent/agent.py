import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Brand Voice Integrity & Linguistic Auditor (Voice-Verify AI v2.0).

Mission: Perform deep linguistic analysis on content to ensure strict adherence to established brand guidelines. Detect "Vibe Mismatches" and provide surgical alignment fixes.

Rules for Audit:
1. **Trait-Based Evaluation**: Measure against the traits in the guidelines (e.g., Professional, Approachable).
2. **Deviation Diagnostics**: Flag slang, hype, or overly casual language that dilutes the brand authority.
3. **Sentiment Calibration**: Analyze if the emotional "frequency" of the writing matches the intended brand feeling.
4. **Resonance Check**: How does the content "sound" to high-value users or founders?

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "audit_overview": {
     "alignment_score": "0-100",
     "verdict": "Critical/Moderate/Excellent Alignment",
     "narrative_assessment": "Short strategic summary"
  },
  "trait_alignment": [
     {"trait": "Trait name", "status": "Aligned/Deviated", "analysis": "Detailed breakdown"}
  ],
  "deviations": [
     {
       "original_segment": "The problematic text",
       "reason": "Slang/Hysteria/Casual/etc.",
       "psychological_impact": "How it confuses the target audience",
       "surgical_fix": "Professional replacement snippet"
     }
  ],
  "strengths": ["List of phrases or elements that embody the brand DNA"]
}
"""

def read_file(path):
    """Reads content from a local text file."""
    if not os.path.exists(path):
        return ""
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

def audit_brand_voice(guidelines, content, model_name="gpt-4o-mini", api_key=None):
    """Performs deep linguistic audit using LiteLLM."""
    prompt = f"Guidelines:\n{guidelines}\n\nContent to Review:\n{content}"
    
    kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    if api_key:
        kwargs["api_key"] = api_key
        
    response = litellm.completion(**kwargs)
    raw_content = response.choices[0].message.content
    return extract_json(raw_content)

def save_outputs(data):
    """Saves the brand voice review as JSON and formatted TXT."""
    with open("brand_voice_review.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("brand_voice_review.txt", "w", encoding="utf-8") as f:
        f.write(f"Voice-Verify AI: Linguistic Audit Report ({date.today()})\n")
        f.write("=" * 65 + "\n\n")

        ao = data.get('audit_overview', {})
        f.write(f"Alignment Score: {ao.get('alignment_score')}/100\n")
        f.write(f"Verdict: {ao.get('verdict')}\n")
        f.write(f"Summary: {ao.get('narrative_assessment')}\n\n")
        
        f.write("--- 🎭 Trait-by-Trait Alignment ---\n")
        for trait in data.get('trait_alignment', []):
            f.write(f"[{trait.get('status')}] {trait.get('trait')}: {trait.get('analysis')}\n")
        
        f.write("\n--- ✂️ Surgical Deviations & Fixes ---\n")
        for dev in data.get('deviations', []):
            f.write(f"Problem: \"{dev.get('original_segment')}\"\n")
            f.write(f"Issue: {dev.get('reason')} - {dev.get('psychological_impact')}\n")
            f.write(f"Fix: \"{dev.get('surgical_fix')}\"\n\n")

        f.write("--- ✅ DNA Strengths ---\n")
        for strength in data.get("strengths", []):
            f.write(f"- {strength}\n")

def main():
    print("🚀 Voice-Verify AI: Running Deep Linguistic Audit...")
    gl = read_file("guidelines.txt")
    ct = read_file("content.txt")
    
    if not gl or not ct:
        print("❌ Error: guidelines.txt or content.txt not found/empty.")
        return

    try:
        review = audit_brand_voice(gl, ct)
        save_outputs(review)
        print("✅ Brand voice consistency audit completed successfully.")
        print("📁 Outputs: brand_voice_review.json, brand_voice_review.txt")
    except Exception as e:
        print(f"❌ Audit failed: {str(e)}")

if __name__ == "__main__":
    main()
