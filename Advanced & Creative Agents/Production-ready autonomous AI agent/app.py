import streamlit as st
import json
import os
import time
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Page Config ---
st.set_page_config(
    page_title="Apex AI | Mission Control",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if 'provider' not in st.session_state:
    st.session_state.provider = "OpenAI"
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if 'latest_apex_decision' not in st.session_state:
    st.session_state.latest_apex_decision = None

# --- SaaS Premium UI (Apex Diamond Mode) ---
def inject_apex_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --bg-main: #020202;
            --bg-card: #0a0a10;
            --accent: #2e6ff2; /* Apex Blue */
            --border: #161625;
            --text-primary: #ffffff;
            --text-secondary: #71717a;
        }

        .main { background: var(--bg-main); color: var(--text-primary); }
        [data-testid="stSidebar"] { background-color: #050508; border-right: 1px solid var(--border); }
        [data-testid="stHeader"] { background: transparent; }
        footer { visibility: hidden; }
        .stDeployButton { display: none; }

        h1, h2, h3, p, span, div { font-family: 'Plus Jakarta Sans', sans-serif !important; }
        
        /* KPI Cards */
        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .kpi-card:hover { border-color: var(--accent); transform: translateY(-2px); }
        .kpi-label { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; margin-bottom: 0.5rem; }
        .kpi-value { font-size: 1.5rem; font-weight: 800; color: var(--text-primary); }

        /* Decision Hero */
        .decision-hero {
            background: linear-gradient(135deg, #0a0a10 0%, #050518 100%);
            border: 1px solid var(--border);
            padding: 3rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            border-left: 6px solid var(--accent);
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* Risk Badge */
        .risk-badge {
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .risk-low { color: #00ff85; border: 1px solid #00ff8522; background: #00ff8511; }
        .risk-medium { color: #ffb800; border: 1px solid #ffb80022; background: #ffb80011; }
        .risk-high { color: #f97316; border: 1px solid #f9731622; background: #f9731611; }
        .risk-critical { color: #ef4444; border: 1px solid #ef444422; background: #ef444411; }

        /* Tactical Log */
        .tactical-entry {
            border-bottom: 1px solid var(--border);
            padding: 1rem 0;
            font-size: 0.9rem;
        }
        .timestamp { font-family: 'JetBrains Mono'; font-size: 0.75rem; color: var(--text-secondary); }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-thumb { background: #161625; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

def call_apex_agent(objective, memory_store, provider, model):
    system_prompt = """
    You are a Production-Ready Autonomous AI Agent (Apex.AI).
    Rules:
    - Respect ethics, constraints, and provide deterministic decision logic.
    - Log all strategic maneuvers.
    - Use persistent memory context for cross-interaction alignment.
    Return ONLY JSON:
    {
      "decision": "",
      "rationale": "",
      "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
      "memory_update": ""
    }
    """
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Neural Memory Context:\n{json.dumps(memory_store)}\n\nObjective:\n{objective}"}],
            response_format={ "type": "json_object" },
            temperature=0.2
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

def main():
    inject_apex_css()
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>💎 Apex Studio</h2>", unsafe_allow_html=True)
        nav = st.radio("PRIMARY INTERFACE", ["Mission Control", "Neural Memory Store", "Tactical Logs"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#161625'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#71717a; font-size:0.7rem; font-weight:700;'>CONTROL PARAMETERS</p>", unsafe_allow_html=True)
        st.session_state.model = st.selectbox("Neural Engine", ["gpt-4o", "gpt-4o-mini"], index=1, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(46,111,242,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(46,111,242,0.1);'>
                <div style='font-size:0.75rem; color:#2e6ff2; font-weight:800; letter-spacing:0.05em;'>APEX STATUS</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.3rem;'>Active Protocol // Stage 100</div>
            </div>
        """, unsafe_allow_html=True)

    # Persistence Artifact Discovery
    base_path = os.path.dirname(__file__)
    memory_path = os.path.join(base_path, "memory.json")
    log_path = os.path.join(base_path, "log.json")
    
    try:
        with open(memory_path, "r", encoding="utf-8") as f:
            memory = json.load(f)
        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except:
        memory = {"past_decisions": [], "learned_constraints": []}
        logs = []

    if nav == "Mission Control":
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.6rem; letter-spacing: -0.06em; font-weight: 800;'>Mission Control.</h1>
                    <p style='color:#71717a; font-size:1.1rem;'>The ultimate culmination of the 100-Agent autonomous matrix.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_in, col_spacer, col_out = st.columns([1, 0.08, 1.4])

        with col_in:
            st.markdown("<h4 style='font-size:0.85rem; color:#71717a; margin-bottom:1.5rem; letter-spacing:0.1em; font-weight:700;'>MISSION OBJECTIVE</h4>", unsafe_allow_html=True)
            objective = st.text_area("mission_input", placeholder="Enter Strategic Directive...", height=300, label_visibility="collapsed")
            
            if st.button("ENGAGE APEX CORE", use_container_width=True):
                if objective:
                    with st.status("Initializing Production Subsystems...", expanded=True) as status:
                        res = call_apex_agent(objective, memory, "OpenAI", st.session_state.model)
                        if "error" in res:
                            st.error(res["error"])
                        else:
                            st.session_state.latest_apex_decision = res
                            # Persist Updates
                            memory["past_decisions"].append(res["decision"])
                            if res.get("memory_update"):
                                memory["learned_constraints"].append(res["memory_update"])
                            with open(memory_path, "w", encoding="utf-8") as f:
                                json.dump(memory, f, indent=2)
                            
                            logs.insert(0, {"timestamp": datetime.utcnow().isoformat(), "decision": res})
                            with open(log_path, "w", encoding="utf-8") as f:
                                json.dump(logs[:100], f, indent=2)
                                
                            status.update(label="Autonomous Decision Synchronized", state="complete")
                            st.rerun()

        with col_out:
            if st.session_state.latest_apex_decision:
                r = st.session_state.latest_apex_decision
                risk_tag = f"<span class='risk-badge risk-{r['risk_level'].lower()}'>{r['risk_level']}</span>"
                
                st.markdown(f"""
                    <div class="decision-hero">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;">
                            <div style="font-size:0.8rem; color:#2e6ff2; font-weight:800; text-transform:uppercase; letter-spacing:0.15em;">Strategic Decision</div>
                            {risk_tag}
                        </div>
                        <h2 style="font-size:2.2rem; font-weight:800; line-height:1.1; margin-bottom:1.5rem;">{r['decision']}</h2>
                        <p style="color:#a1a1aa; font-size:1.1rem; line-height:1.6; border-top: 1px solid #ffffff11; padding-top:1.5rem;">{r['rationale']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                col_m, col_l = st.columns(2)
                with col_m:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Neural Memory Update</div><div class="kpi-value" style="font-size:0.95rem; font-weight:500; color:#71717a;">{r["memory_update"] if r["memory_update"] else "No updates required."}</div></div>', unsafe_allow_html=True)
                with col_l:
                    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Autonomous Health</div><div class="kpi-value">99.98%</div></div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="height:550px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed #ffffff11; border-radius:24px;">
                        <span style="font-size:3rem; opacity:0.15;">💎</span>
                        <div style="color:#3f3f46; font-size:0.95rem; margin-top:1.5rem; letter-spacing:0.05em; font-weight:600;">Awaiting APEX Synchronization</div>
                    </div>
                """, unsafe_allow_html=True)

    elif nav == "Neural Memory Store":
        st.markdown("<h1 style='font-size:2.5rem; font-weight:800;'>Neural Vault.</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Decision History", "Learned Governance"])
        with tab1:
            for d in reversed(memory['past_decisions']):
                st.markdown(f"<div class='tactical-entry' style='padding:1.5rem; border: 1px solid #161625; border-radius:12px; margin-bottom:10px;'>{d}</div>", unsafe_allow_html=True)
        with tab2:
            for c in reversed(memory['learned_constraints']):
                st.markdown(f"<div class='tactical-entry' style='padding:1.5rem; border: 1px solid #161625; border-radius:12px; margin-bottom:10px; color:#ffb800;'>{c}</div>", unsafe_allow_html=True)

    elif nav == "Tactical Logs":
        st.markdown("<h1 style='font-size:2.5rem; font-weight:800;'>Tactical Logs.</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for log in logs:
            st.markdown(f"""
                <div class="tactical-entry" style='background:rgba(255,255,255,0.02); padding:1.2rem; border-radius:12px; margin-bottom:10px;'>
                    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                        <span class="timestamp">{log['timestamp']}</span>
                        <span class='risk-badge risk-{log['decision']['risk_level'].lower()}'>{log['decision']['risk_level']}</span>
                    </div>
                    <div style="font-weight:700; font-size:1.1rem;">{log['decision']['decision']}</div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
