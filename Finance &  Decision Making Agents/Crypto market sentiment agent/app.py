import streamlit as st
import json
import pandas as pd
import plotly.express as px
from agent import analyze_sentiment, save_outputs
import os
from datetime import date

# Set page config
st.set_page_config(
    page_title="Crypto Sentiment | Intelligence Agent",
    page_icon="🪙",
    layout="wide"
)

# Custom CSS for a clean, professional "simple" look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #6B7280;
        margin-bottom: 2rem;
    }
    
    .sentiment-card {
        padding: 1.5rem;
        border-radius: 0.75rem;
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
    
    .sentiment-label {
        font-size: 0.875rem;
        color: #6B7280;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    .sentiment-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #111827;
    }
</style>
""", unsafe_allow_html=True)

# Layout
st.markdown('<div class="main-header">Crypto Sentiment Core</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered qualitative data synthesis and sentiment auditing.</div>', unsafe_allow_html=True)

col_ctrl, col_res = st.columns([1, 2], gap="large")

with col_ctrl:
    st.subheader("Configuration")
    model_choice = st.selectbox("Intelligence Core", ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet-20240620", "gemini-1.5-pro"])
    
    st.info("The agent analyzes news, social feeds, and technical signals to generate a synthesized sentiment score.")
    
    if st.button("Run Neural Audit", type="primary", use_container_width=True):
        with st.spinner("Analyzing signals..."):
            try:
                # Read from input file
                with open("sentiment_input.txt", "r", encoding="utf-8") as f:
                    input_text = f.read()
                
                # Perform analysis
                data = analyze_sentiment(input_text, model_name=model_choice)
                save_outputs(data)
                
                st.session_state['latest_data'] = data
                st.success("Analysis Complete.")
            except Exception as e:
                st.error(f"Error: {e}")

with col_res:
    if 'latest_data' in st.session_state:
        data = st.session_state['latest_data']
        
        # Performance Indicators
        idx1, idx2, idx3 = st.columns(3)
        with idx1:
            st.markdown(f'<div class="sentiment-card"><div class="sentiment-label">Sentiment Score</div><div class="sentiment-value">{data["sentiment_score"]}/100</div></div>', unsafe_allow_html=True)
        with idx2:
            st.markdown(f'<div class="sentiment-card"><div class="sentiment-label">Overall Sentiment</div><div class="sentiment-value">{data["overall_sentiment"]}</div></div>', unsafe_allow_html=True)
        with idx3:
            st.markdown(f'<div class="sentiment-card"><div class="sentiment-label">Confidence</div><div class="sentiment-value">{data["confidence_level"]}</div></div>', unsafe_allow_html=True)
        
        # Tabs for details
        tab1, tab2 = st.tabs(["Signals Audit", "Executive Summary"])
        
        with tab1:
            st.markdown("### Detected Signals")
            for signal in data.get("supporting_signals", []):
                with st.expander(f"{signal.get('source')} | {signal.get('signal')}", expanded=True):
                    st.write(signal.get('summary'))
            
            st.markdown("### Divergence Detection")
            st.warning(data.get("divergence_notes", "No significant divergence detected."))
            
        with tab2:
            st.markdown("### Strategic Analysis")
            st.write(data.get("executive_summary"))
            
            st.divider()
            st.markdown(f"**Asset State:** {data.get('trend_direction')}")
            st.caption(f"Audit timestamp: {date.today()}")
    else:
        st.info("Configure the agent on the left and click 'Run Neural Audit' to start.")
        
        # Placeholder
        st.image("https://images.unsplash.com/photo-1621761191319-c6fb62004040?q=80&w=2000&auto=format&fit=crop", caption="Awaiting intelligence feed...")
