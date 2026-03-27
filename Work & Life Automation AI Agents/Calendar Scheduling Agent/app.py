import streamlit as st
import time
import os
import sys
import json
import uuid
from datetime import datetime, timedelta

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import generate_schedule, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Calendar AI Navigator", 
    page_icon="📅", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Visual Blocks) ---
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #020617 50%, #0f172a 100%);
    color: #f8fafc;
}

/* Glassmorphism Title Card */
.title-container {
    padding: 2rem;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(14px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 2rem;
    text-align: center;
}

.title-container h1 {
    font-size: 3.2rem;
    background: linear-gradient(to right, #0ea5e9, #6366f1, #d946ef);
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
.stat-box:hover { transform: translateY(-3px); border-color: #6366f166; }

.stat-val { font-size: 1.8rem; font-weight: 800; color: #38bdf8; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Time Block Cards */
.timeline-card {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.8rem;
    border-radius: 20px;
    border-left: 6px solid #6366f1;
    margin-bottom: 1.5rem;
    position: relative;
    transition: all 0.3s ease;
}
.timeline-card:hover { background: rgba(15, 23, 42, 0.85); transform: scale(1.02); }

.block-time { font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: #38bdf8; font-weight: 800; margin-bottom: 0.5rem; }
.block-task { font-size: 1.25rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.8rem; }
.block-energy { display: inline-block; padding: 4px 12px; border-radius: 100px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; margin-right: 0.5rem; }

.energy-high { background: rgba(244, 114, 182, 0.2); color: #f472b6; border: 1px solid #f472b644; }
.energy-medium { background: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid #818cf844; }
.energy-low { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid #4ade8044; }

.node-label { font-size: 0.8rem; color: #64748b; font-weight: 600; margin-top: 5px; }

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
    background: linear-gradient(90deg, #0ea5e9, #6366f1);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(14, 165, 233, 0.3);
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Helper: ICS Generator ---
def create_ics(schedule):
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ProductivityOS Calendar AI//EN"
    ]
    
    for block in schedule:
        try:
            # We assume today's date for simplicity
            summary = block.get("task", "Focus Session")
            notes = block.get("notes", "")
            
            # This is a very basic simulation; proper time parsing would be complex
            ics_lines.extend([
                "BEGIN:VEVENT",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{notes}",
                f"DTSTART:{datetime.now().strftime('%Y%m%d')}T090000",
                f"DTEND:{datetime.now().strftime('%Y%m%d')}T100000",
                "END:VEVENT"
            ])
        except:
            continue
            
    ics_lines.append("END:VCALENDAR")
    return "\n".join(ics_lines)

# --- Sidebar: Intelligence Swarm settings ---
with st.sidebar:
    st.markdown("### 🧬 AI Calendar Pilot")
    provider = st.selectbox("Intelligence Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Architecture", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password", placeholder="Bearer...")
    
    st.markdown("---")
    st.markdown("#### ⚡ Focus Chronotype")
    pref = st.segmented_control(
        "Energy Distribution", 
        ["Morning Burst", "Steady Flow", "Night Shift"], 
        default="Steady Flow"
    )
    st.caption("AI adjusts focus windows based on your biological peak nodes.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Autonomous Calendar AI</h1>
    <p>Architecture of Time: Transform chaos into high-density performance sequences. 🌌</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">100%</div>
        <div class="stat-label">Neural Integrity</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Adaptive</div>
        <div class="stat-label">Model Type</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Enabled</div>
        <div class="stat-label">Energy Matching</div>
    </div>""", unsafe_allow_html=True)
with col_v4:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Gcal</div>
        <div class="stat-label">Sync Status</div>
    </div>""", unsafe_allow_html=True)

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 🖊 Mission Feed")
    tasks_input = st.text_area(
        "Current Backlog / Tasks", 
        height=250, 
        placeholder="Paste your tasks from Notion, Task Planner, or BrainVault... \n- Build MVP\n- Review budget\n- Design UI..."
    )

with col_in2:
    st.markdown("### ⏱ Constraints")
    h_capacity = st.slider("Active Execution Hours", 1, 16, 8)
    st.markdown("---")
    res_btn = st.button("🚀 Architect Daily Calendar")
    st.caption("The AI utilizes multi-step reasoning to optimize your energy-depletion curve.")

# --- Generation Logic ---
if res_btn:
    if not tasks_input:
        st.error("⚠️ We need your missions to architect the sequence.")
    else:
        with st.status("🧠 Deconstructing Temporal Nodes...", expanded=True) as status:
            st.write("🌌 Mapping energy requirements to tasks...")
            time.sleep(1)
            st.write("🔬 Identifying peak focus cycles...")
            time.sleep(1)
            st.write("📊 Finalizing High-Precision Schedule...")
            
            result = generate_schedule(tasks_input, h_capacity, pref, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Architecture Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Sequence Architected!", state="complete")
                st.session_state["cal_result"] = result
                st.snow()

# --- Results Presentation ---
res = st.session_state.get("cal_result")
if res:
    st.markdown("---")
    st.markdown(f"### ⚡ Daily Strategy Architecture: {res.get('daily_focus_mode', 'Balanced Focus')}")
    
    col_out1, col_out2 = st.columns([3, 1], gap="large")
    
    with col_out1:
        st.markdown("#### 📅 Time-Blocked Sequence")
        for block in res.get("schedule", []):
            energy_class = f"energy-{block.get('energy_level', 'medium').lower()}"
            st.markdown(f"""
            <div class="timeline-card">
                <div class="block-time">{block.get('time_slot', 'N/A')} ({block.get('duration', 'N/A')})</div>
                <div class="block-task">{block.get('task', 'Deep Focus Session')}</div>
                <div>
                    <span class="block-energy {energy_class}">{block.get('energy_level', 'Medium')}</span>
                    <span class="node-label">NODE: {block.get('energy_node', 'Tactical')}</span>
                </div>
                <div style="margin-top: 10px; color: #94a3b8; font-size: 0.95rem;">{block.get('notes', '')}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_out2:
        st.markdown("#### 🚀 Intelligence Scores")
        st.markdown(f"""<div class="stat-box">
            <div class="stat-val">{res.get('energy_score', 88)}%</div>
            <div class="stat-label">Energy Efficiency Score</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("#### 🧠 Strategic Tips")
        for tip in res.get("productivity_tips", []):
            st.success(f"💡 {tip}")
            
        st.markdown("---")
        # ICS Export Simulation
        ics_data = create_ics(res.get("schedule", []))
        st.download_button(
            label="📅 Export to Calendar (.ics)",
            data=ics_data,
            file_name="Daily_Schedule.ics",
            mime="text/calendar",
            help="Download as ICS for Google Calendar / Apple Calendar sync."
        )

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Engineering Excellence by Harsh Choudhary<br>
    LiteLLM Framework • Autonomous Temporal Orchestration
</div>
""", unsafe_allow_html=True)
