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
    page_title="Persona | Neural Identity Matrix",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if 'latest_persona_response' not in st.session_state:
    st.session_state.latest_persona_response = None

# --- Providers & Models Mappings ---
LLM_MANIFEST = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
    "Google Gemini": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    "xAI Grok": ["grok-2", "grok-beta"]
}

# --- Predefined Personas ---
PERSONAS = {
    "Senior PM": "Role: Senior Product Manager\nTone: Clear, pragmatic, business-focused\nValues: User impact, feasibility, clarity\nConstraints: Avoid speculation, no marketing hype.",
    "Data Scientist": "Role: Expert Data Scientist\nTone: Analytical, skeptical, precise\nValues: Statistical significance, model explainability, rigor\nConstraints: Mention confidence intervals, cite data limitations.",
    "UX Architect": "Role: Senior UX Architect\nTone: Empathic, visual-centric, user-first\nValues: Accessibility, user flow optimization, aesthetic consistency\nConstraints: Focus on cognitive load, avoid purely technical jargon."
}

# --- SaaS Premium UI (Vercel Style) ---
def inject_premium_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --bg-main: #000000;
            --bg-card: #0a0a0a;
            --accent: #50e3c2; /* Identity Cyan */
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

        /* Persona Chip */
        .persona-chip {
            background: rgba(80, 227, 194, 0.05);
            border: 1px solid rgba(80, 227, 194, 0.2);
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.8rem;
            color: #50e3c2;
            margin-right: 10px;
            margin-bottom: 10px;
            display: inline-block;
        }

        /* Identity Output Box */
        .identity-box {
            background: #050505;
            border: 1px solid var(--border);
            padding: 2.5rem;
            margin: 1.5rem 0;
            border-radius: 12px;
            border-left: 4px solid var(--accent);
            animation: slideIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #111; border-radius: 10px; }

        </style>
    """, unsafe_allow_html=True)

def call_persona_agent(user_input, persona_spec, provider, model):
    system_prompt = """
    You are a Persona-Driven Agent.
    Rules:
    - Strictly adhere to the provided persona in all responses.
    - Maintain consistent tone, values, and constraints as defined.
    - Do NOT express personal opinions or deviate from the role.
    Return ONLY JSON:
    {
      "persona_response": "",
      "persona_used": ""
    }
    """
    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Neural Persona Definition:\n{persona_spec}\n\nRequest:\n{user_input}"}],
                response_format={ "type": "json_object" },
                temperature=0.3
            )
            return json.loads(resp.choices[0].message.content)
        # Placeholder for other providers
        return {"error": "Multi-provider logic implementation pending."}
    except Exception as e:
        return {"error": str(e)}

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>🎭 Identity.AI</h2>", unsafe_allow_html=True)
        nav = st.radio("Primary Modules", ["Identity Studio", "Persona Forge", "Settings"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; font-size:0.7rem;'>PROVIDER SELECTION</p>", unsafe_allow_html=True)
        st.session_state.provider = st.selectbox("LLM Gateway", list(LLM_MANIFEST.keys()), index=0, label_visibility="collapsed")
        
        st.markdown("<p style='color:#888; font-size:0.7rem; margin-top:1rem;'>NEURAL ENGINE</p>", unsafe_allow_html=True)
        st.session_state.model = st.selectbox("Neural Model", LLM_MANIFEST[st.session_state.provider], index=0, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(80,227,194,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(80,227,194,0.1);'>
                <div style='font-size:0.7rem; color:#50e3c2; font-weight:600;'>INTERNAL MATRIX</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'>Active Role // Persistent</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    if current_nav == "Identity Studio":
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.2rem; letter-spacing: -0.05em; font-weight: 700;'>Identity Studio</h1>
                    <p style='color:#888; font-size:0.95rem;'>Project multi-agent intelligence through highly specialized corporate personas.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>PERSONA DEFINITION</h4>", unsafe_allow_html=True)
            sel_persona = st.selectbox("Select Core Identity", list(PERSONAS.keys()), index=0)
            persona_spec = st.text_area("persona_spec", value=PERSONAS[sel_persona], height=180, label_visibility="collapsed")
            
            st.markdown("<br><h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>MISSION INPUT</h4>", unsafe_allow_html=True)
            text_input = st.text_area("neural_input", placeholder="Define the problem space for the persona...", height=150, label_visibility="collapsed")
            
            if st.button("SYNCHRONIZE IDENTITY"):
                if text_input:
                    with st.status("Initializing Role Matrix...", expanded=True) as status:
                        res = call_persona_agent(text_input, persona_spec, st.session_state.provider, st.session_state.model)
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.session_state.latest_persona_response = res
                            status.update(label="Identity Synced", state="complete")
                            st.rerun()

        with col_right:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>ROLE-ALIGNED OUTPUT</h4>", unsafe_allow_html=True)
            if st.session_state.latest_persona_response:
                r = st.session_state.latest_persona_response
                st.markdown(f"""
                    <div class="identity-box">
                        <div style="font-size:0.75rem; color:#50e3c2; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;">Neural Projection: {r['persona_used']}</div>
                        <div style="font-size:1.15rem; line-height:1.7; color:#eee; font-weight:400;">{r['persona_response']}</div>
                        
                        <div style="margin-top:2rem; display:flex; flex-wrap:wrap;">
                            <span class="persona-chip">Role-Aligned</span>
                            <span class="persona-chip">Zero Speculation</span>
                            <span class="persona-chip">Enterprise Ready</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="height:450px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed #222; border-radius:12px;">
                        <span style="font-size:2.5rem; opacity:0.2;">🎭</span>
                        <div style="color:#444; font-size:0.85rem; margin-top:1rem;">Awaiting Identity Signal</div>
                    </div>
                """, unsafe_allow_html=True)

    elif current_nav == "Persona Forge":
        st.markdown("<h1>Persona Forge</h1>")
        st.info("Custom identity design tools pending module integration.")

if __name__ == "__main__":
    main()
