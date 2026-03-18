"""
CRMPulse AI v1.0.0 — Premium Streamlit Dashboard
"""
__version__ = "1.0.0"

import streamlit as st
import json, os, io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
from agent import enrich_crm, save_outputs, save_batch_outputs, parse_csv_to_prompts

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CRMPulse AI | CRM Data Enrichment",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── History ───────────────────────────────────────────────────────────────────
HISTORY_FILE = "crm_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_history(data):
    history = load_history()
    data["processed_at"] = datetime.now().isoformat()
    history.insert(0, data)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[:150], f, indent=2)

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}

.stApp{background:linear-gradient(135deg,#060a14 0%,#0a1628 45%,#080d1e 100%);}
.stApp::before{
    content:'';position:fixed;top:0;left:0;right:0;bottom:0;
    background-image:
        linear-gradient(rgba(16,185,129,.02) 1px,transparent 1px),
        linear-gradient(90deg,rgba(16,185,129,.02) 1px,transparent 1px);
    background-size:64px 64px;pointer-events:none;z-index:0;
}
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#060a14 0%,#091220 100%);
    border-right:1px solid rgba(16,185,129,.18);
}

/* hero */
.hero{
    background:linear-gradient(135deg,rgba(16,185,129,.09) 0%,rgba(59,130,246,.06) 55%,rgba(139,92,246,.04) 100%);
    border:1px solid rgba(16,185,129,.18);border-radius:24px;
    padding:34px 42px;margin-bottom:26px;position:relative;overflow:hidden;
    animation:heroIn .6s ease-out;
}
@keyframes heroIn{from{opacity:0;transform:translateY(-14px);}to{opacity:1;transform:translateY(0);}}
.hero::before{
    content:'';position:absolute;top:-60px;right:-60px;width:240px;height:240px;
    background:radial-gradient(circle,rgba(16,185,129,.12) 0%,transparent 70%);pointer-events:none;
}
.hero-title{
    font-size:2.6rem;font-weight:900;margin:0;
    background:linear-gradient(135deg,#34d399 0%,#3b82f6 55%,#a78bfa 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-sub{color:#94a3b8;font-size:1rem;margin-top:8px;}
.hero-pills{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap;}
.pill{background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.22);border-radius:20px;padding:4px 14px;font-size:.78rem;color:#6ee7b7;}

/* glass card */
.glass{
    background:rgba(255,255,255,.022);backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,.06);border-radius:20px;
    padding:24px;margin-bottom:16px;transition:border-color .3s;
}
.glass:hover{border-color:rgba(16,185,129,.22);}

/* metric box */
.mbox{
    background:linear-gradient(135deg,rgba(16,185,129,.07),rgba(59,130,246,.04));
    border:1px solid rgba(16,185,129,.18);border-radius:16px;
    padding:18px;text-align:center;
    transition:transform .2s,border-color .2s,box-shadow .2s;
    animation:cardIn .5s ease-out;
}
@keyframes cardIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:translateY(0);}}
.mbox:hover{transform:translateY(-4px);border-color:rgba(16,185,129,.4);box-shadow:0 8px 28px rgba(16,185,129,.1);}
.mval{
    font-size:1.85rem;font-weight:800;
    background:linear-gradient(135deg,#34d399,#3b82f6);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.mval-sm{font-size:1rem;font-weight:700;margin-top:6px;color:#34d399;}
.mlab{font-size:.7rem;color:#64748b;text-transform:uppercase;letter-spacing:1.5px;margin-top:6px;}

/* segment badges */
.seg-enterprise{background:rgba(74,222,128,.1);color:#4ade80;border:1px solid #22c55e;padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.seg-midmarket {background:rgba(34,211,238,.1);color:#22d3ee;border:1px solid #06b6d4;padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.seg-smb       {background:rgba(167,139,250,.1);color:#a78bfa;border:1px solid #8b5cf6;padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}
.seg-startup   {background:rgba(251,146,60,.1); color:#fb923c;border:1px solid #f97316;padding:3px 13px;border-radius:20px;font-size:.78rem;font-weight:600;display:inline-block;}

/* confidence badges */
.conf-high  {background:rgba(74,222,128,.1);color:#4ade80;border:1px solid #22c55e;padding:2px 10px;border-radius:12px;font-size:.72rem;font-weight:700;}
.conf-medium{background:rgba(250,204,21,.1); color:#facc15;border:1px solid #ca8a04;padding:2px 10px;border-radius:12px;font-size:.72rem;font-weight:700;}
.conf-low   {background:rgba(239,68,68,.1);  color:#f87171;border:1px solid #ef4444;padding:2px 10px;border-radius:12px;font-size:.72rem;font-weight:700;}

/* field row */
.field-row{display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.04);font-size:.88rem;}
.field-label{color:#64748b;}
.field-val{color:#e2e8f0;font-weight:500;max-width:62%;text-align:right;}

/* flag item */
.flag-item{background:rgba(245,158,11,.04);border-left:4px solid #f59e0b;border-radius:0 10px 10px 0;padding:10px 14px;margin-top:8px;font-size:.87rem;color:#fbbf24;}

/* action item */
.action-item{display:flex;gap:12px;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.04);align-items:flex-start;}
.action-num{background:linear-gradient(135deg,#34d399,#3b82f6);border-radius:50%;width:24px;height:24px;min-width:24px;display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;color:#060a14;}
.action-text{color:#cbd5e1;font-size:.88rem;line-height:1.5;padding-top:2px;}

/* tech chip */
.tech-chip{display:inline-block;background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:14px;padding:3px 12px;font-size:.75rem;color:#93c5fd;margin:3px 3px 3px 0;}

/* section head */
.sec-head{font-size:1rem;font-weight:700;color:#6ee7b7;letter-spacing:.5px;margin-bottom:14px;padding-bottom:6px;border-bottom:1px solid rgba(16,185,129,.18);}

/* info row */
.info-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.04);font-size:.88rem;}
.info-label{color:#64748b;}
.info-val{color:#e2e8f0;font-weight:500;}

/* duplicate badge */
.dup-badge{background:rgba(239,68,68,.08);border:1px solid #ef4444;border-radius:10px;padding:12px 16px;color:#fca5a5;border-left:4px solid #ef4444;margin-bottom:10px;}

/* primary button */
.stButton > button[kind="primary"]{
    background:linear-gradient(135deg,#059669,#1d4ed8) !important;
    border:none !important;border-radius:10px !important;
    font-weight:700 !important;letter-spacing:.3px !important;
    transition:all .25s ease !important;
}
.stButton > button[kind="primary"]:hover{
    transform:translateY(-2px) !important;
    box-shadow:0 6px 24px rgba(16,185,129,.3) !important;
    background:linear-gradient(135deg,#10b981,#2563eb) !important;
}

/* tabs */
.stTabs [data-baseweb="tab"]{color:#64748b !important;font-weight:500;}
.stTabs [aria-selected="true"]{color:#34d399 !important;border-bottom-color:#34d399 !important;}

h1,h2,h3,h4{color:#f1f5f9 !important;}
p,li{color:#cbd5e1;}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
MODELS = {
    "OpenAI":    ["gpt-4.1-mini", "gpt-4o", "gpt-4o-mini"],
    "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
    "Gemini":    ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
    "Groq":      ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
}
CONF_ORDER = {"High": 3, "Medium": 2, "Low": 1}

# ── Helpers ───────────────────────────────────────────────────────────────────
def segment_badge(seg):
    cls = {
        "Enterprise": "seg-enterprise", "Mid-Market": "seg-midmarket",
        "SMB": "seg-smb", "Startup": "seg-startup",
    }.get(seg, "seg-smb")
    return f'<span class="{cls}">{seg}</span>'

def conf_badge(c):
    cls = {"High": "conf-high", "Medium": "conf-medium", "Low": "conf-low"}.get(c, "conf-medium")
    return f'<span class="{cls}">{c}</span>'

def safe_int(v, default=0):
    try: return int(v or default)
    except: return default

def lead_color(score):
    if score >= 75: return "#4ade80"
    if score >= 50: return "#facc15"
    return "#f87171"

def build_history_df(hist):
    rows = []
    for d in hist:
        ef = d.get("enriched_fields", {})
        techs = ef.get("technologies_used", [])
        rows.append({
            "Date":       d.get("processed_at", "")[:10],
            "Name":       d.get("name", ""),
            "Company":    d.get("company", ""),
            "Industry":   ef.get("industry", ""),
            "Segment":    ef.get("account_segment", ""),
            "Funding":    ef.get("funding_stage", ""),
            "LeadScore":  safe_int(d.get("lead_score", 0)),
            "DataQuality":safe_int(d.get("data_quality_score", 0)),
            "TechCount":  len(techs) if isinstance(techs, list) else 0,
            "Flags":      len(d.get("flags", [])),
            "Duplicates": sum(1 for fl in d.get("flags",[]) if "Duplicate" in fl),
        })
    return pd.DataFrame(rows)

# ── Main App ──────────────────────────────────────────────────────────────────
def main():
    # Hero
    st.markdown(f"""
    <div class="hero">
        <p class="hero-title">🧬 CRMPulse AI</p>
        <p class="hero-sub">Enterprise CRM Data Enrichment · Lead Intelligence · Confidence Scoring · B2B Company Profiling</p>
        <div class="hero-pills">
            <span class="pill">🧠 Multi-Model AI</span>
            <span class="pill">🏢 Company Profiling</span>
            <span class="pill">🎯 Lead Scoring</span>
            <span class="pill">🔎 Dedup Detection</span>
            <span class="pill">📊 Confidence Heatmap</span>
            <span class="pill">⚡ Batch Enrichment</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    hist_all   = load_history()
    total      = len(hist_all)
    avg_lead   = (sum(safe_int(d.get("lead_score",0)) for d in hist_all) / total) if total else 0
    avg_qual   = (sum(safe_int(d.get("data_quality_score",0)) for d in hist_all) / total) if total else 0
    dups       = sum(1 for d in hist_all if any("Duplicate" in fl for fl in d.get("flags",[])))
    flagged    = sum(1 for d in hist_all if d.get("flags"))

    k1,k2,k3,k4,k5 = st.columns(5)
    for col,label,val in [
        (k1,"Records Enriched",str(total)),
        (k2,"Avg Lead Score",  f"{avg_lead:.1f}/100"),
        (k3,"Avg Data Quality",f"{avg_qual:.1f}%"),
        (k4,"Duplicates Found",str(dups)),
        (k5,"Records Flagged", str(flagged)),
    ]:
        with col:
            st.markdown(f'<div class="mbox"><div class="mval">{val}</div><div class="mlab">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Engine Control")
        st.markdown(f"""
        <div style="background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.22);
             border-radius:8px;padding:6px 12px;margin-bottom:12px;text-align:center;">
            <span style="color:#6ee7b7;font-size:.75rem;font-weight:600;">🧬 CRMPulse AI v{__version__}</span>
        </div>""", unsafe_allow_html=True)

        provider = st.selectbox("AI Provider", list(MODELS.keys()), key="provider")
        model    = st.selectbox("Model", MODELS[provider], key="model")
        api_key  = st.text_input(f"{provider} API Key", type="password", key="api_key")
        st.caption(f"Or set `{provider.upper()}_API_KEY` in .env")

        st.divider()
        st.markdown("### 📂 Input Mode")
        mode = st.radio("Mode", ["✏️ Manual Record", "📄 Text File", "📊 Batch CSV"], key="mode")

        raw_inputs = []

        if mode == "✏️ Manual Record":
            name     = st.text_input("Full Name",  "Jane Doe")
            email    = st.text_input("Email",       "jane.doe@techstartup.com")
            company  = st.text_input("Company",     "TechStartup Inc.")
            role     = st.text_input("Role",        "Product Manager")
            location = st.text_input("Location",    "San Francisco, CA")
            st.markdown("**Missing Fields to Enrich:**")
            fields_opts = ["industry","company_size","annual_revenue","account_segment",
                           "funding_stage","linkedin_url","technologies_used","headquarters","founded_year"]
            missing = st.multiselect("Select fields", fields_opts,
                                     default=["industry","company_size","account_segment","funding_stage"], key="missing")
            raw_inputs = [
                f"Name: {name}\nEmail: {email}\nCompany: {company}\n"
                f"Known Fields:\n- Role: {role}\n- Location: {location}\n"
                f"Missing Fields:\n" + "".join(f"- {f}\n" for f in missing)
            ]

        elif mode == "📄 Text File":
            ufile = st.file_uploader("Upload input.txt", type=["txt"])
            if ufile:
                raw_inputs = [ufile.getvalue().decode("utf-8")]

        else:
            st.caption("CSV columns: name, email, company, role, location, missing_fields")
            cfile = st.file_uploader("Upload CSV", type=["csv"])
            if cfile:
                df_up = pd.read_csv(io.StringIO(cfile.getvalue().decode("utf-8")))
                for _, row in df_up.iterrows():
                    missing_raw = str(row.get("missing_fields",""))
                    missing = [f.strip() for f in missing_raw.split(",") if f.strip()]
                    raw_inputs.append(
                        f"Name: {row.get('name','')}\nEmail: {row.get('email','')}\n"
                        f"Company: {row.get('company','')}\n"
                        f"Known Fields:\n- Role: {row.get('role','')}\n- Location: {row.get('location','')}\n"
                        f"Missing Fields:\n" + "".join(f"- {f}\n" for f in missing)
                    )

        sample_csv = (
            "name,email,company,role,location,missing_fields\n"
            "Jane Doe,jane.doe@techstartup.com,TechStartup Inc.,Product Manager,\"San Francisco, CA\","
            "\"industry,company_size,account_segment,funding_stage\"\n"
            "John Smith,john.smith@retailco.com,RetailCo Ltd.,VP of Sales,\"New York, NY\","
            "\"industry,annual_revenue,technologies_used\"\n"
        )
        st.download_button("⬇️ Sample Batch CSV", sample_csv, "sample_records.csv", "text/csv", use_container_width=True)

        st.divider()
        enrich_btn = st.button("🚀 Enrich CRM Record", use_container_width=True, type="primary")

        # History sidebar
        if hist_all:
            st.divider()
            st.markdown("### 🕒 Recent Records")
            for i, entry in enumerate(hist_all[:6]):
                nm  = str(entry.get("name","?"))[:14]
                ls  = safe_int(entry.get("lead_score", 0))
                icon = "🔥" if ls >= 75 else "⚡" if ls >= 50 else "📋"
                if st.button(f"{icon} {nm} — {ls}/100", key=f"h_{i}", use_container_width=True):
                    st.session_state["result"] = entry
                    st.session_state["batch"]  = [entry]
            if st.button("🗑️ Clear History", use_container_width=True):
                clear_history()
                st.rerun()

    # ── Processing ────────────────────────────────────────────────────────────
    if enrich_btn:
        if not raw_inputs:
            st.error("⚠️ Input is empty — select a mode and fill in the details.")
        else:
            prog    = st.progress(0, "Enriching CRM records...")
            results = []
            for idx, inp in enumerate(raw_inputs):
                with st.spinner(f"🔍 [{idx+1}/{len(raw_inputs)}] Enriching with {model}..."):
                    try:
                        res = enrich_crm(inp, provider=provider, model=model,
                                         api_key=api_key if api_key else None)
                        results.append(res)
                        save_outputs(res)
                        save_to_history(res)
                    except Exception as e:
                        st.error(f"❌ Record {idx+1} failed: {e}")
                prog.progress((idx+1)/len(raw_inputs))
            prog.empty()
            if results:
                st.session_state["batch"]  = results
                st.session_state["result"] = results[0]
                if len(results) > 1:
                    save_batch_outputs(results)
                st.toast(f"✅ {len(results)} record(s) enriched!", icon="🧬")
                st.rerun()

    # ── Batch Table ───────────────────────────────────────────────────────────
    batch = st.session_state.get("batch", [])
    if len(batch) > 1:
        st.markdown("### 📦 Batch Results")
        bdf = pd.DataFrame([{
            "Name":      r.get("name"),
            "Company":   r.get("company"),
            "Industry":  r.get("enriched_fields",{}).get("industry",""),
            "Segment":   r.get("enriched_fields",{}).get("account_segment",""),
            "Funding":   r.get("enriched_fields",{}).get("funding_stage",""),
            "Lead Score": r.get("lead_score","—"),
            "Quality %": r.get("data_quality_score","—"),
            "Flags":     len(r.get("flags",[])),
        } for r in batch])
        st.dataframe(bdf, use_container_width=True, hide_index=True)

        sel = st.selectbox("🔍 Inspect Record", range(len(batch)),
                           format_func=lambda x: f"{batch[x].get('name')} — {batch[x].get('company')}")
        st.session_state["result"] = batch[sel]

        bc1,bc2,bc3 = st.columns(3)
        with bc1:
            st.download_button("⬇️ JSON (all)", json.dumps(batch,indent=2),
                               "crm_batch.json","application/json",use_container_width=True)
        with bc2:
            st.download_button("⬇️ CSV (all)", bdf.to_csv(index=False),
                               "crm_batch.csv","text/csv",use_container_width=True)
        with bc3:
            avg_q  = sum(safe_int(r.get("data_quality_score",0)) for r in batch)/len(batch)
            avg_ls = sum(safe_int(r.get("lead_score",0)) for r in batch)/len(batch)
            report = (f"CRMPulse Batch — {date.today()}\n"
                      f"Records: {len(batch)}\nAvg Quality: {avg_q:.1f}%\nAvg Lead Score: {avg_ls:.1f}/100\n")
            st.download_button("⬇️ Report TXT", report,
                               "crm_batch_report.txt","text/plain",use_container_width=True)
        st.divider()

    # ── Detail Dashboard ──────────────────────────────────────────────────────
    data = st.session_state.get("result")
    if not data:
        st.markdown("""
        <div class="glass" style="text-align:center;padding:60px 40px;">
            <div style="font-size:3rem;margin-bottom:16px;">🧬</div>
            <h3 style="color:#6ee7b7 !important;">Ready to Enrich</h3>
            <p style="color:#64748b;">Fill in the sidebar and click <strong style="color:#34d399;">Enrich CRM Record</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
        if hist_all:
            _render_analytics(hist_all)
        return

    ef      = data.get("enriched_fields", {})
    conf    = data.get("confidence", {})
    flags   = data.get("flags", [])
    actions = data.get("recommended_actions", [])
    techs   = ef.get("technologies_used", [])
    if not isinstance(techs, list):
        techs = [techs] if techs else []

    lead_score   = safe_int(data.get("lead_score", 0))
    data_quality = safe_int(data.get("data_quality_score", 0))
    segment      = ef.get("account_segment", "—")

    # Top metrics
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    for col,label,val,small in [
        (m1,"Name",     data.get("name","—"),   True),
        (m2,"Company",  data.get("company","—"),True),
        (m3,"Segment",  segment_badge(segment), False),
        (m4,"Industry", ef.get("industry","—"), True),
        (m5,"Lead Score",f"{lead_score}/100",   False),
        (m6,"Quality",  f"{data_quality}%",     False),
    ]:
        with col:
            cls = "mval-sm" if small else "mval"
            st.markdown(f'<div class="mbox"><div class="{cls}">{val}</div><div class="mlab">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["🧬 Enriched Profile", "🎯 Lead Intelligence", "📊 Confidence Map", "⚡ Analytics", "📋 Audit Log", "🔬 Raw JSON"])

    # ── Tab 1: Enriched Profile ───────────────────────────────────────────────
    with tabs[0]:
        left, right = st.columns([3, 2], gap="large")

        with left:
            st.markdown('<p class="sec-head">🏢 Contact Profile</p>', unsafe_allow_html=True)
            contact_rows = [
                ("Name",     data.get("name","—")),
                ("Email",    data.get("email","—")),
                ("Company",  data.get("company","—")),
                ("Role",     data.get("role","—")),
                ("Location", data.get("location","—")),
            ]
            st.markdown('<div class="glass">' + "".join(
                f'<div class="info-row"><span class="info-label">{k}</span><span class="info-val">{v}</span></div>'
                for k,v in contact_rows
            ) + '</div>', unsafe_allow_html=True)

            st.markdown('<p class="sec-head">🔎 Enriched Intelligence</p>', unsafe_allow_html=True)
            plain_ef = [
                ("Industry",        "industry"),
                ("Company Size",    "company_size"),
                ("Annual Revenue",  "annual_revenue"),
                ("Account Segment", "account_segment"),
                ("Funding Stage",   "funding_stage"),
                ("Headquarters",    "headquarters"),
                ("Founded Year",    "founded_year"),
                ("LinkedIn URL",    "linkedin_url"),
            ]
            rows_html = ""
            for label, key in plain_ef:
                val  = ef.get(key, "—")
                cval = conf.get(key, "—")
                cb   = conf_badge(cval) if cval in ("High","Medium","Low") else f'<span style="color:#475569">{cval}</span>'
                rows_html += f'<div class="field-row"><span class="field-label">{label}</span><span class="field-val">{val}&nbsp;&nbsp;{cb}</span></div>'
            st.markdown(f'<div class="glass">{rows_html}</div>', unsafe_allow_html=True)

            # Tech stack
            if techs:
                st.markdown('<p class="sec-head">⚙️ Technology Stack</p>', unsafe_allow_html=True)
                ch = conf_badge(conf.get("technologies_used","—"))
                chips = "".join(f'<span class="tech-chip">🔧 {t}</span>' for t in techs)
                st.markdown(f'<div class="glass">{chips}<br><br><small style="color:#64748b">Confidence: {ch}</small></div>',
                            unsafe_allow_html=True)

            # Recommended actions
            if actions:
                st.markdown('<p class="sec-head">🗺️ Recommended Actions</p>', unsafe_allow_html=True)
                act_html = "".join(
                    f'<div class="action-item"><div class="action-num">{i}</div><div class="action-text">{a}</div></div>'
                    for i, a in enumerate(actions, 1)
                )
                st.markdown(f'<div class="glass">{act_html}</div>', unsafe_allow_html=True)

        with right:
            # Lead score gauge
            st.markdown('<p class="sec-head">🎯 Lead Score</p>', unsafe_allow_html=True)
            lc = lead_color(lead_score)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=lead_score,
                domain={"x":[0,1],"y":[0,1]},
                number={"font":{"color":lc,"size":38},"suffix":"/100"},
                gauge={
                    "axis":{"range":[0,100],"tickfont":{"color":"#64748b"}},
                    "bar":{"color":lc,"thickness":.25},
                    "bgcolor":"rgba(0,0,0,0)",
                    "steps":[
                        {"range":[0,49],  "color":"rgba(239,68,68,.1)"},
                        {"range":[50,74], "color":"rgba(250,204,21,.1)"},
                        {"range":[75,100],"color":"rgba(74,222,128,.1)"},
                    ],
                    "threshold":{"line":{"color":lc,"width":3},"thickness":.75,"value":lead_score},
                },
            ))
            fig_gauge.update_layout(
                height=230, margin=dict(t=30,b=10,l=30,r=30),
                paper_bgcolor="rgba(0,0,0,0)", font_color="white",
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown(f'<div class="glass" style="text-align:center;padding:12px 16px;">'
                        f'<div style="color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:1px;">Lead Reason</div>'
                        f'<div style="color:#e2e8f0;font-size:.88rem;margin-top:6px;">{data.get("lead_score_reason","—")}</div>'
                        f'</div>', unsafe_allow_html=True)

            # Data quality donut
            st.markdown('<p class="sec-head">📈 Data Quality</p>', unsafe_allow_html=True)
            qc = "#4ade80" if data_quality >= 70 else "#facc15" if data_quality >= 40 else "#f87171"
            fig_q = go.Figure(go.Pie(
                values=[data_quality, 100-data_quality],
                labels=["Known","Missing"],
                hole=.62, textinfo="none",
                marker_colors=[qc, "#1e293b"],
            ))
            fig_q.update_layout(
                height=170, margin=dict(t=10,b=10,l=10,r=10),
                paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                annotations=[{"text":f"{data_quality}%","x":.5,"y":.5,
                              "font_size":26,"font_color":qc,"showarrow":False}]
            )
            st.plotly_chart(fig_q, use_container_width=True)

            # Flags
            if flags:
                st.markdown('<p class="sec-head">⚠️ Flags</p>', unsafe_allow_html=True)
                for fl in flags:
                    st.markdown(f'<div class="flag-item">⚠ {fl}</div>', unsafe_allow_html=True)

            # Enrichment summary
            st.markdown('<p class="sec-head">📝 Summary</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass"><div style="color:#cbd5e1;font-size:.9rem;line-height:1.7;">{data.get("enrichment_summary","—")}</div></div>',
                        unsafe_allow_html=True)

            # Exports
            e1,e2 = st.columns(2)
            with e1:
                st.download_button("⬇️ JSON", json.dumps(data,indent=2),
                                   "crm_enriched.json","application/json",use_container_width=True)
            with e2:
                txt_lines = [
                    f"CRMPulse — {data.get('name')} ({date.today()})",
                    f"Company: {data.get('company')}",
                    f"Industry: {ef.get('industry','—')}",
                    f"Segment: {segment}",
                    f"Lead Score: {lead_score}/100",
                    f"Quality: {data_quality}%",
                ]
                st.download_button("⬇️ TXT", "\n".join(txt_lines),
                                   "crm_enriched.txt","text/plain",use_container_width=True)

    # ── Tab 2: Lead Intelligence ──────────────────────────────────────────────
    with tabs[1]:
        l1,l2 = st.columns(2)
        with l1:
            st.markdown('<p class="sec-head">💼 Account Classification</p>', unsafe_allow_html=True)
            seg_rows = [
                ("Account Segment",  segment_badge(segment)),
                ("Funding Stage",    ef.get("funding_stage","—")),
                ("Company Size",     ef.get("company_size","—")),
                ("Annual Revenue",   ef.get("annual_revenue","—")),
                ("Headquarters",     ef.get("headquarters","—")),
                ("Founded Year",     ef.get("founded_year","—")),
            ]
            st.markdown('<div class="glass">' + "".join(
                f'<div class="info-row"><span class="info-label">{k}</span><span class="info-val">{v}</span></div>'
                for k,v in seg_rows
            ) + '</div>', unsafe_allow_html=True)

        with l2:
            st.markdown('<p class="sec-head">📮 Contact Intelligence</p>', unsafe_allow_html=True)
            contact_intel = [
                ("Email",     data.get("email","—")),
                ("Role",      data.get("role","—")),
                ("LinkedIn",  ef.get("linkedin_url","—")),
                ("Location",  data.get("location","—")),
            ]
            st.markdown('<div class="glass">' + "".join(
                f'<div class="info-row"><span class="info-label">{k}</span><span class="info-val">{v}</span></div>'
                for k,v in contact_intel
            ) + '</div>', unsafe_allow_html=True)

            # Lead score bar
            st.markdown('<p class="sec-head">📊 Lead Potential</p>', unsafe_allow_html=True)
            lc = lead_color(lead_score)
            tiers = [("High (75-100)","#4ade80",75),("Medium (50-74)","#facc15",50),("Low (<50)","#f87171",0)]
            tier_label = next((t for t,_,mn in tiers if lead_score >= mn), "Low (<50)")
            st.markdown(f"""
            <div class="glass">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="color:#94a3b8;">Lead Potential Tier</span>
                <strong style="color:{lc};">{tier_label}</strong>
              </div>
              <div style="background:rgba(255,255,255,.07);border-radius:8px;height:10px;overflow:hidden;">
                <div style="width:{lead_score}%;height:10px;background:{lc};border-radius:8px;transition:width .6s;"></div>
              </div>
              <div style="color:#64748b;font-size:.8rem;margin-top:8px;">{data.get('lead_score_reason','—')}</div>
            </div>""", unsafe_allow_html=True)

    # ── Tab 3: Confidence Map ─────────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<p class="sec-head">📊 Per-Field Confidence Heatmap</p>', unsafe_allow_html=True)

        conf_fields = [
            "industry","company_size","annual_revenue","account_segment",
            "funding_stage","linkedin_url","technologies_used","headquarters","founded_year"
        ]
        conf_labels = {
            "industry":"Industry","company_size":"Company Size","annual_revenue":"Annual Revenue",
            "account_segment":"Segment","funding_stage":"Funding Stage","linkedin_url":"LinkedIn",
            "technologies_used":"Tech Stack","headquarters":"HQ","founded_year":"Founded"
        }
        conf_color_map = {"High":2,"Medium":1,"Low":0}

        cf_data = []
        for key in conf_fields:
            val   = ef.get(key, "—")
            cval  = conf.get(key, "Low")
            score = conf_color_map.get(cval, 0)
            display_val = ", ".join(val) if isinstance(val, list) else str(val)[:30]
            cf_data.append({
                "Field":  conf_labels.get(key, key),
                "Value":  display_val,
                "Confidence": cval,
                "Score":  score,
            })

        cdf = pd.DataFrame(cf_data)

        c1, c2 = st.columns([2, 1])
        with c1:
            fig_hm = px.bar(
                cdf, x="Field", y="Score", color="Confidence",
                color_discrete_map={"High":"#4ade80","Medium":"#facc15","Low":"#f87171"},
                title="Confidence by Enriched Field",
                template="plotly_dark",
                hover_data=["Value"],
            )
            fig_hm.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(tickvals=[0,1,2], ticktext=["Low","Medium","High"]),
                showlegend=True, height=340,
                margin=dict(t=50, b=60),
            )
            st.plotly_chart(fig_hm, use_container_width=True)

        with c2:
            st.markdown('<p class="sec-head">🔑 Field Details</p>', unsafe_allow_html=True)
            for row in cf_data:
                cb = conf_badge(row["Confidence"])
                st.markdown(
                    f'<div class="field-row"><span class="field-label">{row["Field"]}</span>'
                    f'<span class="field-val">{cb}</span></div>',
                    unsafe_allow_html=True
                )

        # Tech stack bubble chart
        if techs:
            st.markdown('<p class="sec-head">🔧 Technology Stack Distribution</p>', unsafe_allow_html=True)
            tech_df = pd.DataFrame({"Technology": techs, "Count": [1]*len(techs)})
            fig_tech = px.treemap(tech_df, path=["Technology"], values="Count",
                                  title="Inferred Tech Stack",
                                  color_discrete_sequence=px.colors.qualitative.Vivid)
            fig_tech.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", height=260)
            st.plotly_chart(fig_tech, use_container_width=True)

    # ── Tab 4: Analytics ──────────────────────────────────────────────────────
    with tabs[3]:
        _render_analytics(hist_all)

    # ── Tab 5: Audit Log ──────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown('<p class="sec-head">📋 Enrichment History</p>', unsafe_allow_html=True)
        if hist_all:
            hdf = build_history_df(hist_all)
            fc1,fc2 = st.columns(2)
            with fc1:
                seg_f = st.multiselect("Segment Filter", hdf["Segment"].unique().tolist(),
                                        default=hdf["Segment"].unique().tolist(), key="seg_f")
            with fc2:
                min_ls = st.slider("Min Lead Score", 0, 100, 0, key="ls_f")
            filtered = hdf[hdf["Segment"].isin(seg_f) & (hdf["LeadScore"] >= min_ls)]
            st.dataframe(filtered, use_container_width=True, hide_index=True)
            ac1,ac2 = st.columns(2)
            with ac1:
                st.download_button("⬇️ Export CSV", hdf.to_csv(index=False),
                                   "crm_history.csv","text/csv",use_container_width=True)
            with ac2:
                st.download_button("⬇️ Export JSON", json.dumps(hist_all,indent=2),
                                   "crm_history.json","application/json",use_container_width=True)
        else:
            st.info("No enrichment history yet.")

    # ── Tab 6: Raw JSON ───────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown('<p class="sec-head">🔬 Raw Enrichment Output</p>', unsafe_allow_html=True)
        st.json(data)


def _render_analytics(hist):
    if not hist:
        st.info("No data yet. Enrich some records to see analytics.")
        return
    hdf = build_history_df(hist)
    st.markdown('<p class="sec-head">📊 CRM Enrichment Intelligence Dashboard</p>', unsafe_allow_html=True)

    r1a, r1b = st.columns(2)
    with r1a:
        seg = hdf["Segment"].value_counts().reset_index()
        seg.columns = ["Segment","Count"]
        scmap = {"Enterprise":"#4ade80","Mid-Market":"#22d3ee","SMB":"#a78bfa","Startup":"#fb923c"}
        fig1 = px.pie(seg, values="Count", names="Segment", hole=.45,
                      color="Segment", color_discrete_map=scmap, title="Account Segment Distribution")
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig1, use_container_width=True)

    with r1b:
        ind = hdf["Industry"].value_counts().reset_index()
        ind.columns = ["Industry","Count"]
        fig2 = px.bar(ind.head(10), x="Count", y="Industry", orientation="h",
                      color="Count", color_continuous_scale="Teal",
                      title="Top Industries", template="plotly_dark")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    r2a, r2b, r2c = st.columns(3)
    with r2a:
        fnd = hdf["Funding"].value_counts().reset_index()
        fnd.columns = ["Funding","Count"]
        fig3 = px.pie(fnd, values="Count", names="Funding", hole=.45,
                      title="Funding Stage Mix",
                      color_discrete_sequence=px.colors.qualitative.Vivid)
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig3, use_container_width=True)

    with r2b:
        fig4 = px.scatter(hdf, x="DataQuality", y="LeadScore",
                          color="Segment", size="LeadScore",
                          hover_data=["Name","Company","Industry"],
                          title="Data Quality vs Lead Score",
                          template="plotly_dark",
                          color_discrete_map={"Enterprise":"#4ade80","Mid-Market":"#22d3ee","SMB":"#a78bfa","Startup":"#fb923c"})
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig4, use_container_width=True)

    with r2c:
        avg_ls = hdf.groupby("Segment")["LeadScore"].mean().reset_index().sort_values("LeadScore",ascending=False)
        fig5 = px.bar(avg_ls, x="Segment", y="LeadScore", color="Segment",
                      color_discrete_map={"Enterprise":"#4ade80","Mid-Market":"#22d3ee","SMB":"#a78bfa","Startup":"#fb923c"},
                      title="Avg Lead Score by Segment", template="plotly_dark")
        fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    if "Date" in hdf.columns and hdf["Date"].notna().any():
        tl = hdf.groupby("Date")[["LeadScore","DataQuality"]].mean().reset_index().sort_values("Date")
        fig6 = px.line(tl, x="Date", y=["LeadScore","DataQuality"],
                       title="Lead Score & Data Quality Over Time", template="plotly_dark",
                       color_discrete_sequence=["#34d399","#3b82f6"])
        fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig6, use_container_width=True)

    st.divider()
    st.markdown('<p class="sec-head">📈 Segment Summary Table</p>', unsafe_allow_html=True)
    summary = hdf.groupby("Segment").agg(
        Records=("LeadScore","count"),
        Avg_LeadScore=("LeadScore","mean"),
        Avg_DataQuality=("DataQuality","mean"),
        Avg_TechStack=("TechCount","mean"),
        Total_Flags=("Flags","sum"),
        Duplicates=("Duplicates","sum"),
    ).reset_index().round(2)
    st.dataframe(summary, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
