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
    page_title="Governance | Human-in-the-Loop",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if 'pending_approval' not in st.session_state:
    st.session_state.pending_approval = None
if 'approval_history' not in st.session_state:
    st.session_state.approval_history = []

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
            --accent: #5e5ce6; /* Governance Purple */
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

        /* Approval Box */
        .approval-box {
            background: #050505;
            border: 1px solid var(--border);
            padding: 2.5rem;
            margin: 1.5rem 0;
            border-radius: 16px;
            animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes slideUp { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
        
        .request-text { font-size: 1.2rem; line-height: 1.6; color: white; font-weight: 500; margin-bottom: 2rem; }
        .risk-badge { 
            display: inline-block; 
            padding: 4px 12px; 
            border-radius: 50px; 
            font-size: 0.7rem; 
            font-weight: 700; 
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        /* Decision Buttons */
        .stButton>button[key*="approve"] {
            background: #ffffff !important;
            color: #000000 !important;
        }
        .stButton>button[key*="reject"] {
            background: transparent !important;
            border: 1px solid #ff3b30 !important;
            color: #ff3b30 !important;
        }

        </style>
    """, unsafe_allow_html=True)

def generate_approval_request(context, provider, model):
    system_prompt = """
    You are a Human-in-the-Loop Approval Agent.
    Rules:
    - Formulate a clean, formal approval request for a human.
    - Highlight key risks and required criteria.
    - Be professional and concise.
    Return ONLY JSON:
    {
      "approval_required": true,
      "approval_request": "",
      "proposed_action": "",
      "risk_level": "High|Medium|Low",
      "audit_notes": ""
    }
    """
    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": context}],
                response_format={ "type": "json_object" },
                temperature=0.0
            )
            return json.loads(resp.choices[0].message.content)
        # Add Gemini/Grok logic as needed or use a mock for demo
        return {"error": "Provider logic pending implementation."}
    except Exception as e:
        return {"error": str(e)}

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>⚖️ Governance.AI</h2>", unsafe_allow_html=True)
        nav = st.radio("Primary Modules", ["Approval Hub", "Audit Vault", "Credentials"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; font-size:0.7rem;'>PROVIDER SELECTION</p>", unsafe_allow_html=True)
        st.session_state.provider = st.selectbox("Provider", list(LLM_MANIFEST.keys()), index=0, label_visibility="collapsed")
        
        st.markdown("<p style='color:#888; font-size:0.7rem; margin-top:1rem;'>NEURAL ENGINE</p>", unsafe_allow_html=True)
        st.session_state.model = st.selectbox("Model", LLM_MANIFEST[st.session_state.provider], index=0, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(94,92,230,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(94,92,230,0.1);'>
                <div style='font-size:0.7rem; color:#5e5ce6; font-weight:600;'>NODE STATUS</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'>Active // {st.session_state.model}</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    if current_nav == "Approval Hub":
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.2rem; letter-spacing: -0.05em; font-weight: 700;'>Approval Hub</h1>
                    <p style='color:#888; font-size:0.95rem;'>Review and authorize production-level agentic maneuvers.</p>
                </div>
                <div style='text-align:right'>
                    <div style='color:#888; font-size:0.75rem; margin-bottom:4px;'>PENDING DECISIONS</div>
                    <div style='color:white; font-size:1.1rem; font-weight:700;'>{1 if st.session_state.pending_approval else 0}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_in, col_spacer, col_out = st.columns([1, 0.08, 1.4])

        with col_in:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>PROPOSAL INPUT</h4>", unsafe_allow_html=True)
            proposal = st.text_area("proposal_input", value="Proposed Action: Deploy new model to production\nRisk Level: High\nApproval Criteria:\n- Model performance validated\n- Bias checks completed\nApprover Role: AI Governance Lead", height=250, label_visibility="collapsed")
            
            if st.button("STAGE FOR REVIEW"):
                if proposal:
                    with st.status("Staging Proposal...", expanded=True) as status:
                        req = generate_approval_request(proposal, st.session_state.provider, st.session_state.model)
                        if "error" in req:
                            st.error(req["error"])
                        else:
                            st.session_state.pending_approval = req
                            status.update(label="Staging Complete", state="complete")
                            st.rerun()

        with col_out:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>DECISION CONSOLE</h4>", unsafe_allow_html=True)
            
            if st.session_state.pending_approval:
                p = st.session_state.pending_approval
                risk_color = "#ff3b30" if p["risk_level"] == "High" else "#ffcc00" if p["risk_level"] == "Medium" else "#50e3c2"
                
                st.markdown(f"""
                    <div class="approval-box">
                        <span class="risk-badge" style="background: {risk_color}22; color: {risk_color}; border: 1px solid {risk_color}44;">{p['risk_level']} RISK</span>
                        <div style="font-size:0.7rem; color:#888; font-weight:600; letter-spacing:0.1em; margin-bottom:0.5rem;">PROPOSED ACTION</div>
                        <div class="request-text">{p['proposed_action']}</div>
                        
                        <div style="font-size:0.7rem; color:#888; font-weight:600; letter-spacing:0.1em; margin-bottom:1rem;">FORMAL REQUEST</div>
                        <div style="font-size:0.95rem; line-height:1.7; color:#eee; margin-bottom:2rem;">{p['approval_request']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                c_app, c_rej, c_fill = st.columns([1, 1, 2])
                with c_app:
                    if st.button("AUTHORIZE", key="approve_btn"):
                        p["human_decision"] = "APPROVED"
                        p["final_status"] = "ENFORCED"
                        st.session_state.approval_history.append(p)
                        st.session_state.pending_approval = None
                        st.success("Decision Enforced: Mission Authorized.")
                        time.sleep(1)
                        st.rerun()
                with c_rej:
                    if st.button("REJECT", key="reject_btn"):
                        p["human_decision"] = "REJECTED"
                        p["final_status"] = "TERMINATED"
                        st.session_state.approval_history.append(p)
                        st.session_state.pending_approval = None
                        st.error("Decision Enforced: Mission Terminated.")
                        time.sleep(1)
                        st.rerun()
            else:
                st.markdown("""
                    <div style="height:400px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed #222; border-radius:12px;">
                        <span style="font-size:2.5rem; opacity:0.2;">⚖️</span>
                        <div style="color:#444; font-size:0.85rem; margin-top:1rem;">Awaiting Governance Signal</div>
                    </div>
                """, unsafe_allow_html=True)

    elif current_nav == "Audit Vault":
        st.markdown("<h1>Audit Vault</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;'>Immutable history of all human-authorized maneuvers.</p>", unsafe_allow_html=True)
        
        if st.session_state.approval_history:
            st.table(st.session_state.approval_history)
        else:
            st.info("No audit records found.")

    elif current_nav == "Credentials":
        st.markdown("<h1>System Credentials</h1>", unsafe_allow_html=True)
        openai_key = st.text_input("OpenAI API Key", value=OPENAI_API_KEY if OPENAI_API_KEY else "", type="password")
        if st.button("Update Keys"):
            st.success("Credentials Updated Locally")

if __name__ == "__main__":
    main()
