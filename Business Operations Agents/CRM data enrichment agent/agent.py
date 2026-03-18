"""
CRMPulse AI — CRM Data Enrichment Agent
=========================================
Version : 1.0.0
Author  : Real-world AI Agents Hub

Capabilities:
  - Multi-provider AI  : OpenAI / Anthropic / Gemini / Groq
  - Smart enrichment   : Industry, size, revenue, segment, funding, tech stack, LinkedIn
  - Confidence scoring : Per-field confidence (High / Medium / Low / Inferred)
  - Data preservation  : Never overwrites confirmed existing fields
  - Flag system        : Highlights uncertain, inferred, or conflicting data
  - Dedup protection   : MD5-hash-based duplicate detection across runs
  - Retry logic        : Exponential backoff (3 retries)
  - Batch processing   : CSV input → JSON + CSV + TXT enrichment reports
  - Data quality score : Overall CRM record completeness %
"""

__version__ = "1.0.0"

import json
import os
import re
import time
import csv
import hashlib
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
log = logging.getLogger("CRMPulse")

# ─── Dedup Store ──────────────────────────────────────────────────────────────
DEDUP_DB = "crm_dedup_db.json"

def _make_record_hash(name: str, email: str, company: str) -> str:
    raw = f"{name.lower().strip()}|{email.lower().strip()}|{company.lower().strip()}"
    return hashlib.md5(raw.encode()).hexdigest()

def check_duplicate(name: str, email: str, company: str) -> Optional[str]:
    if not os.path.exists(DEDUP_DB):
        return None
    with open(DEDUP_DB, "r") as f:
        db = json.load(f)
    h = _make_record_hash(name, email, company)
    return db.get(h)

def register_record(name: str, email: str, company: str):
    db = {}
    if os.path.exists(DEDUP_DB):
        with open(DEDUP_DB, "r") as f:
            db = json.load(f)
    h = _make_record_hash(name, email, company)
    db[h] = datetime.now().isoformat()
    with open(DEDUP_DB, "w") as f:
        json.dump(db, f, indent=2)

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are CRMPulse — an elite CRM Data Enrichment Agent with deep expertise in
B2B company intelligence, market segmentation, and contact profiling.

### Mission:
Enrich partial CRM records by intelligently inferring missing fields from available
context (email domain, company name, role, location). Preserve all existing data.
Be transparent about confidence and flag uncertain inferences.

### Strict Rules:
1. NEVER overwrite or contradict existing confirmed fields.
2. Infer industry from email domain and company name patterns.
3. Estimate company size from domain, name signals, and role seniority.
4. Assign account segment: Enterprise (500+), Mid-Market (51-500), SMB (1-50), Startup (<20).
5. Estimate funding stage for startups: Seed / Series A / Series B / Series C+ / Bootstrapped / Public.
6. Suggest a LinkedIn URL pattern (format: linkedin.com/in/firstname-lastname).
7. Infer likely tech stack from industry and company type.
8. Rate confidence for each enriched field: High / Medium / Low.
9. Add flags for any uncertain, inferred, or potentially conflicting data.
10. Score overall data completeness as a percentage.

