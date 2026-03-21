import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from datetime import date
from agent import read_alert_data, interpret_alert_signals, save_outputs

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Alert-Insight AI | SaaS Edition",
    page_icon="📊",
    layout="wide",
)

# --- SaaS ELITE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: radial-gradient(circle at bottom center, #0f172a 0%, #020617 100%);
        color: #f1f5f9;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        padding-top: 20px;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
    }

    /* KPI Glass Cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        animation: slideIn 0.8s ease-out;
    }
    .kpi-card:hover { border-color: #3b82f6; background: rgba(59, 130, 246, 0.03); }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .criticality-badge {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .crit-critical { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid #ef4444; text-shadow: 0 0 8px #ef4444; }
    .crit-moderate { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid #f59e0b; }
    .crit-info { background: rgba(59, 130, 246, 0.1); color: #3b82f6; border: 1px solid #3b82f6; }

    /* Layout Sections */
    .nav-header {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 64px;
        background: rgba(2, 6, 23, 0.8);
        backdrop-filter: blur(12px);
        z-index: 999;
        display: flex;
        align-items: center;
        padding: 0 40px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .nav-logo { font-size: 1.25rem; font-weight: 800; background: linear-gradient(90deg, #3b82f6, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
""", unsafe_allow_html=True)

# --- TOP NAV ---
st.markdown("""
    <div class="nav-header">
        <div class="nav-logo">ALERT-INSIGHT AI</div>
        <div style="flex: 1;"></div>
        <div style="color: #64748b; font-size: 0.8rem;">Monitoring Pulse: 🟢 Stable</div>
    </div>
    <div style="height: 80px;"></div>
""", unsafe_allow_html=True)

# --- SESSION STATE & NAVIGATION ---
if 'view' not in st.session_state:
    st.session_state.view = 'Dashboard'

def switch_view(name):
    st.session_state.view = name

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔭 Exploration")
    if st.button("📊 Snapshot Dashboard", use_container_width=True): switch_view('Dashboard')
    if st.button("📥 Ingest Signal", use_container_width=True): switch_view('Ingest')
    if st.button("🏗️ Roadmap", use_container_width=True): switch_view('Roadmap')
    if st.button("⚙️ Control Panel", use_container_width=True): switch_view('Settings')
    
    st.divider()
    st.markdown("### 🎛️ Provider Forge")
    provider = st.selectbox("Provider", ["OpenAI", "Google Gemini", "Anthropic", "Groq"])
    model = st.selectbox("Model Intelligence", ["gpt-4o-mini", "gemini-1.5-pro", "claude-3-5-sonnet", "llama-3.1-70b"])
    api_key_input = st.text_input("Ingest API Key (Optional)", type="password")
    
    st.divider()
    st.caption("Monitoring Signals interpreted by Alert-Insight AI v2.0")

# --- VIEWS ---
if st.session_state.view == 'Dashboard':
    st.markdown('<h2 style="font-weight: 800; letter-spacing: -1px;">Intelligence Hub</h2>', unsafe_allow_html=True)
    
    if "alert_audit" in st.session_state:
        data = st.session_state.alert_audit
        ab = data.get('alert_briefing', {})
        dd = data.get('diagnostic_deep_dive', {})
        crit = ab.get('criticality', 'Info').lower()
        
        # KPI GRID
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="kpi-card"><div style="color: #64748b; font-size: 0.75rem; font-weight: 800; margin-bottom: 10px;">CRITICALITY</div><span class="criticality-badge crit-{crit}">{ab.get('criticality')}</span></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="kpi-card"><div style="color: #64748b; font-size: 0.75rem; font-weight: 800; margin-bottom: 10px;">INCIDENT CLASS</div><div style="font-size: 1.1rem; font-weight: 800; color: #3b82f6;">{ab.get('incident_title')}</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="kpi-card"><div style="color: #64748b; font-size: 0.75rem; font-weight: 800; margin-bottom: 10px;">IMPACT SCORE</div><div style="font-size: 1.5rem; font-weight: 900; color: #f1f5f9;">88<span style="font-size: 0.8rem; color: #64748b;">/100</span></div></div>""", unsafe_allow_html=True)
            
        st.divider()
        
        col_main, col_stats = st.columns([2, 1])
        
        with col_main:
            st.markdown(f"""<div class="kpi-card" style="text-align: left;"><h3 style="margin-top: 0;">🚀 Briefing Narrative</h3><p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6;">{ab.get('executive_summary')}</p><hr style="border-color: rgba(255,255,255,0.05);"><h4 style="color: #3b82f6;">🧬 Systematic Cause</h4><p style="color: #cbd5e1;">{dd.get('likely_cause')}</p><p style="color: #64748b; font-size: 0.9rem;">{dd.get('technical_explanation')}</p></div>""", unsafe_allow_html=True)
            
            # Simulated Alert Trends
            st.markdown('<div class="kpi-card" style="text-align: left;"><h3>📊 Incident Signal Pattern</h3>', unsafe_allow_html=True)
            chart_df = pd.DataFrame({
                "Timestamp": ["10:00", "10:05", "10:10", "10:15", "10:20", "10:25", "10:30"],
                "Error Rate (%)": [1.2, 1.5, 4.8, 8.4, 7.9, 5.2, 2.1]
            })
            fig = px.area(chart_df, x="Timestamp", y="Error Rate (%)", template="plotly_dark", color_discrete_sequence=["#3b82f6"])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_stats:
            st.markdown('<div class="kpi-card" style="text-align: left;"><h3>🏷️ Alert Vectors</h3>', unsafe_allow_html=True)
            for tag in dd.get('impacted_services', []):
                st.markdown(f"**Target**: `{tag}`")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="kpi-card" style="text-align: left; border-left: 4px solid #10b981;"><h3>⚡ SRE Pro Tips</h3>', unsafe_allow_html=True)
            for tip in data.get('sre_expert_tips', []):
                st.success(f"▶ {tip}")
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        st.info("System is currently stable or no signal has been ingested. Please proceed to 'Ingest Signal' if an alert threshold has been breached.")

elif st.session_state.view == 'Ingest':
    st.markdown('<h2 style="font-weight: 800; letter-spacing: -1px;">Signal Ingestion</h2>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-card" style="text-align: left;"><h3>🚑 Push Monitoring Stream</h3>', unsafe_allow_html=True)
    raw_input = st.text_area("Paste the alert JSON or raw log data here:", height=300, value=st.session_state.get("last_alert_raw", ""))
    
    if st.button("🚀 Analyze Signal Vectors"):
        if raw_input:
            with st.spinner("Decoding monitor metadata and resolving root-cause heuristics..."):
                try:
                    # Save for agent read
                    with open("alert.txt", "w", encoding="utf-8") as f:
                        f.write(raw_input)
                    
                    report = interpret_alert_signals(raw_input, "gpt-4o-mini", api_key_input)
                    st.session_state.alert_audit = report
                    st.session_state.last_alert_raw = raw_input
                    save_outputs(report)
                    st.success("Signal Ingested. Redirecting to Hub...")
                    switch_view('Dashboard')
                    st.rerun()
                except Exception as e:
                    st.error(f"Ingest Error: {e}")
        else:
            st.warning("Please provide signal data.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'Roadmap':
    st.markdown('<h2 style="font-weight: 800; letter-spacing: -1px;">Remediation Roadmap</h2>', unsafe_allow_html=True)
    if "alert_audit" in st.session_state:
        data = st.session_state.alert_audit
        for item in data.get('remediation_roadmap', []):
            st.markdown(f"""
                <div class="kpi-card" style="text-align: left; border-left: 4px solid #2563eb; margin-bottom: 20px;">
                    <h4 style="color: #3b82f6; margin-top: 0;">{item.get('action')}</h4>
                    <p style="color: #94a3b8; margin-bottom: 0;">{item.get('strategy')}</p>
                </div>
            """, unsafe_allow_html=True)
            
        st.divider()
        st.markdown("#### ⚙️ Monitor Optimization Tuning")
        for opt in data.get('alert_optimization', []):
            st.info(f"💡 {opt}")
    else:
        st.warning("No signal has been audited. Remediation paths are locked.")

elif st.session_state.view == 'Settings':
    st.markdown('<h2 style="font-weight: 800; letter-spacing: -1px;">Control Panel</h2>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-card" style="text-align: left;">', unsafe_allow_html=True)
    st.checkbox("Enable Real-time Heuristic Pulse", value=True)
    st.checkbox("Auto-archive audit logs", value=True)
    st.slider("Resolution Sensitivity", 0.1, 1.0, 0.45)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""<div style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(2, 6, 23, 0.6); backdrop-filter: blur(5px); padding: 5px 40px; text-align: center; font-size: 0.65rem; color: #475569; border-top: 1px solid rgba(255,255,255,0.05); z-index: 1000;">Architected by ALERT-INSIGHT AI | Multi-Cloud Observability Intelligence</div>""", unsafe_allow_html=True)
