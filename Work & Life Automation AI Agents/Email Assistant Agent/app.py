import streamlit as st
import time
import os
import sys
import json
from datetime import datetime

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import generate_email, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Email Architect & Intelligence", 
    page_icon="📧", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Visual Blocks) ---
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0c0a09 50%, #020617 100%);
    color: #f8fafc;
}

/* Glassmorphism Title Card */
.title-container {
    padding: 2.5rem;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 2.5rem;
    text-align: center;
}

.title-container h1 {
    font-size: 3.2rem;
    background: linear-gradient(to right, #4ade80, #34d399, #10b981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.title-container p { color: #94a3b8; font-size: 1.1rem; }

/* Dashboard Metric Box */
.stat-box {
    background: rgba(30, 41, 59, 0.4);
    padding: 1.2rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.stat-box:hover { transform: translateY(-3px); border-color: #10b981; }

.stat-val { font-size: 1.6rem; font-weight: 800; color: #10b981; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Dashboard Variant Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.5rem;
    background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border-radius: 10px 10px 0px 0px;
    padding: 10px 20px;
    border: none !important;
    color: #94a3b8 !important;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(16, 185, 129, 0.1) !important;
    color: #10b981 !important;
    border-bottom: 2px solid #10b981 !important;
}

/* Input Fields */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
}

/* Control Buttons */
.stButton button {
    width: 100%;
    height: 3.5rem;
    background: linear-gradient(90deg, #10b981, #059669);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(16, 185, 129, 0.4);
}

.email-draft {
    background: rgba(15, 23, 42, 0.8);
    padding: 2.5rem;
    border-radius: 16px;
    border-left: 5px solid #10b981;
    font-size: 1.05rem;
    color: #cbd5e1;
    line-height: 1.8;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Hub ---
with st.sidebar:
    st.markdown("### 🧬 AI Intelligence Cluster")
    provider = st.selectbox("AI Infrastructure", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Language Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password", placeholder="Bearer Token...")
    
    st.markdown("---")
    st.markdown("#### 📧 Personal Email Strategist")
    st.info("ProductivityOS Email Agent is optimized for conversion-led subject lines and high-nuance responses.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Email Assistant Agent</h1>
    <p>ProductivityOS: Tactical Communication & Draft Architecture 🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Operational</div>
        <div class="stat-label">Communication Node</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Surgical</div>
        <div class="stat-label">Grammar Policing</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">3 Variants</div>
        <div class="stat-label">Output Capacity</div>
    </div>""", unsafe_allow_html=True)
with col_v4:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Enabled</div>
        <div class="stat-label">Context Mapping</div>
    </div>""", unsafe_allow_html=True)

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 🖊 Communication Context")
    context_input = st.text_area(
        "Email Message / Core Situation", 
        height=280, 
        placeholder="Paste an email you want to reply to, or describe exactly what you want to send..."
    )

with col_in2:
    st.markdown("### 🎭 Tone & Objective Architecture")
    intent_choice = st.selectbox("Intelligence Intent", ["New Tactical Email", "Reply to Thread", "High-Priority Follow-up"])
    tone_choice = st.select_slider(
        "Linguistic Tone", 
        options=["Strictly Formal", "Professional Elite", "Friendly & Open", "Confident / Direct"],
        value="Professional Elite"
    )
    st.markdown("---")
    res_btn = st.button("🚀 Architect High-Impact Draft")
    st.caption("The AI utilizes persona simulation to optimize the draft for cross-functional communication.")

# --- Generation Logic ---
if res_btn:
    if not context_input:
        st.error("⚠️ Context Feed Empty: We need a message or situation to work with.")
    else:
        with st.status("🧠 Synthesizing Draft Architecture...", expanded=True) as status:
            st.write("🌌 Analyzing context nodes...")
            time.sleep(1)
            st.write("🔬 Injecting persona-led linguistic triggers...")
            time.sleep(1)
            st.write("📊 Finalizing Multi-Variant Outputs...")
            
            result = generate_email(context_input, intent_choice, tone_choice, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Generation Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Tactical Draft Built!", state="complete")
                st.session_state["email_result"] = result
                st.snow()

# --- Results Presentation ---
res = st.session_state.get("email_result")
if res:
    st.markdown("---")
    
    st.markdown(f"### 🎯 Strategic Subject: `{res.get('subject', 'No Subject Generated')}`")
    
    # Variant Selection via Tabs
    st.markdown("#### 🧬 Dynamic Variants (Smart Reply Swarm)")
    tab_labels = [v.get("label", "Variant") for v in res.get("variants", [])]
    if not tab_labels: tab_labels = ["Primary Draft"]
    
    tabs = st.tabs(tab_labels)
    
    for i, tab in enumerate(tabs):
        with tab:
            variant_content = res.get("variants", [])[i].get("content") if i < len(res.get("variants", [])) else res.get("email")
            st.markdown(f'<div class="email-draft">{variant_content}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                st.button(f"📋 Copy {tab_labels[i]} to Clipboard", key=f"copy_{i}")
            with col_act2:
                st.download_button(
                    label=f"⬇️ Download {tab_labels[i]} (.txt)",
                    data=variant_content,
                    file_name=f"Email_{tab_labels[i].replace(' ', '_')}.txt",
                    key=f"dl_{i}"
                )

    st.markdown("---")
    col_feat1, col_feat2 = st.columns(2, gap="large")
    
    with col_feat1:
        st.markdown("### 🧠 Communication Polishing Tips")
        for tip in res.get("tips", []):
            st.success(f"💡 {tip}")
            
    with col_feat2:
        st.markdown("### 🛡️ Linguistic Grammar Fixes")
        for fix in res.get("polishing_suggestions", []):
            st.warning(f"✍️ {fix}")

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Strategic Architecture by Harsh Choudhary<br>
    Universal Model Support Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
