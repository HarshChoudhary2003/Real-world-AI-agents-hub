import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agent import explain_report, save_outputs
import os
import time

# Page Configuration
st.set_page_config(
    page_title="FinLens | Neural Financial Auditor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'context_files' not in st.session_state:
    st.session_state['context_files'] = ["report_input.txt"]

# --- JARVIS-INSPIRED CINEMATIC UI CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-deep: #020617;
        --bg-panel: rgba(15, 23, 42, 0.7);
        --accent-cyan: #22D3EE;
        --accent-blue: #3B82F6;
        --accent-glow: rgba(34, 211, 238, 0.4);
        --text-bright: #F8FAFC;
        --text-dim: #94A3B8;
        --border-high: rgba(34, 211, 238, 0.2);
        --border-low: rgba(255, 255, 255, 0.05);
    }

    .stApp {
        background: radial-gradient(circle at top right, #1E1B4B, #020617), url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
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
        background: linear-gradient(90deg, #22D3EE, #3B82F6);
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
        box-shadow: 0 10px 40px rgba(0,0,0,0.4), inset 0 0 20px rgba(34, 211, 238, 0.05);
    }
    
    .hologram-card::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(rgba(34, 211, 238, 0.02) 50%, transparent 50%),
                    linear-gradient(90deg, rgba(34, 211, 238, 0.02) 50%, transparent 50%);
        background-size: 4px 4px;
        pointer-events: none;
    }

    /* Message UI */
    .chat-bubble {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 3px solid var(--accent-cyan);
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
        background: var(--accent-cyan);
        border-radius: 2px;
        box-shadow: 0 0 10px var(--accent-cyan);
        animation: wave 1.2s infinite ease-in-out;
    }
    @keyframes wave {
        0%, 100% { transform: scaleY(0.4); opacity: 0.5; }
        50% { transform: scaleY(1.5); opacity: 1; }
    }

    .rotating-arc {
        position: absolute;
        width: 100px;
        height: 100px;
        border: 2px solid var(--accent-cyan);
        border-bottom-color: transparent;
        border-right-color: transparent;
        border-radius: 50%;
        animation: rotate 4s linear infinite;
        opacity: 0.3;
    }
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: JARVIS SYSTEMS ---
with st.sidebar:
    st.markdown(f"""
        <div style="padding: 20px 10px;">
           <div style="font-family: 'Orbitron', sans-serif; font-size: 1.2rem; color: #34D399; margin-bottom: 5px;">SYSTEM STATUS</div>
           <div style="font-size: 0.8rem; color: #94A3B8;">NEURAL LINK: ESTABLISHED</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.selectbox("Active Protocol", ["FinLens AI (Primary)", "Risk Auditor", "Trend Analyst"])
    st.markdown("---")
    
    st.markdown("### Neural Config")
    hub = st.selectbox("Intelligence Hub", ["OpenAI", "Google", "Anthropic", "xAI"])
    model_mapping = {
        "OpenAI": ["gpt-4o", "o1-preview"],
        "Google": ["gemini-1.5-pro"],
        "Anthropic": ["claude-3-5-sonnet-20240620"],
        "xAI": ["grok-beta"]
    }
    selected_model = st.selectbox("Intelligence Core", model_mapping[hub])
    
    st.markdown("---")
    st.markdown("### Ingested Data")
    for f in st.session_state['context_files']:
        st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:8px; border-radius:8px; margin-bottom:5px; font-size:0.8rem;'>📂 {f}</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
st.markdown('<div class="jarvis-header"><h1 class="jarvis-title">FINLENS AUDIT INTERFACE</h1></div>', unsafe_allow_html=True)

col_viz, col_chat = st.columns([0.45, 0.55])

with col_viz:
    st.markdown('<div class="hologram-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:Orbitron; font-size:1.1rem; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;'>HEURISTIC ANALYSIS</h3>", unsafe_allow_html=True)
    
    # Placeholder Heuristic Radar or Metrics
    if st.session_state['messages'] and 'data' in st.session_state['messages'][-1]:
        data = st.session_state['messages'][-1]['data']
        metrics = data.get('key_metrics', [])
        
        # Circular Visualization using Plotly
        categories = [m['label'] for m in metrics]
        values = [float(m['value'].replace('$','').replace(',','').replace('%','')) for m in metrics]
        
        fig = go.Figure(data=go.Scatterpolar(
          r=values,
          theta=categories,
          fill='toself',
          line_color='#22D3EE'
        ))
        fig.update_layout(
          polar=dict(radialaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)'),
          showlegend=False,
          paper_bgcolor='rgba(0,0,0,0)',
          font_color='white',
          height=350,
          margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        for metric in metrics:
            st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:8px 0;">
                    <span style="color:#94A3B8; font-size:0.85rem;">{metric['label']}</span>
                    <span style="color:#22D3EE; font-weight:700;">{metric['value']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("System awaiting data ingestion. Initiate /audit to visualize heuristics.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System Status Panel
    st.markdown('<div class="hologram-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:Orbitron; font-size:1.1rem; color:#F8FAFC;'>RISK DIAGNOSTIC</h3>", unsafe_allow_html=True)
    if st.session_state['messages'] and 'data' in st.session_state['messages'][-1]:
        data = st.session_state['messages'][-1]['data']
        st.markdown(f"<p style='color:#EF4444; font-weight:600; font-size:0.9rem;'>⚠️ {data['risk_assessment']}</p>", unsafe_allow_html=True)
    else:
        st.write("Scan complete. No active risks detected in idle state.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_chat:
    chat_box = st.container(height=500, border=False)
    with chat_box:
        for m in st.session_state['messages']:
            role = "USER" if m['role'] == "user" else "FINLENS"
            accent = "#3B82F6" if role == "USER" else "#22D3EE"
            st.markdown(f"""
                <div class="chat-bubble">
                    <div style="font-family:'Orbitron'; font-size:0.75rem; color:{accent}; margin-bottom:8px;">{role} SESSION</div>
                    <div style="line-height:1.6; font-size:0.95rem;">{m['content']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if 'data' in m:
                with st.expander("Strategic Narrative Details", expanded=False):
                    st.write("**Notable Changes:**")
                    for n in m['data']['notable_changes']: st.write(f"• {n}")
                    st.write("**Business Implications:**")
                    for b in m['data']['business_implications']: st.write(f"• {b}")

    user_input = st.chat_input("Enter Command (e.g., /audit or 'explain expenses')")
    
    if user_input:
        st.session_state['messages'].append({"role": "user", "content": user_input})
        
        if user_input.startswith("/") or "explain" in user_input.lower() or "audit" in user_input.lower():
            # Trigger Thinking Animation
            with st.container():
                st.markdown('<div class="thinking-wave"><div class="wave-bar" style="animation-delay:0s"></div><div class="wave-bar" style="animation-delay:0.2s"></div><div class="wave-bar" style="animation-delay:0.4s"></div><div class="wave-bar" style="animation-delay:0.6s"></div></div>', unsafe_allow_html=True)
                time.sleep(1) # Simulate audit processing
                try:
                    with open("report_input.txt", "r") as f: context = f.read()
                    result = explain_report(context, model_name=selected_model)
                    save_outputs(result)
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": f"Audit complete. {result['summary']}",
                        "data": result
                    })
                except Exception as e:
                    st.session_state['messages'].append({"role": "assistant", "content": f"Neural audit failure: {str(e)}"})
        else:
            st.session_state['messages'].append({"role": "assistant", "content": "I am standing by. Command /audit to perform a heuristic financial sweep."})
        st.rerun()

# Global UI Polish
st.markdown("""
<style>
    .stChatFloatingInputContainer { background: transparent !important; padding-bottom: 20px; }
    .stChatInput { border: 1px solid var(--border-high) !important; background: rgba(15, 23, 42, 0.8) !important; color: white !important; }
</style>
""", unsafe_allow_html=True)
