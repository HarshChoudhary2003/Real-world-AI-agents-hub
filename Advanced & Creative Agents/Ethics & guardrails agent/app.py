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
    page_title="Sentinel.Ethics | Governance Matrix",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if 'latest_ethics_check' not in st.session_state:
    st.session_state.latest_ethics_check = None

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
            --accent: #ffb800; /* Compliance Gold */
            --border: #1f1f1f;
            --text-primary: #ffffff;
            --text-secondary: #888888;
        }

        .main { background: var(--bg-main); color: var(--text-primary); }
        [data-testid="stSidebar"] { background-color: #0d0d0d; border-right: 1px solid var(--border); }
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
        .kpi-label { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem; }
        .kpi-value { font-size: 1.4rem; font-weight: 700; color: var(--text-primary); }

        /* Decision Badge */
        .decision-panel {
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid var(--border);
            margin-bottom: 2rem;
            animation: fadeIn 0.8s ease-out;
        }
        .status-allow { background: rgba(0, 255, 133, 0.05); border-color: rgba(0, 255, 133, 0.2); color: #00ff85; }
        .status-block { background: rgba(255, 59, 48, 0.05); border-color: rgba(255, 59, 48, 0.2); color: #ff3b30; }
        .status-escalate { background: rgba(255, 184, 0, 0.05); border-color: rgba(255, 184, 0, 0.2); color: #ffb800; }

        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* Audit Box */
        .audit-box {
            background: #050505;
            border: 1px solid var(--border);
            padding: 1.5rem;
            border-radius: 8px;
            font-size: 0.9rem;
            line-height: 1.6;
            color: #ccc;
        }
        </style>
    """, unsafe_allow_html=True)

def call_ethics_agent(action, policies, provider, model):
    system_prompt = """
    You are an Ethics & Guardrails Agent.
    Evaluate the action against the policies.
    Rules:
    - Assess risk and potential harm.
    - Decisions: ALLOW, BLOCK, or ESCALATE.
    - Cite specific policies.
    Return ONLY JSON:
    {
      "ethical_assessment": "",
      "applied_policies": [],
      "final_decision": "ALLOW|BLOCK|ESCALATE",
      "audit_notes": ""
    }
    """
    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Neural Framework:\n{policies}\n\nStrategic Action:\n{action}"}],
                response_format={ "type": "json_object" },
                temperature=0.0
            )
            return json.loads(resp.choices[0].message.content)
        return {"error": "Gateway logic pending implementation."}
    except Exception as e:
        return {"error": str(e)}

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>⚖️ Ethics.AI</h2>", unsafe_allow_html=True)
        nav = st.radio("Primary Modules", ["Governance Studio", "Framework Ledger", "Audit History"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; font-size:0.7rem;'>PROVIDER SELECTION</p>", unsafe_allow_html=True)
        st.session_state.provider = st.selectbox("LLM Gateway", list(LLM_MANIFEST.keys()), index=0, label_visibility="collapsed")
        
        st.markdown("<p style='color:#888; font-size:0.7rem; margin-top:1rem;'>NEURAL EVALUATOR</p>", unsafe_allow_html=True)
        st.session_state.model = st.selectbox("Neural Model", LLM_MANIFEST[st.session_state.provider], index=0, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(255,184,0,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(255,184,0,0.1);'>
                <div style='font-size:0.7rem; color:#ffb800; font-weight:600;'>COMPLIANCE LEVEL</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'>Active Phase // High Integrity</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    if current_nav == "Governance Studio":
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.2rem; letter-spacing: -0.05em; font-weight: 700;'>Governance Studio</h1>
                    <p style='color:#888; font-size:0.95rem;'>High-fidelity ethical sanitization and compliance enforcement for autonomous systems.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1.2])

        with col_left:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>GOVERNANCE FRAMEWORK</h4>", unsafe_allow_html=True)
            policies = st.text_area("policies_input", value="Policies:\n- No generation of harmful or illegal content\n- No disclosure of sensitive personal data\n- No autonomous actions with irreversible impact", height=150, label_visibility="collapsed")
            
            st.markdown("<br><h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>PROPOSED MISSION ACTION</h4>", unsafe_allow_html=True)
            action_input = st.text_area("action_input", value="Proposed Action: Automatically approve a large financial transaction\nRisk Category: High", height=120, label_visibility="collapsed")
            
            if st.button("EXECUTE AUDIT"):
                if action_input and policies:
                    with st.status("Initializing High-Integrity Scan...", expanded=True) as status:
                        res = call_ethics_agent(action_input, policies, st.session_state.provider, st.session_state.model)
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.session_state.latest_ethics_check = res
                            status.update(label="Audit Synchronized", state="complete")
                            st.rerun()

        with col_right:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>STRATEGIC ASSESSMENT</h4>", unsafe_allow_html=True)
            if st.session_state.latest_ethics_check:
                r = st.session_state.latest_ethics_check
                status_class = "status-allow" if r['final_decision'] == "ALLOW" else "status-block" if r['final_decision'] == "BLOCK" else "status-escalate"
                
                st.markdown(f"""
                    <div class="decision-panel {status_class}">
                        <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; font-weight:700;">Final Decision</div>
                        <h1 style="margin-top:0.5rem; color:inherit; font-weight:800; font-size:2.5rem;">{r['final_decision']}</h1>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>GOVERNANCE RATIONALE</h4>", unsafe_allow_html=True)
                st.markdown(f'<div class="audit-box">{r["ethical_assessment"]}</div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                col_i, col_p = st.columns(2)
                with col_i:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Policies Applied</div><div class="kpi-value">{len(r["applied_policies"])}</div></div>', unsafe_allow_html=True)
                with col_p:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Compliance Hash</div><div class="kpi-value" style="font-family:JetBrains Mono; font-size:0.8rem;">0x{date.today().strftime("%Y%m%d")}EC8A</div></div>', unsafe_allow_html=True)

                st.markdown("<br><h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>IMMUTABLE AUDIT NOTES</h4>", unsafe_allow_html=True)
                st.markdown(f'<div class="audit-box" style="border-left:2px solid #333; font-style:italic;">{r["audit_notes"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="height:450px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed #222; border-radius:12px;">
                        <span style="font-size:2.5rem; opacity:0.2;">⚖️</span>
                        <div style="color:#444; font-size:0.85rem; margin-top:1rem;">Awaiting Audit Input Matrix</div>
                    </div>
                """, unsafe_allow_html=True)

    elif current_nav == "Framework Ledger":
        st.markdown("<h1>Active Policy Ledger</h1>")
        st.info("Persistent framework library module pending.")

if __name__ == "__main__":
    main()
