import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import load_data, validate_data_mechanically, generate_validation_insights, save_outputs

# Set Page Config
st.set_page_config(
    page_title="Data-Guard AI | Multi-Schema Integrity Engine",
    page_icon="🛡️",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.8); }
        100% { box-shadow: 0 0 5px rgba(239, 68, 68, 0.4); }
    }
    .main { background-color: #0c0a09; }
    .stApp { background: radial-gradient(circle at bottom center, #1c1917 0%, #0c0a09 100%); }
    
    .status-badge {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .status-fail { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid #ef4444; animation: pulseGlow 3s infinite; }
    .status-pass { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid #10b981; }
    
    .violation-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 5px solid #ef4444;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        animation: fadeIn 0.7s ease-out;
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
    .blueprint-step {
        background: rgba(16, 185, 129, 0.05);
        border: 1px dashed #10b981;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #10b981;
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("🛡️ Data-Guard AI")
st.markdown("### Neural Dataset Integrity & Schema Governance OS")
st.caption("Perform hybrid mechanical and AI-driven audits to enforce high-fidelity data quality standards.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Guard Config")
    
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
        temperature = st.slider("Forensic Creativity", 0.0, 1.0, 0.2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Data Import")
    if st.button("Load Transaction Dataset"):
        st.session_state.raw_data_csv = """order_id,amount,currency,order_date
1001,250,USD,2024-05-10
1002,-30,USD,2024-05-12
1003,120,EUR,invalid_date"""

# Layout Split
col_input, col_output = st.columns([1, 1.4])

with col_input:
    st.markdown('<div class="section-header">🛠️ Request Audit</div>', unsafe_allow_html=True)
    raw_csv = st.text_area(
        "Paste the raw CSV data to audit:",
        value=st.session_state.get("raw_data_csv", ""),
        height=400,
        placeholder="order_id,amount,currency..."
    )
    
    if st.button("🚀 Run Deep Integrity Audit"):
        if raw_csv:
            with st.spinner("Analyzing data vectors and cross-referencing schema rules..."):
                try:
                    # Temporary save to CSV
                    with open("input_data.csv", "w", encoding="utf-8") as f:
                        f.write(raw_csv)
                    
                    df = load_data()
                    errors = validate_data_mechanically(df)
                    insights = generate_validation_insights(errors, model_name, api_key)
                    st.session_state.guard_audit = (errors, insights, df)
                    save_outputs(errors, insights)
                    st.success("Integrity Report Generated!")
                except Exception as e:
                    st.error(f"Audit Error: {e}")
        else:
            st.warning("Please provide a dataset first.")

with col_output:
    if "guard_audit" in st.session_state:
        errors, insights, df = st.session_state.guard_audit
        status = "fail" if errors else "pass"
        
        # Summary Header
        st.markdown(f"""
            <div align="center" style="margin-bottom: 30px;">
                <span class="status-badge status-{status}">Global Status: {status}</span>
                <p style="margin-top: 15px; color: #94a3b8; font-style: italic;">{insights.get('forensic_summary')}</p>
            </div>
        """, unsafe_allow_html=True)

        tab_violations, tab_forensics, tab_data = st.tabs(["🛡️ Mechanical Audit", "🧬 Forensic Insights", "📊 Raw Data Grid"])
        
        with tab_violations:
            st.markdown('<div class="section-header">🛡️ Rule Performance Map</div>', unsafe_allow_html=True)
            for e in errors:
                st.markdown(f"""
                    <div class="violation-card" style="border-left-color: {'#ef4444' if e['severity'] == 'critical' else '#f59e0b'};">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="font-weight: 800; color: #f8fafc;">{e['rule'].upper()}</span>
                            <span style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 2px 10px; border-radius: 99px; font-size: 0.7rem; font-weight: 800;">{e['severity'].upper()}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.9rem;">{e['description']}</p>
                        <p style="color: #94a3b8; font-size: 0.8rem;">Affected Row Indices: <strong>{e['rows']}</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            
            if not errors:
                st.success("🎉 No mechanical violations detected. Data is structurally sound.")

        with tab_forensics:
            st.markdown('<div class="section-header">🧬 Forensic Deep Dives</div>', unsafe_allow_html=True)
            for dive in insights.get('violation_deep_dives', []):
                st.markdown(f"**Violation**: `{dive.get('rule')}` | **Impact**: *{dive.get('mechanical_reason')}*")
                st.markdown(f"""
                    <div class="blueprint-step" style="border-style: solid; border-width: 1px; color: #facc15; border-color: rgba(250, 204, 21, 0.3);">
                        <strong>SURGICAL FIX:</strong><br>{dive.get('surgical_fix')}
                    </div>
                """, unsafe_allow_html=True)
                st.divider()
            
            st.divider()
            st.markdown("#### ⚡ Pipeline Hardening Plan")
            for rec in insights.get('strategic_recommendations', []):
                st.success(f"▶ {rec}")

        with tab_data:
            st.markdown('<div class="section-header">📊 Transaction Dataset Browser</div>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
    else:
        st.info("Input a CSV dataset and click 'Run Integrity Audit' to perform a neural forensic review.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Data-Guard AI | Guarding the Purity of Data</div>", unsafe_allow_html=True)
