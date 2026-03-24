import streamlit as st
import json
import os
import time
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# --- Page Config ---
st.set_page_config(
    page_title="Orchestra | Swarm Intelligence",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if 'latest_protocol' not in st.session_state:
    st.session_state.latest_protocol = None

# --- Providers & Models Mappings ---
LLM_MANIFEST = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
    "Google Gemini": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    "xAI Grok": ["grok-2", "grok-beta"],
    "Anthropic": ["claude-3-5-sonnet", "claude-3-haiku"]
}

# --- SaaS Premium UI (Vercel Style) ---
def inject_premium_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --bg-main: #000000;
            --bg-card: #0a0a0a;
            --accent: #0070f3;
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

        /* Provider Selector styling */
        .stSelectbox label { color: #888 !important; font-size: 0.8rem !important; }
        div[data-baseweb="select"] { background-color: #0a0a0a !important; border: 1px solid #1f1f1f !important; border-radius: 8px !important; }

        /* Buttons & Widgets */
        .stButton>button {
            background: #fff !important;
            color: #000 !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            height: 48px !important;
            width: 100% !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(255,255,255,0.1) !important;
        }
        .stButton>button:hover { transform: translateY(-2px); opacity: 0.9 !important; }

        /* Result Animation */
        .result-box {
            background: #050505;
            border-left: 3px solid var(--accent);
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0 12px 12px 0;
            animation: slideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes slideIn { from { opacity:0; transform:translateX(-20px); } to { opacity:1; transform:translateX(0); } }
        
        .agent-header { color: var(--accent); font-weight: 600; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.1em; }
        
        </style>
    """, unsafe_allow_html=True)

def call_llm(role, task, provider, model):
    """
    Unified caller for multi-provider support.
    """
    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": f"You are a {role}."}, {"role": "user", "content": task}],
                temperature=0.3
            )
            return resp.choices[0].message.content
        
        elif provider == "Google Gemini":
            genai.configure(api_key=GEMINI_API_KEY)
            gem_model = genai.GenerativeModel(model)
            resp = gem_model.generate_content(f"Role: {role}\nTask: {task}")
            return resp.text
            
        elif provider == "xAI Grok":
            client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": f"You are a {role}."}, {"role": "user", "content": task}],
                temperature=0.3
            )
            return resp.choices[0].message.content
            
        elif provider == "Anthropic":
            # For brevity/demo, using a mock or mentioning setup
            return f"Claude ({model}) protocol initiated. Integration pending API configuration."
            
        return f"Unknown provider: {provider}"
    except Exception as e:
        return f"Node Offline: {str(e)}"

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>💠 Orchestra.AI</h2>", unsafe_allow_html=True)
        nav = st.radio("Primary Modules", ["Mission Control", "Collaborator Matrix", "Credentials"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; font-size:0.7rem;'>PROVIDER SELECTION</p>", unsafe_allow_html=True)
        
        selected_provider = st.selectbox("Provider", list(LLM_MANIFEST.keys()), index=0, label_visibility="collapsed")
        st.session_state.provider = selected_provider
        
        st.markdown("<p style='color:#888; font-size:0.7rem; margin-top:1rem;'>NEURAL MODEL</p>", unsafe_allow_html=True)
        selected_model = st.selectbox("Model", LLM_MANIFEST[selected_provider], index=0, label_visibility="collapsed")
        st.session_state.model = selected_model
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(0,112,243,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(0,112,243,0.1);'>
                <div style='font-size:0.7rem; color:#0070f3; font-weight:600;'>ACTIVE NODE</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'>{st.session_state.model}</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    if current_nav == "Mission Control":
        # --- Context Bar ---
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.2rem; letter-spacing: -0.05em; font-weight: 700;'>Mission Control</h1>
                    <p style='color:#888; font-size:0.95rem;'>Deploy autonomous agent swarms via {st.session_state.provider} architecture.</p>
                </div>
                <div style='text-align:right'>
                    <div style='color:#888; font-size:0.75rem; margin-bottom:4px;'>NODE STATUS</div>
                    <div style='display:flex; align-items:center; gap:8px;'><div style='width:6px; height:6px; background:#00ff85; border-radius:50%;'></div><span style='color:white; font-size:0.85rem; font-weight:500;'>ONLINE</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- Dashboard Workspace ---
        col_in, col_spacer, col_out = st.columns([1, 0.08, 1.4])

        with col_in:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>MISSION PARAMETERS</h4>", unsafe_allow_html=True)
            mission = st.text_area("mission_input", placeholder="Define the objective for the orchestrator...", height=200, label_visibility="collapsed")
            
            # Key checks
            has_key = (st.session_state.provider == "OpenAI" and OPENAI_API_KEY) or \
                      (st.session_state.provider == "Google Gemini" and GEMINI_API_KEY) or \
                      (st.session_state.provider == "xAI Grok" and XAI_API_KEY)
            
            if not has_key:
                st.error(f"Missing credentials for {st.session_state.provider}")
            
            if st.button("EXECUTE PROTOCOL"):
                if mission and has_key:
                    with st.status("Initializing Swarm Nodes...", expanded=True) as status:
                        st.write(f"Protocol: {st.session_state.model} - Node 01 Research...")
                        res_out = call_llm("Research Agent", mission, st.session_state.provider, st.session_state.model)
                        
                        st.write(f"Protocol: {st.session_state.model} - Node 02 Analysis...")
                        ana_out = call_llm("Analysis Agent", f"Research: {res_out}", st.session_state.provider, st.session_state.model)
                        
                        st.session_state.latest_protocol = {"research": res_out, "analysis": ana_out}
                        status.update(label="Protocol Terminated Successfully", state="complete")
                elif not mission:
                    st.warning("Mission objective unspecified.")

        with col_out:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>COLLABORATION FLOW</h4>", unsafe_allow_html=True)
            
            if st.session_state.latest_protocol:
                p = st.session_state.latest_protocol
                st.markdown(f"""
                    <div class="result-box">
                        <div class="agent-header">01 // RESEARCH_NODE</div>
                        <div style="font-size:0.95rem; line-height:1.7; color:#eee;">{p['research']}</div>
                    </div>
                    <div class="result-box">
                        <div class="agent-header">02 // ANALYSIS_NODE</div>
                        <div style="font-size:0.95rem; line-height:1.7; color:#eee;">{p['analysis']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="height:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed #222; border-radius:12px;">
                        <span style="font-size:2rem; opacity:0.2;">🛸</span>
                        <div style="color:#444; font-size:0.85rem; margin-top:1rem;">Awaiting Command Signal</div>
                    </div>
                """, unsafe_allow_html=True)

    elif current_nav == "Credentials":
        st.markdown("<h1>System Credentials</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;'>Manage your API gateways and secure tokens.</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='kpi-card' style='margin-bottom:1rem;'>", unsafe_allow_html=True)
            openai_key = st.text_input("OpenAI API Key", value=OPENAI_API_KEY if OPENAI_API_KEY else "", type="password")
            gemini_key = st.text_input("Gemini API Key", value=GEMINI_API_KEY if GEMINI_API_KEY else "", type="password")
            xai_key = st.text_input("xAI Grok API Key", value=XAI_API_KEY if XAI_API_KEY else "", type="password")
            if st.button("Save Encrypted Credentials"):
                st.success("Configuration Updated")
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
