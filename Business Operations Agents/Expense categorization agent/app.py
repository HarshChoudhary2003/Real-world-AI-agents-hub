"""
ExpenseIQ AI — Premium Streamlit Dashboard
"""
import streamlit as st
import json, os, io, re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
from agent import categorize_expense, save_outputs, save_batch_outputs, parse_csv_to_prompts

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExpenseIQ AI | Enterprise Expense Intelligence",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── History helpers ───────────────────────────────────────────────────────────
HISTORY_FILE = "expense_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_history(data):
    history = load_history()
    data["processed_at"] = datetime.now().isoformat()
    history.insert(0, data)
    history = list(history)[:100]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}

.stApp{background:linear-gradient(135deg,#060d1f 0%,#0d1535 45%,#110825 100%);}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0a0f20 0%,#0e1428 100%);
    border-right:1px solid rgba(99,102,241,.25);
}

/* ── hero ── */
.hero{
    background:linear-gradient(135deg,rgba(99,102,241,.12) 0%,rgba(168,85,247,.08) 60%,rgba(236,72,153,.05) 100%);
    border:1px solid rgba(99,102,241,.22);
    border-radius:24px;padding:34px 42px;margin-bottom:28px;
    position:relative;overflow:hidden;
}
.hero::before{
    content:'';position:absolute;top:-60px;right:-60px;
    width:240px;height:240px;
    background:radial-gradient(circle,rgba(168,85,247,.18) 0%,transparent 70%);
    pointer-events:none;
}
.hero-title{
    font-size:2.6rem;font-weight:900;margin:0;
    background:linear-gradient(135deg,#818cf8 0%,#c084fc 50%,#f472b6 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{color:#94a3b8;font-size:1rem;margin-top:8px;}
.hero-pills{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;}
.pill{
    background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);
    border-radius:20px;padding:4px 14px;font-size:.78rem;color:#a5b4fc;
}

/* ── glass card ── */
.glass{
    background:rgba(255,255,255,.03);backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,.07);border-radius:20px;
    padding:24px;margin-bottom:18px;transition:border-color .3s;
}
.glass:hover{border-color:rgba(99,102,241,.3);}

/* ── metric box ── */
.mbox{
    background:linear-gradient(135deg,rgba(99,102,241,.09),rgba(168,85,247,.05));
    border:1px solid rgba(99,102,241,.22);border-radius:16px;
    padding:18px;text-align:center;transition:transform .2s,border-color .2s;
}
.mbox:hover{transform:translateY(-3px);border-color:rgba(99,102,241,.45);}
.mval{
    font-size:1.9rem;font-weight:800;
    background:linear-gradient(135deg,#818cf8,#c084fc);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.mval-sm{
    font-size:1.05rem;font-weight:700;margin-top:8px;
    background:linear-gradient(135deg,#818cf8,#c084fc);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.mlab{font-size:.7rem;color:#64748b;text-transform:uppercase;letter-spacing:1.6px;margin-top:6px;}

/* ── badges ── */
.b-hi  {background:rgba(34,197,94,.12);color:#4ade80;border:1px solid #22c55e;  padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.b-med {background:rgba(234,179,8,.12); color:#facc15;border:1px solid #ca8a04; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.b-low {background:rgba(239,68,68,.12); color:#f87171;border:1px solid #ef4444; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}

.p-approved {background:rgba(34,197,94,.1); color:#4ade80;border:1px solid #22c55e; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:700;display:inline-block;}
.p-review   {background:rgba(234,179,8,.1); color:#facc15;border:1px solid #ca8a04; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:700;display:inline-block;}
.p-flagged  {background:rgba(239,68,68,.1); color:#f87171;border:1px solid #ef4444; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:700;display:inline-block;}

/* ── risk meter ── */
.risk-bar-wrap{background:rgba(255,255,255,.06);border-radius:8px;height:10px;margin-top:6px;overflow:hidden;}
.risk-bar{height:10px;border-radius:8px;transition:width .6s ease;}

/* ── flag / info items ── */
.flag-item{background:rgba(245,158,11,.05);border-left:4px solid #f59e0b;border-radius:0 8px 8px 0;padding:10px 14px;margin-top:8px;font-size:.87rem;color:#fbbf24;}
.info-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:.88rem;}
.info-label{color:#64748b;}
.info-val{color:#e2e8f0;font-weight:500;}

/* ── category pill ── */
.cat-pill{background:linear-gradient(135deg,rgba(99,102,241,.22),rgba(168,85,247,.18));border:1px solid rgba(99,102,241,.4);border-radius:24px;padding:6px 18px;font-size:.9rem;font-weight:600;color:#a5b4fc;display:inline-block;}

/* ── section header ── */
.sec-head{font-size:1rem;font-weight:700;color:#c7d2fe;letter-spacing:.5px;margin-bottom:14px;padding-bottom:6px;border-bottom:1px solid rgba(99,102,241,.2);}

/* ── tabs ── */
.stTabs [data-baseweb="tab"]{color:#64748b !important;font-weight:500;}
.stTabs [aria-selected="true"]{color:#818cf8 !important;border-bottom-color:#818cf8 !important;}

h1,h2,h3,h4{color:#f1f5f9 !important;}
p,li{color:#cbd5e1;}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
CATEGORY_ICONS = {
    "Software":"💻","Travel":"✈️","Marketing":"📣","Office Supplies":"📎",
    "Professional Services":"🤝","Meals & Entertainment":"🍽️","Utilities":"💡",
    "Hardware":"🖥️","Training & Education":"📚","Facilities":"🏢",
    "Legal & Compliance":"⚖️","Insurance":"🛡️","Other":"📦",
}
ALL_CATEGORIES = list(CATEGORY_ICONS.keys())

BUDGET_DEFAULTS = {
    "Software":500,"Travel":2000,"Marketing":1500,"Office Supplies":300,
    "Professional Services":3000,"Meals & Entertainment":400,"Utilities":200,
    "Hardware":1000,"Training & Education":800,"Other":500,
}

MODELS = {
    "OpenAI":    ["gpt-4.1-mini","gpt-4o","gpt-4o-mini","gpt-4-turbo"],
    "Anthropic": ["claude-3-5-sonnet-20240620","claude-3-opus-20240229","claude-3-haiku-20240307"],
    "Gemini":    ["gemini-1.5-flash","gemini-1.5-pro","gemini-2.0-flash"],
    "Groq":      ["llama-3.1-70b-versatile","mixtral-8x7b-32768","llama3-70b-8192"],
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def conf_badge(c):
    cls = {"High":"b-hi","Medium":"b-med","Low":"b-low"}.get(c,"b-low")
    return f'<span class="{cls}">{c}</span>'

def policy_badge(p):
    cls = {"Approved":"p-approved","Review Required":"p-review","Flagged":"p-flagged"}.get(p,"p-review")
    return f'<span class="{cls}">{p}</span>'

def risk_bar(score):
    score = int(score or 0)
    color = "#4ade80" if score<=3 else "#facc15" if score<=6 else "#f87171"
    pct = score * 10
    return f'<div class="risk-bar-wrap"><div class="risk-bar" style="width:{pct}%;background:{color};"></div></div>'

def extract_amount(s):
    nums = re.findall(r"[\d]+\.?\d*", str(s).replace(",",""))
    return float(nums[0]) if nums else 0.0

def build_history_df(hist):
    rows = []
    for d in hist:
        rows.append({
            "Date": d.get("processed_at","")[:10],
            "Vendor": d.get("vendor",""),
            "Category": d.get("category",""),
            "Subcategory": d.get("subcategory",""),
            "Amount": extract_amount(d.get("amount","0")),
            "Currency": d.get("currency","USD"),
            "Confidence": d.get("confidence",""),
            "Conf Score": float(d.get("confidence_score",0) or 0),
            "Policy": d.get("policy_status",""),
            "Tax Ded %": float(d.get("tax_deductibility_pct",0) or 0),
            "GL Code": d.get("suggested_gl_code",""),
            "Risk": int(d.get("risk_score",0) or 0),
            "Recurring": d.get("recurring_likelihood",""),
            "Flags": len(d.get("flags",[])),
        })
    return pd.DataFrame(rows)

# ── Main App ──────────────────────────────────────────────────────────────────
def main():
    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <p class="hero-title">💳 ExpenseIQ AI</p>
        <p class="hero-sub">Enterprise Neural Expense Categorization · Policy Engine · Financial Intelligence</p>
        <div class="hero-pills">
            <span class="pill">🧠 Multi-Model AI</span>
            <span class="pill">⚖️ Policy Compliance</span>
            <span class="pill">💰 Tax Deductibility</span>
            <span class="pill">🔁 Duplicate Detection</span>
            <span class="pill">📊 Spend Analytics</span>
            <span class="pill">🗂️ GL Code Suggestions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row from history ──────────────────────────────────────────────────
    hist_all = load_history()
    total_txns = len(hist_all)
    total_spend = sum(extract_amount(d.get("amount","0")) for d in hist_all)
    flagged_ct  = sum(1 for d in hist_all if d.get("policy_status")=="Flagged")
    avg_risk    = (sum(int(d.get("risk_score",0) or 0) for d in hist_all)/total_txns) if total_txns else 0
    avg_tax_ded = (sum(float(d.get("tax_deductibility_pct",0) or 0) for d in hist_all)/total_txns) if total_txns else 0

    k1,k2,k3,k4,k5 = st.columns(5)
    kpis = [
        (k1,"Total Transactions", str(total_txns), ""),
        (k2,"Total Spend", f"${total_spend:,.0f}", ""),
        (k3,"Flagged Items", str(flagged_ct), ""),
        (k4,"Avg Risk Score", f"{avg_risk:.1f}/10", ""),
        (k5,"Avg Tax Ded.", f"{avg_tax_ded:.0f}%", ""),
    ]
    for col, label, val, _ in kpis:
        with col:
            st.markdown(f'<div class="mbox"><div class="mval">{val}</div><div class="mlab">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Engine Control")
        provider = st.selectbox("AI Provider", list(MODELS.keys()), key="provider")
        model    = st.selectbox("Model", MODELS[provider], key="model")
        api_key  = st.text_input(f"{provider} API Key", type="password", key="api_key")
        st.caption(f"Or set `{provider.upper()}_API_KEY` in .env")

        st.divider()
        st.markdown("### 📥 Input Mode")
        mode = st.radio("Mode", ["✏️ Manual Entry","📄 Text File","📊 Batch CSV"], key="mode")

        raw_inputs = []

        if mode == "✏️ Manual Entry":
            desc     = st.text_area("Transaction Description", "Zoom Video Communications Monthly Subscription", height=80)
            vendor   = st.text_input("Vendor", "Zoom")
            amount   = st.text_input("Amount", "$149.99")
            txn_date = st.date_input("Date", date.today())
            cats     = st.multiselect("Available Categories", ALL_CATEGORIES,
                                      default=["Software","Travel","Marketing","Office Supplies","Professional Services"])
            if cats:
                cats_str = "\n".join(f"- {c}" for c in cats)
                raw_inputs = [f"Transaction Description: {desc}\nVendor: {vendor}\nAmount: {amount}\nDate: {txn_date}\nAvailable Categories:\n{cats_str}"]

        elif mode == "📄 Text File":
            ufile = st.file_uploader("Upload .txt", type=["txt"])
            if ufile:
                raw_inputs = [ufile.getvalue().decode("utf-8")]

        else:  # Batch CSV
            st.caption("CSV columns: description, vendor, amount, date")
            cfile = st.file_uploader("Upload CSV", type=["csv"])
            bcats = st.multiselect("Categories", ALL_CATEGORIES,
                                   default=["Software","Travel","Marketing","Office Supplies","Professional Services"])
            if cfile and bcats:
                df_up = pd.read_csv(io.StringIO(cfile.getvalue().decode("utf-8")))
                cats_str = "\n".join(f"- {c}" for c in bcats)
                for _, row in df_up.iterrows():
                    raw_inputs.append(
                        f"Transaction Description: {row.get('description','')}\n"
                        f"Vendor: {row.get('vendor','')}\nAmount: {row.get('amount','')}\n"
                        f"Date: {row.get('date','')}\nAvailable Categories:\n{cats_str}"
                    )

        st.divider()
        # Budget settings
        with st.expander("💰 Budget Thresholds"):
            budgets = {}
            for cat in ALL_CATEGORIES[:6]:
                budgets[cat] = st.number_input(f"{CATEGORY_ICONS.get(cat,'')} {cat}", value=BUDGET_DEFAULTS.get(cat,500), min_value=0, step=50, key=f"bgt_{cat}")
        st.session_state["budgets"] = budgets

        st.divider()
        process_btn = st.button("🚀 Run ExpenseIQ", use_container_width=True, type="primary")

        # History sidebar
        if hist_all:
            st.divider()
            st.markdown("### 🕒 Recent")
            for i, entry in enumerate(list(hist_all)[:6]):
                vs = str(entry.get("vendor","?"))[:13]
                cs = str(entry.get("category","?"))[:12]
                ps = entry.get("policy_status","")
                icon = "✅" if ps=="Approved" else "🟡" if ps=="Review Required" else "🚩"
                if st.button(f"{icon} {vs} → {cs}", key=f"h_{i}", use_container_width=True):
                    st.session_state["result"] = entry
                    st.session_state["batch"] = [entry]

            if st.button("🗑️ Clear History", use_container_width=True):
                clear_history()
                st.rerun()

    # ── Processing ────────────────────────────────────────────────────────────
    if process_btn:
        if not raw_inputs:
            st.error("⚠️ Input is empty — fill in the fields or upload a file.")
        else:
            prog = st.progress(0, "Processing transactions...")
            results = []
            for idx, inp in enumerate(raw_inputs):
                with st.spinner(f"🔍 [{idx+1}/{len(raw_inputs)}] Analyzing with {model}..."):
                    try:
                        res = categorize_expense(inp, provider=provider, model=model,
                                                 api_key=api_key if api_key else None)
                        results.append(res)
                        save_outputs(res)
                        save_to_history(res)
                    except Exception as e:
                        st.error(f"❌ Transaction {idx+1} failed: {e}")
                prog.progress((idx+1)/len(raw_inputs))

            prog.empty()
            if results:
                st.session_state["batch"]  = results
                st.session_state["result"] = results[0]
                if len(results) > 1:
                    save_batch_outputs(results)
                st.toast(f"✅ {len(results)} transaction(s) categorized!", icon="💳")
                st.rerun()

    # ── Batch Table ───────────────────────────────────────────────────────────
    batch = st.session_state.get("batch", [])
    if len(batch) > 1:
        st.markdown("### 📦 Batch Results")
        bdf = pd.DataFrame([{
            "Vendor": r.get("vendor"), "Amount": r.get("amount"),
            "Category": r.get("category"), "Subcategory": r.get("subcategory",""),
            "Confidence": r.get("confidence"), "Policy": r.get("policy_status"),
            "GL Code": r.get("suggested_gl_code",""), "Tax Ded %": r.get("tax_deductibility_pct",0),
            "Risk": r.get("risk_score",0), "Flags": len(r.get("flags",[]))
        } for r in batch])
        st.dataframe(bdf, use_container_width=True, hide_index=True)

        sel = st.selectbox("🔍 Inspect Transaction",range(len(batch)),
                           format_func=lambda x: f"{batch[x].get('vendor')} — {batch[x].get('category')} ({batch[x].get('policy_status')})")
        st.session_state["result"] = batch[sel]

        # Batch export
        ec1,ec2,ec3 = st.columns(3)
        with ec1:
            st.download_button("⬇️ JSON (all)", json.dumps(batch,indent=2),
                               "expense_batch.json","application/json", use_container_width=True)
        with ec2:
            st.download_button("⬇️ CSV (all)", bdf.to_csv(index=False),
                               "expense_batch.csv","text/csv", use_container_width=True)
        with ec3:
            batch_total = sum(extract_amount(r.get("amount","0")) for r in batch)
            summary_txt = f"Batch Report — {date.today()}\nTransactions: {len(batch)}\nTotal: ${batch_total:,.2f}\n"
            st.download_button("⬇️ Summary TXT", summary_txt,
                               "expense_batch_report.txt","text/plain", use_container_width=True)
        st.divider()

    # ── Single Result Dashboard ───────────────────────────────────────────────
    data = st.session_state.get("result")
    if not data:
        # Welcome state
        st.markdown("""
        <div class="glass" style="text-align:center;padding:60px 40px;">
            <div style="font-size:3rem;margin-bottom:16px;">💳</div>
            <h3 style="color:#c7d2fe !important;">Ready to Categorize</h3>
            <p style="color:#64748b;">Fill in the sidebar and click <strong style="color:#818cf8;">Run ExpenseIQ</strong> to begin.</p>
        </div>
        """, unsafe_allow_html=True)
        # Show analytics if history exists
        if hist_all:
            _render_analytics_preview(hist_all)
        return

    cat = data.get("category","")
    cat_icon = CATEGORY_ICONS.get(cat,"📦")
    confidence = data.get("confidence","Low")
    policy = data.get("policy_status","Approved")
    risk = int(data.get("risk_score", 0) or 0)
    amt_num = extract_amount(data.get("amount","0"))

    # ── Top Metrics ───────────────────────────────────────────────────────────
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    metrics = [
        (m1, "Vendor",      data.get("vendor","—"),    True),
        (m2, "Amount",      data.get("amount","—"),    False),
        (m3, "Category",    f"{cat_icon} {cat}",       True),
        (m4, "Confidence",  conf_badge(confidence),    False),
        (m5, "Policy",      policy_badge(policy),      False),
        (m6, "Risk Score",  f"{risk}/10",              False),
    ]
    for col, label, val, small in metrics:
        with col:
            cls = "mval-sm" if small else "mval"
            st.markdown(f'<div class="mbox"><div class="{cls}">{val}</div><div class="mlab">{label}</div></div>',
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tabs = st.tabs(["🎯 Classification","🛡️ Policy & Compliance","💰 Tax & GL","📊 Analytics","📋 Audit Log","🧬 Raw Output"])

    # ── Tab 1: Classification ────────────────────────────────────────────────
    with tabs[0]:
        left, right = st.columns([3, 2], gap="large")

        with left:
            st.markdown('<p class="sec-head">📋 Transaction Details</p>', unsafe_allow_html=True)
            fields = [
                ("Vendor",       data.get("vendor","—")),
                ("Description",  data.get("description","—")),
                ("Amount",       f"{data.get('amount','—')} {data.get('currency','USD')}"),
                ("Date",         data.get("date","—")),
                ("Category",     f"{cat_icon} {cat}"),
                ("Subcategory",  data.get("subcategory","—")),
                ("Recurring",    data.get("recurring_likelihood","—")),
            ]
            st.markdown('<div class="glass">' + "".join(
                f'<div class="info-row"><span class="info-label">{k}</span><span class="info-val">{v}</span></div>'
                for k,v in fields
            ) + '</div>', unsafe_allow_html=True)

            st.markdown('<p class="sec-head">🧠 Agent Justification</p>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass" style="border-left:4px solid #818cf8;">
              <p style="color:#c7d2fe;font-size:.95rem;line-height:1.7;margin:0;">{data.get("justification","—")}</p>
            </div>""", unsafe_allow_html=True)

        with right:
            st.markdown('<p class="sec-head">📊 Confidence Breakdown</p>', unsafe_allow_html=True)
            conf_score = float(data.get("confidence_score",0) or 0)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=conf_score*100,
                title={"text":"Confidence %","font":{"color":"#94a3b8","size":13}},
                number={"suffix":"%","font":{"color":"#c084fc","size":28}},
                gauge={
                    "axis":{"range":[0,100],"tickcolor":"#334155"},
                    "bar":{"color":"#818cf8"},
                    "bgcolor":"rgba(0,0,0,0)",
                    "steps":[
                        {"range":[0,60],"color":"rgba(239,68,68,.15)"},
                        {"range":[60,90],"color":"rgba(234,179,8,.15)"},
                        {"range":[90,100],"color":"rgba(34,197,94,.15)"},
                    ],
                    "threshold":{"line":{"color":"#c084fc","width":3},"thickness":.75,"value":conf_score*100},
                }
            ))
            fig_gauge.update_layout(height=220, margin=dict(t=30,b=0,l=20,r=20),
                                    paper_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown('<p class="sec-head">⚡ Risk Assessment</p>', unsafe_allow_html=True)
            risk_label = "Low" if risk<=3 else "Medium" if risk<=6 else "High"
            risk_color = "#4ade80" if risk<=3 else "#facc15" if risk<=6 else "#f87171"
            st.markdown(f"""
            <div class="glass">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="color:#94a3b8;font-size:.85rem;">Risk Score</span>
                <strong style="color:{risk_color};">{risk}/10 — {risk_label}</strong>
              </div>
              {risk_bar(risk)}
            </div>""", unsafe_allow_html=True)

            # Budget gauge if category in budgets
            budgets = st.session_state.get("budgets", BUDGET_DEFAULTS)
            if cat in budgets and budgets[cat] > 0:
                budget = budgets[cat]
                pct = min(round(amt_num / budget * 100, 1), 100)
                bar_color = "#4ade80" if pct<70 else "#facc15" if pct<90 else "#f87171"
                st.markdown(f"""
                <div class="glass">
                  <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                    <span style="color:#94a3b8;font-size:.85rem;">Budget Usage ({cat})</span>
                    <strong style="color:{bar_color};">{pct}%</strong>
                  </div>
                  <div class="risk-bar-wrap">
                    <div class="risk-bar" style="width:{pct}%;background:{bar_color};"></div>
                  </div>
                  <p style="color:#64748b;font-size:.75rem;margin-top:6px;">
                    ${amt_num:,.2f} of ${budget:,.2f} limit
                  </p>
                </div>""", unsafe_allow_html=True)

    # ── Tab 2: Policy & Compliance ────────────────────────────────────────────
    with tabs[1]:
        p1, p2 = st.columns([1,1])
        with p1:
            st.markdown('<p class="sec-head">🏛️ Policy Status</p>', unsafe_allow_html=True)
            policy_details = {
                "Status":         policy_badge(policy),
                "Risk Score":     f"{risk}/10",
                "Recurring":      data.get("recurring_likelihood","—"),
                "Confidence":     conf_badge(confidence),
            }
            st.markdown('<div class="glass">' + "".join(
                f'<div class="info-row"><span class="info-label">{k}</span><span class="info-val">{v}</span></div>'
                for k,v in policy_details.items()
            ) + '</div>', unsafe_allow_html=True)

        with p2:
            st.markdown('<p class="sec-head">🚩 Flags & Issues</p>', unsafe_allow_html=True)
            flags = data.get("flags",[])
            if flags:
                for fl in flags:
                    st.markdown(f'<div class="flag-item">⚠ {fl}</div>', unsafe_allow_html=True)
            else:
                st.success("✅ No flags raised — expense is policy-compliant.")

        st.divider()
        st.markdown('<p class="sec-head">💾 Export This Record</p>', unsafe_allow_html=True)
        ex1,ex2,ex3 = st.columns(3)
        txt_out = (
            f"ExpenseIQ — Report ({date.today()})\n{'='*55}\n"
            f"Vendor: {data.get('vendor')}\nAmount: {data.get('amount')}\n"
            f"Category: {cat}\nConfidence: {confidence}\n"
            f"Policy: {policy}\nRisk: {risk}/10\n"
            f"Justification: {data.get('justification','')}\n"
        )
        with ex1:
            st.download_button("⬇️ JSON", json.dumps(data,indent=2),
                               "expense_categorization.json","application/json", use_container_width=True)
        with ex2:
            st.download_button("⬇️ TXT", txt_out, "expense_categorization.txt",
                               "text/plain", use_container_width=True)
        with ex3:
            single_df = pd.DataFrame([data])
            st.download_button("⬇️ CSV", single_df.to_csv(index=False),
                               "expense_categorization.csv","text/csv", use_container_width=True)

    # ── Tab 3: Tax & GL ───────────────────────────────────────────────────────
    with tabs[2]:
        t1, t2 = st.columns(2)
        with t1:
            st.markdown('<p class="sec-head">💰 Tax Deductibility</p>', unsafe_allow_html=True)
            tax_ded  = data.get("tax_deductible", False)
            tax_pct  = float(data.get("tax_deductibility_pct",0) or 0)
            tax_notes= data.get("tax_notes","—")
            deductible_amt = amt_num * (tax_pct/100)

            fig_donut = go.Figure(go.Pie(
                values=[tax_pct, 100-tax_pct],
                labels=["Deductible","Non-Deductible"],
                hole=.55,
                marker_colors=["#4ade80","#1e293b"],
                textinfo="none",
            ))
            fig_donut.update_layout(
                height=200, margin=dict(t=10,b=10,l=10,r=10),
                paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                annotations=[{"text":f"{tax_pct:.0f}%","x":.5,"y":.5,"font_size":26,
                               "font_color":"#4ade80","showarrow":False}]
            )
            st.plotly_chart(fig_donut, use_container_width=True)

            tax_items = [
                ("Tax Deductible",   "✅ Yes" if tax_ded else "❌ No"),
                ("Deductible %",     f"{tax_pct:.0f}%"),
                ("Deductible Amount",f"${deductible_amt:,.2f}"),
                ("Tax Notes",        tax_notes),
            ]
            st.markdown('<div class="glass">' + "".join(
                f'<div class="info-row"><span class="info-label">{k}</span><span class="info-val">{v}</span></div>'
                for k,v in tax_items
            ) + '</div>', unsafe_allow_html=True)

        with t2:
            st.markdown('<p class="sec-head">🗂️ GL Code & Accounting</p>', unsafe_allow_html=True)
            gl = data.get("suggested_gl_code","—")
            st.markdown(f"""
            <div class="glass" style="text-align:center;padding:36px;">
              <p style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">Suggested GL Code</p>
              <p style="font-size:2rem;font-weight:800;background:linear-gradient(135deg,#818cf8,#c084fc);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;">{gl}</p>
            </div>""", unsafe_allow_html=True)

            gl_details = [
                ("Category",    cat),
                ("Subcategory", data.get("subcategory","—")),
                ("Currency",    data.get("currency","USD")),
                ("Amount",      data.get("amount","—")),
                ("Recurring",   data.get("recurring_likelihood","—")),
            ]
            st.markdown('<div class="glass">' + "".join(
                f'<div class="info-row"><span class="info-label">{k}</span><span class="info-val">{v}</span></div>'
                for k,v in gl_details
            ) + '</div>', unsafe_allow_html=True)

    # ── Tab 4: Analytics ──────────────────────────────────────────────────────
    with tabs[3]:
        _render_full_analytics(hist_all)

    # ── Tab 5: Audit Log ──────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown('<p class="sec-head">📋 Full Transaction History</p>', unsafe_allow_html=True)
        if hist_all:
            hdf = build_history_df(hist_all)
            # Filter controls
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                cat_filter = st.multiselect("Filter by Category", hdf["Category"].unique().tolist(),
                                            default=hdf["Category"].unique().tolist(), key="af_cat")
            with fc2:
                pol_filter = st.multiselect("Filter by Policy", hdf["Policy"].unique().tolist(),
                                            default=hdf["Policy"].unique().tolist(), key="af_pol")
            with fc3:
                conf_filter = st.multiselect("Filter by Confidence", ["High","Medium","Low"],
                                             default=["High","Medium","Low"], key="af_conf")

            filtered = hdf[
                hdf["Category"].isin(cat_filter) &
                hdf["Policy"].isin(pol_filter) &
                hdf["Confidence"].isin(conf_filter)
            ]
            st.dataframe(filtered, use_container_width=True, hide_index=True)

            ec1, ec2 = st.columns(2)
            with ec1:
                st.download_button("⬇️ Export History CSV", hdf.to_csv(index=False),
                                   "expense_history.csv","text/csv", use_container_width=True)
            with ec2:
                st.download_button("⬇️ Export History JSON", json.dumps(hist_all,indent=2),
                                   "expense_history.json","application/json", use_container_width=True)
        else:
            st.info("No transaction history yet.")

    # ── Tab 6: Raw JSON ───────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown('<p class="sec-head">🧬 Raw Neural Output</p>', unsafe_allow_html=True)
        st.json(data)


def _render_analytics_preview(hist):
    """Compact analytics when no result is loaded yet."""
    if not hist:
        return
    hdf = build_history_df(hist)
    st.markdown("### 📊 Spend Intelligence Overview")
    a1, a2 = st.columns(2)
    with a1:
        cat_counts = hdf["Category"].value_counts().reset_index()
        cat_counts.columns = ["Category","Count"]
        fig = px.pie(cat_counts, values="Count", names="Category", hole=.45,
                     color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white",title="Category Distribution")
        st.plotly_chart(fig, use_container_width=True)
    with a2:
        spend = hdf.groupby("Category")["Amount"].sum().reset_index()
        fig2 = px.bar(spend, x="Category", y="Amount", color="Category",
                      color_discrete_sequence=px.colors.qualitative.Prism,
                      title="Spend by Category", template="plotly_dark")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)


def _render_full_analytics(hist):
    """Full analytics tab."""
    if not hist:
        st.info("No data yet. Run some categorizations to see analytics.")
        return

    hdf = build_history_df(hist)
    st.markdown('<p class="sec-head">📊 Spend Intelligence Dashboard</p>', unsafe_allow_html=True)

    # Row 1 — Donut + Bar
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        cat_counts = hdf["Category"].value_counts().reset_index()
        cat_counts.columns = ["Category","Count"]
        fig = px.pie(cat_counts, values="Count", names="Category", hole=.45,
                     title="Category Distribution",
                     color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with r1c2:
        spend = hdf.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
        fig2 = px.bar(spend, x="Amount", y="Category", orientation="h",
                      color="Amount", color_continuous_scale="Purples",
                      title="Total Spend by Category", template="plotly_dark")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                           coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2 — Confidence + Policy + Risk
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        conf_d = hdf["Confidence"].value_counts().reset_index()
        conf_d.columns = ["Confidence","Count"]
        cmap = {"High":"#4ade80","Medium":"#facc15","Low":"#f87171"}
        fig3 = px.bar(conf_d, x="Confidence", y="Count", color="Confidence",
                      color_discrete_map=cmap, title="Confidence Distribution", template="plotly_dark")
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with r2c2:
        pol_d = hdf["Policy"].value_counts().reset_index()
        pol_d.columns = ["Policy","Count"]
        pmap = {"Approved":"#4ade80","Review Required":"#facc15","Flagged":"#f87171"}
        fig4 = px.pie(pol_d, values="Count", names="Policy",
                      color="Policy", color_discrete_map=pmap,
                      title="Policy Status Breakdown")
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="white")
        st.plotly_chart(fig4, use_container_width=True)

    with r2c3:
        fig5 = px.scatter(hdf, x="Amount", y="Risk", color="Category",
                          size="Risk", hover_data=["Vendor","Confidence","Policy"],
                          title="Risk vs Amount",
                          color_discrete_sequence=px.colors.qualitative.Vivid,
                          template="plotly_dark")
        fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig5, use_container_width=True)

    # Row 3 — Tax Deductibility treemap + timeline
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        tax_grp = hdf.groupby("Category").agg({"Amount":"sum","Tax Ded %":"mean"}).reset_index()
        tax_grp["Deductible Amount"] = tax_grp["Amount"] * tax_grp["Tax Ded %"] / 100
        fig6 = px.treemap(tax_grp, path=["Category"], values="Deductible Amount",
                          color="Tax Ded %", color_continuous_scale="Greens",
                          title="Deductible Spend Treemap")
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="white",margin=dict(t=40,b=10))
        st.plotly_chart(fig6, use_container_width=True)

    with r3c2:
        if "Date" in hdf.columns and hdf["Date"].notna().any():
            tl = hdf.groupby("Date")["Amount"].sum().reset_index().sort_values("Date")
            fig7 = px.area(tl, x="Date", y="Amount", title="Daily Spend Timeline",
                           template="plotly_dark", color_discrete_sequence=["#818cf8"])
            fig7.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
            fig7.update_traces(fillcolor="rgba(129,140,248,.15)")
            st.plotly_chart(fig7, use_container_width=True)

    # Summary stats table
    st.divider()
    st.markdown('<p class="sec-head">📈 Category Summary Statistics</p>', unsafe_allow_html=True)
    summary = hdf.groupby("Category").agg(
        Transactions=("Amount","count"),
        Total_Spend=("Amount","sum"),
        Avg_Amount=("Amount","mean"),
        Avg_Risk=("Risk","mean"),
        Avg_Tax_Ded=("Tax Ded %","mean"),
        Flags_Total=("Flags","sum"),
    ).reset_index().round(2)
    st.dataframe(summary, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
