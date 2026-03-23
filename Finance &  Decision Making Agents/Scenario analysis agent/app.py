import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agent import analyze_scenarios, save_outputs
import os
import time

# Page Configuration
st.set_page_config(
    page_title="SimuForge | Neural Scenario Auditor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'context_files' not in st.session_state:
    st.session_state['context_files'] = ["scenario_input.txt"]

# --- JARVIS-INSPIRED CINEMATIC UI CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-deep: #020617;
        --bg-panel: rgba(15, 23, 42, 0.7);
        --accent-purple: #A855F7;
        --accent-cyan: #22D3EE;
        --accent-blue: #3B82F6;
        --accent-glow: rgba(168, 85, 247, 0.4);
        --text-bright: #F8FAFC;
        --text-dim: #94A3B8;
        --border-high: rgba(168, 85, 247, 0.2);
        --border-low: rgba(255, 255, 255, 0.05);
    }

    .stApp {
        background: radial-gradient(circle at top right, #312E81, #020617), url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        background-attachment: fixed;
        color: var(--text-bright);
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit Artifacts */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background-color: rgba(2, 6, 23, 0.95);
        border-right: 1px solid var(--border-high);
        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
    }

    /* JARVIS Header */
    .jarvis-header {
        position: relative;
        padding: 40px 0;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .jarvis-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: 4px;
        background: linear-gradient(90deg, #A855F7, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px var(--accent-glow);
        text-transform: uppercase;
    }

    /* Holographic Dashboard Card */
    .hologram-card {
        background: var(--bg-panel);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-high);
        border-radius: 20px;
        padding: 25px;
        position: relative;
        overflow: hidden;
        margin-bottom: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4), inset 0 0 20px rgba(168, 85, 247, 0.05);
    }
    
    .hologram-card::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(rgba(168, 85, 247, 0.02) 50%, transparent 50%),
                    linear-gradient(90deg, rgba(168, 85, 247, 0.02) 50%, transparent 50%);
        background-size: 4px 4px;
        pointer-events: none;
    }

    /* Message UI */
    .chat-bubble {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 3px solid var(--accent-purple);
        background: rgba(255,255,255,0.02);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* Thinking State Animation */
    .thinking-wave {
        display: flex;
        gap: 8px;
        justify-content: center;
        padding: 20px;
    }
    .wave-bar {
        width: 4px;
        height: 20px;
        background: var(--accent-purple);
        border-radius: 2px;
        box-shadow: 0 0 10px var(--accent-purple);
        animation: wave 1.2s infinite ease-in-out;
    }
    @keyframes wave {
        0%, 100% { transform: scaleY(0.4); opacity: 0.5; }
        50% { transform: scaleY(1.5); opacity: 1; }
    }

    .status-panel {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem;
        background: rgba(168, 85, 247, 0.1);
        color: #C084FC;
        padding: 8px 12px;
        border: 1px solid var(--border-high);
        border-radius: 4px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        background: #A855F7;
        border-radius: 50%;
        box-shadow: 0 0 10px #A855F7;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: JARVIS SYSTEMS ---
with st.sidebar:
    st.markdown(f"""
        <div style="padding: 20px 10px;">
           <div class="status-panel"><div class="status-dot"></div>NEURAL PROJECTION: ONLINE</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.selectbox("Active Core", ["SimuForge AI (Primary)", "Scenario Evaluator", "Risk Modeler"])
    st.markdown("---")
    
    st.markdown("### Strategic Config")
    hub = st.selectbox("Intelligence Hub", ["OpenAI", "Google", "Anthropic", "xAI"])
    model_mapping = {
        "OpenAI": ["gpt-4o", "o1-preview"],
        "Google": ["gemini-1.5-pro"],
        "Anthropic": ["claude-3-5-sonnet-20240620"],
        "xAI": ["grok-beta"]
    }
    selected_model = st.selectbox("Intelligence Core", model_mapping[hub])
    
    st.markdown("---")
    st.markdown("### Probabilistic Matrix")
    for f in st.session_state['context_files']:
        st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:8px; border-radius:8px; margin-bottom:5px; font-size:0.8rem;'>📡 {f}</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
st.markdown('<div class="jarvis-header"><h1 class="jarvis-title">SIMUFORGE PROJECTION INTERFACE</h1></div>', unsafe_allow_html=True)

col_viz, col_chat = st.columns([0.45, 0.55])

with col_viz:
    st.markdown('<div class="hologram-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:Orbitron; font-size:1.1rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px; color:#C084FC;'>SCENARIO CLOUD</h3>", unsafe_allow_html=True)
    
    if st.session_state['messages'] and 'data' in st.session_state['messages'][-1]:
        data = st.session_state['messages'][-1]['data']
        # Scenario Comparison Plotly
        scenarios = data.get('scenarios', [])
        df_viz = pd.DataFrame(scenarios)
        if not df_viz.empty:
            df_viz['revenue_num'] = df_viz['projected_revenue'].replace('[\$,]', '', regex=True).astype(float)
            fig = px.bar(df_viz, x="name", y="revenue_num", color="risk_level",
                        text="projected_revenue", color_discrete_sequence=['#A855F7', '#3B82F6', '#EF4444'],
                        labels={"revenue_num": "Projected Outcome ($)", "name": "Scenario"})
            fig.update_layout(
              paper_bgcolor='rgba(0,0,0,0)', 
              plot_bgcolor='rgba(0,0,0,0)', 
              font_color='white',
              margin=dict(t=20, b=20, l=20, r=20),
              height=350
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.markdown(f"""
                <div style="text-align:center; padding:15px; background:rgba(168, 85, 247, 0.05); border-radius:12px; border:1px solid rgba(168, 85, 247, 0.2);">
                    <div style="font-family:'Orbitron'; font-size:0.8rem; color:#A1A1AA;">RESILIENCE INDEX</div>
                    <div style="font-family:'Orbitron'; font-size:2.5rem; font-weight:900; color:#A855F7;">{data['durable_score']}/10</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("System stand-by. Initiate /project to generate the multi-scenario cloud.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Monitoring Signals Panel
    st.markdown('<div class="hologram-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:Orbitron; font-size:1.1rem; color:#F8FAFC;'>RADAR SIGNALS</h3>", unsafe_allow_html=True)
    if st.session_state['messages'] and 'data' in st.session_state['messages'][-1]:
        data = st.session_state['messages'][-1]['data']
        for sig in data['key_variables_tracked']:
            st.markdown(f"<div style='font-size:0.85rem; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.05);'>📡 {sig}</div>", unsafe_allow_html=True)
    else:
        st.write("Awaiting heuristic inputs for radar calibration.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_chat:
    chat_box = st.container(height=500, border=False)
    with chat_box:
        for m in st.session_state['messages']:
            role = "USER" if m['role'] == "user" else "SIMUFORGE"
            accent = "#312E81" if role == "USER" else "#A855F7"
            st.markdown(f"""
                <div class="chat-bubble">
                    <div style="font-family:'Orbitron'; font-size:0.75rem; color:{accent}; margin-bottom:8px;">{role} SESSION</div>
                    <div style="line-height:1.6; font-size:0.95rem;">{m['content']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if 'data' in m:
                with st.expander("Projection Implications", expanded=False):
                    for s in m['data']['scenarios']:
                        st.markdown(f"**{s['name']}**: {s['implications']}")
                    st.markdown("---")
                    st.markdown(f"**Strategic Readiness**: {m['data']['strategic_advice']}")

    user_input = st.chat_input("Enter Protocol (e.g., /project or 'evaluate bear case')")
    
    if user_input:
        st.session_state['messages'].append({"role": "user", "content": user_input})
        
        if user_input.startswith("/") or "project" in user_input.lower() or "scenario" in user_input.lower():
            # Trigger Thinking Animation
            with st.container():
                st.markdown('<div class="thinking-wave"><div class="wave-bar" style="animation-delay:0s"></div><div class="wave-bar" style="animation-delay:0.2s"></div><div class="wave-bar" style="animation-delay:0.4s"></div><div class="wave-bar" style="animation-delay:0.6s"></div></div>', unsafe_allow_html=True)
                time.sleep(1) # Simulate audit processing
                try:
                    with open("scenario_input.txt", "r") as f: context = f.read()
                    result = analyze_scenarios(context, model_name=selected_model)
                    save_outputs(result)
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": f"Projection matrix established. {result['analysis_overview']}",
                        "data": result
                    })
                except Exception as e:
                    st.session_state['messages'].append({"role": "assistant", "content": f"Neural projection failure: {str(e)}"})
        else:
            st.session_state['messages'].append({"role": "assistant", "content": "I am standing by. Command /project to trigger the multi-scenario neural cloud."})
        st.rerun()

# Global UI Polish
st.markdown("""
<style>
    .stChatFloatingInputContainer { background: transparent !important; padding-bottom: 20px; }
    .stChatInput { border: 1px solid var(--border-high) !important; background: rgba(15, 23, 42, 0.8) !important; color: white !important; }
</style>
""", unsafe_allow_html=True)
