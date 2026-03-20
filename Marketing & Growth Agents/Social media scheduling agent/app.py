import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import generate_social_schedule, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Social-Sync AI | Multi-Platform Strategy",
    page_icon="📅",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(139, 92, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
    }
    .main { background-color: #0c0a09; }
    .stApp { background: radial-gradient(circle at center right, #1e1b4b 0%, #0c0a09 100%); }
    
    .schedule-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 6px solid #8b5cf6;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
        animation: slideInUp 0.7s ease-out;
        transition: all 0.3s ease;
    }
    .schedule-card:hover {
        transform: translateX(5px);
        background: rgba(255, 255, 255, 0.06);
        border-right-color: #a78bfa;
    }
    .platform-tag {
        background: rgba(139, 92, 246, 0.15);
        color: #ddd6fe;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .time-badge {
        font-family: 'Courier New', monospace;
        color: #8b5cf6;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .section-header {
        color: #fafaf9;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 15px;
        border-bottom: 2px solid rgba(139, 92, 246, 0.3);
        padding-bottom: 10px;
        width: fit-content;
    }
    .sidebar-section {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .visual-advice {
        background: rgba(16, 185, 129, 0.05);
        border: 1px dashed #10b981;
        padding: 15px;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #10b981;
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("📅 Social-Sync AI")
st.markdown("### Cross-Platform Engagement Architecture")
st.caption("Synthesize high-impact social schedules with Multi-Model intelligence and platform-specific timing logic.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Strategy Brain")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        # Provider Selection Standard
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
        temperature = st.slider("Scheduling Creativity", 0.0, 1.0, 0.4)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Posting Context")
    if st.button("Load Multi-Platform Example"):
        st.session_state.social_input = """Platforms: LinkedIn, Twitter
Audience Timezone: EST
Posting Frequency: 1 post per day
Content: AI Benefits, Success Stories, Workflow threads
Campaign: Awareness Launch"""

# Layout Split
col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.markdown('<div class="section-header">🛠️ Content Brief</div>', unsafe_allow_html=True)
    social_text = st.text_area(
        "Define your platforms, frequencies, and content ideas:",
        value=st.session_state.get("social_input", ""),
        height=350,
        placeholder="e.g., Platforms: Instagram. Goal: Brand Lifestyle..."
    )
    
    if st.button("🚀 Architect Posting Schedule"):
        if social_text:
            with st.spinner("Synthesizing multi-platform timeline and engagement windows..."):
                try:
                    schedule_data = generate_social_schedule(social_text, model_name, api_key)
                    st.session_state.social_schedule = schedule_data
                    save_outputs(schedule_data)
                    st.success("Strategy Orchestrated!")
                except Exception as e:
                    st.error(f"Strategy Error: {e}")
        else:
            st.warning("Please provide scheduling context first.")

with col_output:
    if "social_schedule" in st.session_state:
        data = st.session_state.social_schedule
        
        # Campaign Title Card
        po = data.get('project_overview', {})
        st.markdown(f"""
            <div class="schedule-card" style="border-right-color: #ec4899;">
                <div class="platform-tag" style="background: rgba(236, 72, 153, 0.1); color: #f472b6;">TITLE: {po.get('campaign_identity', 'CAMPAIGN')}</div>
                <h2 style="margin-top: 10px; color: #f8fafc;">{po.get('primary_goal', 'Objective Overview')}</h2>
            </div>
        """, unsafe_allow_html=True)

        # Tabs for result viewing
        tab_timeline, tab_mastery, tab_export = st.tabs(["🕒 Interactive Timeline", "🎯 Platform Mastery", "🗳️ Export"])
        
        with tab_timeline:
            st.markdown('<div class="section-header">🕒 Multi-Platform Timeline</div>', unsafe_allow_html=True)
            
            posts = data.get('posts', [])
            for post in posts:
                st.markdown(f"""
                    <div class="schedule-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <div class="time-badge">🕒 {post.get('scheduled_time_est')}</div>
                            <div class="platform-tag">{post.get('day_index')} | {post.get('platform')}</div>
                        </div>
                        <p style="color: #f1f5f9; font-size: 1.1rem; font-weight: 600;">{post.get('content_hook')}</p>
                        <p style="color: #94a3b8; font-size: 0.9rem; font-style: italic; margin: 15px 0;">Strategy: {post.get('strategic_rationale')}</p>
                        <div class="visual-advice">🖼️ Visual Tip: {post.get('visual_recommendation')}</div>
                        <div style="margin-top: 15px;">
                            {' '.join([f'<span class="platform-tag" style="background: rgba(255,255,255,0.05); color: #8b5cf6; border: 1px solid rgba(139, 92, 246, 0.2);">{tag}</span>' for tag in post.get('hashtags', [])])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with tab_mastery:
            st.markdown('<div class="section-header">🎯 Strategic Best Practices</div>', unsafe_allow_html=True)
            for tip in data.get("platform_best_practices", []):
                st.markdown(f"> ✅ {tip}")
            
            st.divider()
            st.info("💡 **Pro-Tip**: These times are dynamically selected based on peak activity for cross-platform professional networks in your target timezone.")

        with tab_export:
            st.markdown('<div class="section-header">🗳️ Schedule Exports</div>', unsafe_allow_html=True)
            
            st.download_button(
                "📥 Export JSON Schedule",
                data=json.dumps(data, indent=2),
                file_name=f"social_schedule_{date.today()}.json",
                mime="application/json"
            )
            
            st.download_button(
                "📝 Download Draft Summary",
                data=str(data),
                file_name=f"social_draft_{date.today()}.txt",
                mime="text/plain"
            )
    else:
        st.info("Input scheduling details and click 'Architect Schedule' to reveal your cross-platform strategy.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Powered by Social-Sync AI | Architecting Digital Resonance</div>", unsafe_allow_html=True)
