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
    page_title="Decision Engine | Autonomous Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if 'latest_decision' not in st.session_state:
    st.session_state.latest_decision = None

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
            --accent: #ff4b4b; /* Decision Red/Accent */
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

        /* Decision Badge */
        .decision-badge {
            background: #ff4b4b;
            color: white;
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 1rem;
        }

        /* Result Animation */
        .result-box {
            background: #050505;
            border-left: 3px solid var(--accent);
            padding: 2rem;
            margin: 1.5rem 0;
            border-radius: 0 12px 12px 0;
            animation: slideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes slideIn { from { opacity:0; transform:translateX(-20px); } to { opacity:1; transform:translateX(0); } }
        
        .rationale-text { font-size: 1rem; line-height: 1.6; color: #ccc; margin-top: 1rem; }
        .rule-item { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #888; margin-top: 0.2rem; }

        </style>
    """, unsafe_allow_html=True)

def call_decision_engine(context, provider, model):
    system_prompt = """
    You are an Autonomous Decision Agent.
    Rules:
    - Select actions based on goals and constraints
    - Explain decision rationale
    - Be deterministic and safe
    - Do NOT request human approval
    Return ONLY valid JSON with this schema:
    {
      "selected_action": "",
      "decision_rationale": "",
      "applied_rules": [],
      "risk_indicator": "High|Medium|Low"
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
        
        elif provider == "Google Gemini":
            genai.configure(api_key=GEMINI_API_KEY)
            gem_model = genai.GenerativeModel(model)
            resp = gem_model.generate_content(f"{system_prompt}\n\nContext: {context}")
            # Clean JSON from response text
            text = resp.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            return json.loads(text)
            
        elif provider == "xAI Grok":
            client = OpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": context}],
                temperature=0.0
            )
            return json.loads(resp.choices[0].message.content)
            
        return {"error": "Unknown provider"}
    except Exception as e:
        return {"error": str(e)}

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>🧠 Decision.AI</h2>", unsafe_allow_html=True)
        nav = st.radio("Primary Modules", ["Decision Studio", "Inference Metrics", "Credentials"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; font-size:0.7rem;'>PROVIDER SELECTION</p>", unsafe_allow_html=True)
        st.session_state.provider = st.selectbox("Provider", list(LLM_MANIFEST.keys()), index=0, label_visibility="collapsed")
        
        st.markdown("<p style='color:#888; font-size:0.7rem; margin-top:1rem;'>NEURAL ENGINE</p>", unsafe_allow_html=True)
        st.session_state.model = st.selectbox("Model", LLM_MANIFEST[st.session_state.provider], index=0, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(255,75,75,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(255,75,75,0.1);'>
                <div style='font-size:0.7rem; color:#ff4b4b; font-weight:600;'>NODE STATUS</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'>Active // {st.session_state.model}</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    if current_nav == "Decision Studio":
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.2rem; letter-spacing: -0.05em; font-weight: 700;'>Decision Studio</h1>
                    <p style='color:#888; font-size:0.95rem;'>Compute deterministic actions based on complex contextual input.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_in, col_spacer, col_out = st.columns([1, 0.08, 1.4])

        with col_in:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>CONTEXTUAL INPUT</h4>", unsafe_allow_html=True)
            context = st.text_area("context_input", value="Context: Server CPU usage at 85%\nGoal: Maintain system stability\nRules:\n- If CPU > 80%, scale resources\n- If CPU < 50%, reduce resources\nAvailable Actions:\n- Scale up\n- Scale down\n- Take no action", height=250, label_visibility="collapsed")
            
            if st.button("RUN INFERENCE"):
                if context:
                    with st.status("Computing Optimal Action...", expanded=True) as status:
                        decision = call_decision_engine(context, st.session_state.provider, st.session_state.model)
                        if "error" in decision:
                            st.error(decision["error"])
                        else:
                            st.session_state.latest_decision = decision
                            status.update(label="Inference Complete", state="complete")
                else:
                    st.warning("Context parameters required.")

        with col_out:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>INFERENCE RESULT</h4>", unsafe_allow_html=True)
            
            if st.session_state.latest_decision:
                d = st.session_state.latest_decision
                st.markdown(f"""
                    <div class="result-box">
                        <span class="decision-badge">SELECTED ACTION</span>
                        <h2 style='font-size: 2.5rem; font-weight: 700; color: white;'>{d['selected_action']}</h2>
                        
                        <div style='margin-top:2rem;'>
                            <div style='font-size:0.7rem; color:#ff4b4b; font-weight:600; letter-spacing:0.1em;'>RATIONALE</div>
                            <div class="rationale-text">{d['decision_rationale']}</div>
                        </div>

                        <div style='margin-top:2rem;'>
                            <div style='font-size:0.7rem; color:#888; font-weight:600; letter-spacing:0.1em; margin-bottom:0.5rem;'>GOVERNANCE RULES APPLIED</div>
                            {" ".join([f'<div class="rule-item">↳ {r}</div>' for r in d['applied_rules']])}
                        </div>
                        
                        <div style='margin-top:2rem; display:flex; gap:20px;'>
                            <div>
                                <div style='font-size:0.7rem; color:#888; font-weight:600; letter-spacing:0.1em;'>RISK INDEX</div>
                                <div style='font-size:1.1rem; color:{"#ff4b4b" if d["risk_indicator"] == "High" else "#ffcc00" if d["risk_indicator"] == "Medium" else "#00ff85"}; font-weight:700;'>{d['risk_indicator']}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="height:400px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed #222; border-radius:12px;">
                        <span style="font-size:2.5rem; opacity:0.2;">⚙️</span>
                        <div style="color:#444; font-size:0.85rem; margin-top:1rem;">Awaiting Context Signal</div>
                    </div>
                """, unsafe_allow_html=True)

    elif current_nav == "Credentials":
        st.markdown("<h1>System Credentials</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;'>Securely manage your API gateways.</p>", unsafe_allow_html=True)
        openai_key = st.text_input("OpenAI API Key", value=OPENAI_API_KEY if OPENAI_API_KEY else "", type="password")
        gemini_key = st.text_input("Gemini API Key", value=GEMINI_API_KEY if GEMINI_API_KEY else "", type="password")
        xai_key = st.text_input("xAI Grok API Key", value=XAI_API_KEY if XAI_API_KEY else "", type="password")
        if st.button("Update Keys"):
            st.success("Credentials Updated Locally")

if __name__ == "__main__":
    main()
