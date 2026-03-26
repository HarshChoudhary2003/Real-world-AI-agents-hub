import streamlit as st
import time
import os
import sys

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import generate_branding_architecture, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Personal Branding Agent", 
    page_icon="🌐", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Branding Visuals) ---
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

/* Dashboard Metric Box */
.brand-box {
    background: rgba(30, 41, 59, 0.4);
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
    margin-bottom: 1.5rem;
}

.brand-label { font-size: 0.85rem; color: #6366f1; font-weight: 700; text-transform: uppercase; margin-bottom: 0.3rem; }
.brand-val { font-size: 1.5rem; font-weight: 800; color: #fff; }

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

.post-box {
    background: rgba(15, 23, 42, 0.7);
    padding: 1.5rem;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    font-family: 'Inter', sans-serif;
    color: #cbd5e1;
    margin-bottom: 1.5rem;
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Settings ---
with st.sidebar:
    st.markdown("### 🧬 Identity Swarm Config")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Intelligence Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### ⚡ Narrative Architect: Active")
    st.info("The Personal Branding Agent creates a high-entropy, authority-driven digital identity to maximize your market entropy.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Personal Branding Agent</h1>
    <p>Architect your high-impact digital presence. From Applicant to Authority. 🌐</p>
</div>
""", unsafe_allow_html=True)

# --- Pre-fill Check ---
init_resume = st.session_state.get("user_resume", "")
init_role = st.session_state.get("target_role", "Data Scientist")

# --- Input Area ---
col_in1, col_in2 = st.columns([1, 1], gap="large")

with col_in1:
    st.markdown("### 📄 Professional Identity")
    resume_input = st.text_area("Your Core Skills / Resume Context", height=300, value=init_resume, placeholder="Paste your core skills or relevant work highlights...")

with col_in2:
    st.markdown("### 🏆 Achievement Nodes")
    achievements_input = st.text_area("Key Accomplishments / Impacts", height=180, placeholder="List major projects, certifications, or specific measurable results...")
    role_input = st.text_input("Target Authority Role", value=init_role, placeholder="e.g. Lead Machine Learning Engineer")

# --- Generation Logic ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Execute Personal Brand Architecture"):
    if not resume_input or not role_input:
        st.error("⚠️ We need at least a Resume and a Target Role to architect a brand identity.")
    else:
        with st.status("🧠 Synthesizing Identity Meta-Data...", expanded=True) as status:
            st.write("🌌 Mapping technical node entropy...")
            time.sleep(1)
            st.write("🔬 Injecting narrative psychology and authority signals...")
            time.sleep(1)
            st.write("📊 Finalizing digital presence blueprints...")
            
            # Run Generator
            result = generate_branding_architecture(
                resume_input, role_input, achievements_input, ai_model, user_api_key if user_api_key else None
            )
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Identity Synthesized!", state="complete")
                st.session_state["branding_result"] = result

# --- Results Presentation ---
if "branding_result" in st.session_state:
    res = st.session_state["branding_result"]
    
    st.markdown("---")
    st.markdown(f"### 🎯 Identity Destination: {role_input}")
    
    col_stat1, col_stat2 = st.columns([1, 1])
    with col_stat1:
        st.markdown(f"""<div class="brand-box"><div class="brand-label">Core Narrative</div><div class="brand-val" style="font-size: 1.1rem; color: #cbd5e1;">{res.get('strategic_overview', 'Narrative ready.')}</div></div>""", unsafe_allow_html=True)

    with col_stat2:
        st.markdown(f"""<div class="brand-box"><div class="brand-label">Authority Level</div><div class="brand-val">EXPERT-TIER</div></div>""", unsafe_allow_html=True)
        
    # Multi-pane results
    tab1, tab2, tab3 = st.tabs(["✍️ LinkedIn Presence", "🧑💻 Core Bio Architect", "🚀 Strategy Roadmap"])
    
    with tab1:
        st.markdown("### Viral-Style Authority Posts")
        for post in res.get("linkedin_posts", []):
            with st.expander(f"Topic: {post.get('topic', 'Insight Post')}", expanded=True):
                st.markdown(f"<div class='post-box'>{post.get('post_text', '')}</div>", unsafe_allow_html=True)
                st.button(f"📋 Copy to Clipboard", key=f"btn_{post.get('topic')}")

    with tab2:
        col_bio1, col_bio2 = st.columns(2)
        with col_bio1:
            st.markdown("#### GitHub Profile README")
            st.markdown(f"```markdown\n{res.get('github_summary', 'Summary ready.')}\n```")
        with col_bio2:
            st.markdown("#### Portfolio / Personal Bio")
            st.markdown(f"""<div class="post-box" style="border-left: 5px solid #a855f7;">{res.get('portfolio_bio', 'Bio ready.')}</div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("### Personalized Growth Strategy")
        for idx, step in enumerate(res.get("branding_strategy", [])):
            with st.expander(f"Step {idx+1}: {step.get('step', 'Identity Node')}", expanded=(idx==0)):
                st.write(step.get("action", "Execution steps ready."))

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by CareerOS Narrative Swarm • Architected by Harsh Choudhary<br>
    Universal Model Selection Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
