import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import generate_launch_checklist, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Launch-Pad AI | Advanced GTM Checklist",
    page_icon="🚀",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .main { background-color: #020617; }
    .stApp { background: radial-gradient(circle at top right, #1e1b4b 0%, #020617 100%); }
    
    .checklist-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        animation: slideInRight 0.6s ease-out;
    }
    .phase-badge {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .task-item {
        color: #f1f5f9;
        font-size: 1rem;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .owner-tag {
        color: #94a3b8;
        font-size: 0.85rem;
    }
    .section-header {
        color: #f8fafc;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .sidebar-section {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .progress-container {
        margin-bottom: 30px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Application Logo & Title
st.title("🚀 Launch-Pad AI")
st.markdown("### GTM Operational Readiness & Launch Architecture")
st.caption("Strategic launch checklists with Multi-Provider intelligence and real-time phase tracking.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Strategy Brain")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        # Provider Selection - Global Project Standard
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
        temperature = st.slider("Strategy Creative Edge", 0.0, 1.0, 0.3)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Launch Context")
    if st.button("Load Standard Launch Example"):
        st.session_state.launch_input = """Product: AI Workflow Automation Feature
Launch Type: Public release
Audience: Mid-sized business operations teams
Channels: Website, Email, Social media
Timeline: Launch in 3 weeks"""

# Main Content Layout
col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.markdown('<div class="section-header">🛠️ Launch Architect</div>', unsafe_allow_html=True)
    launch_text = st.text_area(
        "Define your product and launch objectives:",
        value=st.session_state.get("launch_input", ""),
        height=350,
        placeholder="e.g., Product: SaaS Dashboard. Goal: 100 signups..."
    )
    
    if st.button("🚀 Synthesize Launch Checklist"):
        if launch_text:
            with st.spinner("Analyzing GTM requirements and synthesizing checklists..."):
                try:
                    checklist = generate_launch_checklist(launch_text, model_name, api_key)
                    st.session_state.launch_checklist = checklist
                    save_outputs(checklist)
                    st.success("GTM Strategy Ready!")
                except Exception as e:
                    st.error(f"Strategy Error: {e}")
        else:
            st.warning("Please provide launch context first.")

with col_output:
    if "launch_checklist" in st.session_state:
        data = st.session_state.launch_checklist
        
        # Launch Identity Card
        li = data.get('launch_identity', {})
        st.markdown(f"""
            <div class="checklist-card" style="border-top-color: #fbbf24;">
                <div class="phase-badge" style="background: rgba(251, 191, 36, 0.1); color: #fbbf24;">MISSION: {li.get('codename', 'CODENAME')}</div>
                <h2 style="margin-top: 10px; color: #f8fafc;">{li.get('value_hook', 'Value Proposition')}</h2>
            </div>
        """, unsafe_allow_html=True)

        # Tabs for result viewing
        tab_flow, tab_channels, tab_risk = st.tabs(["🚀 Launch Phasing", "📡 Channel Focus", "🛡️ Risk Shield"])
        
        with tab_flow:
            st.markdown('<div class="section-header">🗓️ Chronological Phasing</div>', unsafe_allow_html=True)
            
            phases = data.get('phases', {})
            
            # Pre-Launch
            st.markdown("### 🏗️ Pre-Launch (Warm-up)")
            for item in phases.get('pre_launch', []):
                st.checkbox(f"**{item.get('task')}** (Owner: {item.get('role', 'N/A') or item.get('owner', 'N/A')})", key=f"pre_{item.get('task')}")
            
            st.divider()
            
            # Launch Day
            st.markdown("### 🚀 Launch Day (Execution)")
            for item in phases.get('launch_day', []):
                st.checkbox(f"**{item.get('task')}** (Urgency: {item.get('urgency', 'Med')})", key=f"day_{item.get('task')}")

            st.divider()

            # Post-Launch
            st.markdown("### 📈 Post-Launch (Momentum)")
            for item in phases.get('post_launch', []):
                st.checkbox(f"**{item.get('task')}** (Metric: {item.get('metric_to_track')})", key=f"post_{item.get('task')}")

        with tab_channels:
            st.markdown('<div class="section-header">📡 Channel-Specific Tasks</div>', unsafe_allow_html=True)
            
            channels = data.get('channel_specific_tasks', {})
            for channel, tasks in channels.items():
                with st.expander(f"{channel.capitalize()} Tasks", expanded=True):
                    for task in tasks:
                        st.markdown(f"✅ {task}")

        with tab_risk:
            st.markdown('<div class="section-header">🛡️ Risk Mitigation Shield</div>', unsafe_allow_html=True)
            for risk in data.get("risk_mitigation", []):
                st.warning(risk)

        # Export Options
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "📥 Download JSON Strategy",
                data=json.dumps(data, indent=2),
                file_name=f"launch_checklist_{date.today()}.json",
                mime="application/json"
            )
        with c2:
            st.download_button(
                "📝 Download GTM Summary",
                data=str(data),
                file_name=f"launch_summary_{date.today()}.txt",
                mime="text/plain"
            )
    else:
        st.info("Input launch objectives and click 'Synthesize' to reveal your GTM architecture.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Powered by Launch-Pad AI | Engineered for Impact</div>", unsafe_allow_html=True)
