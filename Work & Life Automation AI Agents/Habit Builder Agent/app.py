import streamlit as st
import time
import os
import sys
import json
from datetime import datetime, date

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import build_habit_strategy, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Behavior Change Engine", 
    page_icon="🔥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Persistence: Habits Log ---
DB_FILE = os.path.join(os.path.dirname(__file__), "habits.json")

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"habits": {}, "total_xp": 0}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

db = load_db()

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
    background: linear-gradient(to right, #fb7185, #f43f5e, #e11d48);
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
.stat-box:hover { transform: translateY(-3px); border-color: #f43f5e; }

.stat-val { font-size: 1.6rem; font-weight: 800; color: #f43f5e; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Habit Node Blocks */
.habit-card {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 5px solid #f43f5e;
    margin-bottom: 1.2rem;
}
.habit-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; }
.habit-focus { color: #f43f5e; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; margin-bottom: 0.5rem; }
.habit-body { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }

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
    background: linear-gradient(90deg, #fb7185, #f43f5e);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(244, 63, 94, 0.3);
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Swarm ---
with st.sidebar:
    st.markdown("### 🧬 AI Behavioral Hub")
    provider = st.selectbox("AI Host", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Language Hub", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### 🔥 Gamification Tracker")
    st.metric("Global XP Nodes", f"{db.get('total_xp', 0)} XP", delta="+50 per Session")
    st.info("ProductivityOS Habit Agent uses surgical deconstruction to drive dopamine-led consistency.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Habit Builder Agent</h1>
    <p>ProductivityOS: Architecture of Behavior Change & Dopamine Orchestration 🔥🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Atomic</div>
        <div class="stat-label">Initiation Node</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Enabled</div>
        <div class="stat-label">Loss Aversion</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Active</div>
        <div class="stat-label">Streak Buffer</div>
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
    habit_goal = st.text_input("Macro-Habit Vision (e.g. Master Machine Learning)", placeholder="Study ML 2 hours every single day.")
    current_routine = st.text_area(
        "Describe your existing Daily Sequence/Routine", 
        height=180, 
        placeholder="Morning coffee at 8 AM, Check emails at 10 AM, Workout at 5 PM..."
    )

with col_in2:
    st.markdown("### ⚡ Execution Archetype")
    arc_diff = st.select_slider("Initiation Friction", options=["Zero-Friction", "Low-Friction", "Standard", "High-Intensity"], value="Standard")
    st.markdown("---")
    res_btn = st.button("🚀 Architect Behavioral Sequence")
    st.caption("The AI utilizes persona simulation to optimize the draft for cross-functional communication.")

# --- Generation Logic ---
if res_btn:
    if not habit_goal or not current_routine:
        st.error("⚠️ Context Failed: Desired habit and routine nodes are required.")
    else:
        with st.status("🧠 Synthesizing Behavioral Nodes...", expanded=True) as status:
            st.write("🌌 Deconstructing habit complexity into atomic nodes...")
            time.sleep(1)
            st.write("🔬 Mapping habit stacks of existing routine...")
            time.sleep(1)
            st.write("📊 Finalizing High-Precision Streak Strategy...")
            
            result = build_habit_strategy(habit_goal, arc_diff, current_routine, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Habit Architecture Finalized!", state="complete")
                st.session_state["habit_result"] = result
                
                # Persistence: Update XP
                xp_val = int(result.get("gamification_stats", {}).get("base_xp", "50").replace(" XP", ""))
                db["total_xp"] += xp_val
                
                # Initialize habit in DB if not exists
                if habit_goal not in db["habits"]:
                    db["habits"][habit_goal] = {"streak": 0, "last_check": ""}
                
                save_db(db)
                st.snow()

# --- Results Presentation ---
res = st.session_state.get("habit_result")
if res:
    st.markdown("---")
    
    col_out1, col_out2 = st.columns([3, 2], gap="large")
    
    with col_out1:
        st.markdown(f"### 📈 Behavioral Architecture Score: `{res.get('behavioral_resilience_score', 8)}/10`")
        
        st.markdown("### 📆 Phased Habit Sequence (Atomic Scaling)")
        for node in res.get("habit_architecture", []):
            st.markdown(f"""
            <div class="habit-card">
                <div class="habit-body">{node}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🧬 Tactical Habit Stack Mapping")
        for stack in res.get("daily_routine_stack", []):
            st.markdown(f"""
            <div style="background: rgba(244, 63, 94, 0.05); padding: 1.2rem; border-radius: 12px; border: 1px dashed #f43f5e44; margin-bottom: 1rem;">
                <div style="font-size: 0.8rem; font-weight: 800; color: #f43f5e; margin-bottom: 5px;">TRIGGER NODE: {stack.get('trigger')}</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc; margin-bottom: 5px;">MISSION: {stack.get('habit_node')}</div>
                <div style="font-size: 0.85rem; color: #94a3b8;">DOPAMINE CUE: {stack.get('reward_cue')}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_out2:
        st.markdown("### 🔥 Surgical Streak Strategy")
        st.info(f"🛡️ {res.get('streak_persistence_strategy', 'Protect the streak.')}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚡ Motivation Triggers Swarm")
        for trig in res.get("motivation_triggers", []):
            st.success(f"🔋 {trig}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎮 Gamification & Dopamine Nodes")
        g_stats = res.get("gamification_stats", {})
        st.markdown(f"""<div class="stat-box" style="background: rgba(244, 63, 94, 0.1);">
            <div class="stat-val">{g_stats.get('base_xp', '50 XP')}</div>
            <div class="stat-label">Points per Success Node</div>
        </div>""", unsafe_allow_html=True)
        
        for reward in g_stats.get("milestone_rewards", []):
            st.warning(f"🎁 {reward}")
            
        st.markdown("---")
        # Export logic
        export_text = f"HABIT ARCHITECTURE FOR: {habit_goal}\n\nSTRATEGY:\n{res.get('streak_persistence_strategy')}\n\nMOTIVATION NODES:\n"
        for m in res.get("motivation_triggers", []):
            export_text += f"- {m}\n"
            
        st.download_button(
            label="⬇️ Export Behavioral Brief (.txt)",
            data=export_text,
            file_name=f"Habit_Brief_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Cognitive Architecture by Harsh Choudhary<br>
    Universal Behavioral Engine Powered by LiteLLM Protocol
</div>
""", unsafe_allow_html=True)
