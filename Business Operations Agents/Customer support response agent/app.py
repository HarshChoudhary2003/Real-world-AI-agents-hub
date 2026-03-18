"""
SupportIQ AI v1.0.0 — Premium Streamlit Dashboard
"""
__version__ = "1.0.0"

import streamlit as st
import json, os, io, re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
from agent import generate_response, save_outputs, save_batch_outputs, parse_csv_to_prompts

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SupportIQ AI | Customer Support Intelligence",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── History ───────────────────────────────────────────────────────────────────
HISTORY_FILE = "support_history.json"

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

.stApp{background:linear-gradient(135deg,#060d1a 0%,#0c1628 45%,#0e0a20 100%);}

.stApp::before{
    content:'';position:fixed;top:0;left:0;right:0;bottom:0;
    background-image:
        linear-gradient(rgba(6,182,212,.025) 1px,transparent 1px),
        linear-gradient(90deg,rgba(6,182,212,.025) 1px,transparent 1px);
    background-size:60px 60px;pointer-events:none;z-index:0;
}

[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#080f1e 0%,#0c1525 100%);
    border-right:1px solid rgba(6,182,212,.2);
}

/* hero */
.hero{
    background:linear-gradient(135deg,rgba(6,182,212,.1) 0%,rgba(59,130,246,.07) 50%,rgba(139,92,246,.05) 100%);
    border:1px solid rgba(6,182,212,.2);border-radius:24px;
    padding:34px 42px;margin-bottom:28px;position:relative;overflow:hidden;
    animation:heroIn .6s ease-out;
}
@keyframes heroIn{from{opacity:0;transform:translateY(-12px);}to{opacity:1;transform:translateY(0);}}
.hero::before{
    content:'';position:absolute;top:-50px;right:-50px;width:220px;height:220px;
    background:radial-gradient(circle,rgba(6,182,212,.15) 0%,transparent 70%);pointer-events:none;
}
.hero-title{
    font-size:2.6rem;font-weight:900;margin:0;
    background:linear-gradient(135deg,#22d3ee 0%,#3b82f6 50%,#a78bfa 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{color:#94a3b8;font-size:1rem;margin-top:8px;}
.hero-pills{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;}
.pill{background:rgba(6,182,212,.12);border:1px solid rgba(6,182,212,.25);border-radius:20px;padding:4px 14px;font-size:.78rem;color:#67e8f9;}

/* glass */
.glass{
    background:rgba(255,255,255,.025);backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,.07);border-radius:20px;
    padding:24px;margin-bottom:18px;transition:border-color .3s;
}
.glass:hover{border-color:rgba(6,182,212,.25);}

/* metric box */
.mbox{
    background:linear-gradient(135deg,rgba(6,182,212,.08),rgba(59,130,246,.05));
    border:1px solid rgba(6,182,212,.2);border-radius:16px;
    padding:18px;text-align:center;transition:transform .2s,border-color .2s,box-shadow .2s;
    animation:cardIn .5s ease-out;
}
@keyframes cardIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}
.mbox:hover{transform:translateY(-4px);border-color:rgba(6,182,212,.45);box-shadow:0 8px 28px rgba(6,182,212,.12);}
.mval{
    font-size:1.9rem;font-weight:800;
    background:linear-gradient(135deg,#22d3ee,#3b82f6);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.mval-sm{
    font-size:1.0rem;font-weight:700;margin-top:8px;
    background:linear-gradient(135deg,#22d3ee,#3b82f6);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.mlab{font-size:.7rem;color:#64748b;text-transform:uppercase;letter-spacing:1.5px;margin-top:6px;}

/* sentiment badges */
.s-frustrated{background:rgba(239,68,68,.12);  color:#f87171;border:1px solid #ef4444; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.s-angry     {background:rgba(220,38,38,.15);   color:#fca5a5;border:1px solid #dc2626; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.s-confused  {background:rgba(234,179,8,.12);   color:#facc15;border:1px solid #ca8a04; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.s-neutral   {background:rgba(100,116,139,.12); color:#94a3b8;border:1px solid #475569; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.s-satisfied {background:rgba(34,197,94,.12);   color:#4ade80;border:1px solid #22c55e; padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}

/* urgency badges */
.u-high  {background:rgba(239,68,68,.12); color:#f87171;border:1px solid #ef4444;padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.u-medium{background:rgba(234,179,8,.12); color:#facc15;border:1px solid #ca8a04;padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.u-low   {background:rgba(34,197,94,.12); color:#4ade80;border:1px solid #22c55e;padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}

/* escalation */
.esc-yes{background:rgba(239,68,68,.1);border:1px solid #ef4444;border-radius:12px;padding:14px 18px;color:#fca5a5;border-left:4px solid #ef4444;}
.esc-no {background:rgba(34,197,94,.07);border:1px solid #22c55e;border-radius:12px;padding:14px 18px;color:#86efac;border-left:4px solid #22c55e;}

/* response sections */
.response-card{
    background:rgba(6,182,212,.04);border:1px solid rgba(6,182,212,.15);
    border-radius:14px;padding:20px 24px;margin-bottom:14px;
}
.response-label{color:#22d3ee;font-size:.72rem;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin-bottom:8px;}
.response-body{color:#e2e8f0;font-size:.95rem;line-height:1.7;}

/* step item */
.step-item{
    display:flex;gap:14px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.05);
    align-items:flex-start;
}
.step-num{
    background:linear-gradient(135deg,#22d3ee,#3b82f6);border-radius:50%;
    width:26px;height:26px;min-width:26px;display:flex;align-items:center;
    justify-content:center;font-size:.78rem;font-weight:800;color:#0c1628;
}
.step-text{color:#cbd5e1;font-size:.9rem;line-height:1.5;padding-top:4px;}

/* flag item */
.flag-item{background:rgba(245,158,11,.05);border-left:4px solid #f59e0b;border-radius:0 10px 10px 0;padding:10px 14px;margin-top:8px;font-size:.87rem;color:#fbbf24;}

/* info row */
.info-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:.88rem;}
.info-label{color:#64748b;}
.info-val{color:#e2e8f0;font-weight:500;}

/* section head */
.sec-head{font-size:1rem;font-weight:700;color:#67e8f9;letter-spacing:.5px;margin-bottom:14px;padding-bottom:6px;border-bottom:1px solid rgba(6,182,212,.2);}

/* score bar */
.score-bar-wrap{background:rgba(255,255,255,.06);border-radius:8px;height:8px;margin-top:4px;overflow:hidden;}
.score-bar{height:8px;border-radius:8px;transition:width .6s ease;}

/* tabs */
.stTabs [data-baseweb="tab"]{color:#64748b !important;font-weight:500;}
.stTabs [aria-selected="true"]{color:#22d3ee !important;border-bottom-color:#22d3ee !important;}

h1,h2,h3,h4{color:#f1f5f9 !important;}
p,li{color:#cbd5e1;}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
ISSUE_CATEGORIES = [
    "Billing", "Technical Support", "Account Management", "Shipping & Delivery",
    "Product Quality", "Refund & Returns", "Subscription", "General Inquiry",
    "Feature Request", "Compliance & Legal", "Other"
]
URGENCY_LEVELS   = ["High", "Medium", "Low"]
BRAND_TONES      = [
    "Professional and empathetic", "Friendly and casual",
    "Formal and corporate", "Concise and direct",
    "Warm and supportive", "Technical and detailed"
]
MODELS = {
    "OpenAI":    ["gpt-4.1-mini", "gpt-4o", "gpt-4o-mini"],
    "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
    "Gemini":    ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
    "Groq":      ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
}
SENTIMENT_ICONS = {
    "Frustrated": "😤", "Angry": "😠", "Confused": "😕",
    "Neutral": "😐", "Satisfied": "😊"
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def sentiment_badge(s):
    cls = {
        "Frustrated": "s-frustrated", "Angry": "s-angry",
        "Confused": "s-confused", "Neutral": "s-neutral", "Satisfied": "s-satisfied"
    }.get(s, "s-neutral")
    icon = SENTIMENT_ICONS.get(s, "")
    return f'<span class="{cls}">{icon} {s}</span>'

def urgency_badge(u):
    cls = {"High": "u-high", "Medium": "u-medium", "Low": "u-low"}.get(u, "u-medium")
    return f'<span class="{cls}">{u}</span>'

def score_bar(val, color="#22d3ee"):
    pct = int((val / 10) * 100)
    return f'<div class="score-bar-wrap"><div class="score-bar" style="width:{pct}%;background:{color};"></div></div>'

def extract_frustration(val):
    try: return int(val or 0)
    except: return 0

def build_history_df(hist):
    rows = []
    for d in hist:
        quality = d.get("response_quality", {})
        rows.append({
            "Date":       d.get("processed_at", "")[:10],
            "Customer":   d.get("customer_name", ""),
            "Category":   d.get("issue_category", ""),
            "Urgency":    d.get("urgency", ""),
            "Sentiment":  d.get("detected_sentiment", ""),
            "Frustration":extract_frustration(d.get("frustration_score", 0)),
            "Channel":    d.get("recommended_channel", ""),
            "Escalated":  bool(d.get("escalation_required", False)),
            "Quality":    int(quality.get("overall_score", 0) or 0),
            "Empathy":    int(quality.get("empathy_score", 0) or 0),
            "ETA":        d.get("estimated_resolution_time", ""),
        })
    return pd.DataFrame(rows)

# ── Main App ──────────────────────────────────────────────────────────────────
def main():
    # Hero
    st.markdown(f"""
    <div class="hero">
        <p class="hero-title">🎧 SupportIQ AI</p>
        <p class="hero-sub">Enterprise Customer Support Intelligence · Empathy Engine · Policy Guard · Quality Scoring</p>
        <div class="hero-pills">
            <span class="pill">🧠 Multi-Model AI</span>
            <span class="pill">😤 Sentiment Detection</span>
            <span class="pill">🚨 Auto-Escalation</span>
            <span class="pill">⭐ Quality Scoring</span>
            <span class="pill">📋 Policy Guard</span>
            <span class="pill">📊 Analytics Dashboard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    hist_all    = load_history()
    total_txns  = len(hist_all)
    escalated   = sum(1 for d in hist_all if d.get("escalation_required"))
    avg_quality = (sum(d.get("response_quality", {}).get("overall_score", 0) or 0 for d in hist_all) / total_txns) if total_txns else 0
    avg_frust   = (sum(extract_frustration(d.get("frustration_score", 0)) for d in hist_all) / total_txns) if total_txns else 0
    flagged_ct  = sum(1 for d in hist_all if d.get("policy_flags"))

    k1,k2,k3,k4,k5 = st.columns(5)
    for col, label, val in [
        (k1, "Tickets Processed", str(total_txns)),
        (k2, "Escalated",         str(escalated)),
        (k3, "Avg Quality",       f"{avg_quality:.1f}/10"),
        (k4, "Avg Frustration",   f"{avg_frust:.1f}/10"),
        (k5, "Policy Flags",      str(flagged_ct)),
    ]:
        with col:
            st.markdown(f'<div class="mbox"><div class="mval">{val}</div><div class="mlab">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Engine Control")
        st.markdown(f"""
        <div style="background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.25);
             border-radius:8px;padding:6px 12px;margin-bottom:12px;text-align:center;">
            <span style="color:#67e8f9;font-size:.75rem;font-weight:600;">🎧 SupportIQ AI v{__version__}</span>
        </div>""", unsafe_allow_html=True)

        provider = st.selectbox("AI Provider", list(MODELS.keys()), key="provider")
        model    = st.selectbox("Model", MODELS[provider], key="model")
        api_key  = st.text_input(f"{provider} API Key", type="password", key="api_key")
        st.caption(f"Or set `{provider.upper()}_API_KEY` in .env")

        st.divider()
        st.markdown("### 🎫 Input Mode")
        mode = st.radio("Mode", ["✏️ Manual Ticket", "📄 Text File", "📊 Batch CSV"], key="mode")

        raw_inputs = []

        if mode == "✏️ Manual Ticket":
            customer_name = st.text_input("Customer Name", "James Carter")
            message = st.text_area("Customer Message", 
                "I was charged twice for my subscription this month and I'm really frustrated. "
                "I've been a loyal customer for 3 years and expect this to be resolved immediately.",
                height=120)
            issue_cat = st.selectbox("Issue Category", ISSUE_CATEGORIES, index=0)
            urgency   = st.selectbox("Urgency", URGENCY_LEVELS, index=0)
            tone      = st.selectbox("Brand Tone", BRAND_TONES, index=0)

            raw_inputs = [
                f"Customer Message:\n{message}\n\n"
                f"Issue Category: {issue_cat}\n"
                f"Urgency: {urgency}\n"
                f"Brand Tone: {tone}\n"
                f"Customer Name: {customer_name}\n"
            ]

        elif mode == "📄 Text File":
            ufile = st.file_uploader("Upload input.txt", type=["txt"])
            if ufile:
                raw_inputs = [ufile.getvalue().decode("utf-8")]

        else:  # Batch CSV
            st.caption("CSV columns: message, customer_name, category, urgency, tone")
            cfile = st.file_uploader("Upload CSV", type=["csv"])
            if cfile:
                df_up = pd.read_csv(io.StringIO(cfile.getvalue().decode("utf-8")))
                for _, row in df_up.iterrows():
                    raw_inputs.append(
                        f"Customer Message:\n{row.get('message','')}\n\n"
                        f"Issue Category: {row.get('category','General')}\n"
                        f"Urgency: {row.get('urgency','Medium')}\n"
                        f"Brand Tone: {row.get('tone','Professional and empathetic')}\n"
                        f"Customer Name: {row.get('customer_name','Valued Customer')}\n"
                    )

        # Sample CSV
        sample_csv = (
            "message,customer_name,category,urgency,tone\n"
            "\"I was charged twice this month!\",James Carter,Billing,High,Professional and empathetic\n"
            "\"My order hasn't arrived after 2 weeks.\",Sarah Kim,Shipping & Delivery,High,Friendly and casual\n"
            "\"How do I reset my password?\",Mike T.,Account Management,Low,Concise and direct\n"
        )
        st.download_button("⬇️ Sample Batch CSV", sample_csv, "sample_tickets.csv", "text/csv", use_container_width=True)

        st.divider()
        process_btn = st.button("🚀 Generate Response", use_container_width=True, type="primary")

        # History sidebar
        if hist_all:
            st.divider()
            st.markdown("### 🕒 Recent Tickets")
            for i, entry in enumerate(list(hist_all)[:6]):
                cs  = str(entry.get("customer_name", "?"))[:12]
                cat = str(entry.get("issue_category", "?"))[:12]
                esc_icon = "🚨" if entry.get("escalation_required") else "✅"
                if st.button(f"{esc_icon} {cs} — {cat}", key=f"h_{i}", use_container_width=True):
                    st.session_state["result"] = entry
                    st.session_state["batch"]  = [entry]
            if st.button("🗑️ Clear History", use_container_width=True):
                clear_history()
                st.rerun()

    # ── Processing ────────────────────────────────────────────────────────────
    if process_btn:
        if not raw_inputs:
            st.error("⚠️ Input is empty.")
        else:
            prog = st.progress(0, "Processing tickets...")
            results = []
            for idx, inp in enumerate(raw_inputs):
                with st.spinner(f"🔍 [{idx+1}/{len(raw_inputs)}] Generating with {model}..."):
                    try:
                        res = generate_response(inp, provider=provider, model=model,
                                                api_key=api_key if api_key else None)
                        results.append(res)
                        save_outputs(res)
                        save_to_history(res)
                    except Exception as e:
                        st.error(f"❌ Ticket {idx+1} failed: {e}")
                prog.progress((idx+1)/len(raw_inputs))
            prog.empty()
            if results:
                st.session_state["batch"]  = results
                st.session_state["result"] = results[0]
                if len(results) > 1:
                    save_batch_outputs(results)
                st.toast(f"✅ {len(results)} response(s) generated!", icon="🎧")
                st.rerun()

    # ── Batch Table ───────────────────────────────────────────────────────────
    batch = st.session_state.get("batch", [])
    if len(batch) > 1:
        st.markdown("### 📦 Batch Results")
        bdf = pd.DataFrame([{
            "Customer":  r.get("customer_name"),
            "Category":  r.get("issue_category"),
            "Urgency":   r.get("urgency"),
            "Sentiment": r.get("detected_sentiment"),
            "Channel":   r.get("recommended_channel"),
            "Escalate":  "🚨 Yes" if r.get("escalation_required") else "✅ No",
            "Quality":   r.get("response_quality", {}).get("overall_score", "—"),
            "ETA":       r.get("estimated_resolution_time"),
        } for r in batch])
        st.dataframe(bdf, use_container_width=True, hide_index=True)

        sel = st.selectbox("🔍 Inspect Ticket", range(len(batch)),
                           format_func=lambda x: f"{batch[x].get('customer_name')} — {batch[x].get('issue_category')} ({batch[x].get('urgency')})")
        st.session_state["result"] = batch[sel]

        bc1, bc2, bc3 = st.columns(3)
        with bc1:
            st.download_button("⬇️ JSON (all)", json.dumps(batch, indent=2),
                               "support_batch.json", "application/json", use_container_width=True)
        with bc2:
            st.download_button("⬇️ CSV (all)", bdf.to_csv(index=False),
                               "support_batch.csv", "text/csv", use_container_width=True)
        with bc3:
            esc_ct = sum(1 for r in batch if r.get("escalation_required"))
            summary = f"SupportIQ Batch — {date.today()}\nTickets: {len(batch)}\nEscalated: {esc_ct}\n"
            st.download_button("⬇️ Report TXT", summary, "support_batch_report.txt", "text/plain", use_container_width=True)
        st.divider()

    # ── Detail Dashboard ──────────────────────────────────────────────────────
    data = st.session_state.get("result")
    if not data:
        st.markdown("""
        <div class="glass" style="text-align:center;padding:60px 40px;">
            <div style="font-size:3rem;margin-bottom:16px;">🎧</div>
            <h3 style="color:#67e8f9 !important;">Ready to Generate</h3>
            <p style="color:#64748b;">Fill in the sidebar and click <strong style="color:#22d3ee;">Generate Response</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
        if hist_all:
            _render_analytics_preview(hist_all)
        return

    sentiment   = data.get("detected_sentiment", "Neutral")
    urgency     = data.get("urgency", "Medium")
    quality     = data.get("response_quality", {})
    escalate    = data.get("escalation_required", False)
    frustration = extract_frustration(data.get("frustration_score", 0))

    # Top metrics
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    for col, label, val, small in [
        (m1, "Customer",    data.get("customer_name","—"),   True),
        (m2, "Category",    data.get("issue_category","—"),  True),
        (m3, "Sentiment",   sentiment_badge(sentiment),      False),
        (m4, "Urgency",     urgency_badge(urgency),          False),
        (m5, "Quality",     f"{quality.get('overall_score','—')}/10", False),
        (m6, "Frustration", f"{frustration}/10",             False),
    ]:
        with col:
            cls = "mval-sm" if small else "mval"
            st.markdown(f'<div class="mbox"><div class="{cls}">{val}</div><div class="mlab">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["📝 Draft Response", "🚨 Triage & Escalation", "⭐ Quality Scoring", "📊 Analytics", "📋 Audit Log", "🧬 Raw JSON"])

    # ── Tab 1: Draft Response ─────────────────────────────────────────────────
    with tabs[0]:
        left, right = st.columns([3, 2], gap="large")

        with left:
            st.markdown('<p class="sec-head">📧 Generated Response Draft</p>', unsafe_allow_html=True)

            for label, key in [
                ("👋 Greeting",       "greeting"),
                ("💬 Acknowledgment", "acknowledgment"),
                ("📋 Response",       "response"),
                ("✅ Closing",         "closing"),
            ]:
                val = data.get(key, "—")
                st.markdown(f"""
                <div class="response-card">
                  <div class="response-label">{label}</div>
                  <div class="response-body">{val}</div>
                </div>""", unsafe_allow_html=True)

            # Next steps
            steps = data.get("next_steps", [])
            if steps:
                st.markdown('<p class="sec-head">🗺️ Next Steps</p>', unsafe_allow_html=True)
                steps_html = "".join(
                    f'<div class="step-item"><div class="step-num">{i}</div><div class="step-text">{s}</div></div>'
                    for i, s in enumerate(steps, 1)
                )
                st.markdown(f'<div class="glass">{steps_html}</div>', unsafe_allow_html=True)

            # Copy-ready full response
            st.divider()
            st.markdown('<p class="sec-head">📋 Copy-Ready Response</p>', unsafe_allow_html=True)
            full_response = (
                f"{data.get('greeting','')}\n\n"
                f"{data.get('acknowledgment','')}\n\n"
                f"{data.get('response','')}\n\n"
                + ("Next Steps:\n" + "\n".join(f"{i}. {s}" for i,s in enumerate(steps,1)) + "\n\n" if steps else "")
                + f"{data.get('closing','')}"
            )
            st.text_area("Full Draft (copy from here)", full_response, height=260, key="full_response_text")

        with right:
            st.markdown('<p class="sec-head">📌 Ticket Summary</p>', unsafe_allow_html=True)
            ticket_rows = [
                ("Customer",     data.get("customer_name","—")),
                ("Category",     data.get("issue_category","—")),
                ("Urgency",      urgency_badge(urgency)),
                ("Sentiment",    sentiment_badge(sentiment)),
                ("Frustration",  f"{frustration}/10"),
                ("Channel",      f"📡 {data.get('recommended_channel','—')}"),
                ("ETA",          data.get("estimated_resolution_time","—")),
                ("Tone Used",    data.get("tone_used","—")),
            ]
            st.markdown('<div class="glass">' + "".join(
                f'<div class="info-row"><span class="info-label">{k}</span><span class="info-val">{v}</span></div>'
                for k,v in ticket_rows
            ) + '</div>', unsafe_allow_html=True)

            # Frustration donut
            st.markdown('<p class="sec-head">😤 Frustration Level</p>', unsafe_allow_html=True)
            fig_fr = go.Figure(go.Pie(
                values=[frustration, 10-frustration],
                labels=["Frustration","Calm"],
                hole=.6, textinfo="none",
                marker_colors=[
                    "#ef4444" if frustration>=7 else "#facc15" if frustration>=4 else "#4ade80",
                    "#1e293b"
                ],
            ))
            fig_fr.update_layout(
                height=180, margin=dict(t=10,b=10,l=10,r=10),
                paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                annotations=[{"text":f"{frustration}/10","x":.5,"y":.5,"font_size":24,
                               "font_color":"#f87171","showarrow":False}]
            )
            st.plotly_chart(fig_fr, use_container_width=True)

            # Exports
            st.markdown('<p class="sec-head">💾 Export</p>', unsafe_allow_html=True)
            e1, e2 = st.columns(2)
            with e1:
                st.download_button("⬇️ JSON", json.dumps(data, indent=2),
                                   "support_response.json", "application/json", use_container_width=True)
            with e2:
                txt = (
                    f"SupportIQ — Response ({date.today()})\n{'='*50}\n"
                    f"Customer: {data.get('customer_name')}\n"
                    f"Category: {data.get('issue_category')}\n\n"
                    f"{full_response}"
                )
                st.download_button("⬇️ TXT", txt, "support_response.txt", "text/plain", use_container_width=True)

    # ── Tab 2: Triage & Escalation ────────────────────────────────────────────
    with tabs[1]:
        t1, t2 = st.columns(2)
        with t1:
            st.markdown('<p class="sec-head">🚨 Escalation Status</p>', unsafe_allow_html=True)
            if escalate:
                st.markdown('<div class="esc-yes">🚨 <strong>ESCALATION REQUIRED</strong><br><small>This ticket needs immediate manager attention.</small></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="esc-no">✅ <strong>No Escalation Needed</strong><br><small>Agent can handle this ticket directly.</small></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p class="sec-head">📡 Recommended Channel</p>', unsafe_allow_html=True)
            channel = data.get("recommended_channel", "Email")
            channel_icons = {"Email":"📧","Live Chat":"💬","Phone Call":"📞","Escalate to Manager":"🚨"}
            ch_icon = channel_icons.get(channel, "📡")
            st.markdown(f"""
            <div class="glass" style="text-align:center;padding:28px;">
              <div style="font-size:2.5rem;">{ch_icon}</div>
              <div style="font-size:1.2rem;font-weight:700;color:#22d3ee;margin-top:8px;">{channel}</div>
              <div style="color:#64748b;font-size:.85rem;margin-top:4px;">Recommended for this ticket</div>
            </div>""", unsafe_allow_html=True)

        with t2:
            st.markdown('<p class="sec-head">⚠️ Policy Flags</p>', unsafe_allow_html=True)
            flags = data.get("policy_flags", [])
            if flags:
                for fl in flags:
                    st.markdown(f'<div class="flag-item">⚠ {fl}</div>', unsafe_allow_html=True)
            else:
                st.success("✅ No policy violations detected.")

            st.markdown('<p class="sec-head">⏱️ Resolution Timeline</p>', unsafe_allow_html=True)
            eta = data.get("estimated_resolution_time", "—")
            st.markdown(f"""
            <div class="glass" style="text-align:center;padding:24px;">
              <div style="font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">Estimated Resolution</div>
              <div style="font-size:1.8rem;font-weight:800;background:linear-gradient(135deg,#22d3ee,#3b82f6);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;">{eta}</div>
            </div>""", unsafe_allow_html=True)

    # ── Tab 3: Quality Scoring ────────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<p class="sec-head">⭐ Response Quality Scores</p>', unsafe_allow_html=True)

        score_cols = st.columns(4)
        score_items = [
            ("Empathy",         quality.get("empathy_score", 0),         "#4ade80"),
            ("Clarity",         quality.get("clarity_score", 0),         "#22d3ee"),
            ("Professionalism", quality.get("professionalism_score", 0), "#a78bfa"),
            ("Overall",         quality.get("overall_score", 0),         "#f472b6"),
        ]
        for col, (label, val, color) in zip(score_cols, score_items):
            with col:
                st.markdown(f"""
                <div class="mbox">
                  <div class="mval" style="background:linear-gradient(135deg,{color},{color}aa);
                    -webkit-background-clip:text;">{val}</div>
                  <div style="font-size:.6rem;letter-spacing:1px;margin-top:2px;">/ 10</div>
                  <div class="mlab">{label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Radar / Spider chart
        categories = ["Empathy","Clarity","Professionalism","Overall"]
        values     = [quality.get("empathy_score",0), quality.get("clarity_score",0),
                      quality.get("professionalism_score",0), quality.get("overall_score",0)]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(34,211,238,.1)",
            line=dict(color="#22d3ee", width=2),
            name="Quality"
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,10], tickfont=dict(color="#64748b")),
                angularaxis=dict(tickfont=dict(color="#94a3b8")),
                bgcolor="rgba(0,0,0,0)",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            showlegend=False,
            title=dict(text="Quality Spider Chart", font=dict(color="#94a3b8", size=13)),
            height=360,
            margin=dict(t=60, b=30),
        )
        qa, qb = st.columns([1,1])
        with qa:
            st.plotly_chart(fig_radar, use_container_width=True)
        with qb:
            st.markdown('<p class="sec-head">📊 Score Breakdown</p>', unsafe_allow_html=True)
            for label, val, color in score_items:
                bar_color = "#4ade80" if val>=8 else "#facc15" if val>=5 else "#f87171"
                st.markdown(f"""
                <div style="margin-bottom:14px;">
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="color:#94a3b8;font-size:.85rem;">{label}</span>
                    <strong style="color:{color};">{val}/10</strong>
                  </div>
                  {score_bar(val, bar_color)}
                </div>""", unsafe_allow_html=True)

    # ── Tab 4: Analytics ──────────────────────────────────────────────────────
    with tabs[3]:
        _render_analytics(hist_all)

    # ── Tab 5: Audit Log ──────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown('<p class="sec-head">📋 Full Ticket History</p>', unsafe_allow_html=True)
        if hist_all:
            hdf = build_history_df(hist_all)
            fc1,fc2,fc3 = st.columns(3)
            with fc1:
                cat_filter = st.multiselect("Category", hdf["Category"].unique().tolist(),
                                            default=hdf["Category"].unique().tolist(), key="af_cat")
            with fc2:
                urg_filter = st.multiselect("Urgency", ["High","Medium","Low"],
                                            default=["High","Medium","Low"], key="af_urg")
            with fc3:
                esc_filter = st.multiselect("Escalated", [True, False], default=[True,False], key="af_esc")
            filtered = hdf[
                hdf["Category"].isin(cat_filter) &
                hdf["Urgency"].isin(urg_filter) &
                hdf["Escalated"].isin(esc_filter)
            ]
            st.dataframe(filtered, use_container_width=True, hide_index=True)
            ac1,ac2 = st.columns(2)
            with ac1:
                st.download_button("⬇️ Export CSV", hdf.to_csv(index=False),
                                   "support_history.csv","text/csv",use_container_width=True)
            with ac2:
                st.download_button("⬇️ Export JSON", json.dumps(hist_all,indent=2),
                                   "support_history.json","application/json",use_container_width=True)
        else:
            st.info("No history yet.")

    # ── Tab 6: Raw JSON ───────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown('<p class="sec-head">🧬 Raw Neural Output</p>', unsafe_allow_html=True)
        st.json(data)


def _render_analytics_preview(hist):
    if not hist:
        return
    hdf = build_history_df(hist)
    st.markdown("### 📊 Support Intelligence Overview")
    a1,a2 = st.columns(2)
    with a1:
        cat = hdf["Category"].value_counts().reset_index()
        cat.columns = ["Category","Count"]
        fig = px.pie(cat, values="Count", names="Category", hole=.45,
                     title="Issue Distribution",
                     color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="white")
        st.plotly_chart(fig, use_container_width=True)
    with a2:
        sent = hdf["Sentiment"].value_counts().reset_index()
        sent.columns = ["Sentiment","Count"]
        smap = {"Frustrated":"#ef4444","Angry":"#dc2626","Confused":"#facc15","Neutral":"#94a3b8","Satisfied":"#4ade80"}
        fig2 = px.bar(sent, x="Sentiment", y="Count", color="Sentiment",
                      color_discrete_map=smap, title="Sentiment Breakdown", template="plotly_dark")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)


def _render_analytics(hist):
    if not hist:
        st.info("No data yet. Process some tickets to see analytics.")
        return
    hdf = build_history_df(hist)
    st.markdown('<p class="sec-head">📊 Support Intelligence Dashboard</p>', unsafe_allow_html=True)

    r1a, r1b = st.columns(2)
    with r1a:
        cat = hdf["Category"].value_counts().reset_index()
        cat.columns = ["Category","Count"]
        fig = px.pie(cat, values="Count", names="Category", hole=.45,
                     title="Issue Category Distribution",
                     color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with r1b:
        sent = hdf["Sentiment"].value_counts().reset_index()
        sent.columns = ["Sentiment","Count"]
        smap = {"Frustrated":"#ef4444","Angry":"#dc2626","Confused":"#facc15","Neutral":"#94a3b8","Satisfied":"#4ade80"}
        fig2 = px.bar(sent, x="Sentiment", y="Count", color="Sentiment",
                      color_discrete_map=smap, title="Customer Sentiment", template="plotly_dark")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    r2a, r2b, r2c = st.columns(3)
    with r2a:
        urg = hdf["Urgency"].value_counts().reset_index()
        urg.columns = ["Urgency","Count"]
        umap = {"High":"#ef4444","Medium":"#facc15","Low":"#4ade80"}
        fig3 = px.pie(urg, values="Count", names="Urgency", color="Urgency",
                      color_discrete_map=umap, title="Urgency Distribution")
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="white")
        st.plotly_chart(fig3, use_container_width=True)

    with r2b:
        ch = hdf["Channel"].value_counts().reset_index()
        ch.columns = ["Channel","Count"]
        fig4 = px.bar(ch, x="Count", y="Channel", orientation="h", color="Channel",
                      title="Recommended Channels", template="plotly_dark",
                      color_discrete_sequence=px.colors.qualitative.Vivid)
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    with r2c:
        fig5 = px.scatter(hdf, x="Frustration", y="Quality", color="Sentiment",
                          size="Frustration", hover_data=["Customer","Category","Urgency"],
                          title="Frustration vs Quality", template="plotly_dark",
                          color_discrete_sequence=px.colors.qualitative.Vivid)
        fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig5, use_container_width=True)

    r3a, r3b = st.columns(2)
    with r3a:
        avg_q = hdf.groupby("Category")["Quality"].mean().reset_index().sort_values("Quality")
        fig6 = px.bar(avg_q, x="Quality", y="Category", orientation="h",
                      color="Quality", color_continuous_scale="Teal",
                      title="Avg Quality by Category", template="plotly_dark")
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True)

    with r3b:
        if "Date" in hdf.columns and hdf["Date"].notna().any():
            tl = hdf.groupby("Date")["Quality"].mean().reset_index().sort_values("Date")
            fig7 = px.area(tl, x="Date", y="Quality", title="Quality Score Over Time",
                           template="plotly_dark", color_discrete_sequence=["#22d3ee"])
            fig7.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
            fig7.update_traces(fillcolor="rgba(34,211,238,.1)")
            st.plotly_chart(fig7, use_container_width=True)

    st.divider()
    st.markdown('<p class="sec-head">📈 Category Summary</p>', unsafe_allow_html=True)
    summary = hdf.groupby("Category").agg(
        Tickets=("Quality","count"),
        Avg_Quality=("Quality","mean"),
        Avg_Frustration=("Frustration","mean"),
        Avg_Empathy=("Empathy","mean"),
        Escalations=("Escalated","sum"),
    ).reset_index().round(2)
    st.dataframe(summary, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
