import streamlit as st
import time
import os
import sys

# Add current folder to sys.path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from workflow import run_auto_apply_workflow

# --- Page Config ---
st.set_page_config(
    page_title="Auto Apply Agent", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Consistent Premium Grade) ---
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0c0a09 100%);
    color: #f8fafc;
}

/* Glassmorphism Title Card */
.title-container {
    padding: 3rem;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 3rem;
    text-align: center;
}

.title-container h1 {
    font-size: 3.5rem;
    background: linear-gradient(to right, #4f46e5, #ec4899, #f97316);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.title-container p { color: #94a3b8; font-size: 1.2rem; }

/* Dashboard Cards */
.dash-card {
    background: rgba(30, 41, 59, 0.4);
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Inputs */
.stTextArea textarea, .stTextInput input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(79, 70, 229, 0.2) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
}

/* Generate Button */
.stButton button {
    width: 100%;
    height: 3.5rem;
    background: linear-gradient(90deg, #6366f1, #d946ef);
    color: white;
    font-size: 1.2rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.4s ease;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
}

/* Output Area Style */
.stTextArea [data-baseweb="textarea"] {
    background: #0f172a !important;
    border: 1px solid #334155 !important;
    font-family: inherit;
}

.footer {
    text-align: center;
    color: #475569;
    margin-top: 5rem;
    font-size: 0.9rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Global Intelligence Config ---
with st.sidebar:
    st.markdown("### 🧬 Intelligence Swarm Settings")
    ai_provider = st.selectbox("Orchestration Provider", ["OpenAI", "Google Gemini", "Groq"])
    ai_model = st.selectbox("Agent Intelligence Model", [
        "gpt-4o-mini", "gpt-4o", "gemini/gemini-1.5-pro", "groq/llama3-70b-8192"
    ])
    
    st.markdown("---")
    st.markdown("### 🔑 API Configuration")
    user_api_key = st.text_input(f"{ai_provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### ⚡ Multi-Agent Pipeline Status")
    st.success("🤖 Resume Optimizer: **Online**")
    st.success("✉️ Cover Letter Agent: **Online**")
    st.info("🔄 Assisting: Assisted Apply Mode")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Auto Apply Agent</h1>
    <p>Your multi-agent orchestration bridge to instant, high-quality job applications. 🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Pre-fill Check from Session State (Agent #3 Link) ---
init_resume = st.session_state.get("user_resume", "")
init_job_desc = st.session_state.get("target_job_desc", "")
init_company = st.session_state.get("target_company", "")

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 📄 Step 1: Candidate Context")
    resume_input = st.text_area("Your Resume", height=250, value=init_resume)
    company_input = st.text_input("🏢 Target Company", value=init_company)

with col_in2:
    st.markdown("### 🧾 Step 2: Job Requirements")
    job_desc_input = st.text_area("Job Description", height=250, value=init_job_desc)
    apply_url = st.text_input("🔗 Job Apply Link", placeholder="https://linkedin.com/jobs/view/...")

# --- Action Logic ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Execute Multi-Agent Workflow"):
    if not resume_input or not job_desc_input or not company_input:
        st.error("⚠️ Please fill all required fields to run the multi-agent pipeline.")
    else:
        with st.status("🧠 Orchestrating Career Intelligence Swarm...", expanded=True) as status:
            st.write("🔍 **Agent 1 (Optimizer):** Reshaping resume context for the JD...")
            time.sleep(1)
            st.write("✍️ **Agent 2 (Writer):** Synthesizing impact-driven cover letter...")
            time.sleep(1)
            st.write("🔬 **Agent 3 (Analyst):** Finalizing match intelligence and score metrics...")
            
            # Run Workflow
            result = run_auto_apply_workflow(
                resume=resume_input,
                job_desc=job_desc_input,
                company=company_input,
                api_key=user_api_key if user_api_key else None,
                ai_model=ai_model
            )
            
            st.write("✅ **Workflow Complete!**")
            status.update(label="✅ Success! Your Multi-Agent Application Suite is Ready.", state="complete", expanded=False)
        
        # --- Results Display ---
        st.markdown("---")
        st.markdown("### 🎯 Your Optimized Application Package")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Match Score", f"{result['match_score']}%", help="Calculated by the Resume Optimizer Agent.")
            st.subheader("📄 AI-Optimized Resume")
            st.text_area("Optimized Copy", value=result["optimized_resume"], height=450, key="opt_resume_out")
            st.download_button("⬇️ Download Optimized Resume", result["optimized_resume"], file_name=f"Optimized_Resume_{company_input}.txt")

        with col_res2:
            st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True) # Align with metric
            st.subheader("✉️ Tailored Cover Letter")
            st.text_area("Generated Copy", value=result["cover_letter"], height=450, key="cl_out")
            st.download_button("⬇️ Download Cover Letter", result["cover_letter"], file_name=f"Cover_Letter_{company_input}.txt")
            
        # Final CTA Link
        st.markdown("<br>", unsafe_allow_html=True)
        if apply_url:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: rgba(79, 70, 229, 0.1); border-radius: 16px; border: 1px dashed #6366f1;">
                <h3 style="margin: 0; color: #fff;">Ready to Apply to {company_input}?</h3>
                <p style="color: #94a3b8; font-size: 0.9rem; margin: 0.5rem 0 1.5rem;">The listing link is open. Use the documents above to pre-fill the application.</p>
                <a href="{apply_url}" target="_blank" style="display: inline-block; padding: 1rem 3rem; background: #6366f1; color: white; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);">
                    🚀 Open Job Application Page →
                </a>
            </div>
            """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
    CareerOS Multi-Agent Swarm Orchestrator v1.0<br>
    Built by Antigravity Agent • career-growth-suite v4.0
</div>
""", unsafe_allow_html=True)