### Output Schema — Return ONLY valid JSON, no markdown, no extra text:
{
  "name": "string",
  "email": "string",
  "company": "string",
  "role": "string",
  "location": "string",
  "enriched_fields": {
    "industry": "string",
    "company_size": "string (e.g. '50-200 employees')",
    "annual_revenue": "string (e.g. '$5M-$20M')",
    "account_segment": "Enterprise | Mid-Market | SMB | Startup",
    "funding_stage": "string (Seed | Series A | Series B | Series C+ | Bootstrapped | Public | Unknown)",
    "linkedin_url": "string",
    "technologies_used": ["string", "string"],
    "headquarters": "string",
    "founded_year": "string"
  },
  "confidence": {
    "industry": "High | Medium | Low",
    "company_size": "High | Medium | Low",
    "annual_revenue": "High | Medium | Low",
    "account_segment": "High | Medium | Low",
    "funding_stage": "High | Medium | Low",
    "linkedin_url": "High | Medium | Low",
    "technologies_used": "High | Medium | Low",
    "headquarters": "High | Medium | Low",
    "founded_year": "High | Medium | Low"
  },
  "data_quality_score": number (0-100, percentage of fields confidently known),
  "enrichment_summary": "string (1-2 sentence summary of what was enriched and key insights)",
  "flags": ["string"],
  "lead_score": number (1-100, overall sales lead potential based on role + company + segment),
  "lead_score_reason": "string (brief explanation of lead score)",
  "recommended_actions": ["string (action 1)", "string (action 2)", "string (action 3)"]
}
"""

# ─── CRM Field Config ─────────────────────────────────────────────────────────
ALL_ENRICHABLE_FIELDS = [
    "industry", "company_size", "annual_revenue", "account_segment",
    "funding_stage", "linkedin_url", "technologies_used",
    "headquarters", "founded_year",
]

SEGMENT_COLORS = {
    "Enterprise": "#4ade80",
    "Mid-Market": "#22d3ee",
    "SMB":        "#a78bfa",
    "Startup":    "#fb923c",
}

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
                {"role": "user",   "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.25,
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
            temperature=0.25,
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
                temperature=0.25,
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
                {"role": "user",   "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.25,
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

# ─── Main Enrichment ──────────────────────────────────────────────────────────
def enrich_crm(
    prompt_text: str,
    provider: str = "OpenAI",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Enrich a CRM record using the specified AI provider."""
    if provider not in PROVIDER_MAP:
        raise ValueError(f"Unsupported provider: {provider}. Choose from {list(PROVIDER_MAP)}")
    fn, default_model = PROVIDER_MAP[provider]
    result = fn(prompt_text, model or default_model, api_key)
    result = _post_process(result, prompt_text)
    return result

def _post_process(result: dict, prompt_text: str) -> dict:
    """Normalize, validate, and augment the raw AI output."""
    # Ensure enriched_fields exists
    result.setdefault("enriched_fields", {})
    result.setdefault("confidence", {})
    result.setdefault("flags", [])
    result.setdefault("recommended_actions", [])
    result.setdefault("technologies_used", [])

    # Ensure technologies_used is a list inside enriched_fields
    ef = result["enriched_fields"]
    if "technologies_used" in ef and not isinstance(ef["technologies_used"], list):
        ef["technologies_used"] = [ef["technologies_used"]]

    # Bound lead_score
    ls = result.get("lead_score", 50)
    result["lead_score"] = max(1, min(100, int(ls) if ls else 50))

    # Bound data_quality_score
    dq = result.get("data_quality_score", 0)
    result["data_quality_score"] = max(0, min(100, int(dq) if dq else 0))

    # Dedup check
    name    = result.get("name", "")
    email   = result.get("email", "")
    company = result.get("company", "")
    prev_ts = check_duplicate(name, email, company)
    if prev_ts:
        flag = f"Duplicate detected — this record was previously enriched on {prev_ts[:10]}"
        if flag not in result["flags"]:
            result["flags"].append(flag)
    else:
        register_record(name, email, company)

    # Timestamp
    result["processed_at"]  = datetime.now().isoformat()
    result["agent_version"] = __version__
    return result

