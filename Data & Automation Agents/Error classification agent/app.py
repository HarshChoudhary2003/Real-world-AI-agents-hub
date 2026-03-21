import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from datetime import date
from agent import read_error_data, classify_error_signals, save_outputs

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Error-Forensics AI | SaaS Edition",
    page_icon="🚑",
    layout="wide",
)

# --- PREMIUM SaaS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background & Layout */
    .stApp {
        background: radial-gradient(circle at 0% 0%, #111827 0%, #0c0a09 100%);
        color: #f8fafc;
    }
    
    /* Top Navbar */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: rgba(17, 24, 39, 0.8);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 1000;
        display: flex;
        align-items: center;
        padding: 0 40px;
        justify-content: space-between;
    }
    
    .nav-title {
        font-size: 1.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ef4444, #f87171);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Sidebar Navigation */
    [data-testid="stSidebar"] {
        background-color: #030712 !important;
        border-right: 1px solid rgba(255,255,255,0.05);
        padding-top: 60px;
    }
    
    .sidebar-nav-item {
        padding: 12px 20px;
        margin: 4px 15px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #94a3b8;
    }
    .sidebar-nav-item:hover {
        background: rgba(255, 255, 255, 0.05);
        color: #f8fafc;
    }
    .sidebar-nav-item.active {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        animation: slideUp 0.8s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.05);
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .kpi-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Severity Badges */
    .sev-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
    }
    .sev-critical { color: #ef4444; background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; box-shadow: 0 0 15px rgba(239,68,68,0.3); }
    .sev-high { color: #f59e0b; background: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; }
    .sev-moderate { color: #3b82f6; background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; }

    /* Custom Input */
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- TOP NAVBAR ---
st.markdown("""
    <div class="nav-container">
        <div class="nav-title">ERROR-FORENSICS AI</div>
        <div style="display: flex; align-items: center; gap: 20px; color: #64748b;">
            <span style="font-size: 0.85rem;">SRE Dashboard v2.0</span>
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #ef4444; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 0.7rem;">SRE</div>
        </div>
    </div>
    <div style="height: 80px;"></div>
""", unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'

def set_page(name):
    st.session_state.page = name

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### Navigation")
    
    # Custom Sidebar Nav Components
    if st.button("📊 Dashboard", use_container_width=True): set_page('Dashboard')
    if st.button("📁 Upload Incident", use_container_width=True): set_page('Upload')
    if st.button("🛡️ Remediation", use_container_width=True): set_page('Remediation')
    if st.button("⚙️ Settings", use_container_width=True): set_page('Settings')
    
    st.divider()
    st.markdown("### Model Config")
    provider = st.selectbox("Provider", ["OpenAI", "Gemini", "Claude", "Groq"])
    model = st.selectbox("Model", ["gpt-4o-mini", "gemini-1.5-flash", "claude-3-5-sonnet", "llama-3.1-70b"])
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.divider()
    st.caption("Site Reliability Engineering (SRE) Toolset for Neural Incident Classification.")

# --- PAGE ROUTING ---
if st.session_state.page == 'Dashboard':
    st.markdown('<h2 style="font-weight: 800;">System Intelligence Dashboard</h2>', unsafe_allow_html=True)
    
    if "forensic_report" in st.session_state:
        data = st.session_state.forensic_report
        ar = data.get("audit_report", {})
        fb = data.get("forensic_breakdown", {})
        sev = ar.get("severity", "Moderate").lower()
        
        # KPI ROW
        st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-label">Severity</div>
                    <div class="kpi-value"><span class="sev-badge sev-{sev}">{ar.get('severity')}</span></div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Primary Category</div>
                    <div class="kpi-value" style="font-size: 1.2rem; color: #ef4444;">{ar.get('primary_category')}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Incident Pattern</div>
                    <div class="kpi-value" style="font-size: 1rem; color: #3b82f6;">{fb.get('recognized_patterns', ['None'])[0]}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col_main, col_side = st.columns([2, 1])
        
        with col_main:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('### 🧬 Forensic Diagnosis')
            st.markdown(f"**Description**: {ar.get('logical_gist')}")
            st.divider()
            st.markdown(f"**Root Cause**: {fb.get('root_cause_explanation')}")
            st.info(f"**Impact Assessment**: {fb.get('impact_assessment')}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Interactive Chart (Simulated Pattern Distribution)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('### 📊 Historical Pattern Distribution')
            chart_data = pd.DataFrame({
                "Category": ["Network", "Database", "Auth", "Logic", "Config"],
                "Frequency": [12, 45, 10, 25, 8]
            })
            fig = px.bar(chart_data, x="Category", y="Frequency", template="plotly_dark", color="Category", color_discrete_sequence=px.colors.sequential.Reds)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_side:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('### 🛡️ SRE Standards')
            for tip in data.get("monitoring_guidelines", []):
                st.markdown(f"- {tip}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('### 🛠️ Pro Tips')
            for tip in data.get("sre_expert_tips", []):
                st.success(f"▶ {tip}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No active incident. Please upload or input an error log in the 'Upload' section to generate diagnostics.")

elif st.session_state.page == 'Upload':
    st.markdown('<h2 style="font-weight: 800;">Incident Ingestion</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🚑 Input Raw Error Stream")
    error_input = st.text_area("Paste error logs, tracebacks, or messages here:", height=300, value=st.session_state.get("error_input_raw", ""))
    
    if st.button("🚀 Analyze Error Vector"):
        if error_input:
            with st.spinner("Executing forensic neural auditing..."):
                try:
                    report = classify_error_signals(error_input, "gpt-4o-mini", api_key)
                    st.session_state.forensic_report = report
                    st.session_state.error_input_raw = error_input
                    save_outputs(report)
                    st.success("Audit Complete. Redirecting to Dashboard...")
                    set_page("Dashboard")
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
        else:
            st.warning("Please provide input data.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Remediation':
    st.markdown('<h2 style="font-weight: 800;">Surgical Remediation Path</h2>', unsafe_allow_html=True)
    
    if "forensic_report" in st.session_state:
        data = st.session_state.forensic_report
        for fix in data.get("surgical_remediation", []):
            st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid #ef4444;">
                    <h4 style="color: #ef4444;">{fix.get('action')}</h4>
                    <p style="color: #94a3b8; font-size: 0.9rem;">{fix.get('remediation_blueprint')}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Analyze an incident first to reveal remediation paths.")

elif st.session_state.page == 'Settings':
    st.markdown('<h2 style="font-weight: 800;">System Settings</h2>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### UI Personalization")
    st.checkbox("Enable Dark Mode Glassmorphism", value=True)
    st.checkbox("Show Performance Tooltips", value=True)
    st.slider("UI Refresh Rate (Hz)", 30, 120, 60)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.4); padding: 10px 40px; text-align: center; font-size: 0.7rem; color: #475569; border-top: 1px solid rgba(255,255,255,0.05); backdrop-filter: blur(5px);">
        Architected by ERROR-FORENSICS AI | Powered by LiteLLM Multi-Cloud Intelligence Hub
    </div>
""", unsafe_allow_html=True)
