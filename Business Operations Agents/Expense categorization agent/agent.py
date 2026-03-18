"""
ExpenseIQ AI — Advanced Expense Categorization Agent
=====================================================
Version : 2.0.0
Author  : Real-world AI Agents Hub

Capabilities:
  - AI categorization  : OpenAI / Anthropic / Gemini / Groq
  - Tax deductibility  : Estimated % + deductible amount
  - Policy engine      : Approved / Review Required / Flagged
  - Duplicate detection: MD5-hash dedup across all runs
  - Retry logic        : Exponential backoff (3 retries)
  - Batch processing   : CSV input → JSON + CSV + TXT outputs
  - GL code suggestion : Accounting-ready general ledger codes
  - Risk scoring       : 0–10 risk score per transaction
"""

__version__ = "2.0.0"

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

# ─── Optional Provider Imports ───────────────────────────────────────────────
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
log = logging.getLogger("ExpenseIQ")

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are ExpenseIQ — an advanced enterprise Expense Categorization Agent with deep expertise in corporate finance and tax compliance.

### Your Mission:
Classify business transactions with precision, providing rich structured metadata that supports finance teams, auditors, and CFOs.

### Strict Rules:
1. ONLY assign categories explicitly listed in the user's "Available Categories" list.
2. Never invent categories. If truly uncertain, assign the closest valid category and set confidence to "Low".
3. Analyze all signals: vendor name, description, amount, date context.
4. Detect policy concerns: personal expenses billed to business, luxury items, duplicate patterns, unusually large amounts.
5. Estimate tax deductibility based on category and jurisdiction context (default: US business).
6. Return confidence: "High" (>90% certain), "Medium" (60–90%), "Low" (<60%).

