import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import audit_brand_voice, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Voice-Verify AI | Linguistic Integrity Engine",
    page_icon="🎭",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes glowPulse {
        0% { box-shadow: 0 0 5px rgba(251, 191, 36, 0.2); }
        50% { box-shadow: 0 0 20px rgba(251, 191, 36, 0.5); }
        100% { box-shadow: 0 0 5px rgba(251, 191, 36, 0.2); }
    }
    .main { background-color: #0f172a; }
    .stApp { background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 100%); }
    
    .audit-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        animation: fadeInSlide 0.7s ease-out;
    }
    .score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: rgba(251, 191, 36, 0.1);
        border: 4px solid #fbbf24;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px auto;
        animation: glowPulse 3s infinite;
    }
    .status-chip {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .aligned { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid #10b981; }
    .deviated { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid #ef4444; }
    
    .surgical-fix {
        background: rgba(255, 255, 255, 0.02);
        border-left: 4px solid #fbbf24;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    .section-header {
        color: #f1f5f9;
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
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("🎭 Voice-Verify AI")
st.markdown("### Brand Integrity & Linguistic Linguistic Audit OS")
st.caption("Deep neural audit of content resonance against established brand guidelines.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Audit Config")
    
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
        temperature = st.slider("Audit Sensitivity", 0.0, 1.0, 0.2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Data Context")
    if st.button("Load Tech Brand Example"):
        st.session_state.voice_guidelines = """Brand Voice Traits: Clear, Professional, Confident, Approachable. Avoid: Slang, Overly casual language, Excessive hype."""
        st.session_state.voice_content = """Our platform totally transforms how teams work. It's super easy to use and insanely powerful. You'll love how fast you can automate everything."""

# Layout Split
col_input, col_output = st.columns([1, 1.2])

with col_input:
    st.markdown('<div class="section-header">🔍 Audit Input</div>', unsafe_allow_html=True)
    
    guidelines_text = st.text_area(
        "Enter Brand Voice Guidelines:",
        value=st.session_state.get("voice_guidelines", ""),
        height=150,
        placeholder="Traits: High-end, Exclusive, Scientific..."
    )
    
    content_text = st.text_area(
        "Paste Content to Audit:",
        value=st.session_state.get("voice_content", ""),
        height=350,
        placeholder="Paste your ad copy, blog post, or email draft here..."
    )
    
    if st.button("🚀 Run Deep Linguistic Audit"):
        if guidelines_text and content_text:
            with st.spinner("Analyzing linguistic patterns & cross-referencing brand DNA..."):
                try:
                    audit_data = audit_brand_voice(guidelines_text, content_text, model_name, api_key)
                    st.session_state.voice_audit = audit_data
                    save_outputs(audit_data)
                    st.success("Audit Completed!")
                except Exception as e:
                    st.error(f"Audit Error: {e}")
        else:
            st.warning("Provide both guidelines and content.")

with col_output:
    if "voice_audit" in st.session_state:
        data = st.session_state.voice_audit
        
        # Summary Row with Score
        ao = data.get('audit_overview', {})
        score = ao.get('alignment_score', '0')
        st.markdown(f"""
            <div class="score-circle">
                <span style="font-size: 1.8rem; font-weight: 800; color: #fbbf24;">{score}%</span>
                <span style="font-size: 0.7rem; color: #94a3b8; font-weight: 600;">ALIGNMENT</span>
            </div>
            <div align="center" style="margin-bottom: 30px;">
                <span class="status-chip {'aligned' if int(score) > 70 else 'deviated'}">{ao.get('verdict')}</span>
                <p style="margin-top: 15px; color: #94a3b8; font-style: italic;">{ao.get('narrative_assessment')}</p>
            </div>
        """, unsafe_allow_html=True)

        # Tabs
        tab_traits, tab_surgeries, tab_export = st.tabs(["🎭 Trait Breakdown", "✂️ Surgical Fixes", "🗳️ Export"])
        
        with tab_traits:
            st.markdown('<div class="section-header">🎭 Persona Diagnostics</div>', unsafe_allow_html=True)
            for trait in data.get('trait_alignment', []):
                status = trait.get('status', 'Deviated')
                st.markdown(f"""
                    <div class="audit-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="font-weight: 800; color: #f1f5f9;">{trait.get('trait')}</span>
                            <span class="status-chip {status.lower()}">{status}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.9rem;">{trait.get('analysis')}</p>
                    </div>
                """, unsafe_allow_html=True)

        with tab_surgeries:
            st.markdown('<div class="section-header">✂️ Surgical Alignment Fixes</div>', unsafe_allow_html=True)
            
            for dev in data.get('deviations', []):
                st.markdown(f"**Original**: *\"{dev.get('original_segment')}\"*")
                st.markdown(f"""
                    <div class="surgical-fix">
                        <span style="color: #ef4444; font-size: 0.8rem; font-weight: 700;">ISSUE: {dev.get('reason')}</span><br>
                        <span style="color: #fbbf24; font-weight: 700;">FIX: \"{dev.get('surgical_fix')}\"</span><br>
                        <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 5px;">Effect: {dev.get('psychological_impact')}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            st.markdown("#### ✅ Brand DNA Strengths")
            for strength in data.get('strengths', []):
                st.success(f"🧬 {strength}")

        with tab_export:
            st.markdown('<div class="section-header">🗳️ Audit Package</div>', unsafe_allow_html=True)
            
            st.download_button(
                "📥 Export Audit JSON",
                data=json.dumps(data, indent=2),
                file_name=f"brand_audit_{date.today()}.json",
                mime="application/json"
            )
            
            st.download_button(
                "📝 Download Linguistic Brief",
                data=str(data),
                file_name=f"audit_summary_{date.today()}.txt",
                mime="text/plain"
            )
    else:
        st.info("Input guidelines and content to reveal the brand resonance audit.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Voice-Verify AI | Guarding Brand Integrity</div>", unsafe_allow_html=True)
