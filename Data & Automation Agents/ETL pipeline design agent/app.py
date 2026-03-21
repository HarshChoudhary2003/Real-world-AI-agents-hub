import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import read_input, design_etl_pipeline, save_outputs

# Set Page Config
st.set_page_config(
    page_title="Pipeline-Forge AI | Cloud Data Architect",
    page_icon="💾",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes lineFlow {
        0% { stroke-dashoffset: 100; opacity: 0.3; }
        100% { stroke-dashoffset: 0; opacity: 1; }
    }
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(25px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main { background-color: #0c0a09; }
    .stApp { background: radial-gradient(circle at center, #111827 0%, #0c0a09 100%); }
    
    .etl-node {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        animation: fadeInSlide 0.7s ease-out;
        border-top: 4px solid #10b981;
    }
    .etl-node:nth-child(2) { border-top-color: #3b82f6; animation-delay: 0.1s; }
    .etl-node:nth-child(3) { border-top-color: #f59e0b; animation-delay: 0.2s; }

    .pulse-glow {
        color: #10b981;
        font-weight: 800;
        text-shadow: 0 0 10px #10b981;
    }
    .section-header {
        color: #f8fafc;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 15px;
        border-right: 4px solid #10b981;
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
    .logic-step {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("💾 Pipeline-Forge AI")
st.markdown("### Cloud Data Ingestion & ETL Flow Architect")
st.caption("Architect high-performance ETL pipelines with neural flow synthesis and scalability diagnostics.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Ingestion Config")
    
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
        temperature = st.slider("Architectural Creativity", 0.0, 1.0, 0.3)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Ingestion Context")
    if st.button("Load CRM Postgres Example"):
        st.session_state.etl_input_raw = """Source: CRM database (PostgreSQL)
Target: Data warehouse
Transformations:
- Clean customer emails
- Normalize country codes
- Aggregate monthly activity
Frequency: Daily
Volume: 5 million records"""

# Layout Split
col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.markdown('<div class="section-header">🛠️ Request Blueprint</div>', unsafe_allow_html=True)
    request_text = st.text_area(
        "Define your ETL requirements below:",
        value=st.session_state.get("etl_input_raw", ""),
        height=450,
        placeholder="Sources: API1, API2. Target: Snowflake. Logic: Join user data..."
    )
    
    if st.button("🚀 Architect Pipeline Design"):
        if request_text:
            with st.spinner("Synthesizing data flow, mapping partitions, and resolving schema logic..."):
                try:
                    # Save for agent read
                    with open("input.txt", "w", encoding="utf-8") as f:
                        f.write(request_text)
                        
                    pb_data = design_etl_pipeline(request_text, model_name, api_key)
                    st.session_state.pb_audit = pb_data
                    save_outputs(pb_data)
                    st.success("Pipeline Architecture Synced!")
                except Exception as e:
                    st.error(f"Design failure: {e}")
        else:
            st.warning("Please provide requirements first.")

with col_output:
    if "pb_audit" in st.session_state:
        data = st.session_state.pb_audit
        pb = data.get('pipeline_blueprint', {})
        
        # Dashboard Area
        st.markdown(f"**Architecture**: `{pb.get('architecture_style')}` | **Complexity**: `{pb.get('complexity_level')}`")
        st.markdown(f"*{pb.get('strategic_overview')}*")
        
        # Horizontal ETL Tabs
        st.divider()
        tab_flow, tab_meta, tab_export = st.tabs(["🚀 ETL Flow Map", "🧬 SRE & Ops", "📦 Design Package"])
        
        with tab_flow:
            col_e, col_t, col_l = st.columns(3)
            
            with col_e:
                st.markdown(f'<div class="etl-node"><h4>📡 EXTRACT</h4>', unsafe_allow_html=True)
                for item in data.get('extraction_protocol', []):
                    st.markdown(f"**{item.get('component')}**")
                    st.caption(f"Strategy: {item.get('strategy')}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_t:
                st.markdown(f'<div class="etl-node"><h4>🧬 TRANSFORM</h4>', unsafe_allow_html=True)
                for item in data.get('transformation_logic', []):
                    st.markdown(f"**{item.get('operation')}**")
                    st.caption(f"Logic: {item.get('performance_logic')}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_l:
                st.markdown(f'<div class="etl-node"><h4>💾 LOAD</h4>', unsafe_allow_html=True)
                for item in data.get('loading_strategy', []):
                    st.markdown(f"**{item.get('target')}**")
                    st.caption(f"Method: {item.get('method')}")
                st.markdown('</div>', unsafe_allow_html=True)

        with tab_meta:
            st.markdown('<div class="section-header">🛡️ Reliability & Observability</div>', unsafe_allow_html=True)
            sla = data.get('monitoring_and_slas', {})
            st.info(f"**Observability**: {sla.get('observability')}")
            st.warning(f"**Recovery Objective**: {sla.get('recovery_objective')}")
            
            st.divider()
            st.markdown("#### 🛠️ Architect Pro-Tips")
            for tip in data.get('architect_pro_tips', []):
                st.success(f"▶ {tip}")

        with tab_export:
            st.markdown('<div class="section-header">🗳️ Deployment Package</div>', unsafe_allow_html=True)
            st.download_button("📥 Export Logic JSON", json.dumps(data, indent=2), "etl_arch.json", "application/json")
            st.download_button("📝 Download Design Document", str(data), "etl_design.txt", "text/plain")
            
    else:
        st.info("Input requirements and click 'Architect' to generate the ETL design manifold.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Pipeline-Forge AI | Mastering Ingestion Integrity</div>", unsafe_allow_html=True)
