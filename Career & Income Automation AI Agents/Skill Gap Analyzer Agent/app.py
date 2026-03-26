import streamlit as st
import time
import os
import sys

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import analyze_skill_gap, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Skill Gap Analyzer", 
    page_icon="🧠", 
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

/* Glassmorphism Cards */
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
}

.stat-val { font-size: 2.5rem; font-weight: 800; color: #6366f1; }
.stat-label { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Results Badges */
.badge-red { background: rgba(239, 68, 68, 0.15); color: #f87171; border-radius: 6px; padding: 2px 8px; font-weight: 600; font-size: 0.9rem; margin: 4px; display: inline-block; }
.badge-green { background: rgba(34, 197, 94, 0.15); color: #4ade80; border-radius: 6px; padding: 2px 8px; font-weight: 600; font-size: 0.9rem; margin: 4px; display: inline-block; }
.badge-yellow { background: rgba(234, 179, 8, 0.15); color: #fbbf24; border-radius: 6px; padding: 2px 8px; font-weight: 600; font-size: 0.9rem; margin: 4px; display: inline-block; }

/* Input Fields */
.stTextArea textarea, .stTextInput input {
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

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Settings ---
with st.sidebar:
    st.markdown("### 🧬 Intelligence Configuration")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Intelligence Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### ⚡ Analyst Persona: Enabled")
    st.info("The Skill Gap Analyzer uses a Lead Career Strategist persona to extract technical keywords and missing experience nodes.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Skill Gap Analyzer</h1>
    <p>Strategic gap mapping between your resume and target opportunities using CareerOS AI nodes. 🧠</p>
</div>
""", unsafe_allow_html=True)

# --- Pre-fill Check ---
init_resume = st.session_state.get("user_resume", "")
init_job_desc = st.session_state.get("target_job_desc", "")

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 📄 Candidate Context")
    resume_input = st.text_area("Your Resume", height=300, value=init_resume, placeholder="Paste your resume here...")

with col_in2:
    st.markdown("### 🎯 Target Job Role")
    job_desc_input = st.text_area("Job Description", height=300, value=init_job_desc, placeholder="Paste the target job description or role requirements...")

# --- Analysis Logic ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Execute Strategic Gap Analysis"):
    if not resume_input or not job_desc_input:
        st.error("⚠️ Please specify both a Resume and a Job Description for analysis.")
    else:
        with st.status("🧠 Processing Career Intelligence Swarm...", expanded=True) as status:
            st.write("🌌 Extracting technical nodes from JD...")
            time.sleep(1)
            st.write("🔬 Deconstructing resume against requirements...")
            time.sleep(1)
            st.write("📊 Calculating gap density and match score...")
            
            # Run Analysis
            result = analyze_skill_gap(
                resume_input, job_desc_input, ai_model, user_api_key if user_api_key else None
            )
            
            if "error" in result:
                status.update(label="❌ Analysis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Analysis Complete!", state="complete")
                st.session_state["gap_result"] = result

# --- Results Presentation ---
if "gap_result" in st.session_state:
    res = st.session_state["gap_result"]
    
    st.markdown("---")
    st.markdown("### 🏆 Strategic Gap Overview")
    
    # Hero Metrics
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-val">{res.get('match_score', 0)}%</div>
            <div class="stat-label">Hiring Match Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        missing_count = len(res.get('missing_skills', []))
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-val">{missing_count}</div>
            <div class="stat-label">Critical Gaps Detected</div>
        </div>
        """, unsafe_allow_html=True)

    with col_stat3:
        status_text = "READY TO APPLY" if res.get('match_score', 0) >= 80 else "NEEDS BRIDGING"
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-val" style="font-size: 1.8rem; margin-top: 10px;">{status_text}</div>
            <div class="stat-label">Candidate Status</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**🔬 Detailed Summary:** {res.get('detailed_analysis', 'Analysis complete.')}")
    
    # Skills Visualization
    col_grid1, col_grid2 = st.columns(2)
    
    with col_grid1:
        st.subheader("💪 Core Strengths (Matching Skills)")
        for s in res.get("strengths", []):
            st.markdown(f"<span class='badge-green'>{s}</span>", unsafe_allow_html=True)
            
        st.subheader("❌ Missing Fundamentals (Critical)")
        for m in res.get("missing_skills", []):
            st.markdown(f"<span class='badge-red'>{m}</span>", unsafe_allow_html=True)

        st.subheader("⚠️ Weak Areas (Partial Match)")
        for w in res.get("weak_areas", []):
            st.markdown(f"<span class='badge-yellow'>{w}</span>", unsafe_allow_html=True)

    with col_grid2:
        st.subheader("🧭 Actionable Learning Plan")
        for idx, item in enumerate(res.get("learning_plan", [])):
            with st.expander(f"Skill: {item.get('skill', 'Skill Hub')}", expanded=(idx==0)):
                st.markdown(f"**Recommended Strategy:**\n{item.get('action', 'Research and build a small proof-of-concept project.')}")
                st.button(f"🔍 Find Practice Projects for {item.get('skill', '')}", key=f"btn_{idx}")

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by CareerOS Analyst Swarm • Architected by Harsh Choudhary<br>
    Universal Model Selection Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
