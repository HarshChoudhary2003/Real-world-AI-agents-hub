import streamlit as st
import time
import os
import sys
import json
from datetime import datetime

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import generate_plan, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Smart Task Planner", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Persistence ---
PLANS_FILE = os.path.join(os.path.dirname(__file__), "plans.json")

def load_data():
    if os.path.exists(PLANS_FILE):
        try:
            with open(PLANS_FILE, "r") as f:
                return json.load(f)
        except:
            return {"plans": [], "streak": 0, "last_date": None}
    return {"plans": [], "streak": 0, "last_date": None}

def save_data(data):
    with open(PLANS_FILE, "w") as f:
        json.dump(data, f, indent=2)

if "data" not in st.session_state:
    st.session_state["data"] = load_data()

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
    padding: 2rem;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(16px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 2rem;
    text-align: center;
}

.title-container h1 {
    font-size: 3rem;
    background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.title-container p { color: #94a3b8; font-size: 1.1rem; }

/* Dashboard Metric Box */
.stat-box {
    background: rgba(30, 41, 59, 0.3);
    padding: 1.2rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}
.stat-box:hover { transform: translateY(-3px); border-color: rgba(99, 102, 241, 0.3); }

.stat-val { font-size: 1.8rem; font-weight: 800; color: #6366f1; }
.stat-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Time Blocking Card */
.task-card {
    background: rgba(15, 23, 42, 0.5);
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 4px solid #3b82f6;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.task-card:hover { background: rgba(15, 23, 42, 0.8); }
.task-time { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: #3b82f6; font-weight: 700; margin-bottom: 0.5rem; }
.task-title { font-size: 1.1rem; font-weight: 600; color: #f8fafc; margin-bottom: 0.5rem; }
.task-priority { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; margin-right: 0.5rem; }
.priority-high { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.priority-medium { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.priority-low { background: rgba(16, 185, 129, 0.2); color: #10b981; }

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
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(99, 102, 241, 0.3);
}

.footer { text-align: center; color: #475569; margin-top: 4rem; font-size: 0.85rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Configuration ---
with st.sidebar:
    st.markdown("### 🧬 Intelligence Swarm")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Intelligence Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    
    # --- Streak Tracker ---
    streak = st.session_state["data"]["streak"]
    st.markdown(f"### 🔥 Streak: {streak} Days")
    st.progress(min(streak / 30, 1.0))
    st.caption("Complete your daily plan to keep the streak alive!")

    st.markdown("---")
    if st.button("🗑️ Clear History"):
        st.session_state["data"] = {"plans": [], "streak": 0, "last_date": None}
        save_data(st.session_state["data"])
        st.rerun()

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Smart Task Planner</h1>
    <p>ProductivityOS: High-Performance Daily Strategy Architecture 🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown(f'<div class="stat-box"><div class="stat-val">{streak}</div><div class="stat-label">Current Streak</div></div>', unsafe_allow_html=True)
with col_v2:
    total_tasks_done = sum(1 for p in st.session_state["data"]["plans"] for t in p.get("daily_plan", []) if t.get("done", False))
    st.markdown(f'<div class="stat-box"><div class="stat-val">{total_tasks_done}</div><div class="stat-label">Tasks Finished</div></div>', unsafe_allow_html=True)
with col_v3:
    avg_score = sum(p.get("productivity_score", 0) for p in st.session_state["data"]["plans"]) / max(len(st.session_state["data"]["plans"]), 1)
    st.markdown(f'<div class="stat-box"><div class="stat-val">{int(avg_score)}%</div><div class="stat-label">Average Focus</div></div>', unsafe_allow_html=True)
with col_v4:
    st.markdown(f'<div class="stat-box"><div class="stat-val">Elite</div><div class="stat-label">Rank Status</div></div>', unsafe_allow_html=True)

# --- Input Section ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 🎯 Mission Objectives")
    goals = st.text_area(
        "Current Priorities & Future Goals", 
        height=200, 
        placeholder="e.g., Finish Backend API, Learn Vector Databases, Meditate for 20 mins..."
    )

with col_in2:
    st.markdown("### ⏱ Time Allocation")
    hours = st.slider("Available Deep Work / Shallow Work Hours", 1, 16, 8)
    st.info("The AI optimizes your schedule based on biological peak focus nodes (90-min cycles).")
    
    gen_btn = st.button("🚀 Architect Daily Plan")

# --- Generation Logic ---
if gen_btn:
    if not goals:
        st.warning("⚠️ Please define your mission objectives first.")
    else:
        with st.status("🧠 Synthesizing Daily Strategy...", expanded=True) as status:
            st.write("🌌 Deconstructing goal hierarchy...")
            time.sleep(1)
            st.write("🔬 Calculating optimal time slots...")
            time.sleep(1)
            st.write("📊 Finalizing focus suggestions...")
            
            result = generate_plan(goals, hours, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                # Add metadata
                result["timestamp"] = datetime.now().isoformat()
                result["date"] = datetime.now().strftime("%Y-%m-%d")
                
                # Check for streak update
                today = result["date"]
                last_date = st.session_state["data"].get("last_date")
                
                if last_date != today:
                    st.session_state["data"]["streak"] += 1
                    st.session_state["data"]["last_date"] = today
                
                # Add to history
                st.session_state["data"]["plans"].append(result)
                save_data(st.session_state["data"])
                
                status.update(label="✅ Daily Strategy Ready!", state="complete")
                st.session_state["current_plan"] = result
                st.snow()

# --- Plan Presentation ---
current_plan = st.session_state.get("current_plan")
if not current_plan and st.session_state["data"]["plans"]:
    current_plan = st.session_state["data"]["plans"][-1]

if current_plan:
    st.markdown("---")
    
    col_out1, col_out2 = st.columns([3, 1], gap="large")
    
    with col_out1:
        st.markdown(f"### 📅 Tactical Execution: {current_plan.get('date', 'Today')}")
        
        for i, task in enumerate(current_plan.get("daily_plan", [])):
            with st.container():
                st.markdown(f"""
                <div class="task-card">
                    <div class="task-time">{task.get('time_slot', 'N/A')} ({task.get('time_required', 'N/A')})</div>
                    <div class="task-title">{task.get('task', 'No Task Name')}</div>
                    <div>
                        <span class="task-priority priority-{task.get('priority', 'medium').lower()}">{task.get('priority', 'Medium')}</span>
                        <span style="color: #64748b; font-size: 0.9rem;">{task.get('notes', '')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Checkbox for marking as done (stateful)
                done_key = f"done_{current_plan.get('date')}_{i}"
                is_done = st.checkbox("Mark as completed", key=done_key, value=task.get("done", False))
                
                # Update data if changed
                if is_done != task.get("done", False):
                    task["done"] = is_done
                    save_data(st.session_state["data"])

    with col_out2:
        st.markdown("### 🔥 Strategic Insights")
        
        st.markdown(f"""<div class="stat-box">
            <div class="stat-val">{current_plan.get('productivity_score', 85)}%</div>
            <div class="stat-label">Projected Focus Score</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("#### 🧠 Focus Tips")
        for tip in current_plan.get("focus_tips", []):
            st.info(f"💡 {tip}")
            
        st.markdown("#### 📜 Daily Mantra")
        st.markdown(f"> *{current_plan.get('daily_quote', 'The only way to do great work is to love what you do.')}*")

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Engineering Excellence by Harsh Choudhary<br>
    LiteLLM Universal Model Selection Protocol Active
</div>
""", unsafe_allow_html=True)
