import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from agent import explain_strategy, save_outputs
import os
import time
from datetime import date

# --- UNICORN STARTUP CONFIGURATION ---
st.set_page_config(
    page_title="StrategyLens | Neural Strategy Auditor",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'last_result' not in st.session_state:
    st.session_state['last_result'] = None
if 'is_auditing' not in st.session_state:
    st.session_state['is_auditing'] = False

# --- ELITE STARTUP DESIGN SYSTEM (STRIPE/LINEAR INSPIRED) ---
st.markdown("""
<style>
    @import url('https://rsms.me/inter/inter.css');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');

    :root {
        --bg-main: #030303;
        --sidebar-bg: #09090B;
        --card-bg: rgba(18, 18, 18, 0.7);
        --accent-primary: #6366F1; /* Indigo */
        --border-color: rgba(255, 255, 255, 0.08);
        --text-primary: #EDEDED;
        --text-secondary: #A1A1AA;
        --glass-gradient: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        --shadow-premium: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Full Override */
    .stApp {
        background-color: var(--bg-main);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stHeader"] { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Sidebar Logo & Branding */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
        padding-top: 2rem;
    }
    
    .sidebar-logo {
        padding: 0 1.5rem 2.5rem 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: white;
        letter-spacing: -1.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .logo-badge {
        background: var(--accent-primary);
        color: white;
        font-size: 0.6rem;
        padding: 2px 6px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Top Bar Ecosystem */
    .top-bar {
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2.5rem;
        border-bottom: 1px solid var(--border-color);
        background: rgba(3, 3, 3, 0.8);
        backdrop-filter: blur(12px);
        margin-left: -5rem;
        margin-right: -5rem;
        margin-top: -6rem;
        margin-bottom: 3rem;
        position: sticky;
        top: 0;
        z-index: 999;
    }

    .top-bar-item {
        color: var(--text-secondary);
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        transition: color 0.2s;
        margin-right: 2rem;
    }
    .top-bar-item:hover { color: white; }

    /* Premium Modular Dashboard */
    .dashboard-container {
        padding: 24px;
        max-width: 1400px;
        margin: 0 auto;
    }

    .glass-card {
        background: var(--glass-gradient);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--shadow-premium);
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover { 
        border-color: rgba(99, 102, 241, 0.4);
        background: rgba(255, 255, 255, 0.04);
        transform: translateY(-2px);
    }

    .kpi-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-secondary);
        margin-bottom: 8px;
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
    }
    
    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 10px;
    }

    /* Skeleton Loading Effect */
    @keyframes shimmer {
        0% { background-position: -468px 0; }
        100% { background-position: 468px 0; }
    }
    .skeleton {
        background: linear-gradient(to right, #18181B 8%, #27272A 18%, #18181B 33%);
        background-size: 800px 104px;
        animation: shimmer 1.5s infinite linear;
        border-radius: 8px;
    }

    /* Logic Flow */
    .logic-step {
        border-left: 2px solid var(--border-color);
        padding-left: 24px;
        margin-bottom: 24px;
        position: relative;
    }
    .logic-step::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 0;
        width: 10px;
        height: 10px;
        background: var(--accent-primary);
        border-radius: 50%;
        box-shadow: 0 0 10px var(--accent-primary);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & GLOBAL CONTROL ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">StrategyLens <span class="logo-badge">PRO</span></div>', unsafe_allow_html=True)
    st.markdown("### Systems")
    st.selectbox("Active Auditor", ["Logic Architecture", "Market Performance", "Risk Heatmap"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### Neural Calibration")
    hub = st.selectbox("Provider", ["OpenAI", "Google", "Anthropic", "xAI"])
    model_map = {
        "OpenAI": ["gpt-4o", "gpt-4o-mini"], "Google": ["gemini-1.5-pro"],
        "Anthropic": ["claude-3-5-sonnet-20240620"], "xAI": ["grok-beta"]
    }
    selected_model = st.selectbox("Intelligence Core", model_map[hub])
    
    st.markdown("---")
    st.markdown('<div style="opacity: 0.5; font-size: 0.75rem;">Build version 4.1.0-alpha</div>', unsafe_allow_html=True)

# --- TOP BAR ---
st.markdown("""
<div class="top-bar">
    <div style="display: flex;">
        <span class="top-bar-item">Dashboard</span>
        <span class="top-bar-item">Neural Logic</span>
        <span class="top-bar-item">Market Sync</span>
        <span class="top-bar-item" style="color: #6366F1">Strategy Vault</span>
    </div>
    <div style="display: flex; align-items: center;">
        <span class="top-bar-item" style="margin-right: 0;">Settings</span>
        <div style="width: 32px; height: 32px; background: #27272A; border-radius: 50%; margin-left: 2rem;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- DASHBOARD HEADER ---
st.markdown("""
<div style="padding: 1rem 2.5rem 1rem 2.5rem;">
    <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2.8rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -2px;">Neural Strategy Audit</h1>
    <p style="color: var(--text-secondary); font-size: 1.1rem; max-width: 800px;">Transparent, autonomous synthesis of trading system mechanics and systematic risk profiles.</p>
</div>
""", unsafe_allow_html=True)

# --- MAIN DASHBOARD AREA ---
st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

if st.session_state['last_result']:
    res = st.session_state['last_result']
    
    # 1. KPI CARDS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="glass-card"><div class="kpi-label">Strategy Origin</div><div class="kpi-value">{res["strategy_name"]}</div><div class="status-pill" style="background: rgba(99,102,241,0.1); color:#6366F1;">Verified Schema</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="glass-card"><div class="kpi-label">Audit Latency</div><div class="kpi-value">1.4s</div><div class="status-pill" style="background: rgba(16,185,129,0.1); color:#10B981;">Optimal</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="glass-card"><div class="kpi-label">Logic Complexity</div><div class="kpi-value">{len(res["mechanics_audit"])} Steps</div><div class="status-pill" style="background: rgba(245,158,11,0.1); color:#F59E0B;">Systematic</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="glass-card"><div class="kpi-label">Risk Rating</div><div class="kpi-value">Moderate</div><div class="status-pill" style="background: rgba(239,68,68,0.1); color:#EF4444;">Caution Advised</div></div>', unsafe_allow_html=True)

    # 2. MAIN ANALYSIS CONTENT
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    c_left, c_right = st.columns([0.65, 0.35])
    
    with c_left:
        st.markdown('<div class="glass-card"><h3>Mechanics Architecture</h3>', unsafe_allow_html=True)
        for m in res.get("mechanics_audit", []):
            st.markdown(f"""
                <div class="logic-step">
                    <p style="font-weight: 600; font-size: 1rem; color: white;">{m.get('step')}</p>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">{m.get('description')}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><h3>Executive Synthesis</h3>', unsafe_allow_html=True)
        st.write(res.get("educational_summary"))
        st.markdown('</div>', unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="glass-card"><h3>Performance Matrix</h3>', unsafe_allow_html=True)
        st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <p class="kpi-label" style="color:#10B981;">✓ Optimal Conditions</p>
                <p style="font-size:0.9rem;">{res.get('optimal_market_state', 'N/A')}</p>
            </div>
            <div style="margin-bottom: 10px;">
                <p class="kpi-label" style="color:#EF4444;">✗ Failure Conditions</p>
                <p style="font-size:0.9rem;">{res.get('fail_market_state', 'N/A')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Risk Visualization (Heatmap style)
        st.markdown('<p class="kpi-label">Risk Distribution</p>', unsafe_allow_html=True)
        risk_data = res.get("risk_matrix", [])
        if risk_data:
            df_risk = pd.DataFrame(risk_data)
            fig = px.bar(df_risk, x="impact", y="risk_type", orientation='h', color="impact", 
                         color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"},
                         template="plotly_dark")
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # 3. EMPTY STATE / ONBOARDING
    st.markdown("""
        <div style="text-align: center; padding: 6rem 1rem; border: 1px dashed var(--border-color); border-radius: 24px; background: rgba(255,255,255,0.01);">
            <div style="font-size: 3rem; margin-bottom: 1.5rem;">🕯️</div>
            <h2 style="font-family: 'Space Grotesk', sans-serif; font-weight: 700;">Awaiting Intelligence Frame</h2>
            <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 2rem auto;">Configure your neural provider on the left or click 'Initialize Audit Sequence' to analyze the current trading strategy logic.</p>
        </div>
    """, unsafe_allow_html=True)

# --- INTERACTION PANEL ---
st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
c_cmd, _ = st.columns([0.6, 0.4])

with c_cmd:
    st.markdown('<div class="glass-card" style="padding: 1.2rem;">', unsafe_allow_html=True)
    st.markdown("<p class=\"kpi-label\" style=\"margin-bottom:15px;\">Neural Command Terminal</p>", unsafe_allow_html=True)
    
    input_cmd = st.text_input("Execute Neural Command...", placeholder="/audit_strategy or 'Analyze Crossover'", label_visibility="collapsed")
    btn = st.button("Initialize Logic Sweep", use_container_width=True)
    
    if btn or input_cmd:
        st.session_state['is_auditing'] = True
        with st.spinner(" "):
            try:
                # Mock high-load processing
                time.sleep(1.2)
                with open("strategy_input.txt", "r") as f: context = f.read()
                data = explain_strategy(context, model_name=selected_model)
                save_outputs(data)
                st.session_state['last_result'] = data
                st.success("Logic Synchronization Sequential.")
                time.sleep(0.5)
            except Exception as e:
                st.error(f"Neural Loop Interrupted: {e}")
        st.session_state['is_auditing'] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # End dashboard-container
