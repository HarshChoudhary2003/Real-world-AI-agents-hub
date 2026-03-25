import streamlit as st
import time
import os
import sys

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import generate_interview_question, SUPPORTED_MODELS
from evaluator import evaluate_interview_answer

# --- Page Config ---
st.set_page_config(
    page_title="AI Interview Simulator", 
    page_icon="🎤", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Design) ---
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #020617 100%);
    color: #f8fafc;
}

/* Glassmorphism Cards */
.title-container {
    padding: 2.5rem;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 2rem;
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

/* Question Area Glassmorphism */
.q-card {
    background: rgba(30, 41, 59, 0.4);
    padding: 2.5rem;
    border-radius: 16px;
    border-left: 5px solid #6366f1;
    margin-bottom: 1.5rem;
}

.q-label { font-size: 1rem; color: #6366f1; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.8rem; }
.q-text { font-size: 1.6rem; color: #fff; line-height: 1.4; font-weight: 600; }

/* Control Buttons */
.stButton button {
    width: 100%;
    height: 3.2rem;
    font-size: 1.1rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    color: white;
    border: none;
    border-radius: 12px;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(79, 70, 229, 0.4);
}

/* Metrics and Results */
.metric-box {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-score { font-size: 2.5rem; font-weight: 800; color: #4ade80; }
.metric-label { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Swarm Settings ---
with st.sidebar:
    st.markdown("### 🧬 AI Swarm Config")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Intelligence Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 🎯 Interview Profile")
    role = st.text_input("💼 Target Role", placeholder="e.g. Senior Data Engineer")
    difficulty = st.select_slider("🔥 Difficulty Level", options=["Easy", "Medium", "Hard"], value="Medium")
    resume_context = st.text_area("Paste Resume (Optional)", placeholder="Paste your resume for role-specific questions...")
    
    st.markdown("---")
    st.markdown("#### 🔄 Interaction Control")
    if st.button("🎤 New Interview Session"):
        st.session_state["cur_question"] = None
        st.session_state["cur_eval"] = None
        st.rerun()

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>AI Interview Simulator</h1>
    <p>Real-time technical screening, evaluation, and feedback loops with professional AI hiring managers. 🎤</p>
</div>
""", unsafe_allow_html=True)

# --- Session Initialization ---
if "cur_question" not in st.session_state: st.session_state["cur_question"] = None
if "cur_eval" not in st.session_state: st.session_state["cur_eval"] = None

# --- Main Interaction Logic ---
if not st.session_state["cur_question"]:
    st.markdown("### 🚀 Step 1: Start the Session")
    st.info("Prepare your role and difficulty in the sidebar, then click the button below to generate your first technical question.")
    if st.button("🎤 Initiate AI Interview"):
        if not role:
            st.error("⚠️ Please specify a Role in the sidebar to begin.")
        else:
            with st.spinner("🤖 Generative AI Interviewer is thinking..."):
                q_text = generate_interview_question(
                    role, difficulty, resume_context, ai_model, user_api_key if user_api_key else None
                )
                st.session_state["cur_question"] = q_text
                st.rerun()

else:
    # --- Question Screen ---
    st.markdown(f"""
    <div class="q-card">
        <div class="q-label">Current Question - {difficulty} Level</div>
        <div class="q-text">{st.session_state['cur_question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # User Input
    user_answer = st.text_area("✍️ Your Detailed Answer", height=250, placeholder="Type your answer here or paste notes for evaluation...")
    
    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("📊 Evaluate Answer"):
            with st.spinner("🤖 Lead Hiring Manager analyzing response..."):
                eval_result = evaluate_interview_answer(
                    st.session_state["cur_question"], user_answer, ai_model, user_api_key if user_api_key else None
                )
                st.session_state["cur_eval"] = eval_result
        
    # --- Results Rendering ---
    if st.session_state["cur_eval"]:
        eval_data = st.session_state["cur_eval"]
        
        if "error" in eval_data:
            st.error(eval_data["error"])
        else:
            st.markdown("---")
            st.markdown("### 🏆 Performance Analysis")
            
            # Score and Core Summary
            col_res1, col_res2, col_res3 = st.columns([1, 1, 3])
            
            with col_res1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-score">{eval_data.get('score', 0)}/10</div>
                    <div class="metric-label">Hiring Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_res2:
                # Progress circle or simple status
                status_color = "#4ade80" if eval_data.get('score', 0) >= 7 else "#f87171"
                st.markdown(f"""
                <div class="metric-box" style="border-color: {status_color};">
                    <div class="metric-score" style="color: {status_color};">{'PASSED' if eval_data.get('score', 0) >= 7 else 'REJECT'}</div>
                    <div class="metric-label">Selection Status</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_res3:
                st.markdown("#### 🔬 Detailed Analysis")
                st.write(eval_data.get('analysis', "Evaluation complete."))

            # Strengths, Weaknesses, Improvements
            st.markdown("<br>", unsafe_allow_html=True)
            col_det1, col_det2 = st.columns(2)
            
            with col_det1:
                st.success("💪 **Strengths**")
                for s in eval_data.get("strengths", []):
                    st.write(f"- {s}")
                
                st.error("📉 **Weaknesses**")
                for w in eval_data.get("weaknesses", []):
                    st.write(f"- {w}")

            with col_det2:
                st.info("🚀 **Actionable Improvements**")
                st.write(eval_data.get("improvement", "No specific improvements suggested."))
            
            # The Ideal Answer
            with st.expander("💡 View Ideal Answer (Model Response)", expanded=False):
                st.markdown(f"**Interviewer's Benchmarking Solution:**\n\n{eval_data.get('ideal_answer', 'Not provided.')}")
            
            # Next Action
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⏭️ Next Interview Question"):
                st.session_state["cur_question"] = None
                st.session_state["cur_eval"] = None
                st.rerun()

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by CareerOS Interview Swarm • Architected by Antigravity Agent v5.0<br>
    Universal Model Selection Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
