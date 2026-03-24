import streamlit as st
import json
import os
import time
from openai import OpenAI
from datetime import date
from dotenv import load_dotenv

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# --- Page Config ---
st.set_page_config(
    page_title="HealDesk | Autonomous Recovery",
    page_icon="🩹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if 'latest_recovery' not in st.session_state:
    st.session_state.latest_recovery = None

# --- Providers & Models Mappings ---
LLM_MANIFEST = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
    "Google Gemini": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    "xAI Grok": ["grok-2", "grok-beta"]
}

# --- SaaS Premium UI (Vercel Style) ---
def inject_premium_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --bg-main: #000000;
            --bg-card: #0a0a0a;
            --accent: #f5a623; /* Recovery Orange */
            --border: #1f1f1f;
            --text-primary: #ffffff;
            --text-secondary: #888888;
        }

        .main { background: var(--bg-main); color: var(--text-primary); }
        [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid var(--border); }
        [data-testid="stHeader"] { background: transparent; }
        footer { visibility: hidden; }
        .stDeployButton { display: none; }

        h1, h2, h3, p, span, div { font-family: 'Inter', sans-serif !important; }
        
        /* KPI Cards */
        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s ease;
        }
        .kpi-card:hover { border-color: #444; }
        .kpi-label { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
        .kpi-value { font-size: 1.5rem; font-weight: 600; color: var(--text-primary); }

        /* Anomaly Header */
        .anomaly-header {
            background: rgba(245, 166, 35, 0.05);
            border: 1px solid rgba(245, 166, 35, 0.2);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* Timeline Action */
        .action-step {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
            padding: 1rem;
            background: #050505;
            border-radius: 8px;
            border: 1px solid #111;
        }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #00ff85; }

        /* Escalation Alert */
        .escalation-alert {
            background: #ff3b3022;
            border: 1px solid #ff3b30;
            color: #ff3b30;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1.5rem;
            text-align: center;
            font-weight: 700;
            letter-spacing: 0.05em;
        }

        </style>
    """, unsafe_allow_html=True)

def call_recovery_engine(error_context, provider, model):
    system_prompt = """
    You are an Error Recovery Agent.
    Rules:
    - Classify errors precisely.
    - Select safe, autonomous recovery actions.
    - Avoid infinite loops.
    - Escalate if resolution is impossible.
    Return ONLY JSON:
    {
      "error_classification": "",
      "recovery_actions": [],
      "recovery_status": "Recovered|Degraded|FAILED",
      "escalation_required": true/false
    }
    """
    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": error_context}],
                response_format={ "type": "json_object" },
                temperature=0.0
            )
            return json.loads(resp.choices[0].message.content)
        # Placeholder for other providers
        return {"error": "Multi-provider logic coming soon."}
    except Exception as e:
        return {"error": str(e)}

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>🩹 HealDesk.AI</h2>", unsafe_allow_html=True)
        nav = st.radio("Primary Modules", ["Recovery Studio", "Heal History", "Configuration"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; font-size:0.7rem;'>PROVIDER SELECTION</p>", unsafe_allow_html=True)
        st.session_state.provider = st.selectbox("Provider", list(LLM_MANIFEST.keys()), index=0, label_visibility="collapsed")
        
        st.markdown("<p style='color:#888; font-size:0.7rem; margin-top:1rem;'>NEURAL ENGINE</p>", unsafe_allow_html=True)
        st.session_state.model = st.selectbox("Model", LLM_MANIFEST[st.session_state.provider], index=0, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(245,166,35,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(245,166,35,0.1);'>
                <div style='font-size:0.7rem; color:#f5a623; font-weight:600;'>HEALER STATUS</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'>Active // {st.session_state.model}</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    if current_nav == "Recovery Studio":
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.2rem; letter-spacing: -0.05em; font-weight: 700;'>Recovery Studio</h1>
                    <p style='color:#888; font-size:0.95rem;'>Detect, classify, and autonomously heal system anomalies.</p>
                </div>
                <div style='text-align:right'>
                    <div style='color:#888; font-size:0.75rem; margin-bottom:4px;'>HEAL ENFORCEMENT</div>
                    <div style='display:flex; align-items:center; gap:8px;'><div style='width:6px; height:6px; background:#00ff85; border-radius:50%;'></div><span style='color:white; font-size:0.85rem; font-weight:500;'>ARMED</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_in, col_spacer, col_out = st.columns([1, 0.08, 1.4])

        with col_in:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>ANOMALY CONTEXT</h4>", unsafe_allow_html=True)
            error_input = st.text_area("error_input", value="Error Type: Database connection timeout\nSeverity: High\nContext:\n- Query execution\n- User authentication flow", height=250, label_visibility="collapsed")
            
            if st.button("INITIATE HEALING"):
                if error_input:
                    with st.status("Analyzing Anomaly Architecture...", expanded=True) as status:
                        res = call_recovery_engine(error_input, st.session_state.provider, st.session_state.model)
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.session_state.latest_recovery = res
                            status.update(label="Healing Procedure Computed", state="complete")
                            st.rerun()

        with col_out:
            if st.session_state.latest_recovery:
                r = st.session_state.latest_recovery
                status_color = "#00ff85" if r['recovery_status'] == "Recovered" else "#f5a623" if r['recovery_status'] == "Degraded" else "#ff3b30"
                
                st.markdown(f"""
                    <div class="anomaly-header">
                        <div style="font-size:0.75rem; color:#f5a623; font-weight:700; text-transform:uppercase; letter-spacing:0.1em;">Error Classification</div>
                        <h2 style="margin-top:0.5rem; font-weight:700;">{r['error_classification']}</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>AUTONOMOUS ACTIONS TAKEN</h4>", unsafe_allow_html=True)
                for action in r['recovery_actions']:
                    st.markdown(f"""<div class="action-step"><div class="status-dot"></div><div style="font-size:0.95rem; color:#eee;">{action}</div></div>""", unsafe_allow_html=True)
                
                col_s, col_e = st.columns(2)
                with col_s:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Outcome Status</div><div class="kpi-value" style="color:{status_color};">{r["recovery_status"]}</div></div>', unsafe_allow_html=True)
                with col_e:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Escalated</div><div class="kpi-value">{"YES" if r["escalation_required"] else "NO"}</div></div>', unsafe_allow_html=True)
                
                if r["escalation_required"]:
                    st.markdown("<div class='escalation-alert'>⚠️ OPERATOR INTERVENTION REQUIRED ⚠️</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="height:450px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed #222; border-radius:12px;">
                        <span style="font-size:2.5rem; opacity:0.2;">🩺</span>
                        <div style="color:#444; font-size:0.85rem; margin-top:1rem;">Awaiting Anomaly Signal</div>
                    </div>
                """, unsafe_allow_html=True)

    elif current_nav == "Heal History":
        st.markdown("<h1>Heal History</h1>", unsafe_allow_html=True)
        st.info("Log records pending persistence layer integration.")

if __name__ == "__main__":
    main()
