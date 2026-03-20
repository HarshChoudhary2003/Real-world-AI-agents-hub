import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import build_persona, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Persona-Forge AI | Advanced Customer Research",
    page_icon="🛡️",
    layout="wide",
)

# Premium Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1c1e26 100%);
    }
    .persona-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .persona-title {
        color: #ff9d00;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem;
    }
    .persona-archetype {
        color: #00d4ff;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.9rem;
    }
    .section-header {
        color: #f0f2f6;
        border-bottom: 2px solid #ff9d00;
        padding-bottom: 5px;
        margin-top: 25px;
        margin-bottom: 15px;
        font-size: 1.4rem;
        font-weight: 700;
    }
    .metric-box {
        background: rgba(0, 212, 255, 0.1);
        border-left: 5px solid #00d4ff;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .sidebar-section {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff9d00 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px !important;
        font-weight: bold !important;
        transition: 0.3s all ease;
    }
    .stButton>button:hover {
        background-color: #e68a00 !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Application Logo and Title
st.title("🛡️ Persona-Forge AI")
st.markdown("### Advanced Customer Persona Synthesis Engine")
st.caption("Synthesize raw market data into deep, actionable customer personas using multi-model AI.")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        # AI Provider Selection
        provider = st.selectbox(
            "Select Intelligence Provider",
            ["OpenAI", "Google Gemini", "Anthropic Claude", "DeepSeek", "Groq (Llama 3)", "Custom"]
        )

        # Dynamic Model Selection based on Provider
        if provider == "OpenAI":
            model_name = st.selectbox("Select Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
        elif provider == "Google Gemini":
            model_name = st.selectbox("Select Model", ["gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash"])
        elif provider == "Anthropic Claude":
            model_name = st.selectbox("Select Model", ["claude-3-5-sonnet-20240620", "claude-3-opus-20240401"])
        elif provider == "DeepSeek":
            model_name = st.selectbox("Select Model", ["deepseek/deepseek-chat"])
        elif provider == "Groq (Llama 3)":
            model_name = st.selectbox("Select Model", ["groq/llama-3.1-70b-versatile", "groq/llama-3.1-8b-instant"])
        else:
            model_name = st.text_input("Enter LiteLLM Model ID (e.g., perplexity/llama-3-sonar-large-32k-online)", "")

        api_key = st.text_input("Provider API Key (Optional)", type="password", help="Leave blank if using environment variables (.env)")
        temperature = st.slider("Synthesis Creativity", 0.0, 1.0, 0.4)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Data Import")
    uploaded_file = st.file_uploader("Upload Market Context (TXT)", type=["txt"])
    
    # Example Data
    if st.button("Load Example Context"):
        st.session_state.market_context = """Product: B2B Workflow Automation Tool
Target Segment: Mid-level operations managers at mid-sized companies

Data:
- Responsible for efficiency improvements
- Limited technical background
- Measured on cost savings and process speed

Challenges:
- Manual workflows
- Tool overload"""

# Main Content Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="section-header">🔍 Market Data Context</div>', unsafe_allow_html=True)
    
    # Context Input
    market_context = st.text_area(
        "Paste product info, target segments, and raw data below:",
        value=st.session_state.get("market_context", ""),
        height=350,
        placeholder="e.g., Product: Luxury Coffee Gear\nTarget: Urban professionals 25-45..."
    )
    
    if uploaded_file is not None:
        market_context = str(uploaded_file.read(), "utf-8")
        st.text_area("Uploaded Context", value=market_context, height=150)

    if st.button("⚡ Synthesize Persona"):
        if market_context:
            with st.spinner("Analyzing market patterns & synthesizing persona..."):
                try:
                    persona_data = build_persona(market_context, model_name, api_key)
                    st.session_state.persona_data = persona_data
                    save_outputs(persona_data)
                    st.success("Synthesis Complete!")
                except Exception as e:
                    st.error(f"Synthesis failed: {e}")
        else:
            st.warning("Please provide market data first.")

with col2:
    st.markdown('<div class="section-header">🤖 Generated Persona Strategy</div>', unsafe_allow_html=True)
    
    if "persona_data" in st.session_state:
        data = st.session_state.persona_data
        
        # Display Card
        st.markdown(f"""
            <div class="persona-card">
                <div class="persona-archetype">{data.get('archetype', 'UNDEFINED')}</div>
                <div class="persona-title">{data.get('persona_name', 'Unnamed Persona')}</div>
                <p style="font-style: italic; color: #ced4da; margin-bottom: 20px;">{data.get('overview', 'No summary available.')}</p>
            </div>
        """, unsafe_allow_html=True)

        # Tabs for details
        tab1, tab2, tab3, tab4 = st.tabs(["📑 Background", "🎯 Psychology", "📈 Messaging", "⚔️ Objections"])
        
        with tab1:
            st.markdown("#### Context & Role")
            st.write(data.get("demographics_and_role"))
            
            st.markdown("#### Goals & Objectives")
            for goal in data.get("goals", []):
                st.markdown(f"- **{goal}**")

        with tab2:
            st.markdown("#### Motivations")
            for motivation in data.get("core_motivations", []):
                st.markdown(f"- {motivation}")
            
            st.markdown("#### Pain Points")
            for pp in data.get("pain_points", []):
                st.markdown(f"- {pp}")
                
            st.markdown("#### Fears & Anxieties")
            for f in data.get("fears_and_anxieties", []):
                st.warning(f)

        with tab3:
            ms = data.get("messaging_strategy", {})
            st.markdown("#### Strategic Hooks")
            for hook in ms.get("hooks", []):
                st.info(f"🪝 {hook}")
                
            col_words, col_trust = st.columns(2)
            with col_words:
                st.markdown("#### Power Words")
                st.write(", ".join(ms.get("power_words", [])))
            with col_trust:
                st.markdown("#### Trust Signals")
                st.write(", ".join(ms.get("trust_signals", [])))

        with tab4:
            st.markdown("#### Buying Objections")
            for obj in data.get("buying_objections", []):
                st.error(obj)

        # Export Actions
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "📥 Download JSON",
                data=json.dumps(data, indent=2),
                file_name=f"persona_{date.today()}.json",
                mime="application/json"
            )
        with c2:
            # Simple text format for download
            text_str = f"Persona: {data.get('persona_name')}\nArchetype: {data.get('archetype')}\n\n{data.get('overview')}"
            st.download_button(
                "📝 Download Summary",
                data=text_str,
                file_name=f"persona_{date.today()}.txt",
                mime="text/plain"
            )
    else:
        st.info("Input market data and click 'Synthesize' to build the persona.")

# Footer
st.markdown("---")
st.markdown("Developed by Antigravity | Advanced Agentic Coding for Real-world Hub")
