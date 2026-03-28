import streamlit as st
import time
import os
import sys
import json
from datetime import datetime

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import analyze_decision_strategy, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Decision Intelligence Agent", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Visual Blocks) ---
st.markdown("""
<style>
/* App Background */
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0c0a09 50%, #020617 100%);
    color: #f1f5f9;
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
    background: linear-gradient(to right, #10b981, #0ea5e9, #6366f1);
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
.stat-box:hover { transform: translateY(-3px); border-color: #10b981; }

.stat-val { font-size: 1.6rem; font-weight: 800; color: #10b981; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Choice Cards */
.choice-card {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 5px solid #10b981;
    margin-bottom: 1.2rem;
}
.choice-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; }
.choice-body { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }

/* Input Fields */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f1f5f9 !important;
    border-radius: 12px !important;
}

/* Control Buttons */
.stButton button {
    width: 100%;
    height: 3.5rem;
    background: linear-gradient(90deg, #10b981, #0ea5e9);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Swarm ---
with st.sidebar:
    st.markdown("### 🧬 AI Intelligence Intelligence")
    provider = st.selectbox("AI Host", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Language Hub", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### ⚖️ Decision Focus")
    st.info("ProductivityOS Decision Agent utilizes cross-functional risk models to eliminate cognitive bias.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Decision Intelligence Agent</h1>
    <p>ProductivityOS: Choices Deconstructed via High-Fidelity Logic & Risk Synthesis ⚖️🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Enabled</div>
        <div class="stat-label">Logic Audit</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Forensic</div>
        <div class="stat-label">Choice Mapping</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Active</div>
        <div class="stat-label">Bias Scan</div>
    </div>""", unsafe_allow_html=True)
with col_v4:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Synced</div>
        <div class="stat-label">Productivity Hub</div>
    </div>""", unsafe_allow_html=True)

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### ❓ Decision Dilemma Archetype")
    dilemma = st.text_area(
        "Describe your Mission Critical Decision", 
        height=180, 
        placeholder="Should I leave my job to build a SaaS startup? Or stay for stability while side-hustling..."
    )

with col_in2:
    st.markdown("### 📌 Tactical Options & Criteria")
    current_options = st.text_area("Options (leave empty for AI generation)", height=80, placeholder="Option A: Full time startup, Option B: Hybrid side-hustle...")
    priorities = st.text_input("Success Criteria / Priorities", placeholder="Profitability, Creative Freedom, Risk mitigation...")

proc_btn = st.button("🚀 Architect Forensic Decision Synthesis")

# --- Generation Logic ---
if proc_btn:
    if not dilemma:
        st.error("⚠️ Mission Failed: DIlemma context required for forensic analysis.")
    else:
        with st.status("🧠 Synthesizing Logical Choice Architectures...", expanded=True) as status:
            st.write("🌌 Deconstructing dilemma nodes and options...")
            time.sleep(1)
            st.write("🔬 Auditing Pros/Cons against success criteria...")
            time.sleep(1)
            st.write("📊 Finalizing High-Precision Reasoning Memeo...")
            
            result = analyze_decision_strategy(dilemma, current_options, priorities, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Decision Intelligence Finalized!", state="complete")
                st.session_state["decision_result"] = result
                st.snow()

# --- Results Presentation ---
res = st.session_state.get("decision_result")
if res:
    st.markdown("---")
    
    col_out1, col_out2 = st.columns([2, 1], gap="large")
    
    with col_out1:
        st.markdown(f"### 🏆 Primary Strategic Selection: **{res.get('best_choice')}**")
        
        st.markdown("### ⚖️ Choice Comparison Grid")
        for idx, item in enumerate(res.get("analysis", [])):
            with st.expander(f"OPT #{idx+1}: {item.get('option')} (Strategic Weight: {item.get('strategic_weight', 50)}/100)", expanded=(idx==0)):
                col_p, col_c = st.columns(2)
                with col_p:
                    st.markdown("**🛡️ PROS:**")
                    for p in item.get("pros", []):
                        st.success(f"✔️ {p}")
                with col_c:
                    st.markdown("**🔴 CONS:**")
                    for c in item.get("cons", []):
                        st.error(f"❌ {c}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🧠 Logic-Driven Reasoning Architecture")
        st.write(res.get("reasoning_architecture", "Synthesis complete."))

    with col_out2:
        st.markdown("### 📊 Consistency & Confidence Metrics")
        
        metrics = res.get("confidence_metrics", {})
        score = metrics.get("score", 0)
        risk = metrics.get("risk_level", "Medium")
        
        st.markdown(f"""
        <div class="stat-box" style="background: rgba(16, 185, 129, 0.1);">
            <div class="stat-val">{score}/10</div>
            <div class="stat-label">Logic Confidence</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-box" style="background: rgba(239, 68, 68, 0.05);">
            <div style="font-size: 1.2rem; font-weight: 800; color: {'#ef4444' if risk == 'High' else '#10b981'}">RISK: {risk}</div>
            <div class="stat-label">Execution Uncertainty</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🧪 Ambiguity Detection")
        st.info(f"🧬 {metrics.get('ambiguity_factor', 'Detected clear variables.')}")
        
        st.markdown("---")
        st.markdown("### 🧠 Decision Mentor's Pith")
        st.markdown(f"> *{res.get('decision_pith', 'The cost of overthinking is always greater than the cost of a slightly imperfect choice.')}*")
        
        # Export logic
        export_text = f"DECISION INTELLIGENCE BRIEF: {res.get('best_choice')}\n\nREASONING:\n{res.get('reasoning_architecture')}\n\nCONFIDENCE: {score}/10\n"
        st.download_button(
            label="⬇️ Export Decision Memo (.txt)",
            data=export_text,
            file_name=f"Decision_Brief_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Strategic Engineering by Harsh Choudhary<br>
    Universal Decision Model Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
