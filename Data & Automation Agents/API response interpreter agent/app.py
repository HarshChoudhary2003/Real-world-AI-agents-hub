import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import interpret_api_response, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="API-Insight AI | Forensic Diagnostic OS",
    page_icon="🔌",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes pulseShadow {
        0% { box-shadow: 0 0 5px rgba(56, 189, 248, 0.2); }
        50% { box-shadow: 0 0 25px rgba(56, 189, 248, 0.6); }
        100% { box-shadow: 0 0 5px rgba(56, 189, 248, 0.2); }
    }
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main { background-color: #0b0f1a; }
    .stApp { background: radial-gradient(circle at top right, #1a2236 0%, #0b0f1a 100%); }
    
    .diagnostic-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        animation: slideInUp 0.7s ease-out;
    }
    .severity-indicator {
        width: 100%;
        height: 8px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .severity-high { background: #ef4444; box-shadow: 0 0 10px #ef4444; }
    .severity-medium { background: #f59e0b; box-shadow: 0 0 10px #f59e0b; }
    .severity-low { background: #10b981; box-shadow: 0 0 10px #10b981; }

    .json-preview {
        background: #1e293b;
        color: #e2e8f0;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.1);
        height: 350px;
        overflow-y: auto;
    }
    .section-header {
        color: #e0f2fe;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .sidebar-section {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .fix-blueprint {
        background: rgba(16, 185, 129, 0.05);
        border: 1px dashed #10b981;
        padding: 15px;
        border-radius: 8px;
        color: #10b981;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("🔌 API-Insight AI")
st.markdown("### Forensic Payload & Status Diagnostic Engine")
st.caption("Perform deep neural analysis on JSON responses to architect surgical remediations.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ System Config")
    
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
        temperature = st.slider("Diagnostic Creativity", 0.0, 1.0, 0.2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Data Import")
    if st.button("Load Error 400 Example"):
        st.session_state.api_json_raw = """{
  "status": 400,
  "error": "InvalidRequest",
  "message": "Missing required field: email",
  "request_id": "abc-123"
}"""

# Layout Split
col_input, col_output = st.columns([1, 1.2])

with col_input:
    st.markdown('<div class="section-header">🛠️ Request Audit</div>', unsafe_allow_html=True)
    json_raw = st.text_area(
        "Paste the raw JSON response to audit:",
        value=st.session_state.get("api_json_raw", ""),
        height=350,
        placeholder="Paste JSON here..."
    )
    
    if st.button("🚀 Run Forensic Diagnostic"):
        if json_raw:
            with st.spinner("Analyzing payload integrity and root-cause logic..."):
                try:
                    diagnostic_data = interpret_api_response(json_raw, model_name, api_key)
                    st.session_state.api_diagnostic = diagnostic_data
                    save_outputs(diagnostic_data)
                    st.success("Diagnostic Ready!")
                except Exception as e:
                    st.error(f"Diagnostic Error: {e}")
        else:
            st.warning("Please provide an API response first.")

with col_output:
    if "api_diagnostic" in st.session_state:
        data = st.session_state.api_diagnostic
        
        ar = data.get('audit_report', {})
        severity = ar.get('severity', 'Low').lower()
        
        # Summary Area
        st.markdown(f"""
            <div class="diagnostic-card">
                <div class="severity-indicator severity-{severity}"></div>
                <h4 style="color: #e0f2fe; margin-bottom: 5px;">Summary: {ar.get('brief_executive_summary')}</h4>
                <p style="color: #94a3b8; font-size: 0.9rem;"><strong>Status Intent:</strong> {ar.get('http_status_intent')}</p>
            </div>
        """, unsafe_allow_html=True)

        tab_nodes, tab_errors, tab_security = st.tabs(["🏗️ Payload Nodes", "🚨 Error Forensics", "🛡️ Posture & Ops"])
        
        with tab_nodes:
            st.markdown('<div class="section-header">🏗️ Payload Schema Mapping</div>', unsafe_allow_html=True)
            for node in data.get('payload_nodes', []):
                st.markdown(f"""
                    <div class="diagnostic-card" style="padding: 15px; margin-bottom: 10px;">
                        <span style="font-weight: 800; color: #38bdf8;">[{node.get('status')}] {node.get('field')}</span><br>
                        <span style="color: #94a3b8; font-size: 0.85rem;">{node.get('intent')} | Type: {node.get('value_type')}</span>
                    </div>
                """, unsafe_allow_html=True)

        with tab_errors:
            st.markdown('<div class="section-header">🚨 Root Cause Forensics</div>', unsafe_allow_html=True)
            for err in data.get('root_cause_forensics', []):
                st.markdown(f"**Error Code**: `{err.get('error_code')}`")
                st.markdown(f"**Mechanical Reason**: *{err.get('mechanical_reason')}*")
                st.markdown(f"""
                    <div class="fix-blueprint">
                        <strong>Blueprint Fix:</strong><br>{err.get('fix_blueprint')}
                    </div>
                """, unsafe_allow_html=True)
                st.divider()

        with tab_security:
            st.markdown('<div class="section-header">🛡️ Security & Ops</div>', unsafe_allow_html=True)
            for signal in data.get('security_observations', []):
                st.warning(f"🔒 {signal}")
            
            st.divider()
            st.markdown("#### 🚀 Developer Next Actions")
            for action in data.get('ops_next_actions', []):
                st.success(f"▶ {action}")

            st.divider()
            st.download_button("📥 Export JSON Diagnostic", json.dumps(data, indent=2), "api_diag.json", "application/json")
    else:
        st.info("Paste an API response and click 'Run Forensic' to reveal the diagnostic signals.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with API-Insight AI | Maintaining Payload Purity</div>", unsafe_allow_html=True)
