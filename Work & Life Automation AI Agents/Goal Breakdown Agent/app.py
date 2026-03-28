import streamlit as st
import time
import os
import sys
import json
import pandas as pd

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import breakdown_goal_strategy, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Goal Breakdown Architect", 
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
    background: linear-gradient(to right, #0ea5e9, #3b82f6, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.title-container p { color: #94a3b8; font-size: 1.1rem; }

/* Dashboard Metric Box */
.stat-box {
    background: rgba(30, 41, 59, 0.4);
    padding: 1.5rem;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}
.stat-box:hover { transform: translateY(-3px); border-color: #3b82f6; }

.stat-val { font-size: 1.6rem; font-weight: 800; color: #3b82f6; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Strategic Phasing Cards */
.phase-card {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 5px solid #3b82f6;
    margin-bottom: 1.2rem;
}
.phase-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; }
.phase-focus { color: #3b82f6; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem; }
.phase-body { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }

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
    background: linear-gradient(90deg, #0ea5e9, #3b82f6);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Cluster ---
with st.sidebar:
    st.markdown("### 🧬 AI Intelligence Intelligence")
    provider = st.selectbox("AI Host", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Language Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### 🎯 Execution Mode")
    st.info("ProductivityOS Goal Deconstructor is optimized for surgical milestone extraction.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Goal Breakdown Agent</h1>
    <p>ProductivityOS: Tactical Roadmap Architecture & Strategic Synthesis 🎯🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Enabled</div>
        <div class="stat-label">Milestone Mapping</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Surgical</div>
        <div class="stat-label">Task Phasing</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Active</div>
        <div class="stat-label">Resilience Protocol</div>
    </div>""", unsafe_allow_html=True)
with col_v4:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Synced</div>
        <div class="stat-label">Productivity Hub</div>
    </div>""", unsafe_allow_html=True)

# --- Input Area ---
col_in1, col_in2 = st.columns([2, 1], gap="large")

with col_in1:
    st.markdown("### 🎯 Mission Archetype")
    macro_goal = st.text_area(
        "Define your Macro-Goal (The Big Vision)", 
        height=180, 
        placeholder="Become a world-class Data Analyst and secure a $150k+ position..."
    )

with col_in2:
    st.markdown("### 📅 Temporal Constraints")
    time_frame = st.text_input("Execution Timeline", placeholder="3 months, 6 weeks, etc.")
    st.markdown("---")
    res_btn = st.button("🚀 Architect Strategic Roadmap")
    st.caption("The AI utilizes persona simulation to optimize the draft for cross-functional communication.")

# --- Generation Logic ---
if res_btn:
    if not macro_goal or not time_frame:
        st.error("⚠️ Mission Feed Failed: Macro-goal and timeline nodes are required.")
    else:
        with st.status("🧠 Deconstructing Strategic Nodes...", expanded=True) as status:
            st.write("🌌 Synthesizing milestone sequences...")
            time.sleep(1)
            st.write("🔬 Auditing execution risks & failure-recovery protocols...")
            time.sleep(1)
            st.write("📊 Finalizing High-Acuity Execution Strategy...")
            
            result = breakdown_goal_strategy(macro_goal, time_frame, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Roadmap Architecture Finalized!", state="complete")
                st.session_state["goal_result"] = result
                st.snow()

# --- Results Presentation ---
res = st.session_state.get("goal_result")
if res:
    st.markdown("---")
    
    col_out1, col_out2 = st.columns([3, 2], gap="large")
    
    with col_out1:
        st.markdown("### 📈 Visual Strategy Roadmap")
        # Plotly/Graph simulation via data points
        viz_data = res.get("roadmap_viz", [])
        if viz_data:
            chart_df = pd.DataFrame(viz_data)
            st.line_chart(chart_df.set_index("node")["progress"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📑 Strategic Execution Phases")
        for p in res.get("timeline", []):
            st.markdown(f"""
            <div class="phase-card">
                <div class="phase-focus">FOCUS: {p.get('focus', 'Deep Level Integration')}</div>
                <div class="phase-title">{p.get('phase', 'Phase Alpha')}</div>
                <div class="phase-body">
                    <strong>Tactical Execution Sequence:</strong><br>
                    {' • '.join(p.get('tasks', []))}
                </div>
                <div style="margin-top: 10px;">
                    <progress value="{p.get('progress_marker', 0)}" max="100" style="width: 100%; height: 5px;"></progress>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_out2:
        st.markdown("### 🎯 Mission Milestones")
        for m in res.get("milestones", []):
            st.info(f"💎 {m}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Primary Execution Nodes")
        for t in res.get("tasks", []):
            st.success(f"⚡ {t}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🛡️ Recovery & Resilience Protocols")
        for r in res.get("failure_recovery", []):
            st.warning(f"🛡️ {r}")
            
        st.markdown("---")
        # Export logic
        export_text = f"ARCHITECTED ROADMAP FOR: {macro_goal}\nTIMELINE: {time_frame}\n\nSTRATEGIC NODES:\n"
        for s in res.get("strategy", []):
            export_text += f"- {s}\n"
            
        st.download_button(
            label="⬇️ Export Strategic Brief (.txt)",
            data=export_text,
            file_name=f"Roadmap_Brief.txt",
            mime="text/plain"
        )

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Engineering Excellence by Harsh Choudhary<br>
    Universal Behavioral Engine Powered by LiteLLM Protocol
</div>
""", unsafe_allow_html=True)
