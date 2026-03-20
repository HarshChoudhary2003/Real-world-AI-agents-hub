import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import generate_outreach_strategy, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Influence-Core AI | Influencer Outreach Strategy",
    page_icon="🤝",
    layout="wide",
)

# Premium Animated Styling
st.markdown("""
    <style>
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main { background-color: #0c0a09; }
    .stApp { background: radial-gradient(circle at bottom left, #1c1917 0%, #0c0a09 100%); }
    
    .animated-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        animation: slideInUp 0.7s ease-out;
        transition: transform 0.3s ease, background 0.3s ease;
    }
    .animated-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid #d97706;
    }
    
    .social-preview {
        background: #1e1e1e;
        color: #e5e5e5;
        border-radius: 12px;
        padding: 20px;
        max-width: 500px;
        margin: 0 auto;
        border: 1px solid #444;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        animation: slideInUp 1s ease-out;
    }
    .strategy-chip {
        background: rgba(217, 119, 6, 0.15);
        color: #fbbf24;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
        border: 1px solid rgba(217, 119, 6, 0.3);
    }
    .section-header {
        color: #fafaf9;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 12px;
        border-right: 4px solid #d97706;
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
st.title("🤝 Influence-Core AI")
st.markdown("### Relationship-First Influencer Outreach Engine")
st.caption("Architect highly personalized, high-value-exchange outreach strategies with multi-model intelligence.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Strategy Config")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        # Provider Selection - Multi-Provider Standard
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
        temperature = st.slider("Outreach Creative Edge", 0.0, 1.0, 0.5)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Outreach Context")
    if st.button("Load LinkedIn Example"):
        st.session_state.outreach_input = """Brand: AI Productivity Platform
Campaign Goal: Promote new automation features
Influencer Platform: LinkedIn
Influencer Focus: Operations and productivity content
Audience: Mid-level managers and founders
Tone: Professional, respectful, collaborative"""

# Layout Split
col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.markdown('<div class="section-header">🛠️ Campaign Context</div>', unsafe_allow_html=True)
    outreach_context = st.text_area(
        "Define the influencer and campaign details:",
        value=st.session_state.get("outreach_input", ""),
        height=350,
        placeholder="e.g., Influencer: TechReviewer. Goal: Product Unboxing..."
    )
    
    if st.button("🚀 Architect Outreach Strategy"):
        if outreach_context:
            with st.spinner("Analyzing influencer context and synthesizing reciprocal value..."):
                try:
                    strategy = generate_outreach_strategy(outreach_context, model_name, api_key)
                    st.session_state.outreach_strategy = strategy
                    save_outputs(strategy)
                    st.success("Strategy Architected!")
                except Exception as e:
                    st.error(f"Strategy Error: {e}")
        else:
            st.warning("Please provide outreach context.")

with col_output:
    if "outreach_strategy" in st.session_state:
        data = st.session_state.outreach_strategy
        
        # Result View Tabs
        tab_social, tab_logic, tab_export = st.tabs(["💬 Platform Preview", "🧠 Strategic Pillars", "🗳️ Export"])
        
        with tab_social:
            st.markdown('<div class="section-header">📱 Outreach Previews</div>', unsafe_allow_html=True)
            
            # Show variants
            for msg_var in data.get("messages", []):
                variant_name = msg_var.get("variant_name", "Outreach")
                st.markdown(f"#### {variant_name}")
                
                # Visual Social Message
                if 'composition' in msg_var:
                    comp = msg_var.get('composition')
                    full_text = f"{comp.get('greeting')}\n\n{comp.get('opening')}\n\n{comp.get('value_proposition')}\n\n{comp.get('proposal')}\n\n{comp.get('call_to_action')}\n\n{comp.get('closing')}"
                else:
                    full_text = msg_var.get("full_text", "No message content.")
                
                st.markdown(f"""
                    <div class="social-preview">
                        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                            <div style="width: 40px; height: 40px; border-radius: 50%; background: #444;"></div>
                            <div style="display: flex; flex-direction: column;">
                                <span style="font-weight: 700; font-size: 0.9rem;">Brand Ambassador</span>
                                <span style="font-size: 0.75rem; color: #888;">Active now</span>
                            </div>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 0 12px 12px 12px; font-size: 0.95rem; line-height: 1.5; white-space: pre-wrap;">{full_text}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.write("")

        with tab_logic:
            st.markdown('<div class="section-header">🧪 Behavioral Logic</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Thematic Hooks")
                for anchor in data.get("psychological_anchors", []):
                    st.markdown(f'<span class="strategy-chip">{anchor}</span>', unsafe_allow_html=True)
            with col2:
                st.markdown("#### Reciprocity Angle")
                st.info(data.get("outreach_strategy", {}).get("reciprocity_angle", "Value exchange not clarified."))

            st.divider()
            st.markdown("#### Engagement Timing & Frequency")
            st.write(f"👁️ {data.get('follow_up_logic')}")

        with tab_export:
            st.markdown('<div class="section-header">🗳️ Data Exports</div>', unsafe_allow_html=True)
            
            st.download_button(
                "📥 Download Strategy JSON",
                data=json.dumps(data, indent=2),
                file_name=f"outreach_strategy_{date.today()}.json",
                mime="application/json"
            )
            
            st.download_button(
                "📝 Download Draft TXT",
                data=str(data),
                file_name=f"outreach_draft_{date.today()}.txt",
                mime="text/plain"
            )
            
            if st.button("📋 Copy Best Message Body"):
                st.toast("Copied to clipboard! (Simulated)")
    else:
        st.info("Input campaign details and click 'Architect Strategy' to generate outreach.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Influence-Core AI | Advanced Influencer Engine</div>", unsafe_allow_html=True)
