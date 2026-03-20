import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import generate_email_strategy, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Email-Mind AI | Advanced Copywriting Strategy",
    page_icon="📩",
    layout="wide",
)

# Premium Animated Styling
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main { background-color: #0f172a; }
    .stApp { background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 100%); }
    
    .animated-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        animation: fadeIn 0.6s ease-out;
        transition: all 0.3s ease;
    }
    .animated-card:hover {
        border: 1px solid #38bdf8;
        background: rgba(255, 255, 255, 0.05);
        transform: scale(1.01);
    }
    
    .email-preview {
        background: white;
        color: #334155;
        border-radius: 20px;
        padding: 40px;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        border: 12px solid #334155;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .subject-pill {
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 8px;
    }
    .section-header {
        color: #f1f5f9;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sidebar-section {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
    }
    .cta-button {
        display: inline-block;
        background: #38bdf8;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("📩 Email-Mind AI")
st.markdown("### High-Conversion Multi-Model Copywriting Engine")
st.caption("Generate psychologically-grounded email campaigns with animated previews and strategic frameworks.")

# Sidebar - Multi-Provider Standard
with st.sidebar:
    st.header("⚙️ Neural Config")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        # Provider-first Selection
        provider = st.selectbox(
            "Select Intelligence Provider",
            ["OpenAI", "Google Gemini", "Anthropic Claude", "DeepSeek", "Groq (Llama 3)", "Custom"]
        )

        if provider == "OpenAI":
            model_name = st.selectbox("Select Model", ["gpt-4o-mini", "gpt-4o", "o1-preview"])
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
        temperature = st.slider("Copywriting Creativity", 0.0, 1.0, 0.6)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Campaign Input")
    if st.button("Load Re-engagement Example"):
        st.session_state.email_input = """Campaign Goal: Re-engage inactive users
Audience: Trial users inactive for 30 days
Email Type: Re-engagement
Offer: New automation templates
Brand Tone: Friendly, professional"""

# Layout Divide
col_input, col_output = st.columns([1, 1.4])

with col_input:
    st.markdown('<div class="section-header">🛠️ Campaign Architect</div>', unsafe_allow_html=True)
    campaign_context = st.text_area(
        "Define your campaign parameters:",
        value=st.session_state.get("email_input", ""),
        height=350,
        placeholder="e.g., Offer: 20% off yearly plan\nTarget: Recently churned users..."
    )
    
    if st.button("🚀 Generate Email Strategy"):
        if campaign_context:
            with st.spinner("Synthesizing copy and psychological triggers..."):
                try:
                    strategy = generate_email_strategy(campaign_context, model_name, api_key)
                    st.session_state.email_strategy = strategy
                    save_outputs(strategy)
                    st.success("Strategy Synthesized!")
                except Exception as e:
                    st.error(f"Generation failed: {e}")
        else:
            st.warning("Please provide campaign context.")

with col_output:
    if "email_strategy" in st.session_state:
        data = st.session_state.email_strategy
        
        # Tabs for result viewing
        tab_preview, tab_strategy, tab_export = st.tabs(["📱 Inbox Preview", "🧩 Strategic Breakdown", "📦 Export"])
        
        with tab_preview:
            st.markdown('<div class="section-header">📬 Mobile Preview</div>', unsafe_allow_html=True)
            
            # Fix: Calculate body with break lines outside the f-string for Python <3.12 compatibility
            email_body_html = data.get('email_content', {}).get('body', 'Your content goes here.').replace('\n', '<br>')
            
            # Simulated Email App
            with st.container():
                st.markdown(f"""
                <div class="animated-card" style="max-width: 600px; margin: 0 auto; background: white; color: black; padding: 0; overflow: hidden; border: 8px solid #1e293b; border-radius: 40px;">
                    <div style="background: #f8fafc; padding: 20px; border-bottom: 1px solid #e2e8f0;">
                         <div style="font-size: 14px; color: #64748b;">To: customer@example.com</div>
                         <div style="font-weight: bold; margin-top: 5px;">Subject: {data.get('subject_line_options', [{}])[0].get('text', 'No Subject')}</div>
                    </div>
                    <div style="padding: 40px; font-family: sans-serif; line-height: 1.6;">
                        <p>{data.get('email_content', {}).get('salutation', 'Hi there,')}</p>
                        <p>{email_body_html}</p>
                        <div style="text-align: center; margin: 40px 0;">
                            <a href="#" style="background: #38bdf8; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold;">{data.get('call_to_action', {}).get('text', 'Get Started')}</a>
                        </div>
                        <p style="color: #64748b; font-size: 14px; margin-top: 40px;">{data.get('email_content', {}).get('footer', 'Best, The Team')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with tab_strategy:
            st.markdown('<div class="section-header">🧪 Psychological Composition</div>', unsafe_allow_html=True)
            
            st.markdown(f"**Copywriting Framework**: `{data.get('copywriting_framework_used', 'N/A')}`")
            
            st.markdown("#### Dynamic Subject Lines")
            for subj in data.get("subject_line_options", []):
                st.markdown(f"""
                <div class="animated-card">
                    <span class="subject-pill">{subj.get('type')}</span>
                    <span style="color: #f1f5f9;">{subj.get('text')}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### Triggers & Logic")
            cols = st.columns(2)
            with cols[0]:
                st.info(f"**CTA Strategy**: {data.get('call_to_action', {}).get('logic')}")
            with cols[1]:
                st.success(f"**Active Triggers**: {', '.join(data.get('psychological_triggers', []))}")

        with tab_export:
            st.markdown('<div class="section-header">📦 Package Exports</div>', unsafe_allow_html=True)
            
            st.download_button(
                "📥 Download Campaign JSON",
                data=json.dumps(data, indent=2),
                file_name=f"email_strategy_{date.today()}.json",
                mime="application/json"
            )
            
            st.download_button(
                "📝 Download Draft TXT",
                data=str(data),
                file_name=f"email_draft_{date.today()}.txt",
                mime="text/plain"
            )
            
            if st.button("📋 Copy Email Body"):
                st.write("Email body copied to clipboard! (Simulated)")
                st.toast("Copied to clipboard!")
    else:
        st.info("Input campaign details and click 'Generate Strategy' to craft your email.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Email-Mind AI | Advanced Copywriting OS</div>", unsafe_allow_html=True)
