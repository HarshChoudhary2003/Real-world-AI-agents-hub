import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import os
from agent import categorize_expense, save_outputs

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExpenseIQ AI | Smart Expense Categorization",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Persistent History ──────────────────────────────────────────────────────
HISTORY_FILE = "expense_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_history(data):
    history = load_history()
    data["processed_at"] = date.today().isoformat()
    history.insert(0, data)
    history = list(history)[:50]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ─── Premium CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0f1a2e 50%, #130a2a 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }

    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 20px;
        transition: border-color 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
    }

    /* Metric boxes */
    .metric-box {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.5);
    }
    .metric-val {
        font-size: 1.9rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-val-sm {
        font-size: 1.1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-lab {
        font-size: 0.72rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 6px;
    }

    /* Confidence Badges */
    .badge-high   { background: rgba(34,197,94,0.12); color:#4ade80; border:1px solid #22c55e; padding:4px 14px; border-radius:20px; font-size:0.8rem; font-weight:600; display:inline-block; }
    .badge-medium { background: rgba(234,179,8,0.12);  color:#facc15; border:1px solid #ca8a04; padding:4px 14px; border-radius:20px; font-size:0.8rem; font-weight:600; display:inline-block; }
    .badge-low    { background: rgba(239,68,68,0.12);  color:#f87171; border:1px solid #ef4444; padding:4px 14px; border-radius:20px; font-size:0.8rem; font-weight:600; display:inline-block; }

    /* Category pill */
    .category-pill {
        background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2));
        border: 1px solid rgba(99,102,241,0.4);
        border-radius: 24px;
        padding: 6px 18px;
        font-size: 0.9rem;
        font-weight: 600;
        color: #a5b4fc;
        display: inline-block;
    }

    /* Flag item */
    .flag-item {
        background: rgba(245,158,11,0.05);
        border-left: 4px solid #f59e0b;
        border-radius: 0 8px 8px 0;
        padding: 10px 15px;
        margin-top: 8px;
        font-size: 0.88rem;
        color: #fbbf24;
    }

    /* Justification box */
    .justification-box {
        background: rgba(99,102,241,0.05);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 12px;
        padding: 14px 18px;
        color: #cbd5e1;
        font-size: 0.92rem;
        line-height: 1.6;
        margin-top: 8px;
    }

    /* Header */
    .hero-header {
        background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(168,85,247,0.08) 100%);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 24px;
        padding: 32px 36px;
        margin-bottom: 28px;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 6px;
    }

    h1, h2, h3, h4 { color: #f8fafc !important; }
    p, li { color: #cbd5e1; }
    .stTabs [data-baseweb="tab"] { color: #94a3b8 !important; }
    .stTabs [aria-selected="true"] { color: #818cf8 !important; border-bottom-color: #818cf8 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Category Config ──────────────────────────────────────────────────────────
CATEGORY_ICONS = {
    "Software": "💻",
    "Travel": "✈️",
    "Marketing": "📣",
    "Office Supplies": "📎",
    "Professional Services": "🤝",
    "Meals & Entertainment": "🍽️",
    "Utilities": "💡",
    "Hardware": "🖥️",
    "Training & Education": "📚",
    "Other": "📦",
}

ALL_CATEGORIES = list(CATEGORY_ICONS.keys())

# ─── Main App ─────────────────────────────────────────────────────────────────
def main():
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <p class="hero-title">💳 ExpenseIQ AI</p>
        <p class="hero-sub">Neural Expense Categorization & Financial Intelligence Engine</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Engine Control")
        provider = st.selectbox(
            "Intelligence Provider",
            ["OpenAI", "Anthropic", "Gemini", "Groq"],
            key="provider_select"
        )

        models = {
            "OpenAI":    ["gpt-4.1-mini", "gpt-4o", "gpt-4o-mini"],
            "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"],
            "Gemini":    ["gemini-1.5-flash", "gemini-1.5-pro"],
            "Groq":      ["llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
        }
        selected_model = st.selectbox("Model Architecture", models[provider], key="model_select")

        api_key = st.text_input(f"{provider} API Key", type="password", key="api_key_input")
        st.caption(f"Leave empty to use `{provider.upper()}_API_KEY` from .env")

        st.divider()
        st.markdown("### 🏷️ Input Mode")
        input_mode = st.radio("Mode", ["Manual Entry", "Text File Upload", "Batch CSV"])

        raw_inputs = []

        if input_mode == "Manual Entry":
            with st.expander("📝 Transaction Details", expanded=True):
                description = st.text_input("Transaction Description", "Zoom Video Communications Monthly Subscription")
                vendor = st.text_input("Vendor", "Zoom")
                amount = st.text_input("Amount", "$149.99")
                txn_date = st.date_input("Date", value=date.today())
                cats = st.multiselect(
                    "Available Categories",
                    ALL_CATEGORIES,
                    default=["Software", "Travel", "Marketing", "Office Supplies", "Professional Services"]
                )
                if cats:
                    cats_str = "\n".join(f"- {c}" for c in cats)
                    raw_inputs = [
                        f"Transaction Description: {description}\nVendor: {vendor}\nAmount: {amount}\nDate: {txn_date}\nAvailable Categories:\n{cats_str}"
                    ]

        elif input_mode == "Text File Upload":
            uploaded = st.file_uploader("Upload input.txt", type=["txt"])
            if uploaded:
                raw_inputs = [uploaded.getvalue().decode("utf-8")]

        else:  # Batch CSV
            st.info("Upload a CSV with columns: description, vendor, amount, date")
            csv_file = st.file_uploader("Upload CSV", type=["csv"])
            cats_batch = st.multiselect(
                "Available Categories for all",
                ALL_CATEGORIES,
                default=["Software", "Travel", "Marketing", "Office Supplies", "Professional Services"]
            )
            if csv_file and cats_batch:
                import io
                df_upload = pd.read_csv(io.StringIO(csv_file.getvalue().decode("utf-8")))
                cats_str = "\n".join(f"- {c}" for c in cats_batch)
                for _, row in df_upload.iterrows():
                    raw_inputs.append(
                        f"Transaction Description: {row.get('description','')}\n"
                        f"Vendor: {row.get('vendor','')}\n"
                        f"Amount: {row.get('amount','')}\n"
                        f"Date: {row.get('date','')}\n"
                        f"Available Categories:\n{cats_str}"
                    )

        st.divider()
        process_btn = st.button("🚀 Categorize Expense", use_container_width=True)

        # Recent History
        history = load_history()
        if history:
            st.divider()
            st.markdown("### 🕒 Recent History")
            for i, entry in enumerate(list(history)[:8]):
                vendor_short = str(entry.get("vendor", "Unknown"))[:14]
                cat_short = str(entry.get("category", "?"))
                if st.button(f"💳 {vendor_short} → {cat_short}", key=f"hist_{i}"):
                    st.session_state["expense_result"] = entry
                    st.session_state["batch_results"] = [entry]

    # ── Processing ────────────────────────────────────────────────────────────
    if process_btn:
        if not raw_inputs:
            st.error("⚠️ Input buffer is empty. Please fill in the required fields.")
        else:
            with st.spinner(f"🔍 Synchronizing neural pathways with {selected_model}..."):
                try:
                    all_results = []
                    for single_input in raw_inputs:
                        result = categorize_expense(
                            single_input,
                            provider=provider,
                            model=selected_model,
                            api_key=api_key if api_key else None
                        )
                        all_results.append(result)
                        save_outputs(result)
                        save_to_history(result)

                    st.session_state["batch_results"] = all_results
                    st.session_state["expense_result"] = all_results[0]
                    st.toast(f"✅ Categorized {len(all_results)} transaction(s) successfully!", icon="💳")
                except Exception as e:
                    st.error(f"❌ Execution Fault: {str(e)}")

    # ── Batch Summary ─────────────────────────────────────────────────────────
    if "batch_results" in st.session_state and len(st.session_state["batch_results"]) > 1:
        st.markdown("### 📦 Batch Summary")
        batch_df = pd.DataFrame([
            {
                "Vendor": r.get("vendor"),
                "Amount": r.get("amount"),
                "Category": r.get("category"),
                "Confidence": r.get("confidence"),
                "Flags": len(r.get("flags", []))
            }
            for r in st.session_state["batch_results"]
        ])
        st.dataframe(batch_df, use_container_width=True)
        idx = st.selectbox(
            "View Details For",
            range(len(st.session_state["batch_results"])),
            format_func=lambda x: f"{st.session_state['batch_results'][x].get('vendor')} — {st.session_state['batch_results'][x].get('category')}"
        )
        st.session_state["expense_result"] = st.session_state["batch_results"][idx]
        st.divider()

    # ── Detail Dashboard ───────────────────────────────────────────────────────
    if "expense_result" in st.session_state:
        data = st.session_state["expense_result"]
        confidence = data.get("confidence", "Low")
        confidence_class = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}.get(confidence, "badge-low")
        cat_icon = CATEGORY_ICONS.get(data.get("category", ""), "📦")

        tabs = st.tabs(["📊 Classification Hub", "📋 Audit Details", "📈 Spend Analytics", "🧬 Raw JSON"])

        # ── Tab 1: Classification Hub ─────────────────────────────────────────
        with tabs[0]:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f'<div class="metric-box"><div class="metric-lab">Vendor</div><div class="metric-val-sm" style="margin-top:10px;">{data.get("vendor", "—")}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-box"><div class="metric-lab">Amount</div><div class="metric-val">{data.get("amount", "—")}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-box"><div class="metric-lab">Category</div><div class="metric-val-sm" style="margin-top:10px;">{cat_icon} {data.get("category", "—")}</div></div>', unsafe_allow_html=True)
            with c4:
                st.markdown(f'<div class="metric-box"><div class="metric-lab">Confidence</div><div style="margin-top:12px;"><span class="{confidence_class}">{confidence}</span></div></div>', unsafe_allow_html=True)

            st.divider()

            left, right = st.columns([3, 2])

            with left:
                st.markdown("#### 🗂️ Category Distribution (History)")
                hist_data = load_history()
                if hist_data:
                    cat_counts = {}
                    for entry in hist_data:
                        cat = entry.get("category", "Unknown")
                        cat_counts[cat] = cat_counts.get(cat, 0) + 1
                    cat_df = pd.DataFrame(list(cat_counts.items()), columns=["Category", "Count"])
                    fig_pie = px.pie(
                        cat_df, values="Count", names="Category", hole=0.45,
                        color_discrete_sequence=px.colors.qualitative.Vivid
                    )
                    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("Run more categorizations to populate historical charts.")

            with right:
                st.markdown("#### 🔍 Transaction Details")
                st.markdown(f"""
                <div class="glass-card">
                    <p style="color:#94a3b8; font-size:0.78rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px;">Description</p>
                    <p style="color:#e2e8f0; font-size:0.95rem;">{data.get('description', '—')}</p>
                    <p style="color:#94a3b8; font-size:0.78rem; letter-spacing:1px; text-transform:uppercase; margin: 14px 0 4px;">Date</p>
                    <p style="color:#e2e8f0;">{data.get('date', '—')}</p>
                    <p style="color:#94a3b8; font-size:0.78rem; letter-spacing:1px; text-transform:uppercase; margin: 14px 0 4px;">Category</p>
                    <span class="category-pill">{cat_icon} {data.get('category', '—')}</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### 🧠 Agent Justification")
                st.markdown(f'<div class="justification-box">{data.get("justification", "No justification provided.")}</div>', unsafe_allow_html=True)

        # ── Tab 2: Audit Details ──────────────────────────────────────────────
        with tabs[1]:
            st.markdown("#### 🛡️ Validation & Flags")
            flags = data.get("flags", [])
            if flags:
                for flag in flags:
                    st.markdown(f'<div class="flag-item">⚠ {flag}</div>', unsafe_allow_html=True)
            else:
                st.success("✅ No flags raised — clean categorization.")

            st.divider()
            st.markdown("#### 💾 Export Artifacts")
            ex1, ex2 = st.columns(2)
            with ex1:
                st.download_button(
                    "⬇️ Download JSON Report",
                    json.dumps(data, indent=2),
                    "expense_categorization.json",
                    "application/json",
                    use_container_width=True
                )
            with ex2:
                txt_content = (
                    f"Expense Categorization Report ({date.today()})\n"
                    + "=" * 55 + "\n\n"
                    + f"Vendor       : {data.get('vendor')}\n"
                    + f"Description  : {data.get('description')}\n"
                    + f"Amount       : {data.get('amount')}\n"
                    + f"Date         : {data.get('date')}\n"
                    + f"Category     : {data.get('category')}\n"
                    + f"Confidence   : {data.get('confidence')}\n"
                    + f"Justification: {data.get('justification')}\n"
                )
                if flags:
                    txt_content += "\nFlags:\n" + "\n".join(f"  - {fl}" for fl in flags)
                st.download_button(
                    "⬇️ Download TXT Report",
                    txt_content,
                    "expense_categorization.txt",
                    "text/plain",
                    use_container_width=True
                )

        # ── Tab 3: Spend Analytics ────────────────────────────────────────────
        with tabs[2]:
            st.markdown("#### 📊 Historical Spend Intelligence")
            hist_all = load_history()
            if hist_all:
                h_df = pd.DataFrame([
                    {
                        "Date": d.get("processed_at"),
                        "Vendor": d.get("vendor"),
                        "Category": d.get("category"),
                        "Confidence": d.get("confidence"),
                    }
                    for d in hist_all
                ])

                col_a, col_b = st.columns(2)
                with col_a:
                    cat_bar = h_df["Category"].value_counts().reset_index()
                    cat_bar.columns = ["Category", "Count"]
                    fig_bar = px.bar(
                        cat_bar, x="Category", y="Count",
                        title="Category Frequency",
                        color="Category",
                        color_discrete_sequence=px.colors.qualitative.Prism,
                        template="plotly_dark"
                    )
                    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)

                with col_b:
                    conf_bar = h_df["Confidence"].value_counts().reset_index()
                    conf_bar.columns = ["Confidence", "Count"]
                    color_map = {"High": "#4ade80", "Medium": "#facc15", "Low": "#f87171"}
                    fig_conf = px.bar(
                        conf_bar, x="Confidence", y="Count",
                        title="Confidence Level Distribution",
                        color="Confidence",
                        color_discrete_map=color_map,
                        template="plotly_dark"
                    )
                    fig_conf.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                    st.plotly_chart(fig_conf, use_container_width=True)

                st.divider()
                st.markdown("#### 📋 Full Transaction Log")
                st.dataframe(h_df, use_container_width=True)
            else:
                st.info("No historical data yet. Run more categorizations to see analytics.")

        # ── Tab 4: Raw JSON ───────────────────────────────────────────────────
        with tabs[3]:
            st.markdown("#### 🧬 Raw Neural Output")
            st.json(data)

if __name__ == "__main__":
    main()
