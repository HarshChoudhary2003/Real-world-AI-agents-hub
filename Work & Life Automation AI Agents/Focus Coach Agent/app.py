import streamlit as st
import time
import os
import sys
import json
from datetime import datetime

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import generate_focus_plan, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Focus Coach | Deep Work Engine", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Visual Blocks) ---
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #020617 0%, #030712 50%, #020617 100%);
    color: #f8fafc;
}

/* Glassmorphism Title Card */
.title-container {
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 2rem;
    text-align: center;
}

.title-container h1 {
    font-size: 2.8rem;
    background: linear-gradient(to right, #ec4899, #8b5cf6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.title-container p { color: #94a3b8; font-size: 1rem; }

/* Dashboard Metric Box */
.stat-box {
    background: rgba(30, 41, 59, 0.3);
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
    margin-bottom: 1rem;
}

.stat-val { font-size: 1.6rem; font-weight: 800; color: #ec4899; }
.stat-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.3rem; }

/* Focus Cards */
.focus-card {
    background: rgba(15, 23, 42, 0.5);
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 4px solid #ec4899;
    margin-bottom: 1.2rem;
}
.focus-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; }
.focus-desc { color: #94a3b8; font-size: 0.95rem; line-height: 1.5; }

/* Pomodoro UI */
.timer-display {
    font-family: 'JetBrains Mono', monospace;
    font-size: 4.5rem;
    font-weight: 800;
    color: #ec4899;
    text-align: center;
    text-shadow: 0 0 20px rgba(236, 72, 153, 0.3);
    margin: 1.5rem 0;
}

/* Input Fields */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: rgba(15, 23, 10, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #f8fafc !important;
}

/* Control Buttons */
.stButton button {
    width: 100%;
    height: 3.5rem;
    background: linear-gradient(90deg, #ec4899, #8b5cf6);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(236, 72, 153, 0.3);
}

.deep-work-active { border: 2px solid #ec489966 !important; background: rgba(236, 72, 153, 0.05) !important; }

.footer { text-align: center; color: #475569; margin-top: 4rem; font-size: 0.85rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Configuration ---
with st.sidebar:
    st.markdown("### 🧬 Focus Swarm Control")
    provider = st.selectbox("AI Intelligence", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Architecture", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### ⚡ Performance Mode")
    deep_mode = st.toggle("Activate Deep Work Protocol", value=False)
    if deep_mode:
        st.warning("⚡ DEEP WORK MODE ACTIVE: Environmental suppression engaged.")

# --- Header ---
st.markdown(f"""
<div class="title-container {'deep-work-active' if deep_mode else ''}">
    <h1>Focus Coach Agent</h1>
    <p>ProductivityOS: High-Acuity Flow-State Orchestration 🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Pomodoro Session Block (Top Layout) ---
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "time_left" not in st.session_state:
    st.session_state.time_left = 25 * 60

# Layout col
timer_col_1, timer_col_2 = st.columns([1, 1], gap="large")

with timer_col_1:
    st.markdown("### ⏱ Flow Core: Pomodoro")
    placeholder = st.empty()
    
    # Progress bar and UI
    mins, secs = divmod(st.session_state.time_left, 60)
    placeholder.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("▶️ Start"):
            st.session_state.timer_running = True
    with btn_col2:
        if st.button("⏸ Pause"):
            st.session_state.timer_running = False
    with btn_col3:
        if st.button("🔄 Reset"):
            st.session_state.timer_running = False
            st.session_state.time_left = 25 * 60
            st.rerun()

    # Timer logic (Simulation in Streamlit loop)
    # Note: Precise timers in Streamlit are tricky, but this provides a simple UI loop for demo.
    if st.session_state.timer_running and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()

with timer_col_2:
    st.markdown("### 🎯 Mission Context")
    task_input = st.text_input("Current Mission Node", "Coding Neural Architecture...", placeholder="What are you doing RIGHT NOW?")
    dist_input = st.text_area("Environmental Distractions", "Phone, Notifications, Background Noise...", height=68)
    e_level = st.select_slider("Energy Reservoir", options=["Depleted", "Low", "Medium", "High", "Peak"], value="Medium")
    
    if st.button("🚀 Architect Focus Strategy"):
        if not task_input:
            st.error("⚠️ Mission node is null. Defining context required.")
        else:
            with st.status("🧠 Synthesizing Performance Plan...", expanded=True) as status:
                st.write("🌌 Deconstructing mission complexity...")
                time.sleep(1)
                st.write("🔬 Injecting flow-state triggers...")
                time.sleep(1)
                
                result = generate_focus_plan(task_input, dist_input, e_level, ai_model, user_api_key if user_api_key else None)
                
                if "error" in result:
                    status.update(label="❌ Synthesis Failed", state="error")
                    st.error(result["error"])
                else:
                    status.update(label="✅ Strategy Ready!", state="complete")
                    st.session_state["focus_result"] = result
                    st.toast("Deep Work Protocol Compiled.")

# --- Results Presentation ---
res = st.session_state.get("focus_result")
if res:
    st.markdown("---")
    
    col_out1, col_out2 = st.columns([3, 1], gap="large")
    
    with col_out1:
        st.markdown(f"### 🎯 The Strategy: {res.get('focus_strategy', 'Standard Flow')}")
        
        # Focus Score Box
        score = res.get('focus_score', 8)
        st.markdown(f"#### 📊 Projected Concentration Depth: {score}/10")
        st.progress(score / 10)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Work session plan
        st.subheader("⏱ Flow Execution Plan")
        for i, s in enumerate(res.get("session_plan", [])):
            st.markdown(f"""
            <div class="focus-card">
                <div class="focus-title">Session Node {i+1}: {s.get('duration', 'N/A')}</div>
                <div class="focus-desc">{s.get('activity', 'Deep Focus')}</div>
                <div style="margin-top: 5px; font-weight: 700; color: #ec4899; font-size: 0.8rem;">INTENSITY: {s.get('focus_intensity', 'High')}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_out2:
        st.markdown("### 🔥 Flow Triggers")
        
        st.markdown("""<div class="stat-box">
            <div class="stat-val">Enabled</div>
            <div class="stat-label">Binaural Mode</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("#### 🚫 Distraction Shields")
        for control in res.get("distraction_controls", []):
            st.warning(f"🛡️ {control}")
            
        with st.expander("🔬 Deep Work Protocol"):
            st.write(res.get("deep_work_protocol", "Environment secured. Context isolated."))
            
        st.markdown("#### 🔥 Resilience Boost")
        st.info(f"🌟 {res.get('motivation', 'Keep pushing.')}")

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Performance Architecture by Harsh Choudhary<br>
    LiteLLM Universal Protocol • Flow State Active
</div>
""", unsafe_allow_html=True)
