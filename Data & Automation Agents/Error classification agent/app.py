import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import read_error_data, classify_error_signals, save_outputs

# Set Page Config
st.set_page_config(
    page_title="Error-Forensics AI | SRE Incident OS",
    page_icon="🚑",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes pulseRed {
        0% { box-shadow: 0 0 10px rgba(239, 68, 68, 0.4); border-color: #ef4444; }
        50% { box-shadow: 0 0 30px rgba(239, 68, 68, 0.6); border-color: #f87171; }
        100% { box-shadow: 0 0 10px rgba(239, 68, 68, 0.4); border-color: #ef4444; }
    }
    @keyframes pulseOrange {
        0% { box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); border-color: #f59e0b; }
        50% { box-shadow: 0 0 30px rgba(245, 158, 11, 0.6); border-color: #fbbf24; }
        100% { box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); border-color: #f59e0b; }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main { background-color: #0c0a09; }
    .stApp { background: radial-gradient(circle at top right, #111827 0%, #0c0a09 100%); }
    
    .forensic-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        animation: slideIn 0.6s ease-out;
    }
    .severity-badge {
        padding: 6px 16px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .severity-critical { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid #ef4444; animation: pulseRed 3s infinite; }
    .severity-high { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid #f59e0b; animation: pulseOrange 3s infinite; }
    .severity-moderate { background: rgba(59, 130, 246, 0.1); color: #3b82f6; border: 1px solid #3b82f6; }
    .severity-low { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid #10b981; }

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
    .remediation-blueprint {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
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
st.title("🚑 Error-Forensics AI")
st.markdown("### Systems Reliability & Multi-Vector Incident Diagnosis")
st.caption("Perform deep forensic analysis on system errors to resolve root causes and architect surgical remediation paths.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Forensic Config")
    
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
        temperature = st.slider("Forensic Depth", 0.0, 1.0, 0.2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Data Import")
    if st.button("Load DB Timeout Example"):
        st.session_state.error_input_raw = "DatabaseConnectionError: Timeout while connecting to primary database"

# Layout Split
col_input, col_output = st.columns([1, 1.4])

with col_input:
    st.markdown('<div class="section-header">🛠️ Request Audit</div>', unsafe_allow_html=True)
    error_text = st.text_area(
        "Paste the raw error/log message below:",
        value=st.session_state.get("error_input_raw", ""),
        height=450,
        placeholder="ZeroDivisionError: division by zero..."
    )
    
    if st.button("🚀 Perform Diagnostic Forensics"):
        if error_text:
            with st.spinner("Analyzing error vectors and cross-referencing incident patterns..."):
                try:
                    # Save for agent read
                    with open("error.txt", "w", encoding="utf-8") as f:
                        f.write(error_text)
                        
                    report_data = classify_error_signals(error_text, model_name, api_key)
                    st.session_state.forensic_report = report_data
                    save_outputs(report_data)
                    st.success("Incident Report Synthesized!")
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
        else:
            st.warning("Please provide an error message first.")

with col_output:
    if "forensic_report" in st.session_state:
        data = st.session_state.forensic_report
        ar = data.get('audit_report', {})
        severity = ar.get('severity', 'moderate').lower()
        
        # Incident Summary Area
        st.markdown(f"""
            <div align="center" style="margin-bottom: 30px; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                <span class="severity-badge severity-{severity}">Severity: {severity}</span>
                <p style="margin-top: 15px; color: #94a3b8; font-size: 1.1rem;">Category: <strong>{ar.get('primary_category')}</strong></p>
                <p style="color: #64748b; font-style: italic;">{ar.get('logical_gist')}</p>
            </div>
        """, unsafe_allow_html=True)

        tab_diag, tab_fix, tab_mon = st.tabs(["🧬 Incident Diagnosis", "🛠️ Surgical Fix", "🛡️ SRE Standards"])
        
        with tab_diag:
            fb = data.get('forensic_breakdown', {})
            st.markdown(f'<div class="section-header">🧬 Forensic Breakdown</div>', unsafe_allow_html=True)
            st.markdown(f"**Root Cause Explanation**: {fb.get('root_cause_explanation')}")
            st.warning(f"**Impact Assessment**: {fb.get('impact_assessment')}")
            
            st.divider()
            st.markdown("#### Recognized Incident Patterns")
            for pattern in fb.get('recognized_patterns', []):
                st.info(f"🔍 Pattern: {pattern}")

        with tab_fix:
            st.markdown(f'<div class="section-header">🛠️ Remediation Blueprints</div>', unsafe_allow_html=True)
            for fix in data.get('surgical_remediation', []):
                st.markdown(f"**Action**: `{fix.get('action')}`")
                st.markdown(f"""
                    <div class="remediation-blueprint" style="border-left: 4px solid #3b82f6;">
                        <strong>GUIDE:</strong><br>{fix.get('remediation_blueprint')}
                    </div>
                """, unsafe_allow_html=True)
                st.divider()

        with tab_mon:
            st.markdown(f'<div class="section-header">🛡️ Monitoring & Excellence</div>', unsafe_allow_html=True)
            st.markdown("#### Logging & Metrics Standard")
            for tip in data.get('monitoring_guidelines', []):
                st.markdown(f"• {tip}")
                
            st.divider()
            st.markdown("#### Strategic SRE Pro-Tips")
            for tip in data.get('sre_expert_tips', []):
                st.success(f"▶ {tip}")
            
            st.download_button("📥 Export Diagnostic Object", json.dumps(data, indent=2), "error_diag.json", "application/json")
    else:
        st.info("Paste an error log and click 'Perform Diagnostic' to reveal forensic insights and surgical fixes.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Error-Forensics AI | Mastering System Reliability</div>", unsafe_allow_html=True)
