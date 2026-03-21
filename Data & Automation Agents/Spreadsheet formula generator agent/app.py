import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import generate_sheet_logic, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Sheet-Logic AI | Multi-Platform Data Architect",
    page_icon="📊",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main { background-color: #0c0a09; }
    .stApp { background: radial-gradient(circle at bottom center, #1c1917 0%, #0c0a09 100%); }
    
    .formula-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 24px;
        animation: fadeIn 0.7s ease-out;
    }
    .formula-code {
        background: #1e1b1e;
        color: #10b981;
        padding: 20px;
        border-radius: 8px;
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 1.2rem;
        border-left: 5px solid #10b981;
        margin-top: 15px;
        white-space: pre-wrap;
    }
    .step-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .complexity-chip {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
    }
    .section-header {
        color: #fafaf9;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 12px;
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
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("📊 Sheet-Logic AI")
st.markdown("### Multi-Platform Data & Formula Architect")
st.caption("Generate high-performance spreadsheet formulas with real-time logic synthesis and technical breakdowns.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Strategy Config")
    
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
        temperature = st.slider("Logical Precision", 0.0, 1.0, 0.2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Data Context")
    if st.button("Load Conditional Sum Example"):
        st.session_state.sheet_input = """Platform: Excel
Request: Calculate the total sales in column C only for rows where column B is 'Completed' and column D is greater than 100."""

# Layout Split
col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.markdown('<div class="section-header">🛠️ Request Architect</div>', unsafe_allow_html=True)
    request_text = st.text_area(
        "Define your formula request in plain English:",
        value=st.session_state.get("sheet_input", ""),
        height=350,
        placeholder="e.g., Sum column A if column B starts with 'PROD'..."
    )
    
    if st.button("🚀 Synthesize Formula Architecture"):
        if request_text:
            with st.spinner("Analyzing spreadsheet logic and cross-referencing platform syntax..."):
                try:
                    logic_data = generate_sheet_logic(request_text, model_name, api_key)
                    st.session_state.sheet_logic = logic_data
                    save_outputs(logic_data)
                    st.success("Logic Synthesized!")
                except Exception as e:
                    st.error(f"Logic Error: {e}")
        else:
            st.warning("Please provide a formula request first.")

with col_output:
    if "sheet_logic" in st.session_state:
        data = st.session_state.sheet_logic
        
        # Result Tabs
        tab_formula, tab_technical, tab_validated = st.tabs(["🚀 Primary Formula", "🧬 Technical Breakdown", "📦 Package Export"])
        
        with tab_formula:
            st.markdown('<div class="section-header">🔍 Synthesized Output</div>', unsafe_allow_html=True)
            
            pm = data.get('project_meta', {})
            st.markdown(f"**Platform**: `{pm.get('platform')}` | **Complexity**: `{pm.get('complexity_level')}`")
            
            st.markdown(f"""
                <div class="formula-card">
                    <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 700;">FINAL FORMULA</span>
                    <div class="formula-code" id="formula-text">{data.get('primary_formula', 'N/A')}</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 Copy Formula"):
                st.toast("Formula copied to clipboard! (Simulated)")

        with tab_technical:
            st.markdown('<div class="section-header">🧬 Component Logic Decomposition</div>', unsafe_allow_html=True)
            
            for step in data.get('technical_breakdown', []):
                st.markdown(f"""
                    <div class="step-card">
                        <span style="font-weight: 800; color: #10b981;">{step.get('step')}</span><br>
                        <span style="color: #94a3b8; font-size: 0.9rem;">{step.get('explanation')}</span>
                    </div>
                """, unsafe_allow_html=True)

            st.divider()
            st.markdown("#### Alternative Methods")
            for alt in data.get('alternative_methods', []):
                st.info(f"**{alt.get('name')}**: `{alt.get('formula_or_method')}`")

        with tab_validated:
            st.markdown('<div class="section-header">🛡️ Validation & Guardrails</div>', unsafe_allow_html=True)
            for rule in data.get('validation_rules', []):
                st.warning(rule)
            
            st.divider()
            st.markdown("#### 💡 Pro-Tips")
            for tip in data.get('pro_tips', []):
                st.success(tip)

            st.divider()
            st.download_button(
                "📥 Export Logic JSON",
                data=json.dumps(data, indent=2),
                file_name=f"sheet_logic_{date.today()}.json",
                mime="application/json"
            )
            
            st.download_button(
                "📝 Download Draft Summary",
                data=str(data),
                file_name=f"sheet_draft_{date.today()}.txt",
                mime="text/plain"
            )
    else:
        st.info("Input a request and click 'Synthesize' to reveal the data architecture.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Sheet-Logic AI | Mastering Data One Formula at a Time</div>", unsafe_allow_html=True)
