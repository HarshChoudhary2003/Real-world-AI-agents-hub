"""
SupportIQ AI — Customer Support Response Agent
================================================
Version : 1.0.0
Author  : Real-world AI Agents Hub

Capabilities:
  - Multi-provider AI  : OpenAI / Anthropic / Gemini / Groq
  - Tone adaptation    : Matches brand tone + urgency level
  - Sentiment analysis : Detects customer emotion + frustration score
  - Response drafting  : Structured: greeting, acknowledgment, response, next steps, closing
  - Policy guard       : Flags responses with unsupported promises
  - Retry logic        : Exponential backoff (3 retries)
  - Batch processing   : CSV input → JSON + TXT batch reports
  - Quality scoring    : Empathy, clarity, professionalism scoring
"""

__version__ = "1.0.0"

import json
import os
import re
import time
import csv
import argparse
import logging
from datetime import date, datetime
from typing import Optional
from dotenv import load_dotenv

# ─── Optional Provider Imports ────────────────────────────────────────────────
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("SupportIQ")

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are SupportIQ — an elite Customer Support Response Agent with deep expertise in
customer satisfaction, empathetic communication, and brand-consistent messaging.

### Mission:
Draft professional, empathetic customer support responses that resolve issues,
retain customer loyalty, and reflect the company's brand tone perfectly.

### Strict Rules:
1. Match the brand tone specified in the input exactly.
2. Acknowledge the customer's emotion directly — never dismiss frustration.
3. Be clear and specific — avoid vague platitudes.
4. Do NOT promise actions beyond realistic scope (e.g., "immediate refund" unless policy allows).
5. Keep next steps concrete, numbered, and actionable.
6. Score your own response honestly.
7. Adapt urgency: High urgency = faster, more decisive language.

### Output Schema — Return ONLY valid JSON, no markdown, no extra text:
{
  "customer_name": "string (extracted from input or 'Valued Customer')",
  "issue_category": "string",
  "urgency": "High | Medium | Low",
  "detected_sentiment": "Frustrated | Angry | Confused | Neutral | Satisfied",
  "frustration_score": number (1-10, 10=most frustrated),
  "greeting": "string (personalized opening)",
  "acknowledgment": "string (empathetic acknowledgment of the issue)",
  "response": "string (main response body — clear, helpful, solution-focused)",
  "next_steps": ["string (step 1)", "string (step 2)", "string (step 3)"],
  "closing": "string (warm, professional closing)",
  "tone_used": "string (describe tone applied, e.g. 'Empathetic and decisive')",
  "response_quality": {
    "empathy_score": number (1-10),
    "clarity_score": number (1-10),
    "professionalism_score": number (1-10),
    "overall_score": number (1-10)
  },
  "policy_flags": ["string (any promises that may need manager approval)"],
  "recommended_channel": "string (Email | Live Chat | Phone Call | Escalate to Manager)",
  "escalation_required": true | false,
  "estimated_resolution_time": "string (e.g. '24-48 hours', 'Immediate')"
}
"""

# ─── Urgency & Sentiment Config ───────────────────────────────────────────────
URGENCY_ESCALATION_MAP = {
    "High":   True,
    "Medium": False,
    "Low":    False,
}

ESCALATION_KEYWORDS = [
    "lawyer", "legal", "sue", "refund immediately", "cancel account",
    "social media", "BBB", "complaint", "never again", "furious", "scam"
]

# ─── JSON Extraction ──────────────────────────────────────────────────────────
def _extract_json(text: str) -> dict:
    """Robustly extract JSON from model response."""
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if fence_match:
        text = fence_match.group(1).strip()
    else:
        brace_match = re.search(r"(\{[\s\S]+\})", text)
        if brace_match:
            text = brace_match.group(1).strip()
    return json.loads(text)

# ─── Retry Logic ─────────────────────────────────────────────────────────────
def _with_retry(fn, retries: int = 3, delay: float = 2.0):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if attempt < retries - 1:
                wait = delay * (2 ** attempt)
                log.warning(f"Attempt {attempt+1} failed: {e}. Retrying in {wait:.1f}s...")
                time.sleep(wait)
            else:
                raise

# ─── Provider Calls ───────────────────────────────────────────────────────────
def _call_openai(prompt: str, model: str, api_key: Optional[str]) -> dict:
    assert OpenAI, "openai package not installed."
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    def call():
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.35,
            max_tokens=1500,
        )
        return json.loads(resp.choices[0].message.content)
    return _with_retry(call)

def _call_anthropic(prompt: str, model: str, api_key: Optional[str]) -> dict:
    assert anthropic, "anthropic package not installed."
    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    def call():
        resp = client.messages.create(
            model=model,
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.35,
        )
        return _extract_json(resp.content[0].text)
    return _with_retry(call)

def _call_gemini(prompt: str, model: str, api_key: Optional[str]) -> dict:
    assert genai, "google-generativeai package not installed."
    genai.configure(api_key=api_key or os.getenv("GEMINI_API_KEY"))
    mi = genai.GenerativeModel(model_name=model, system_instruction=SYSTEM_PROMPT)
    def call():
        resp = mi.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.35,
            )
        )
        return json.loads(resp.text)
    return _with_retry(call)

def _call_groq(prompt: str, model: str, api_key: Optional[str]) -> dict:
    assert Groq, "groq package not installed."
    client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
    def call():
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.35,
            max_tokens=1500,
        )
        return json.loads(resp.choices[0].message.content)
    return _with_retry(call)

# ─── Provider Map ─────────────────────────────────────────────────────────────
PROVIDER_MAP = {
    "OpenAI":    (_call_openai,    "gpt-4.1-mini"),
    "Anthropic": (_call_anthropic, "claude-3-5-sonnet-20240620"),
    "Gemini":    (_call_gemini,    "gemini-2.0-flash"),
    "Groq":      (_call_groq,      "llama-3.3-70b-versatile"),
}

# ─── Main Generation ──────────────────────────────────────────────────────────
def generate_response(
    prompt_text: str,
    provider: str = "OpenAI",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Generate a customer support response for a given ticket."""
    if provider not in PROVIDER_MAP:
        raise ValueError(f"Unsupported provider: {provider}. Choose from {list(PROVIDER_MAP)}")
    fn, default_model = PROVIDER_MAP[provider]
    result = fn(prompt_text, model or default_model, api_key)
    result = _post_process(result, prompt_text)
    return result

