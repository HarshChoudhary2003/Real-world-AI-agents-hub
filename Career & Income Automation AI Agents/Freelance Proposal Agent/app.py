import streamlit as st
import time
import os
import sys

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import generate_freelance_proposal, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Freelance Proposal Agent", 
    page_icon="💰", 
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
    background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.title-container p { color: #94a3b8; font-size: 1.1rem; }

/* Dashboard Metric Box */
.stat-box {
    background: rgba(30, 41, 59, 0.4);
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
    margin-bottom: 1rem;
}

.stat-val { font-size: 1.5rem; font-weight: 800; color: #6366f1; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Input Fields */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(79, 70, 229, 0.2) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
}

/* Control Buttons */
.stButton button {
    width: 100%;
    height: 3.2rem;
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(79, 70, 229, 0.4);
}

.proposal-box {
    background: rgba(15, 23, 42, 0.8);
    padding: 2rem;
    border-radius: 16px;
    border-left: 5px solid #6366f1;
    font-size: 1.05rem;
    color: #cbd5e1;
    line-height: 1.6;
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Swarm settings ---
with st.sidebar:
    st.markdown("### 🧬 AI Swarm Config")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Intelligence Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### ⚡ Freelance Strategist: Active")
    st.info("The Freelance Proposal Agent uses an elite consultant persona to maximize conversion across global gig platforms.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Freelance Proposal Agent</h1>
    <p>Winning pitches for Upwork, Fiverr, and more. From learning to earning in seconds. 💰</p>
</div>
""", unsafe_allow_html=True)

# --- Pre-fill Check ---
init_resume = st.session_state.get("user_resume", "")

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 📄 Job Context")
    job_desc_input = st.text_area("Gig Job Description", height=250, placeholder="Paste the job description from Upwork, Fiverr, etc...")
    
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        platform_choice = st.selectbox("Platform Target", ["Upwork", "Fiverr", "Freelancer", "Direct Outreach"])
    with col_sub2:
        budget_input = st.text_input("Estimated Client Budget", placeholder="e.g. $500 - $1,000")

with col_in2:
    st.markdown("### 🧠 My Sales Engine")
    skills_input = st.text_area("Your Core Skills / Highlights", height=250, value=init_resume, placeholder="Paste your core skills or relevant work highlights...")
    pitch_tone = st.radio("Proposal Pitch Style", ["Expert (Premium)", "Friendly (Relatable)", "Aggressive (Impact-Driven)"], horizontal=True)

# --- Generation Logic ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Craft Winning Freelance Pitch"):
    if not job_desc_input or not skills_input:
        st.error("⚠️ We need both a job description and your skills to build a winning pitch.")
    else:
        with st.status("🧠 Synthesizing Gig Intelligence...", expanded=True) as status:
            st.write("🌌 Deconstructing client problem nodes...")
            time.sleep(1)
            st.write("🔬 Injecting psychology layers and trust signals...")
            time.sleep(1)
            st.write("📊 Calculating pricing strategy...")
            
            # Run Generator
            result = generate_freelance_proposal(
                job_desc_input, skills_input, platform_choice, budget_input, pitch_tone, ai_model, user_api_key if user_api_key else None
            )
            
            if "error" in result:
                status.update(label="❌ Generation Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Proposal Synthesized!", state="complete")
                st.session_state["proposal_result"] = result

# --- Results Presentation ---
if "proposal_result" in st.session_state:
    res = st.session_state["proposal_result"]
    
    st.markdown("---")
    st.markdown(f"### 🎯 The Winning Pitch: {pitch_tone}")
    
    col_res1, col_res2 = st.columns([3, 1])
    
    with col_res1:
        st.markdown(f"""<div class="proposal-box">{res.get('proposal', 'Proposal ready.')}</div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("⬇️ Download Winning Proposal (.txt)", res.get("proposal", ""), file_name=f"Proposal_{platform_choice}.txt")

    with col_res2:
        st.markdown("""<div class="stat-box">
            <div class="stat-val">""" + res.get('estimated_price', '$ -') + """</div>
            <div class="stat-label">Suggested Price</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="stat-box">
            <div class="stat-label" style="color: #4ade80; font-weight: 700;">Pricing Strategy</div>
            <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 5px;">""" + res.get('pricing_strategy', 'Standard bid.') + """</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("#### 🧠 Psychology Nodes")
        for point in res.get("key_points", []):
            st.write(f"• {point}")
            
        with st.expander("🔬 Client Psychology Analysis"):
            st.write(res.get("client_psychology", "Deep analysis complete."))

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by CareerOS Gig Swarm • Architected by Harsh Choudhary<br>
    Universal Model Selection Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
