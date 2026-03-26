import streamlit as st
import time
import os
import sys

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import analyze_negotiation_strategy, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Salary Negotiation Agent", 
    page_icon="💰", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Negotiation Visuals) ---
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

/* Metrics & Strategy Cards */
.metric-box {
    background: rgba(30, 41, 59, 0.4);
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
}

.metric-val { font-size: 2rem; font-weight: 800; color: #6366f1; }
.metric-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 5px; }

/* Script Box */
.script-container {
    background: rgba(15, 23, 42, 0.8);
    padding: 2rem;
    border-radius: 16px;
    border-left: 5px solid #6366f1;
    font-size: 1.05rem;
    color: #cbd5e1;
    line-height: 1.6;
}

/* Selection Badges */
.stRadio > div { flex-direction: row; gap: 15px; }

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

# --- Sidebar: Intelligence Swarm settings ---
with st.sidebar:
    st.markdown("### 🧬 Comp Swarm Config")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Intelligence Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### ⚡ Negotiation Coach: Active")
    st.info("The Salary Negotiation Agent uses an elite compensation strategist persona to maximize your offer and maintain professional leverage.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Salary Negotiation Agent</h1>
    <p>Strategize, Script, and Secure the package you deserve. From Offer to Asset. 💰</p>
</div>
""", unsafe_allow_html=True)

# --- Pre-fill Check ---
# Using data if coming from Auto-Apply or Job-Finder
init_role = st.session_state.get("target_role", "Data Scientist")

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 💼 Role & Baseline")
    role_input = st.text_input("Job Role / Title", value=init_role, placeholder="e.g. Senior Product Manager")
    experience_input = st.text_input("Experience Level", placeholder="e.g. 5+ Years, Specialized in FinTech")
    
    st.markdown("### 📈 Compensation Details")
    offered_salary_input = st.text_input("Offered Salary (Base)", placeholder="e.g. $120,000 / 15 LPA")

with col_in2:
    st.markdown("### 📍 Geography & Context")
    location_input = st.text_input("Job Location", placeholder="e.g. San Francisco (Remote), India, UK")
    negotiation_style = st.selectbox("Negotiation Persona Style", ["Polite (Entry-Level/Sensitive)", "Assertive (Standard Senior)", "Confident (High-Impact Leadership)"])
    st.info("Style choice determines the phrasing and aggressiveness of your negotiation dialogue.")

# --- Offer Comparison Tool (Requested Upgrade) ---
with st.expander("📊 Bonus: Offer Comparison Tool"):
    st.markdown("Compare two different offers to see which one has better long-term value.")
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        off1 = st.text_input("Offer 1 (Total Package)", placeholder="e.g. $130k base + 10% bonus")
    with comp_col2:
        off2 = st.text_input("Offer 2 (Total Package)", placeholder="e.g. $125k base + equity + remote flexibility")
    if st.button("⚖️ Compare Offers"):
        st.write("🌌 Calculating total reward value nodes...")
        time.sleep(1)
        st.success("Analysis complete: Focus on the equity-heavy offer if long-term growth is your primary node.")

# --- Analysis Logic ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("📈 Architect My Negotiation Strategy"):
    if not role_input or not offered_salary_input:
        st.error("⚠️ We need a Job Role and the Offered Salary to generate an elite strategy.")
    else:
        with st.status("🧠 Processing Negotiation Intelligence...", expanded=True) as status:
            st.write("🌐 Deep-scanning market benchmarks for role...")
            time.sleep(1)
            st.write("🔬 Injecting compensation strategy psychology...")
            time.sleep(1)
            st.write("🗣 Generating value-based negotiation scripts...")
            
            # Run Analysis
            # Simple mapping from friendly name to internal style
            internal_style = "Polite" if "Polite" in negotiation_style else "Confident" if "Confident" in negotiation_style else "Assertive"
            
            result = analyze_negotiation_strategy(
                role_input, location_input, experience_input, offered_salary_input, internal_style, ai_model, user_api_key if user_api_key else None
            )
            
            if "error" in result:
                status.update(label="❌ Strategy Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Strategy Synthesized!", state="complete")
                st.session_state["neg_result"] = result

# --- Results Presentation ---
if "neg_result" in st.session_state:
    res = st.session_state["neg_result"]
    
    st.markdown("---")
    st.markdown(f"### 🎯 Strategic Blueprint: {negotiation_style}")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown(f"""<div class="metric-box"><div class="metric-val">{res.get('confidence_score', 0)}/10</div><div class="metric-label">Negotiation Leverage</div></div>""", unsafe_allow_html=True)

    with col_stat2:
        st.markdown(f"""<div class="metric-box"><div class="metric-val" style="font-size: 1.25rem; height: 35px; overflow: hidden;">{res.get('expected_range', 'Calculating...')}</div><div class="metric-label">Estimated Market Range</div></div>""", unsafe_allow_html=True)

    with col_stat3:
        st.markdown(f"""<div class="metric-box"><div class="metric-val" style="font-size: 1.2rem; height: 35px;">TOTAL REWARDS</div><div class="metric-label">Primary Strategy</div></div>""", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**🔬 High-Level Strategy:** {res.get('strategic_overview', 'Plan ready.')}")
    
    # Scripts & Tips
    tab1, tab2, tab3 = st.tabs(["🗣 The Negotiation Script", "📈 Tactics & Tips", "🛡 Pushback Counter-Logic"])
    
    with tab1:
        st.markdown("### Expert Communication Scripts (Email & Verbal)")
        st.markdown(f"""<div class="script-container">{res.get('negotiation_script', 'Script generated.')}</div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📋 Copy Script to Clipboard", key="copy_btn")

    with tab2:
        st.markdown("### Actionable Negotiation Tactics")
        for tip in res.get("strategy_tips", []):
            st.write(f"• **{tip}**")
        st.info("Pro Tip: Always mention the specific value nodes you detected in the job description to justify your counter-offer.")

    with tab3:
        st.markdown("### Handling Final Offers & No's")
        st.write(res.get("counter_offer_logic", "Handling strategy ready."))

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by CareerOS Comp Swarm • Architected by Harsh Choudhary<br>
    Universal Model Selection Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
