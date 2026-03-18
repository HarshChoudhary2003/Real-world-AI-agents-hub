import json
import os
from litellm import completion
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """
You are an Elite Expense Categorization Agent for Enterprise Finance Teams.

Rules:
- Analyze the provided expense data and categorize each transaction intelligently.
- Assign standard accounting categories (e.g. Travel, Software, Office Supplies, Marketing, Payroll, etc.).
- Flag potential anomalies, duplicate charges, or policy violations.
- Provide spending insights and trends.
- Generate budget allocation recommendations.
- Ensure accuracy — misclassification has real financial impact.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "categorized_expenses": [
    {
      "description": "Expense description",
      "amount": 150.00,
      "category": "Assigned category",
      "subcategory": "More specific classification",
      "confidence": 0.95,
      "flag": null or "anomaly | duplicate | policy_violation",
      "flag_reason": "Why flagged, if applicable"
    }
  ],
  "summary": {
    "total_amount": 0.00,
    "category_breakdown": {"Category": 0.00},
    "flagged_count": 0,
    "top_category": "Highest spend category"
  },
  "insights": ["Array of spending insights and recommendations"],
  "policy_alerts": ["Array of potential policy concerns"]
}
"""

def read_input(path="input.txt"):
    if not os.path.exists(path):
        return (
            "Expenses to categorize:\n"
            "1. Uber ride to client meeting — $45.00\n"
            "2. AWS monthly hosting — $892.50\n"
            "3. Team lunch at Olive Garden — $127.30\n"
            "4. Adobe Creative Cloud subscription — $54.99\n"
            "5. Office printer paper (bulk) — $89.00\n"
            "6. Google Ads campaign — $2,500.00\n"
            "7. Uber ride to client meeting — $45.00\n"
            "8. Conference ticket (TechCrunch) — $1,200.00\n"
            "Company: TechStart Inc.\n"
            "Department: Engineering\n"
            "Period: March 2026"
        )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def categorize_expenses(prompt_text, model="openai/gpt-4o-mini", api_key=None, provider="openai"):
    """Categorize expenses using any LLM provider via litellm."""
    try:
        if api_key:
            env_map = {
                "openai": "OPENAI_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "google": "GEMINI_API_KEY",
                "groq": "GROQ_API_KEY",
            }
            env_var = env_map.get(provider)
            if env_var:
                os.environ[env_var] = api_key

        response = completion(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.2,
            response_format={"type": "json_object"} if provider == "openai" else None
        )

        content = response.choices[0].message.content

        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif "```" in content:
            content = content.split("```")[1].replace("json", "").strip()

        return json.loads(content)
    except Exception as e:
        print(f"Error calling {model}: {e}")
        return None

def save_outputs(data, base_path="."):
    if not data:
        print("No data to save.")
        return

    json_path = os.path.join(base_path, "expense_report.json")
    txt_path = os.path.join(base_path, "expense_report.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Expense Categorization Report ({date.today()})\n")
        f.write("=" * 50 + "\n\n")

        summary = data.get("summary", {})
        f.write(f"Total: ${summary.get('total_amount', 0):,.2f}\n")
        f.write(f"Top Category: {summary.get('top_category', 'N/A')}\n")
        f.write(f"Flagged Items: {summary.get('flagged_count', 0)}\n\n")

        f.write("Category Breakdown:\n")
        for cat, amt in summary.get("category_breakdown", {}).items():
            f.write(f"  {cat}: ${amt:,.2f}\n")

        f.write("\nCategorized Expenses:\n")
        for exp in data.get("categorized_expenses", []):
            flag_str = f" ⚠️ [{exp['flag']}]" if exp.get("flag") else ""
            f.write(f"  - {exp.get('description', '')} — ${exp.get('amount', 0):,.2f} → {exp.get('category', 'Unknown')}{flag_str}\n")

        f.write("\nInsights:\n")
        for insight in data.get("insights", []):
            f.write(f"  • {insight}\n")

        f.write("\nPolicy Alerts:\n")
        for alert in data.get("policy_alerts", []):
            f.write(f"  ⚠️ {alert}\n")

def main():
    print("🚀 Expense Categorization Agent starting...")
    prompt_text = read_input()
    result = categorize_expenses(prompt_text, model="openai/gpt-4o-mini")
    if result:
        save_outputs(result)
        summary = result.get("summary", {})
        print("✨ Categorization complete. Built `expense_report.json` and `expense_report.txt`.")
        print(f"\n💰 Total: ${summary.get('total_amount', 0):,.2f}")
        print(f"📊 Top Category: {summary.get('top_category', 'N/A')}")
        print(f"⚠️ Flagged Items: {summary.get('flagged_count', 0)}")
    else:
        print("❌ Failed to categorize expenses.")

if __name__ == "__main__":
    main()