def _post_process(result: dict, prompt_text: str) -> dict:
    """Post-process: auto-detect escalation triggers, normalize fields."""
    # Ensure lists exist
    if not isinstance(result.get("next_steps"), list):
        raw = result.get("next_steps", "")
        result["next_steps"] = [raw] if raw else ["Our team will contact you shortly."]

    if not isinstance(result.get("policy_flags"), list):
        result["policy_flags"] = []

    # Auto-escalation detection from message body
    msg_lower = prompt_text.lower()
    if any(kw in msg_lower for kw in ESCALATION_KEYWORDS):
        result["escalation_required"] = True
        flag = "Auto-flagged: Message contains escalation trigger keywords"
        if flag not in result.get("policy_flags", []):
            result.setdefault("policy_flags", []).append(flag)

    # Ensure quality scores exist and are bounded
    quality = result.get("response_quality", {})
    for key in ["empathy_score", "clarity_score", "professionalism_score", "overall_score"]:
        val = quality.get(key, 7)
        quality[key] = max(1, min(10, int(val) if val else 7))
    result["response_quality"] = quality

    # Timestamp
    result["processed_at"] = datetime.now().isoformat()
    result["agent_version"] = __version__
    return result

# ─── Input / Output ───────────────────────────────────────────────────────────
def read_input(path: str = "input.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_csv_to_prompts(csv_path: str) -> list:
    """Parse a CSV of support tickets into prompt strings."""
    prompts = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = (
                f"Customer Message:\n{row.get('message', '')}\n\n"
                f"Issue Category: {row.get('category', 'General')}\n"
                f"Urgency: {row.get('urgency', 'Medium')}\n"
                f"Brand Tone: {row.get('tone', 'Professional and empathetic')}\n"
                f"Customer Name: {row.get('customer_name', 'Valued Customer')}\n"
            )
            prompts.append(prompt)
    return prompts

def save_outputs(data: dict, base_path: str = ""):
    """Save single ticket response as JSON + TXT."""
    _save_json(data, os.path.join(base_path, "support_response.json"))
    _save_txt(data, os.path.join(base_path, "support_response.txt"))

def save_batch_outputs(results: list, base_path: str = ""):
    """Save batch results as JSON + CSV + TXT report."""
    json_path = os.path.join(base_path, "support_batch_results.json")
    csv_path  = os.path.join(base_path, "support_batch_results.csv")
    txt_path  = os.path.join(base_path, "support_batch_report.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    if results:
        fieldnames = [
            "customer_name", "issue_category", "urgency", "detected_sentiment",
            "frustration_score", "tone_used", "recommended_channel",
            "escalation_required", "estimated_resolution_time",
            "empathy_score", "clarity_score", "professionalism_score", "overall_score",
            "processed_at",
        ]
        # Flatten quality scores for CSV export
        for r in results:
            q = r.get("response_quality", {})
            r["empathy_score"]        = q.get("empathy_score", "")
            r["clarity_score"]        = q.get("clarity_score", "")
            r["professionalism_score"] = q.get("professionalism_score", "")
            r["overall_score"]        = q.get("overall_score", "")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in results:
                writer.writerow({k: row.get(k, "") for k in fieldnames})

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"SupportIQ AI — Batch Support Report ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total Tickets      : {len(results)}\n")
        escalated = sum(1 for r in results if r.get("escalation_required"))
        avg_q = sum(r.get("response_quality", {}).get("overall_score", 0) for r in results)
        avg_q = avg_q / len(results) if results else 0
        f.write(f"Escalated          : {escalated}\n")
        f.write(f"Avg Quality Score  : {avg_q:.1f}/10\n\n")
        for i, r in enumerate(results, 1):
            esc = "🚨 YES" if r.get("escalation_required") else "✅ No"
            f.write(f"─── Ticket {i} ──────────────────────────────────────────\n")
            f.write(f"  Customer  : {r.get('customer_name', '—')}\n")
            f.write(f"  Category  : {r.get('issue_category', '—')}\n")
            f.write(f"  Urgency   : {r.get('urgency', '—')}\n")
            f.write(f"  Sentiment : {r.get('detected_sentiment', '—')} (score: {r.get('frustration_score', '—')}/10)\n")
            f.write(f"  Channel   : {r.get('recommended_channel', '—')}\n")
            f.write(f"  Escalate  : {esc}\n")
            f.write(f"  Quality   : {r.get('response_quality', {}).get('overall_score', '—')}/10\n")
            f.write(f"  ETA       : {r.get('estimated_resolution_time', '—')}\n\n")

def _save_json(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _save_txt(data: dict, path: str):
    esc = "🚨 ESCALATION REQUIRED" if data.get("escalation_required") else "✅ No Escalation Needed"
    quality = data.get("response_quality", {})

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"SupportIQ AI — Customer Support Response ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"── Ticket Info ─────────────────────────────────────────\n")
        f.write(f"Customer          : {data.get('customer_name', '—')}\n")
        f.write(f"Issue Category    : {data.get('issue_category', '—')}\n")
        f.write(f"Urgency           : {data.get('urgency', '—')}\n")
        f.write(f"Sentiment         : {data.get('detected_sentiment', '—')} ({data.get('frustration_score', '—')}/10)\n")
        f.write(f"Recommended Chan. : {data.get('recommended_channel', '—')}\n")
        f.write(f"Escalation        : {esc}\n")
        f.write(f"Resolution ETA    : {data.get('estimated_resolution_time', '—')}\n\n")
        f.write(f"── Draft Response ──────────────────────────────────────\n\n")
        f.write(f"{data.get('greeting', '')}\n\n")
        f.write(f"{data.get('acknowledgment', '')}\n\n")
        f.write(f"{data.get('response', '')}\n\n")
        steps = data.get("next_steps", [])
        if steps:
            f.write("Next Steps:\n")
            for idx, step in enumerate(steps, 1):
                f.write(f"  {idx}. {step}\n")
            f.write("\n")
        f.write(f"{data.get('closing', '')}\n\n")
        f.write(f"── Quality Scores ──────────────────────────────────────\n")
        f.write(f"Empathy           : {quality.get('empathy_score', '—')}/10\n")
        f.write(f"Clarity           : {quality.get('clarity_score', '—')}/10\n")
        f.write(f"Professionalism   : {quality.get('professionalism_score', '—')}/10\n")
        f.write(f"Overall           : {quality.get('overall_score', '—')}/10\n")
        flags = data.get("policy_flags", [])
        if flags:
            f.write(f"\n── Policy Flags ────────────────────────────────────────\n")
            for flag in flags:
                f.write(f"  ⚠ {flag}\n")
        f.write(f"\nProcessed At      : {data.get('processed_at', '—')}\n")
        f.write(f"Agent Version     : SupportIQ v{data.get('agent_version', __version__)}\n")

# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"SupportIQ AI v{__version__} — Customer Support Response Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python agent.py\n"
            "  python agent.py --provider Gemini --model gemini-1.5-flash\n"
            "  python agent.py --csv tickets.csv --provider OpenAI"
        )
    )
    parser.add_argument("--input",    default="input.txt", help="Input TXT file (default: input.txt)")
    parser.add_argument("--csv",      default=None,        help="Batch CSV of tickets")
    parser.add_argument("--provider", default="OpenAI",    help="OpenAI | Anthropic | Gemini | Groq")
    parser.add_argument("--model",    default=None,        help="Model name (uses provider default if omitted)")
    parser.add_argument("--api-key",  default=None,        dest="api_key", help="API key (uses .env if omitted)")
    parser.add_argument("--version",  action="version",    version=f"SupportIQ AI v{__version__}")
    args = parser.parse_args()

    log.info(f"SupportIQ AI v{__version__} | Provider: {args.provider}")

    if args.csv:
        if not os.path.exists(args.csv):
            log.error(f"CSV not found: {args.csv}")
            return
        prompts = parse_csv_to_prompts(args.csv)
        log.info(f"Processing {len(prompts)} tickets from CSV...")
        results = []
        for i, prompt in enumerate(prompts, 1):
            log.info(f"  [{i}/{len(prompts)}] Generating response...")
            result = generate_response(prompt, args.provider, args.model, args.api_key)
            results.append(result)
            save_outputs(result)
        save_batch_outputs(results)
        escalated = sum(1 for r in results if r.get("escalation_required"))
        print(f"\n✅ Batch complete: {len(results)} tickets processed.")
        print(f"   Escalated : {escalated}")
        print(f"   Outputs   : support_batch_results.json / .csv / .txt")
    else:
        if not os.path.exists(args.input):
            log.error(f"Input file not found: {args.input}")
            return
        prompt_text = read_input(args.input)
        log.info(f"Generating response | Provider: {args.provider} | Model: {args.model or 'default'}")
        result = generate_response(prompt_text, args.provider, args.model, args.api_key)
        save_outputs(result)

        esc_icon = "🚨" if result.get("escalation_required") else "✅"
        quality  = result.get("response_quality", {})

        print("\n" + "=" * 55)
        print("  SupportIQ AI — Response Generated")
        print("=" * 55)
        print(f"  Customer   : {result.get('customer_name', '—')}")
        print(f"  Category   : {result.get('issue_category', '—')}")
        print(f"  Sentiment  : {result.get('detected_sentiment', '—')} ({result.get('frustration_score', '—')}/10)")
        print(f"  Channel    : {result.get('recommended_channel', '—')}")
        print(f"  Escalate   : {esc_icon} {result.get('escalation_required')}")
        print(f"  Quality    : {quality.get('overall_score', '—')}/10")
        print(f"  ETA        : {result.get('estimated_resolution_time', '—')}")
        policy_flags = result.get("policy_flags", [])
        if policy_flags:
            print("  Flags:")
            for fl in policy_flags:
                print(f"    ⚠ {fl}")
        print("=" * 55)
        print("  ✅ Saved: support_response.json / support_response.txt")

if __name__ == "__main__":
    main()
