import streamlit as st
import time
import os
import sys

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import generate_learning_roadmap, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Learning Roadmap", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Visual Timelines) ---
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

/* Dashboard Cards */
.plan-card {
    background: rgba(30, 41, 59, 0.4);
    padding: 1.5rem;
    border-radius: 16px;
    border-top: 4px solid #6366f1;
    height: 100%;
    margin-bottom: 1.5rem;
}

.plan-title { font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 1rem; }
.plan-item { font-size: 0.95rem; color: #cbd5e1; margin-bottom: 0.5rem; }

/* Weekly Box */
.week-box {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.2rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 1rem;
}

.week-label { font-size: 0.85rem; color: #6366f1; font-weight: 700; text-transform: uppercase; margin-bottom: 0.3rem; }
.week-focus { font-size: 1.1rem; color: #fff; font-weight: 600; margin-bottom: 0.5rem; }

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
    st.markdown("### 🧬 Roadmap Swarm Config")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Intelligence Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### ⚡ Transformation Strategy: Active")
    st.info("The Roadmap Agent aligns your current knowledge with the elite benchmarks for your target role.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Learning Roadmap</h1>
    <p>90-day mastery blueprints across portfolio, theory, and high-ROI career nodes. 📚</p>
</div>
""", unsafe_allow_html=True)

# --- Pre-fill Check ---
init_role = st.session_state.get("target_role", "Data Scientist")
init_skills = st.session_state.get("user_resume", "") # Or extracted skills if previous agent provided them

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 🎯 Career Destination")
    target_role_input = st.text_input("Target Job Role", value=init_role, placeholder="e.g. Senior Backend Engineer (Node.js/AWS)")

with col_in2:
    st.markdown("### 🧠 Current Baseline")
    current_skills_input = st.text_area("Your Existing Skills / Experience", height=100, value=init_skills, placeholder="e.g. Python, basic SQL, Flask...")

# --- Initialization Logic ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Architect My 90-Day Mastery Blueprint"):
    if not target_role_input or not current_skills_input:
        st.error("⚠️ We need both a Target Role and Current Baseline to build your roadmap.")
    else:
        with st.status("🧠 Synthesizing Mastery Nodes...", expanded=True) as status:
            st.write("🌐 Deep-scanning role meta-data...")
            time.sleep(1)
            st.write("📈 Mapping learning trajectories...")
            time.sleep(1)
            st.write("🛠 Designing project-based benchmarks...")
            
            # Run Generator
            result = generate_learning_roadmap(
                target_role_input, current_skills_input, ai_model, user_api_key if user_api_key else None
            )
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Roadmap Synthesized!", state="complete")
                st.session_state["roadmap_result"] = result

# --- Results Presentation ---
if "roadmap_result" in st.session_state:
    res = st.session_state["roadmap_result"]
    
    st.markdown("---")
    st.markdown(f"### 🏆 Destination: {target_role_input}")
    st.markdown(f"**Strategic Strategy:** {res.get('strategic_overview', 'Plan ready.')}")
    
    # Month Cards
    col_m1, col_m2, col_m3 = st.columns(3, gap="medium")
    
    with col_m2:
        st.markdown("""<div class="plan-card" style="border-top-color: #f97316;">
            <div class="plan-title">📅 Phase 2: Building Mastery (Day 60)</div>
        """, unsafe_allow_html=True)
        for item in res.get("60_day_plan", []):
            st.markdown(f"<div class='plan-item'>✔ {item}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_m1:
        st.markdown("""<div class="plan-card">
            <div class="plan-title">📅 Phase 1: Foundation (Day 30)</div>
        """, unsafe_allow_html=True)
        for item in res.get("30_day_plan", []):
            st.markdown(f"<div class='plan-item'>✔ {item}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_m3:
        st.markdown("""<div class="plan-card" style="border-top-color: #22c55e;">
            <div class="plan-title">📅 Phase 3: Final Polishing (Day 90)</div>
        """, unsafe_allow_html=True)
        for item in res.get("90_day_plan", []):
            st.markdown(f"<div class='plan-item'>✔ {item}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Weekly & Projects
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📆 Weekly Infiltration Plan", "🛠 Portfolio Project Pipeline"])
    
    with tab1:
        st.markdown("### Week-by-Week Breakdown")
        for week in res.get("weekly_breakdown", []):
            st.markdown(f"""
            <div class="week-box">
                <div class="week-label">Week {week.get('week_number', week.get('week', ''))}</div>
                <div class="week-focus">{week.get('focus', 'Deep Dive')}</div>
                <div style="font-size: 0.9rem; color: #94a3b8;">
                    {" • ".join(week.get('tasks', []))}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Portfolio-Grade Impact Projects")
        for proj in res.get("projects", []):
            with st.expander(f"{proj.get('title', 'Project Node')} [{proj.get('complexity', 'Mid')}]", expanded=True):
                st.write(proj.get("description", "Demonstrate mastery through this build."))
                st.button(f"🔗 Find Starter Code / Tutorials for {proj.get('title', '')}")

    # Recommended Resources
    if res.get("recommended_resources"):
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 📚 High-Sync Resources")
            for res_item in res["recommended_resources"]:
                st.write(f"- {res_item}")

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by CareerOS Roadmap Swarm • Architected by Harsh Choudhary<br>
    Universal Model Selection Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
