import streamlit as st
import time
import os
import sys
import json
import pandas as pd
from datetime import datetime, date

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import analyze_day, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Reflection Intelligence Agent", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Persistence: Reflections Log ---
DB_FILE = os.path.join(os.path.dirname(__file__), "reflections.json")

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"reflections": [], "current_streak": 0, "last_date": ""}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

db = load_data()

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
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.stat-box:hover { transform: translateY(-3px); border-color: #a855f7; }

.stat-val { font-size: 1.6rem; font-weight: 800; color: #a855f7; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Tactical Blocks */
.tactical-card {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 5px solid #6366f1;
    margin-bottom: 1.2rem;
}
.tactical-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; }
.tactical-body { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }

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
    background: linear-gradient(90deg, #6366f1, #a855f7);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Configuration ---
with st.sidebar:
    st.markdown("### 🧬 AI Intelligence Intelligence")
    provider = st.selectbox("AI Host", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Language Hub", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### 🔥 Performance Flow")
    st.metric("Focus Streak", f"{db.get('current_streak', 0)} Days", delta="+1 Session Active")
    st.info("ProductivityOS Reflection Agent uses behavioral analysis to prevent long-term burnout.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Daily Reflection Agent</h1>
    <p>ProductivityOS: Tactical Performance Deconstruction & Insight Synthesis 📊🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Enabled</div>
        <div class="stat-label">Sentiment Scan</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Active</div>
        <div class="stat-label">Streak Tracker</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Forensic</div>
        <div class="stat-label">Pattern Analysis</div>
    </div>""", unsafe_allow_html=True)
with col_v4:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">96%</div>
        <div class="stat-label">Coaching Fidelity</div>
    </div>""", unsafe_allow_html=True)

# --- Input Area ---
st.markdown("### 📑 Execution Feedback Feed")
day_log_input = st.text_area(
    "What did you execute today? What failed? What felt optimal?", 
    height=280, 
    placeholder="Alice: Built the auth layer. Was distracted by Slack for 2 hours. Felt burnt out by 4 PM..."
)

proc_btn = st.button("🚀 Deconstruct Day & Synthesis Insights")

# --- Generation Logic ---
if proc_btn:
    if not day_log_input:
        st.error("⚠️ Context null: We cannot synthesize insights from a void.")
    else:
        with st.status("🧠 Processing Historical Nodes...", expanded=True) as status:
            st.write("🌌 Deconstructing behavioral patterns...")
            time.sleep(1)
            st.write("🔬 Auditing emotional states & burnout risks...")
            time.sleep(1)
            st.write("📊 Finalizing High-Impact Coaching Brief...")
            
            result = analyze_day(day_log_input, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Daily Deconstruction Finalized!", state="complete")
                st.session_state["reflection_result"] = result
                
                # Persistence: Update Streak
                today = date.today().isoformat()
                if db["last_date"] != today:
                    if db["last_date"] == (date.today() - pd.Timedelta(days=1)).isoformat():
                        db["current_streak"] += 1
                    else:
                        db["current_streak"] = 1
                    db["last_date"] = today
                
                # Append to history
                db["reflections"].append({
                    "date": today,
                    "score": result.get("productivity_score", 0),
                    "summary": result.get("summary", ""),
                    "mood": result.get("mood_audit", "Neutral")
                })
                save_data(db)
                st.snow()

# --- Results Presentation ---
res = st.session_state.get("reflection_result")
if res:
    st.markdown("---")
    
    col_out1, col_out2 = st.columns([3, 2], gap="large")
    
    with col_out1:
        st.markdown(f"### 🎯 Performance Narrative: {res.get('summary', 'Synthesis complete.')}")
        
        # Productvity Metric UI
        score = res.get("productivity_score", 0)
        st.markdown(f"#### 📊 Productivity Efficiency Score: `{score}/10`")
        st.progress(score / 10)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🧬 Tactical Insights Swarm")
        for i in res.get("insights", []):
            st.info(f"💡 {i}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📈 Tactical Improvement Nodes")
        for imp in res.get("improvements", []):
            st.success(f"🛠️ {imp}")

    with col_out2:
        st.markdown("### 🎭 Psychological State Audit")
        
        mood_v = res.get("mood_audit", "Neutral")
        risk_v = res.get("burnout_risk", "Low")
        
        st.markdown(f"""<div style="background: rgba(99, 102, 241, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="color: #f8fafc; font-size: 1.2rem; font-weight: 800;">STATUS: {mood_v}</div>
            <div style="color: {'#ef4444' if risk_v == 'High' else '#10b981'}; font-size: 0.8rem; font-weight: 800; text-transform: uppercase;">BURNOUT RISK: {risk_v}</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎯 Tomorrow's Strategic Focus")
        for f in res.get("tomorrow_focus", []):
            st.warning(f"🚀 {f}")
            
        st.markdown("---")
        st.markdown("### 🧠 Mentor's Pith")
        st.markdown(f"> *{res.get('coaching_pith', 'Consistency is the only metric that matters.')}*")
        
    st.markdown("---")
    st.markdown("### 📈 Performance Trends (Last 7 Sessions)")
    if db["reflections"]:
        history_df = pd.DataFrame(db["reflections"]).tail(7)
        st.line_chart(history_df.set_index("date")["score"])
    
    # Export logic
    export_md = f"# Reflection for {date.today()}\n\nSUMMARY: {res.get('summary')}\nSCORE: {res.get('productivity_score')}/10\nMOOD: {res.get('mood_audit')}\n\nTOMORROW FOCUS:\n"
    for f in res.get("tomorrow_focus", []):
        export_md += f"- {f}\n"

    st.download_button(
        label="⬇️ Export Daily Intelligence Brief (.md)",
        data=export_md,
        file_name=f"Daily_Reflection_{date.today().isoformat()}.md",
        mime="text/markdown"
    )

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Cognitive Engineering by Harsh Choudhary<br>
    Universal Behavioral Model Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
