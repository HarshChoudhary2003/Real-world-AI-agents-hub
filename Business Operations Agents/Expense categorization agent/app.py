import streamlit as st
import json
import os
import time
import re
from datetime import date
from litellm import completion
from dotenv import load_dotenv

# Page Config
st.set_page_config(
    page_title="ExpenseIQ AI",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load context
load_dotenv()

# --- Premium Custom CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        .main {
            background: linear-gradient(135deg, #052e16 0%, #064e3b 50%, #0f172a 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
            border-radius: 10px;
            border: 1px solid rgba(52, 211, 153, 0.2);
            transition: all 0.3s ease;
            font-size: 15px;
            background: rgba(15, 23, 42, 0.8);
            color: #e2e8f0;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #34d399;
            box-shadow: 0 0 0 1px #34d399, 0 0 20px rgba(52, 211, 153, 0.15);
        }
        .stButton button {
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #059669 0%, #34d399 50%, #6ee7b7 100%);
            color: #020617;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3);
        }
        .stButton button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(52, 211, 153, 0.5);
            color: #020617;
        }
        .header-title {
            background: linear-gradient(135deg, #34d399, #10b981, #6ee7b7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 3.2rem;
            letter-spacing: -1.5px;
            margin-bottom: 0px;
            line-height: 1.1;
        }
        .header-subtitle {
            color: #64748b;
            font-size: 1.15rem;
            margin-bottom: 30px;
            line-height: 1.5;
        }
        .expense-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(52, 211, 153, 0.15);
            padding: 20px 24px;
            border-radius: 12px;
            margin-bottom: 12px;
            backdrop-filter: blur(12px);
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }
        .expense-card:hover {
            border-color: rgba(52, 211, 153, 0.35);
            transform: translateX(4px);
        }
        .expense-flagged {
            border-left: 4px solid #ef4444;
        }
        .category-chip {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            background: rgba(52, 211, 153, 0.1);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.2);
        }
        .amount-display {
            font-size: 1.1rem;
            font-weight: 800;
            color: #6ee7b7;
        }
        .flag-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        .summary-stat {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(52, 211, 153, 0.12);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            backdrop-filter: blur(12px);
        }
        .stat-value {
            font-size: 2.2rem;
            font-weight: 900;
            color: #34d399;
            line-height: 1;
        }
        .stat-label {
            color: #64748b;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 8px;
        }
        .insight-card {
            background: rgba(52, 211, 153, 0.05);
            border-left: 3px solid #34d399;
            padding: 14px 20px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 10px;
            color: #e2e8f0;
            font-size: 0.92rem;
        }
        .alert-card {
            background: rgba(239, 68, 68, 0.05);
            border-left: 3px solid #ef4444;
            padding: 14px 20px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 10px;
            color: #fca5a5;
            font-size: 0.92rem;
        }
    </style>
""", unsafe_allow_html=True)


# --- AI Core Logic ---
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
      "flag": null,
      "flag_reason": null
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
Use null (not the string "null") for flag and flag_reason when no issue is detected.
"""

# Provider Data
PROVIDERS = {
    "OpenAI": {
        "models": ["openai/gpt-4o-mini", "openai/gpt-4o", "openai/gpt-3.5-turbo"],
        "env_key": "OPENAI_API_KEY"
    },
    "Anthropic": {
        "models": ["anthropic/claude-3-5-sonnet-20240620", "anthropic/claude-3-haiku-20240307", "anthropic/claude-3-opus-20240229"],
        "env_key": "ANTHROPIC_API_KEY"
    },
    "Google (Gemini)": {
        "models": ["gemini/gemini-1.5-flash", "gemini/gemini-1.5-pro", "gemini/gemini-pro"],
        "env_key": "GEMINI_API_KEY"
    },
    "Groq": {
        "models": ["groq/llama-3.1-70b-versatile", "groq/llama-3.1-8b-instant", "groq/mixtral-8x7b-32768"],
        "env_key": "GROQ_API_KEY"
    },
    "Mistral": {
        "models": ["mistral/mistral-large-latest", "mistral/mistral-small-latest"],
        "env_key": "MISTRAL_API_KEY"
    },
    "DeepSeek": {
        "models": ["deepseek/deepseek-chat", "deepseek/deepseek-coder"],
        "env_key": "DEEPSEEK_API_KEY"
    },
    "OpenRouter": {
        "models": ["openrouter/auto", "openrouter/anthropic/claude-3.5-sonnet"],
        "env_key": "OPENROUTER_API_KEY"
    }
}