### Output Schema — Return ONLY valid JSON, no markdown, no extra text:
{
  "vendor": "string",
  "description": "string",
  "amount": "string",
  "amount_numeric": number,
  "currency": "string (3-letter ISO, e.g. USD)",
  "date": "string",
  "category": "string (must be from Available Categories)",
  "subcategory": "string (more specific label, e.g. 'Video Conferencing' under 'Software')",
  "confidence": "High | Medium | Low",
  "confidence_score": number (0.0 to 1.0),
  "justification": "string (2-3 sentences explaining reasoning)",
  "tax_deductible": true | false,
  "tax_deductibility_pct": number (0 to 100, estimated % deductible),
  "tax_notes": "string (brief note on tax treatment)",
  "policy_status": "Approved | Review Required | Flagged",
  "flags": ["string"],
  "suggested_gl_code": "string (e.g. '6100-Software' — make a reasonable suggestion)",
  "recurring_likelihood": "One-time | Likely Recurring | Definitely Recurring",
  "risk_score": number (0 to 10, 0=no risk, 10=high risk)
}
"""

# ─── Known Policy Thresholds ──────────────────────────────────────────────────
POLICY_LIMITS = {
    "Meals & Entertainment": 75,
    "Travel": 500,
    "Office Supplies": 200,
    "default": 1000,
}

# ─── Duplicate Detection ──────────────────────────────────────────────────────
DEDUP_DB_FILE = "expense_dedup_db.json"

def _load_dedup_db() -> dict:
    if os.path.exists(DEDUP_DB_FILE):
        with open(DEDUP_DB_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_dedup_db(db: dict):
    with open(DEDUP_DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def _make_txn_hash(vendor: str, amount: str, txn_date: str) -> str:
    raw = f"{vendor.lower().strip()}|{amount.strip()}|{txn_date.strip()}"
    return hashlib.md5(raw.encode()).hexdigest()

def check_duplicate(vendor: str, amount: str, txn_date: str) -> Optional[str]:
    """Returns the original date if a duplicate is found, else None."""
    db = _load_dedup_db()
    key = _make_txn_hash(vendor, amount, txn_date)
    return db.get(key)

def register_transaction(vendor: str, amount: str, txn_date: str):
    db = _load_dedup_db()
    key = _make_txn_hash(vendor, amount, txn_date)
    db[key] = txn_date
    _save_dedup_db(db)

# ─── JSON Extraction ──────────────────────────────────────────────────────────
def _extract_json(text: str) -> dict:
    """Robustly extract JSON from model response.
    Handles: bare JSON, ```json fences, ```...``` fences, mixed text around {}.
    """
    text = text.strip()
    # 1. Strip markdown code fences
    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if fence_match:
        text = fence_match.group(1).strip()
    else:
        # 2. Extract the outermost {...} block if surrounded by prose
        brace_match = re.search(r"(\{[\s\S]+\})", text)
        if brace_match:
            text = brace_match.group(1).strip()
    return json.loads(text)

# ─── Retry Logic ─────────────────────────────────────────────────────────────
def _with_retry(fn, retries: int = 3, delay: float = 2.0):
    """Call fn with exponential backoff retry."""
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
            temperature=0.2,
            max_tokens=1024,
        )
        return json.loads(resp.choices[0].message.content)
    return _with_retry(call)

def _call_anthropic(prompt: str, model: str, api_key: Optional[str]) -> dict:
    assert anthropic, "anthropic package not installed."
    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    def call():
        resp = client.messages.create(
            model=model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
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
                temperature=0.2,
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
            temperature=0.2,
            max_tokens=1024,
        )
        return json.loads(resp.choices[0].message.content)
    return _with_retry(call)

# ─── Main Categorization ──────────────────────────────────────────────────────
PROVIDER_MAP = {
    "OpenAI":    (_call_openai,    "gpt-4.1-mini"),
    "Anthropic": (_call_anthropic, "claude-3-5-sonnet-20240620"),
    "Gemini":    (_call_gemini,    "gemini-1.5-flash"),
    "Groq":      (_call_groq,      "llama-3.1-70b-versatile"),
}

def categorize_expense(
    prompt_text: str,
    provider: str = "OpenAI",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Categorize a single expense transaction."""
    if provider not in PROVIDER_MAP:
        raise ValueError(f"Unsupported provider: {provider}. Choose from {list(PROVIDER_MAP)}")
    fn, default_model = PROVIDER_MAP[provider]
    result = fn(prompt_text, model or default_model, api_key)

    # ── Post-processing: policy check ───────────────────────────────────────
    result = _post_process(result, prompt_text)
    return result

def _post_process(result: dict, prompt_text: str) -> dict:
    """Enrich result with policy checks and duplicate detection."""
    # Ensure flags list exists
    if "flags" not in result:
        result["flags"] = []
    if "policy_status" not in result:
        result["policy_status"] = "Approved"

    # Amount numeric extraction if AI missed it
    if not result.get("amount_numeric"):
        raw_amt = result.get("amount", "0")
        nums = re.findall(r"[\d,]+\.?\d*", raw_amt.replace(",", ""))
        if nums:
            try:
                result["amount_numeric"] = float(nums[0])
            except ValueError:
                result["amount_numeric"] = 0.0

    amt = result.get("amount_numeric", 0) or 0
    cat = result.get("category", "")
    limit = POLICY_LIMITS.get(cat, POLICY_LIMITS["default"])

    # Policy: over-limit
    if amt > limit:
        flag = f"Amount ${amt:.2f} exceeds policy limit of ${limit:.2f} for '{cat}'"
        if flag not in result["flags"]:
            result["flags"].append(flag)
        result["policy_status"] = "Review Required"

    # Policy: high risk score
    risk = result.get("risk_score", 0) or 0
    if risk >= 7:
        result["policy_status"] = "Flagged"

    # Duplicate detection
    vendor = result.get("vendor", "")
    amount = result.get("amount", "")
    txn_date = result.get("date", "")
    dup_date = check_duplicate(vendor, amount, txn_date)
    if dup_date:
        flag = f"Potential duplicate: identical transaction from {dup_date}"
        if flag not in result["flags"]:
            result["flags"].append(flag)
        if result["policy_status"] == "Approved":
            result["policy_status"] = "Review Required"
    else:
        register_transaction(vendor, amount, txn_date)

    # Timestamp
    result["processed_at"] = datetime.now().isoformat()

    return result

# ─── Input Parsing ────────────────────────────────────────────────────────────
def read_input(path: str = "input.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_csv_to_prompts(csv_path: str, categories: list) -> list:
    """Parse a CSV file into a list of prompt strings."""
    prompts = []
    cats_str = "\n".join(f"- {c}" for c in categories)
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = (
                f"Transaction Description: {row.get('description', '')}\n"
                f"Vendor: {row.get('vendor', '')}\n"
                f"Amount: {row.get('amount', '')}\n"
                f"Date: {row.get('date', '')}\n"
                f"Available Categories:\n{cats_str}"
            )
            prompts.append(prompt)
    return prompts

# ─── Output Saving ────────────────────────────────────────────────────────────
def save_outputs(data: dict, base_path: str = ""):
    """Save expense result as JSON and TXT."""
    _save_json(data, os.path.join(base_path, "expense_categorization.json"))
    _save_txt(data, os.path.join(base_path, "expense_categorization.txt"))

def save_batch_outputs(results: list, base_path: str = ""):
    """Save a batch of expense results as multi-record JSON and CSV."""
    json_path = os.path.join(base_path, "expense_batch_results.json")
    csv_path = os.path.join(base_path, "expense_batch_results.csv")
    txt_path = os.path.join(base_path, "expense_batch_report.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # CSV
    if results:
        fieldnames = [
            "vendor", "description", "amount", "amount_numeric", "currency",
            "date", "category", "subcategory", "confidence", "confidence_score",
            "tax_deductible", "tax_deductibility_pct", "policy_status",
            "suggested_gl_code", "recurring_likelihood", "risk_score",
            "justification", "processed_at",
        ]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in results:
                writer.writerow({k: row.get(k, "") for k in fieldnames})

    # Summary TXT report
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"ExpenseIQ AI — Batch Expense Report ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total Transactions : {len(results)}\n")
        approved = sum(1 for r in results if r.get("policy_status") == "Approved")
        review   = sum(1 for r in results if r.get("policy_status") == "Review Required")
        flagged  = sum(1 for r in results if r.get("policy_status") == "Flagged")
        f.write(f"Approved           : {approved}\n")
        f.write(f"Review Required    : {review}\n")
        f.write(f"Flagged            : {flagged}\n")
        total_amt = sum(r.get("amount_numeric", 0) or 0 for r in results)
        f.write(f"Total Spend        : ${total_amt:,.2f}\n\n")

        for i, r in enumerate(results, 1):
            f.write(f"─── Transaction {i} ───────────────────────────────\n")
            f.write(f"  Vendor     : {r.get('vendor')}\n")
            f.write(f"  Amount     : {r.get('amount')}\n")
            f.write(f"  Category   : {r.get('category')} ({r.get('subcategory', '')})\n")
            f.write(f"  Confidence : {r.get('confidence')} ({r.get('confidence_score', 0):.0%})\n")
            f.write(f"  Policy     : {r.get('policy_status')}\n")
            f.write(f"  GL Code    : {r.get('suggested_gl_code', '—')}\n")
            f.write(f"  Tax Ded.   : {r.get('tax_deductibility_pct', 0)}%\n")
            flags = r.get("flags", [])
            if flags:
                f.write("  Flags:\n")
                for flag in flags:
                    f.write(f"    ⚠ {flag}\n")
            f.write("\n")

def _save_json(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _save_txt(data: dict, path: str):
    policy_icons = {"Approved": "✅", "Review Required": "🟡", "Flagged": "🚩"}
    policy_icon = policy_icons.get(data.get("policy_status", "Approved"), "❓")

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"ExpenseIQ AI — Expense Categorization Report ({date.today()})\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Vendor              : {data.get('vendor')}\n")
        f.write(f"Description         : {data.get('description')}\n")
        f.write(f"Amount              : {data.get('amount')} ({data.get('currency', 'USD')})\n")
        f.write(f"Date                : {data.get('date')}\n")
        f.write("\n── Classification ──────────────────────────────────────\n")
        f.write(f"Category            : {data.get('category')}\n")
        f.write(f"Subcategory         : {data.get('subcategory', '—')}\n")
        f.write(f"GL Code Suggestion  : {data.get('suggested_gl_code', '—')}\n")
        f.write(f"Confidence          : {data.get('confidence')} ({data.get('confidence_score', 0):.0%})\n")
        f.write(f"Recurring Likelihood: {data.get('recurring_likelihood', '—')}\n")
        f.write(f"\nJustification       : {data.get('justification')}\n")
        f.write("\n── Tax & Compliance ─────────────────────────────────────\n")
        deductible = "Yes" if data.get("tax_deductible") else "No"
        f.write(f"Tax Deductible      : {deductible} ({data.get('tax_deductibility_pct', 0)}%)\n")
        f.write(f"Tax Notes           : {data.get('tax_notes', '—')}\n")
        f.write(f"Policy Status       : {policy_icon} {data.get('policy_status', '—')}\n")
        f.write(f"Risk Score          : {data.get('risk_score', 0)}/10\n")
        flags = data.get("flags", [])
        if flags:
            f.write("\n── Flags ────────────────────────────────────────────────\n")
            for flag in flags:
                f.write(f"  ⚠ {flag}\n")
        else:
            f.write("\nFlags               : None\n")
        f.write(f"\nProcessed At        : {data.get('processed_at', '—')}\n")

# ─── CLI Entry Point ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"ExpenseIQ AI v{__version__} — Advanced Expense Categorization Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python agent.py\n"
               "  python agent.py --provider Gemini --model gemini-1.5-flash\n"
               "  python agent.py --csv sample_batch.csv --provider OpenAI"
    )
    parser.add_argument("--input",      default="input.txt", help="Input TXT file (default: input.txt)")
    parser.add_argument("--csv",        default=None,        help="Batch CSV input file")
    parser.add_argument("--provider",   default="OpenAI",    help="AI provider: OpenAI, Anthropic, Gemini, Groq")
    parser.add_argument("--model",      default=None,        help="Model name (uses provider default if omitted)")
    parser.add_argument("--api-key",    default=None,        dest="api_key", help="API key (uses .env if omitted)")
    parser.add_argument("--categories", default=None,        help="Comma-separated categories (for CSV mode)")
    parser.add_argument("--version",    action="version",    version=f"ExpenseIQ AI v{__version__}")
    args = parser.parse_args()

    log.info(f"ExpenseIQ AI starting | Provider: {args.provider}")

    if args.csv:
        # ── Batch CSV Mode ──────────────────────────────────────────────────
        if not os.path.exists(args.csv):
            log.error(f"CSV file not found: {args.csv}")
            return
        default_cats = ["Software", "Travel", "Marketing", "Office Supplies",
                        "Professional Services", "Meals & Entertainment",
                        "Utilities", "Hardware", "Training & Education",
                        "Facilities", "Legal & Compliance", "Insurance", "Other"]
        cats = [c.strip() for c in args.categories.split(",")] if args.categories else default_cats
        prompts = parse_csv_to_prompts(args.csv, cats)
        log.info(f"Processing {len(prompts)} transactions from CSV...")
        results = []
        for i, prompt in enumerate(prompts, 1):
            log.info(f"  [{i}/{len(prompts)}] Categorizing...")
            result = categorize_expense(prompt, args.provider, args.model, args.api_key)
            results.append(result)
            # Single file updated per transaction too
            save_outputs(result)
        save_batch_outputs(results)
        print(f"\n✅ Batch complete: {len(results)} transactions categorized.")
        approved = sum(1 for r in results if r.get("policy_status") == "Approved")
        flagged  = sum(1 for r in results if r.get("policy_status") == "Flagged")
        total    = sum(r.get("amount_numeric", 0) or 0 for r in results)
        print(f"   Approved  : {approved}")
        print(f"   Flagged   : {flagged}")
        print(f"   Total     : ${total:,.2f}")
        print("   Output    : expense_batch_results.json, expense_batch_results.csv, expense_batch_report.txt")
    else:
        # ── Single TXT Mode ─────────────────────────────────────────────────
        if not os.path.exists(args.input):
            log.error(f"Input file not found: {args.input}")
            return
        prompt_text = read_input(args.input)
        log.info(f"Analyzing expense | Provider: {args.provider} | Model: {args.model or 'default'}")
        result = categorize_expense(prompt_text, args.provider, args.model, args.api_key)
        save_outputs(result)

        status_icons = {"Approved": "✅", "Review Required": "🟡", "Flagged": "🚩"}
        status_icon  = status_icons.get(result.get("policy_status", ""), "❓")

        print("\n" + "=" * 55)
        print("  ExpenseIQ AI — Result")
        print("=" * 55)
        print(f"  Vendor      : {result.get('vendor')}")
        print(f"  Category    : {result.get('category')} / {result.get('subcategory', '—')}")
        print(f"  Confidence  : {result.get('confidence')} ({result.get('confidence_score', 0):.0%})")
        print(f"  GL Code     : {result.get('suggested_gl_code', '—')}")
        print(f"  Tax Ded.    : {result.get('tax_deductibility_pct', 0)}%")
        print(f"  Policy      : {status_icon} {result.get('policy_status')}")
        print(f"  Risk Score  : {result.get('risk_score', 0)}/10")
        flags = result.get("flags", [])
        if flags:
            print("  Flags:")
            for f in flags:
                print(f"    ⚠ {f}")
        print("=" * 55)
        print("  ✅ Saved: expense_categorization.json / .txt")

if __name__ == "__main__":
    main()
