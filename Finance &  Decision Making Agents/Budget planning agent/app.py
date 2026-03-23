import streamlit as st
import json
import pandas as pd
import plotly.express as px
from agent import generate_budget, save_outputs
import os
import time

# Page Configuration
st.set_page_config(
    page_title="BudgetForge | Neural AI Interface",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'agent_status' not in st.session_state:
    st.session_state['agent_status'] = "Idle"
if 'context_files' not in st.session_state:
    st.session_state['context_files'] = ["budget_input.txt"]

# --- NEXT-GEN AI INTERFACE CSS (DARK MODE DEFAULT) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-editor: #0A0A0B;
        --bg-sidebar: #111113;
        --bg-chat-user: #232326;
        --accent: #0062FF;
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
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border);
    }
    
    /* Chat Container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 120px;
    }
    
    /* Message Bubbles */
    .message {
        display: flex;
        flex-direction: column;
        margin-bottom: 24px;
        animation: fadeIn 0.4s ease-out;
    }
    
    .message.user {
        align-items: flex-end;
    }
    
    .bubble {
        padding: 16px 20px;
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

    /* Agent Identity */
    .agent-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 40px;
        padding: 20px;
        background: rgba(255,255,255,0.03);
        border-radius: var(--radius);
        border: 1px solid var(--border);
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #22C55E;
        box-shadow: 0 0 10px #22C55E;
    }

    /* Floating Input */
    .input-container {
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 800px;
        background: rgba(17, 17, 19, 0.8);
        backdrop-filter: blur(20px);
        padding: 16px;
        border-radius: 20px;
        border: 1px solid var(--border);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        z-index: 1000;
        display: flex;
        gap: 12px;
        align-items: center;
    }

    /* Premium Cards for Tools */
    .tool-card {
        background: #18181B;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-top: 12px;
        transition: transform 0.2s ease;
    }
    .tool-card:hover {
        transform: translateY(-2px);
        border-color: var(--accent);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #27272A; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: AGENT MANAGEMENT ---
with st.sidebar:
    st.markdown("### Neural Agents")
    
    agents = [
        {"name": "BudgetForge Pro", "status": "Active", "icon": "💎"},
        {"name": "Data Analyst", "status": "Standby", "icon": "📊"},
        {"name": "Risk Auditor", "status": "Standby", "icon": "🛡️"}
    ]
    
    for agent in agents:
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; padding:12px; margin-bottom:8px; background:{'rgba(0,98,255,0.1)' if agent['name'] == 'BudgetForge Pro' else 'transparent'}; border-radius:12px; border:1px solid {'var(--accent)' if agent['name'] == 'BudgetForge Pro' else 'transparent'};">
                <span style="font-size:1.2rem;">{agent['icon']}</span>
                <div style="flex:1;">
                    <div style="font-size:0.9rem; font-weight:600; color:{'white' if agent['name'] == 'BudgetForge Pro' else 'var(--text-body)'};">{agent['name']}</div>
                    <div style="font-size:0.75rem; color:{'#0062FF' if agent['name'] == 'BudgetForge Pro' else '#71717A'};">{agent['status']}</div>
                </div>
                {f'<div class="status-indicator"></div>' if agent['status'] == 'Active' else ''}
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Intelligence Context")
    provider = st.selectbox("Provider", ["OpenAI", "Google", "Anthropic", "xAI (Grok)"])
    model_mapping = {
        "OpenAI": ["gpt-4o", "gpt-4o-mini"],
        "Google": ["gemini-1.5-pro", "gemini-1.5-flash"],
        "Anthropic": ["claude-3-5-sonnet-20240620"],
        "xAI (Grok)": ["grok-beta"]
    }
    selected_model = st.selectbox("Model", model_mapping[provider])
    
    st.markdown("---")
    st.markdown("### Memory Space")
    for f in st.session_state['context_files']:
        st.markdown(f"<div style='font-size:0.8rem; color:var(--text-body); padding:4px 0;'>📄 {f}</div>", unsafe_allow_html=True)

# --- MAIN CHAT PANEL ---
col_left, col_main, col_right = st.columns([0.1, 1, 0.4])

with col_main:
    # Agent Header
    st.markdown(f"""
        <div class="agent-header">
            <div style="font-size:2rem;">💎</div>
            <div>
                <div style="font-size:1.1rem; font-weight:700; color:white;">BudgetForge Pro</div>
                <div style="font-size:0.8rem; color:#71717A;">Autonomous Financial Strategy Engine • {selected_model}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Chat History
    chat_placeholder = st.container()
    
    with chat_placeholder:
        for msg in st.session_state['messages']:
            role_class = "user" if msg['role'] == "user" else "ai"
            st.markdown(f"""
                <div class="message {role_class}">
                    <div class="bubble">
                        {msg['content']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # If AI message has metadata (visuals), show them
            if 'viz' in msg and msg['viz']:
                with st.expander("Strategic Analysis Visualization", expanded=True):
                    # Show the chart or metrics from stored data
                    if 'chart_data' in msg:
                        df = pd.DataFrame(msg['chart_data'])
                        fig = px.pie(df, values='percentage', names='category', hole=0.6,
                                   color_discrete_sequence=['#0062FF', '#FFFFFF', '#27272A', '#52525B'])
                        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                        font_color='white', margin=dict(t=0, b=0, l=0, r=0))
                        st.plotly_chart(fig, use_container_width=True)

    # Floating Input
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) # Spacer

    with st.container():
        user_query = st.chat_input("Message BudgetForge... (try '/analyze' or ask for status)")
        
        if user_query:
            # Add user message
            st.session_state['messages'].append({"role": "user", "content": user_query})
            
            # Processing Simulation
            with st.spinner(" "): # Hidden spinner for manual control
                # Logic to handle commands or queries
                if user_query.startswith("/analyze") or "budget" in user_query.lower():
                    # Read input file for context
                    try:
                        with open("budget_input.txt", "r") as f:
                            context = f.read()
                        
                        data = generate_budget(context, model_name=selected_model)
                        save_outputs(data)
                        
                        # Add AI response with viz
                        st.session_state['messages'].append({
                            "role": "assistant", 
                            "content": f"Neural analysis complete. Based on the provided context, I've projected a strategic allocation with a remaining liquidity of **{data['remaining_balance']}**.",
                            "viz": True,
                            "chart_data": data['allocations']
                        })
                    except Exception as e:
                        st.session_state['messages'].append({"role": "assistant", "content": f"I encountered an error while accessing the memory space: {e}"})
                else:
                    st.session_state['messages'].append({
                        "role": "assistant", 
                        "content": "I am standing by. You can use `/analyze` to process the current budget context or ask me specific questions about your capital structure."
                    })
            st.rerun()

# --- RIGHT PANEL: STRATEGIC INSIGHTS ---
with col_right:
    st.markdown("<h3 style='color:white; margin-top:20px;'>Strategic Insights</h3>", unsafe_allow_html=True)
    
    if st.session_state['messages'] and 'data' in globals(): # Note: this logic needs session state for 'data'
        pass # Handle persistent data display here
    
    # Static Premium Info for demonstration
    insights = [
        {"title": "Liquidity Audit", "desc": "High confidence in 12-month runway.", "icon": "✅"},
        {"title": "Allocation Alert", "desc": "Software costs are 8% above benchmark.", "icon": "⚠️"}
    ]
    
    for insight in insights:
        st.markdown(f"""
            <div class="tool-card">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <span>{insight['icon']}</span>
                    <div style="font-weight:600; color:white; font-size:0.9rem;">{insight['title']}</div>
                </div>
                <div style="font-size:0.85rem; color:var(--text-body);">{insight['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

# Hidden overrides for Streamlit elements
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        bottom: 40px !important;
        background: transparent !important;
    }
    div[data-testid="stChatMessageContainer"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)