def extract_json(text_response):
    try:
        return json.loads(text_response)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text_response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Failed to parse output into JSON format")


def process_expenses(expense_data, company, department, period, budget_limit,
                     provider_name, api_key, model, temp):
    prompt_text = (
        f"Expenses to categorize:\n{expense_data}\n\n"
        f"Company: {company}\n"
        f"Department: {department}\n"
        f"Period: {period}\n"
        f"Budget Limit: ${budget_limit:,.2f}/month\n"
    )

    env_key = PROVIDERS[provider_name]["env_key"]
    if api_key:
        os.environ[env_key] = api_key

    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=temp,
    )

    return extract_json(response.choices[0].message.content)


# --- UI Layout ---
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### 💸 Finance Engine")

        provider = st.selectbox("LLM Provider", list(PROVIDERS.keys()))
        env_key_name = PROVIDERS[provider]["env_key"]
        api_key = st.text_input(f"{provider} API Key", type="password", value=os.getenv(env_key_name, ""))

        if api_key:
            os.environ[env_key_name] = api_key
            st.success("🔗 Connection Active")
        else:
            st.warning("🔑 Key Required")

        st.markdown("---")
        st.markdown("### 🧠 Model Selection")
        model = st.selectbox("Intelligence Model", PROVIDERS[provider]["models"])

        st.markdown("---")
        st.markdown("### 🎛️ Precision Tuning")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05,
                                help="Lower = more accurate categorization. Keep low for financial data.")

        st.markdown("---")
        st.markdown("*ExpenseIQ AI v1.0*")

    # Main Area
    st.markdown('<div class="header-title">ExpenseIQ AI 💸</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">AI-powered expense categorization, anomaly detection, and spending intelligence for enterprise finance teams.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 📋 Expense Data")
        expense_data = st.text_area("Paste expenses (one per line)", height=200,
                                    placeholder="1. Uber ride to client meeting — $45.00\n2. AWS monthly hosting — $892.50\n3. Team lunch — $127.30\n4. Adobe CC subscription — $54.99")

    with col2:
        st.markdown("#### 🏢 Context")
        company = st.text_input("🏢 Company Name", placeholder="e.g. TechStart Inc.")
        department = st.selectbox("📂 Department",
                                  ["Engineering", "Marketing", "Sales", "Operations",
                                   "Finance", "HR", "Executive", "General"])
        period = st.text_input("📅 Period", value="March 2026")
        budget_limit = st.number_input("💰 Monthly Budget Limit ($)", min_value=0.0,
                                       value=10000.0, step=500.0)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Categorize & Analyze Expenses", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()

        if not expense_data.strip():
            st.warning("⚠️ Expense data is required.")
            st.stop()

        with st.spinner(f"💸 Categorizing expenses via {model}..."):
            try:
                start_time = time.time()
                result = process_expenses(expense_data, company, department, period,
                                          budget_limit, provider, api_key, model, temperature)
                delay = time.time() - start_time

                st.success(f"✨ Categorization Complete! Processed in {delay:.2f}s")

                summary = result.get("summary", {})
                expenses = result.get("categorized_expenses", [])
                total = summary.get("total_amount", 0)

                # --- Summary Stats ---
                st.markdown("### 📊 Expense Summary")
                stat_cols = st.columns(4)

                with stat_cols[0]:
                    st.markdown(f"""
                    <div class="summary-stat">
                        <div class="stat-value">${total:,.0f}</div>
                        <div class="stat-label">Total Spend</div>
                    </div>
                    """, unsafe_allow_html=True)

                with stat_cols[1]:
                    pct = (total / budget_limit * 100) if budget_limit > 0 else 0
                    pct_color = "#ef4444" if pct > 100 else "#eab308" if pct > 80 else "#34d399"
                    st.markdown(f"""
                    <div class="summary-stat">
                        <div class="stat-value" style="color: {pct_color};">{pct:.0f}%</div>
                        <div class="stat-label">Budget Used</div>
                    </div>
                    """, unsafe_allow_html=True)

                with stat_cols[2]:
                    st.markdown(f"""
                    <div class="summary-stat">
                        <div class="stat-value">{len(expenses)}</div>
                        <div class="stat-label">Transactions</div>
                    </div>
                    """, unsafe_allow_html=True)

                with stat_cols[3]:
                    flag_count = summary.get("flagged_count", 0)
                    flag_color = "#ef4444" if flag_count > 0 else "#34d399"
                    st.markdown(f"""
                    <div class="summary-stat">
                        <div class="stat-value" style="color: {flag_color};">{"⚠️ " + str(flag_count) if flag_count > 0 else "✅ 0"}</div>
                        <div class="stat-label">Flagged</div>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Category Breakdown Chart ---
                breakdown = summary.get("category_breakdown", {})
                if breakdown:
                    st.markdown("### 📈 Category Breakdown")
                    import pandas as pd
                    df = pd.DataFrame([
                        {"Category": k, "Amount": v}
                        for k, v in sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
                    ])
                    st.bar_chart(df.set_index("Category"))

                # --- Individual Expenses ---
                st.markdown("### 📝 Categorized Transactions")
                for exp in expenses:
                    flag = exp.get("flag")
                    flag_class = " expense-flagged" if flag else ""
                    flag_html = f'<span class="flag-badge">⚠️ {flag}</span>' if flag else ""
                    conf = exp.get("confidence", 0) * 100

                    st.markdown(f"""
                    <div class="expense-card{flag_class}">
                        <div>
                            <strong style="color: #f1f5f9;">{exp.get('description', '')}</strong><br>
                            <span class="category-chip">{exp.get('category', 'Unknown')}</span>
                            <span style="color: #64748b; font-size: 0.8rem; margin-left: 8px;">{exp.get('subcategory', '')}</span>
                            {f'<br><span style="color: #fca5a5; font-size: 0.8rem; margin-top: 4px;">{exp.get("flag_reason", "")}</span>' if flag else ""}
                        </div>
                        <div style="text-align: right;">
                            <span class="amount-display">${exp.get('amount', 0):,.2f}</span><br>
                            {flag_html}
                            <span style="color: #64748b; font-size: 0.75rem;">Confidence: {conf:.0f}%</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Insights ---
                insights = result.get("insights", [])
                if insights:
                    st.markdown("### 💡 Spending Insights")
                    for insight in insights:
                        st.markdown(f'<div class="insight-card">💡 {insight}</div>', unsafe_allow_html=True)

                # --- Policy Alerts ---
                alerts = result.get("policy_alerts", [])
                if alerts:
                    st.markdown("### 🚨 Policy Alerts")
                    for alert in alerts:
                        st.markdown(f'<div class="alert-card">⚠️ {alert}</div>', unsafe_allow_html=True)

                # --- Export ---
                st.markdown("---")
                st.markdown("### 💾 Export Report")

                txt_output = f"Expense Report — {company} ({period})\n"
                txt_output += "=" * 60 + "\n\n"
                txt_output += f"Total: ${total:,.2f}\n"
                txt_output += f"Budget: ${budget_limit:,.2f} ({pct:.0f}% used)\n"
                txt_output += f"Flagged: {flag_count}\n\n"
                for exp in expenses:
                    flag_str = f" [⚠️ {exp['flag']}]" if exp.get("flag") else ""
                    txt_output += f"  {exp.get('description', '')} — ${exp.get('amount', 0):,.2f} → {exp.get('category', '')}{flag_str}\n"
                txt_output += "\nInsights:\n"
                for i in insights:
                    txt_output += f"  • {i}\n"

                json_content = json.dumps(result, indent=2)

                exp_col1, exp_col2, _ = st.columns([1, 1, 2])
                with exp_col1:
                    st.download_button("📄 Download TXT Report", txt_output,
                                       f"expense_report_{period.replace(' ', '_')}.txt", "text/plain")
                with exp_col2:
                    st.download_button("{ } Download JSON", json_content,
                                       f"expense_report_{period.replace(' ', '_')}.json", "application/json")

            except Exception as e:
                import traceback
                st.error(f"❌ Categorization failed: {str(e)}")
                st.code(traceback.format_exc())

    st.markdown("---")
    st.caption("ExpenseIQ AI • Powered by LiteLLM Multi-Provider Relay")

if __name__ == "__main__":
    main()
