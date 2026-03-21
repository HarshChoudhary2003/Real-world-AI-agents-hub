import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from datetime import date
from agent import analyze_log_anomalies, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Log-Sentinel AI | Systems Telemetry OS",
    page_icon="🛡️",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes pulseRed {
        0% { box-shadow: 0 0 5px rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.8); }
        100% { box-shadow: 0 0 5px rgba(239, 68, 68, 0.4); }
    }
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main { background-color: #0c0a09; }
    .stApp { background: radial-gradient(circle at bottom center, #1c1917 0%, #0c0a09 100%); }
    
    .health-meter {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        border: 5px solid #ef4444;
        background: rgba(239, 68, 68, 0.1);
        animation: pulseRed 3s infinite;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
    }
    .incident-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #ef4444;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        animation: slideInUp 0.7s ease-out;
    }
    .blueprint-step {
        background: rgba(16, 185, 129, 0.05);
        border: 1px dashed #10b981;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #10b981;
    }
    .section-header {
        color: #f8fafc;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 15px;
        border-right: 4px solid #ef4444;
        padding-right: 15px;
        width: fit-content;
    }
    .sidebar-section {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("🛡️ Log-Sentinel AI")
st.markdown("### Advanced Systems Telemetry & Health Audit OS")
st.caption("Detect anomalies, security threats, and performance regressions through deep log heuristic analysis.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Sentinel Config")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        # Global Provider-first Standard
        provider = st.selectbox(
            "Select Intelligence Provider",
            ["OpenAI", "Google Gemini", "Anthropic Claude", "DeepSeek", "Groq (Llama 3)", "Custom"]
        )

        if provider == "OpenAI":
            model_name = st.selectbox("Select Model", ["gpt-4o-mini", "gpt-4o", "o1-mini"])
        elif provider == "Google Gemini":
            model_name = st.selectbox("Select Model", ["gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash"])
        elif provider == "Anthropic Claude":
            model_name = st.selectbox("Select Model", ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"])
        elif provider == "DeepSeek":
            model_name = st.selectbox("Select Model", ["deepseek/deepseek-chat"])
        elif provider == "Groq (Llama 3)":
            model_name = st.selectbox("Select Model", ["groq/llama-3.1-70b-versatile", "groq/llama-3.1-8b-instant"])
        else:
            model_name = st.text_input("Enter LiteLLM Model ID", "")

        api_key = st.text_input("Provider API Key (Optional)", type="password")
        temperature = st.slider("Anomaly Sensitivity", 0.0, 1.0, 0.2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Telemetry Input")
    if st.button("Load DB Timeout Logs"):
        st.session_state.raw_logs = """2024-06-01 10:01 INFO Service started
2024-06-01 10:02 INFO Request processed
2024-06-01 10:03 ERROR Database timeout
2024-06-01 10:03 ERROR Database timeout
2024-06-01 10:03 ERROR Database timeout
2024-06-01 10:04 INFO Request processed"""

# Layout Split
col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.markdown('<div class="section-header">🛠️ Log Telemetry</div>', unsafe_allow_html=True)
    log_text = st.text_area(
        "Paste system logs or event telemetry below:",
        value=st.session_state.get("raw_logs", ""),
        height=400,
        placeholder="2024-06-01 12:35 INFO: Application running..."
    )
    
    if st.button("🚀 Run Forensic Telemetry Audit"):
        if log_text:
            with st.spinner("Analyzing telemetry signals for regression / intrusion patterns..."):
                try:
                    report_data = analyze_log_anomalies(log_text, model_name, api_key)
                    st.session_state.log_audit = report_data
                    save_outputs(report_data)
                    st.success("Audit Completed!")
                except Exception as e:
                    st.error(f"Audit Error: {e}")
        else:
            st.warning("Please provide log telemetry data first.")

with col_output:
    if "log_audit" in st.session_state:
        data = st.session_state.log_audit
        sa = data.get('sentinel_assessment', {})
        health_idx = int(sa.get('health_index', '0'))
        
        # Health Meter Area
        color = "#10b981" if health_idx > 75 else "#f59e0b" if health_idx > 40 else "#ef4444"
        st.markdown(f"""
            <div class="health-meter" style="border-color: {color}; background: rgba({color[1:3]},{color[3:5]},{color[5:7]},0.1);">
                <span style="font-size: 2.2rem; font-weight: 900; color: {color};">{health_idx}%</span>
                <span style="font-size: 0.7rem; color: #94a3b8; font-weight: 600;">HEALTH INDEX</span>
            </div>
            <div align="center" style="margin-top: 20px; color: #94a3b8; font-style: italic;">
                Verdict: <strong style="color: {color};">{sa.get('verdict')}</strong><br>
                {sa.get('diagnostic_overview')}
            </div>
        """, unsafe_allow_html=True)

        # Result Tabs
        tab_incidents, tab_blueprint, tab_export = st.tabs(["🚑 Incident Diagnostics", "🔍 SRE Blueprint", "🗳️ Forensic Export"])
        
        with tab_incidents:
            st.markdown('<div class="section-header">🚑 Detected Telemetry Signals</div>', unsafe_allow_html=True)
            for incident in data.get('detected_incidents', []):
                st.markdown(f"""
                    <div class="incident-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="font-weight: 800; color: #f8fafc;">{incident.get('signature')}</span>
                            <span style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 2px 10px; border-radius: 99px; font-size: 0.7rem; font-weight: 800;">{incident.get('event_type')} x{incident.get('frequency')}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.9rem;">Impact: {incident.get('technical_impact')}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            if data.get("security_alerts"):
                st.markdown("#### 🔒 Security Threat Posture")
                for alert in data.get("security_alerts", []):
                    st.error(f"⚠️ {alert}")

        with tab_blueprint:
            st.markdown('<div class="section-header">🔍 SRE Response Blueprint</div>', unsafe_allow_html=True)
            for step in data.get('sre_blueprint', []):
                st.markdown(f"""<div class="blueprint-step">▶ {step}</div>""", unsafe_allow_html=True)
                
            st.divider()
            st.markdown("#### 👁️ Recognized Behavioral Patterns")
            for pattern in data.get('structural_patterns', []):
                st.info(f"pattern: {pattern}")

        with tab_export:
            st.markdown('<div class="section-header">🗳️ Forensic Audit Package</div>', unsafe_allow_html=True)
            st.download_button("📥 Export JSON Audit", json.dumps(data, indent=2), "log_forensics.json", "application/json")
            st.download_button("📝 Download SRE Brief", str(data), "sre_brief.txt", "text/plain")
            
    else:
        st.info("Input system telemetry or log files and click 'Run Telemetry Audit' to reveal system health signals.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Log-Sentinel AI | Protecting System Reliability</div>", unsafe_allow_html=True)