# ─── Input / Output ───────────────────────────────────────────────────────────
def read_input(path: str = "input.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_csv_to_prompts(csv_path: str) -> list:
    """Parse a CSV of CRM records into enrichment prompt strings."""
    prompts = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            missing_raw = row.get("missing_fields", "")
            missing = [f.strip() for f in missing_raw.split(",") if f.strip()]
            prompt = (
                f"Name: {row.get('name','')}\n"
                f"Email: {row.get('email','')}\n"
                f"Company: {row.get('company','')}\n"
                f"Known Fields:\n"
                f"- Role: {row.get('role','')}\n"
                f"- Location: {row.get('location','')}\n"
                f"Missing Fields:\n"
                + "".join(f"- {f}\n" for f in missing)
            )
            prompts.append(prompt)
    return prompts

def save_outputs(data: dict, base_path: str = ""):
    """Save single record enrichment as JSON + TXT."""
    _save_json(data, os.path.join(base_path, "crm_enriched.json"))
    _save_txt(data,  os.path.join(base_path, "crm_enriched.txt"))

def save_batch_outputs(results: list, base_path: str = ""):
    """Save batch enrichment results as JSON + CSV + TXT report."""
    json_path = os.path.join(base_path, "crm_batch_results.json")
    csv_path  = os.path.join(base_path, "crm_batch_results.csv")
    txt_path  = os.path.join(base_path, "crm_batch_report.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    if results:
        fieldnames = [
            "name", "email", "company", "role",
            "industry", "company_size", "annual_revenue", "account_segment",
            "funding_stage", "lead_score", "data_quality_score", "processed_at",
        ]
        for r in results:
            ef = r.get("enriched_fields", {})
            r["industry"]          = ef.get("industry", "")
            r["company_size"]      = ef.get("company_size", "")
            r["annual_revenue"]    = ef.get("annual_revenue", "")
            r["account_segment"]   = ef.get("account_segment", "")
            r["funding_stage"]     = ef.get("funding_stage", "")

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in results:
                writer.writerow({k: row.get(k, "") for k in fieldnames})

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"CRMPulse AI — Batch Enrichment Report ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        avg_q  = sum(r.get("data_quality_score", 0) for r in results) / len(results) if results else 0
        avg_ls = sum(r.get("lead_score", 0) for r in results) / len(results) if results else 0
        dups   = sum(1 for r in results if any("Duplicate" in fl for fl in r.get("flags", [])))
        f.write(f"Total Records      : {len(results)}\n")
        f.write(f"Avg Data Quality   : {avg_q:.1f}%\n")
        f.write(f"Avg Lead Score     : {avg_ls:.1f}/100\n")
        f.write(f"Duplicates Flagged : {dups}\n\n")
        for i, r in enumerate(results, 1):
            ef = r.get("enriched_fields", {})
            f.write(f"─── Record {i} ────────────────────────────────────────────\n")
            f.write(f"  Name       : {r.get('name','—')}\n")
            f.write(f"  Email      : {r.get('email','—')}\n")
            f.write(f"  Company    : {r.get('company','—')}\n")
            f.write(f"  Industry   : {ef.get('industry','—')}\n")
            f.write(f"  Segment    : {ef.get('account_segment','—')}\n")
            f.write(f"  Lead Score : {r.get('lead_score','—')}/100\n")
            f.write(f"  Quality    : {r.get('data_quality_score','—')}%\n")
            flags = r.get("flags", [])
            if flags:
                f.write(f"  Flags      : {'; '.join(flags)}\n")
            f.write("\n")

def _save_json(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _save_txt(data: dict, path: str):
    ef   = data.get("enriched_fields", {})
    conf = data.get("confidence", {})
    techs = ef.get("technologies_used", [])
    if isinstance(techs, list):
        techs_str = ", ".join(techs)
    else:
        techs_str = str(techs)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"CRMPulse AI — Enrichment Result ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"── Contact Info ────────────────────────────────────────────\n")
        f.write(f"Name              : {data.get('name','—')}\n")
        f.write(f"Email             : {data.get('email','—')}\n")
        f.write(f"Company           : {data.get('company','—')}\n")
        f.write(f"Role              : {data.get('role','—')}\n")
        f.write(f"Location          : {data.get('location','—')}\n\n")
        f.write(f"── Enriched Fields ─────────────────────────────────────────\n")
        plain_fields = [
            ("Industry",        "industry"),
            ("Company Size",    "company_size"),
            ("Annual Revenue",  "annual_revenue"),
            ("Account Segment", "account_segment"),
            ("Funding Stage",   "funding_stage"),
            ("LinkedIn URL",    "linkedin_url"),
            ("Headquarters",    "headquarters"),
            ("Founded Year",    "founded_year"),
        ]
        for label, key in plain_fields:
            val  = ef.get(key, "—")
            cval = conf.get(key, "—")
            f.write(f"  {label:<18}: {val}  [Confidence: {cval}]\n")
        f.write(f"  {'Tech Stack':<18}: {techs_str}  [Confidence: {conf.get('technologies_used','—')}]\n\n")
        f.write(f"── Quality & Lead Score ────────────────────────────────────\n")
        f.write(f"  Data Quality    : {data.get('data_quality_score','—')}%\n")
        f.write(f"  Lead Score      : {data.get('lead_score','—')}/100\n")
        f.write(f"  Lead Reason     : {data.get('lead_score_reason','—')}\n\n")
        f.write(f"── Enrichment Summary ──────────────────────────────────────\n")
        f.write(f"  {data.get('enrichment_summary','—')}\n\n")
        actions = data.get("recommended_actions", [])
        if actions:
            f.write(f"── Recommended Actions ─────────────────────────────────────\n")
            for idx, action in enumerate(actions, 1):
                f.write(f"  {idx}. {action}\n")
            f.write("\n")
        flags = data.get("flags", [])
        if flags:
            f.write(f"── Flags ───────────────────────────────────────────────────\n")
            for flag in flags:
                f.write(f"  ⚠ {flag}\n")
            f.write("\n")
        f.write(f"Processed At      : {data.get('processed_at','—')}\n")
        f.write(f"Agent Version     : CRMPulse v{data.get('agent_version', __version__)}\n")

# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"CRMPulse AI v{__version__} — CRM Data Enrichment Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python agent.py\n"
            "  python agent.py --provider Gemini --model gemini-2.0-flash\n"
            "  python agent.py --csv sample_records.csv --provider OpenAI"
        )
    )
    parser.add_argument("--input",    default="input.txt", help="Input TXT file (default: input.txt)")
    parser.add_argument("--csv",      default=None,        help="Batch CSV of CRM records")
    parser.add_argument("--provider", default="OpenAI",    help="OpenAI | Anthropic | Gemini | Groq")
    parser.add_argument("--model",    default=None,        help="Model name (uses provider default if omitted)")
    parser.add_argument("--api-key",  default=None,        dest="api_key", help="API key (uses .env if omitted)")
    parser.add_argument("--version",  action="version",    version=f"CRMPulse AI v{__version__}")
    args = parser.parse_args()

    log.info(f"CRMPulse AI v{__version__} | Provider: {args.provider}")

    if args.csv:
        if not os.path.exists(args.csv):
            log.error(f"CSV not found: {args.csv}")
            return
        prompts = parse_csv_to_prompts(args.csv)
        log.info(f"Enriching {len(prompts)} CRM records from CSV...")
        results = []
        for i, prompt in enumerate(prompts, 1):
            log.info(f"  [{i}/{len(prompts)}] Enriching record...")
            result = enrich_crm(prompt, args.provider, args.model, args.api_key)
            results.append(result)
            save_outputs(result)
        save_batch_outputs(results)
        avg_q  = sum(r.get("data_quality_score", 0) for r in results) / len(results)
        avg_ls = sum(r.get("lead_score", 0) for r in results) / len(results)
        print(f"\n✅ Batch enrichment complete: {len(results)} records processed.")
        print(f"   Avg Data Quality : {avg_q:.1f}%")
        print(f"   Avg Lead Score   : {avg_ls:.1f}/100")
        print(f"   Outputs          : crm_batch_results.json / .csv / .txt")
    else:
        if not os.path.exists(args.input):
            log.error(f"Input file not found: {args.input}")
            return
        prompt_text = read_input(args.input)
        log.info(f"Enriching CRM record | Provider: {args.provider} | Model: {args.model or 'default'}")
        result = enrich_crm(prompt_text, args.provider, args.model, args.api_key)
        save_outputs(result)

        ef    = result.get("enriched_fields", {})
        flags = result.get("flags", [])

        print("\n" + "=" * 58)
        print("  CRMPulse AI — Record Enriched")
        print("=" * 58)
        print(f"  Name       : {result.get('name','—')}")
        print(f"  Company    : {result.get('company','—')}")
        print(f"  Industry   : {ef.get('industry','—')}")
        print(f"  Segment    : {ef.get('account_segment','—')}")
        print(f"  Funding    : {ef.get('funding_stage','—')}")
        print(f"  Lead Score : {result.get('lead_score','—')}/100")
        print(f"  Quality    : {result.get('data_quality_score','—')}%")
        if flags:
            print("  Flags:")
            for fl in flags:
                print(f"    ⚠ {fl}")
        print("=" * 58)
        print("  ✅ Saved: crm_enriched.json / crm_enriched.txt")

if __name__ == "__main__":
    main()
