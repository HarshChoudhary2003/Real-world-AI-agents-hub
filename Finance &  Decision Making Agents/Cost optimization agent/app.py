import streamlit as st
import json
import pandas as pd
import plotly.express as px
from agent import optimize_costs, save_outputs
import os
import time

# Page Configuration
st.set_page_config(
    page_title="OptiForge | Intelligent Cost Optimization",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'context_files' not in st.session_state:
    st.session_state['context_files'] = ["cost_input.txt"]

# --- NEXT-GEN AI INTERFACE CSS (DARK MODE DEFAULT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-editor: #0A0A0B;
        --bg-sidebar: #111113;
        --bg-chat-user: #1D1D1F;
        --accent: #FF5C00; /* Orange/Coral for cost/alert optimization */
        --text-headline: #FFFFFF;
        --text-body: #A1A1AA;
        --border: #27272A;
        --radius: 16px;
    }

    .stApp {
        background-color: var(--bg-editor);
        color: var(--text-body);
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit Artifacts */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border);
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 120px;
    }
    
    .message {
        display: flex;
        flex-direction: column;
        margin-bottom: 24px;
        animation: fadeIn 0.4s ease-out;
    }
    
    .message.user { align-items: flex-end; }
    
    .bubble {
        padding: 18px 22px;
        border-radius: var(--radius);
        max-width: 85%;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .user .bubble {
        background-color: var(--bg-chat-user);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .ai .bubble {
        background-color: transparent;
        color: var(--text-headline);
        padding-left: 0;
    }

    .agent-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 40px;
        padding: 20px;
        background: rgba(255,255,255,0.02);
        border-radius: var(--radius);
        border: 1px solid var(--border);
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #FF5C00;
        box-shadow: 0 0 10px #FF5C00;
    }

    .tool-card {
        background: #18181B;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-top: 12px;
        transition: all 0.2s ease;
    }
    .tool-card:hover { border-color: var(--accent); }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: AGENT MANAGEMENT ---
with st.sidebar:
    st.markdown("### Efficiency Agents")
    
    agents = [
        {"name": "OptiForge Pro", "status": "Active", "icon": "💸"},
        {"name": "Supply Auditor", "status": "Standby", "icon": "📦"}
    ]
    
    for agent in agents:
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:12px; margin-bottom:8px; background:{'rgba(255,92,0,0.1)' if agent['name'] == 'OptiForge Pro' else 'transparent'}; border-radius:12px; border:1px solid {'var(--accent)' if agent['name'] == 'OptiForge Pro' else 'transparent'};">
                <span style="font-size:1.2rem;">{agent['icon']}</span>
                <div style="flex:1;">
                    <div style="font-size:0.9rem; font-weight:600; color:{'white' if agent['name'] == 'OptiForge Pro' else '#A1A1AA'};">{agent['name']}</div>
                    <div style="font-size:0.75rem; color:{'#FF5C00' if agent['name'] == 'OptiForge Pro' else '#71717A'};">{agent['status']}</div>
                </div>
                {f'<div class="status-indicator"></div>' if agent['status'] == 'Active' else ''}
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    provider = st.selectbox("Strategic Hub", ["OpenAI", "Google", "Anthropic", "xAI (Grok)"])
    model_mapping = {
        "OpenAI": ["gpt-4o", "gpt-4o-mini"],
        "Google": ["gemini-1.5-pro", "gemini-1.5-flash"],
        "Anthropic": ["claude-3-5-sonnet-20240620"],
        "xAI (Grok)": ["grok-beta"]
    }
    selected_model = st.selectbox("Efficiency Model", model_mapping[provider])
    
    st.markdown("---")
    st.markdown("### Context Memory")
    for f in st.session_state['context_files']:
        st.markdown(f"<div style='font-size:0.8rem; padding:4px 0;'>📄 {f}</div>", unsafe_allow_html=True)

# --- PANEL LAYOUT ---
col_left, col_main, col_right = st.columns([0.1, 1, 0.4])

with col_main:
    st.markdown(f"""
        <div class="agent-header">
            <div style="font-size:2rem;">💸</div>
            <div>
                <div style="font-size:1.1rem; font-weight:700; color:white;">OptiForge Pro</div>
                <div style="font-size:0.8rem; color:#71717A;">Autonomous Efficiency Architect • {selected_model}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state['messages']:
            role_class = "user" if msg['role'] == "user" else "ai"
            st.markdown(f"""
                <div class="message {role_class}">
                    <div class="bubble">{msg['content']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if 'viz' in msg and msg['viz']:
                with st.expander("Cost Optimization Roadmap", expanded=True):
                    # Multi-Opportunity Impact Chart
                    df_viz = pd.DataFrame(msg['data'].get("opportunity_list", []))
                    if not df_viz.empty:
                        # Extract numeric savings if possible
                        df_viz['savings_num'] = df_viz['estimated_savings'].astype(str).str.extract('(\d+)').fillna(0).astype(float)
                        fig = px.bar(df_viz, x="area", y="savings_num", color="effort_level", 
                                    text="estimated_savings", color_discrete_sequence=['#FF5C00', '#A1A1AA', '#FFFFFF'],
                                    labels={"savings_num": "Estimated Savings ($)", "area": "Category", "effort_level": "Complexity"})
                        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
                        st.plotly_chart(fig, use_container_width=True)

    user_query = st.chat_input("Message OptiForge... (e.g., '/analyze' or 'optimize cloud')")
    
    if user_query:
        st.session_state['messages'].append({"role": "user", "content": user_query})
        
        if user_query.startswith("/analyze") or "optimize" in user_query.lower() or "cost" in user_query.lower():
            with st.spinner(" "):
                try:
                    with open("cost_input.txt", "r") as f: context = f.read()
                    data = optimize_costs(context, model_name=selected_model)
                    save_outputs(data)
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": f"Cost audit complete. **{data['optimization_summary']}**. I've identified **{len(data['opportunity_list'])}** strategic areas for optimization. Primary focus: **{data['priority_focus']}**.",
                        "viz": True,
                        "data": data
                    })
                except Exception as e:
                    st.session_state['messages'].append({"role": "assistant", "content": f"Audit execution error: {e}"})
        else:
            st.session_state['messages'].append({"role": "assistant", "content": "OptiForge Pro is standby. Send `/analyze` to perform a granular cost audit and identify latent efficiency gains."})
        st.rerun()

with col_right:
    st.markdown("<h3 style='color:white; margin-top:20px;'>Efficiency Pulse</h3>", unsafe_allow_html=True)
    
    insights = [
        {"title": "Burn Rate Signal", "desc": "Current burn is 12% above quarterly benchmark.", "status": "🟠"},
        {"title": "Vendor Audit", "desc": "Unused SaaS seats detected in Salesforce/Slack.", "status": "📈"}
    ]
    
    for insight in insights:
        st.markdown(f"""
            <div class="tool-card">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <span style='font-size:1rem;'>{insight['status']}</span>
                    <div style="font-weight:600; color:white; font-size:0.9rem;">{insight['title']}</div>
                </div>
                <div style="font-size:0.85rem; color:#A1A1AA;">{insight['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""<style>.stChatFloatingInputContainer { bottom: 40px !important; background: transparent !important; }</style>""", unsafe_allow_html=True)
