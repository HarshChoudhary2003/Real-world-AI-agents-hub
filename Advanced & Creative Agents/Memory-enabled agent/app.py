import streamlit as st
import json
import os
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
    page_title="Neural Memory | Persistent Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if 'latest_response' not in st.session_state:
    st.session_state.latest_response = None

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
            --accent: #5e5ce6; /* Neural Purple */
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

        /* Memory Chip */
        .memory-chip {
            background: rgba(94, 92, 230, 0.05);
            border: 1px solid rgba(94, 92, 230, 0.2);
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.8rem;
            color: #5e5ce6;
            margin-right: 10px;
            margin-bottom: 10px;
            display: inline-block;
        }

        /* Interaction Card */
        .interaction-card {
            background: #050505;
            border: 1px solid var(--border);
            padding: 2rem;
            margin: 1.5rem 0;
            border-radius: 12px;
            border-left: 4px solid var(--accent);
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #111; border-radius: 10px; }

        </style>
    """, unsafe_allow_html=True)

def call_memory_agent(text_input, memory_store, provider, model):
    system_prompt = """
    You are a Memory-Enabled Agent.
    Rules:
    - Use stored context to personalize responses.
    - Update memory selectively with new facts or interaction summaries.
    - Be concise and efficient.
    Return ONLY JSON:
    {
      "response": "",
      "memory_used": [],
      "memory_updates": []
    }
    """
    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Neural Memory Context: {json.dumps(memory_store)}\n\nInput: {text_input}"}],
                response_format={ "type": "json_object" },
                temperature=0.3
            )
            return json.loads(resp.choices[0].message.content)
        # Add Gemini/Grok logic as needed or use a mock for demo
        return {"error": "Provider logic pending implementation."}
    except Exception as e:
        return {"error": str(e)}

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>🧠 Neural.AI</h2>", unsafe_allow_html=True)
        nav = st.radio("Primary Modules", ["Conversation Studio", "Neural Context Vault", "Settings"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; font-size:0.7rem;'>PROVIDER SELECTION</p>", unsafe_allow_html=True)
        st.session_state.provider = st.selectbox("Provider", list(LLM_MANIFEST.keys()), index=0, label_visibility="collapsed")
        
        st.markdown("<p style='color:#888; font-size:0.7rem; margin-top:1rem;'>NEURAL ENGINE</p>", unsafe_allow_html=True)
        st.session_state.model = st.selectbox("Model", LLM_MANIFEST[st.session_state.provider], index=0, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(94,92,230,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(94,92,230,0.1);'>
                <div style='font-size:0.7rem; color:#5e5ce6; font-weight:600;'>INTERNAL MEMORY</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'>Active State // Persistent</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    # Shared Memory Persistence Setup
    base_path = os.path.dirname(__file__)
    memory_path = os.path.join(base_path, "memory.json")
    try:
        with open(memory_path, "r", encoding="utf-8") as f:
            memory_store = json.load(f)
    except:
        memory_store = {"facts": [], "interactions": []}

    if current_nav == "Conversation Studio":
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.2rem; letter-spacing: -0.05em; font-weight: 700;'>Neural Studio</h1>
                    <p style='color:#888; font-size:0.95rem;'>Engage with the persistent intelligence swarm.</p>
                </div>
                <div style='text-align:right'>
                    <div style='color:#888; font-size:0.75rem; margin-bottom:4px;'>FACTS REMEMBERED</div>
                    <div style='color:white; font-size:1.1rem; font-weight:700;'>{len(memory_store['facts']) + len(memory_store['interactions'])}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>INPUT PIPELINE</h4>", unsafe_allow_html=True)
            text_input = st.text_area("neural_input", placeholder="Share something new or ask about previous context...", height=250, label_visibility="collapsed")
            
            if st.button("SYNCHRONIZE INTELLIGENCE"):
                if text_input:
                    with st.status("Accessing Long-term Memory...", expanded=True) as status:
                        res = call_memory_agent(text_input, memory_store, st.session_state.provider, st.session_state.model)
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.session_state.latest_response = res
                            # Persist Updates
                            if res.get("memory_updates"):
                                memory_store["interactions"].extend(res["memory_updates"])
                                memory_store["interactions"] = memory_store["interactions"][-20:]
                                with open(memory_path, "w", encoding="utf-8") as f:
                                    json.dump(memory_store, f, indent=2)
                            status.update(label="Intelligence Synced", state="complete")
                            st.rerun()

        with col_right:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>INTELLIGENCE OUTPUT</h4>", unsafe_allow_html=True)
            if st.session_state.latest_response:
                r = st.session_state.latest_response
                st.markdown(f"""
                    <div class="interaction-card">
                        <div style="font-size:0.75rem; color:#5e5ce6; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;">Neural Core Response</div>
                        <div style="font-size:1.1rem; line-height:1.7; color:#eee;">{r['response']}</div>
                        
                        <div style="margin-top:2rem;">
                            <div style="font-size:0.7rem; color:#888; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.5rem;">Memories Accessed</div>
                            {" ".join([f'<span class="memory-chip">{m}</span>' for m in r['memory_used']]) if r['memory_used'] else '<div style="color:#444; font-size:0.8rem italic;">No direct memory access required.</div>'}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="height:350px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed #222; border-radius:12px;">
                        <span style="font-size:2.5rem; opacity:0.2;">🧠</span>
                        <div style="color:#444; font-size:0.85rem; margin-top:1rem;">Awaiting Neural Signal</div>
                    </div>
                """, unsafe_allow_html=True)

    elif current_nav == "Neural Context Vault":
        st.markdown("<h1>Neural Context Vault</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;'>Explore and audit the agent's long-term persistent memory store.</p>", unsafe_allow_html=True)
        
        if memory_store['interactions']:
            for i, item in enumerate(reversed(memory_store['interactions'])):
                st.markdown(f"""<div class="interaction-card" style="margin-bottom:10px; padding:1.2rem;"><div style="color:#5e5ce6; font-size:0.75rem; font-weight:600;">RECORD {len(memory_store['interactions'])-i}</div><div style="color:#eee; font-size:0.9rem; margin-top:4px;">{item}</div></div>""", unsafe_allow_html=True)
        else:
            st.info("Neural vault is currently empty.")

    elif current_nav == "Settings":
        st.markdown("<h1>System Settings</h1>", unsafe_allow_html=True)
        if st.button("Wipe Global Memory Store"):
            with open(memory_path, "w", encoding="utf-8") as f:
                json.dump({"facts": [], "interactions": []}, f, indent=2)
            st.success("Universal Memory Reset Complete.")

if __name__ == "__main__":
    main()
