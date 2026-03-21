import pandas as pd
import json
import re
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables (e.g., from ../../.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

SYSTEM_PROMPT = """
You are a world-class Data Integrity & Quality Architect (Data-Guard AI v2.0).

Mission: Perform deep forensic analysis on dataset violations found by mechanical validation.

Rules for Insight:
1. **Root Cause Analysis**: Explain WHY specific data points failed (e.g., potential human entry error, system export bug).
2. **Surgical Remediation**: Suggest precise cleanup steps or code fixes for the specific failures.
3. **Strategic Blueprint**: Provide a high-level plan to prevent these specific validation breaches in the future.

Return ONLY valid JSON with this schema. No markdown wrapping:

{
  "forensic_summary": "Overall assessment of the data breaches",
  "violation_deep_dives": [
     {
       "rule": "...",
       "count": #,
       "mechanical_reason": "Technical description of the fail",
       "surgical_fix": "How to resolve this in the dataset"
     }
  ],
  "strategic_recommendations": ["List of steps to harden the data pipeline"]
}
"""

def load_data(path="input_data.csv"):
    """Loads raw data from a local CSV file."""
    if not os.path.exists(path):
        # Create default if missing
        df = pd.DataFrame([
            {"order_id": 1001, "amount": 250, "currency": "USD", "order_date": "2024-05-10"},
            {"order_id": 1002, "amount": -30, "currency": "USD", "order_date": "2024-05-12"},
            {"order_id": 1003, "amount": 120, "currency": "EUR", "order_date": "invalid_date"}
        ])
        df.to_csv(path, index=False)
        return df
    return pd.read_csv(path)

def validate_data_mechanically(df):
    """Performs strict pandas-based validation."""
    errors = []

    # 1. Amount must be positive
    invalid_amounts = df[df["amount"] <= 0].index.tolist()
    if invalid_amounts:
        errors.append({
            "rule": "amount_positive",
            "rows": [int(r) for r in invalid_amounts],
            "severity": "critical",
            "description": "Financial value cannot be zero or negative."
        })

    # 2. Currency must be 3-letter uppercase code
    # Handling potential NaNs in currency
    currency_col = df["currency"].fillna("").astype(str)
    invalid_currency = df[~currency_col.str.match(r"^[A-Z]{3}$")].index.tolist()
    if invalid_currency:
        errors.append({
            "rule": "currency_format",
            "rows": [int(r) for r in invalid_currency],
            "severity": "warning",
            "description": "Currency must adhere to ISO 4217 (3 uppercase letters)."
        })

    # 3. Valid date format
    parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
    invalid_dates = parsed_dates[parsed_dates.isnull()].index.tolist()
    if invalid_dates:
        errors.append({
            "rule": "valid_date",
            "rows": [int(r) for r in invalid_dates],
            "severity": "critical",
            "description": "Date format is unrecognizable or non-existent."
        })

    return errors

def extract_json(response_content):
    """Robustly parse JSON out of an LLM response."""
    try:
        return json.loads(response_content)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", str(response_content))
        if match:
            try: return json.loads(match.group(1).strip())
            except: pass
        match = re.search(r"\{[\s\S]*\}", str(response_content))
        if match:
            try: return json.loads(match.group(0).strip())
            except: pass
    raise ValueError("Linguistic insight extraction failed.")

def generate_validation_insights(errors, model_name="gpt-4o-mini", api_key=None):
    """Generates deep forensic insights for the identified errors using LiteLLM."""
    if not errors:
        return {"forensic_summary": "Dataset is pristine. No anomalies detected.", "violation_deep_dives": [], "strategic_recommendations": ["Maintain current ingestion standards."]}
        
    prompt = f"Detected Validation Failures:\n{json.dumps(errors, indent=2)}"
    
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
    return extract_json(response.choices[0].message.content)

def save_outputs(mechanical_errors, insights):
    """Saves the validation report as JSON and formatted TXT."""
    report = {
        "date": str(date.today()),
        "status": "fail" if mechanical_errors else "pass",
        "mechanical_audit": mechanical_errors,
        "forensic_insights": insights
    }

    with open("validation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    with open("validation_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Data-Guard AI: Dataset Integrity Report ({date.today()})\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"Global Status: {report['status'].upper()}\n")
        f.write(f"Summary: {insights.get('forensic_summary')}\n\n")

        f.write("--- 🛡️ Mechanical Violation Inventory ---\n")
        for e in mechanical_errors:
            f.write(f"RULE: {e['rule']} [{e['severity'].upper()}]\n")
            f.write(f"Description: {e['description']}\n")
            f.write(f"Affected Row Indices: {e['rows']}\n\n")

        f.write("--- 🧬 Forensic Deep Dives ---\n")
        for dive in insights.get('violation_deep_dives', []):
            f.write(f"▶ RULE: {dive.get('rule')}\n")
            f.write(f"Fix Strategy: {dive.get('surgical_fix')}\n\n")

        f.write("--- ⚡ Pipeline Hardening ---\n")
        for rec in insights.get('strategic_recommendations', []):
            f.write(f"• {rec}\n")

def main():
    print("🚀 Data-Guard AI: Auditing Dataset Integrity...")
    try:
        df = load_data()
        errors = validate_data_mechanically(df)
        insights = generate_validation_insights(errors)
        save_outputs(errors, insights)
        print("✅ Data validation audit completed successfully.")
        print("📁 Outputs: validation_report.json, validation_report.txt")
    except Exception as e:
        print(f"❌ Logic fail: {str(e)}")

if __name__ == "__main__":
    main()
