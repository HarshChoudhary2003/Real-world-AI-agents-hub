import streamlit as st
import time
import os
import sys
import json
from datetime import datetime

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import summarize_knowledge, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Knowledge Intelligence Hub", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Visual Blocks) ---
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
    background: linear-gradient(to right, #facc15, #fbbf24, #f59e0b);
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
.stat-box:hover { transform: translateY(-3px); border-color: #facc15; }

.stat-val { font-size: 1.6rem; font-weight: 800; color: #facc15; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Knowledge Nodes */
.knowledge-card {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 5px solid #facc15;
    margin-bottom: 1.2rem;
}
.knowledge-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; }
.knowledge-body { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }

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
    background: linear-gradient(90deg, #facc15, #f59e0b);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(250, 204, 21, 0.3);
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Intelligence Cluster ---
with st.sidebar:
    st.markdown("### 🧬 AI Intelligence Cluster")
    provider = st.selectbox("Intelligence Node", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Language Engine", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### 📂 Content Ingestion")
    uploaded_file = st.file_uploader("Upload Knowledge Node (.txt/.md)", type=["txt", "md"])
    if uploaded_file:
        st.success("Knowledge Source Ingested.")
    
    st.markdown("---")
    st.markdown("#### ⚙️ Synthesis Configuration")
    synth_mode = st.radio("Compression Density", ["Short & Punchy", "Detailed Synthesis"])

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Knowledge Summarizer Agent</h1>
    <p>ProductivityOS: Tactical Deconstruction of High-Density Content 📚🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Enabled</div>
        <div class="stat-label">Learning Acceleration</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Surgical</div>
        <div class="stat-label">Synthesis Hub</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Active</div>
        <div class="stat-label">Sentiment Scan</div>
    </div>""", unsafe_allow_html=True)
with col_v4:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Synced</div>
        <div class="stat-label">Productivity Hub</div>
    </div>""", unsafe_allow_html=True)

# --- Input Area ---
st.markdown("### 📑 Macro-Content Feed")
default_text = ""
if uploaded_file:
    default_text = uploaded_file.read().decode("utf-8")

content_input = st.text_area(
    "Paste Article, Research Notes, or Blog Content", 
    height=280, 
    value=default_text,
    placeholder="Alice: Paste any long content here that you want to deconstruct into tactical intelligence..."
)

proc_btn = st.button("🚀 Architect Knowledge Synthesis")

# --- Generation Logic ---
if proc_btn:
    if not content_input:
        st.error("⚠️ Feed Failed: No content detected for synthesis.")
    else:
        with st.status("🧠 Processing Content Clusters...", expanded=True) as status:
            st.write("🌌 Deconstructing narrative nodes...")
            time.sleep(1)
            st.write("🔬 Extracting tactical first principles...")
            time.sleep(1)
            st.write("📊 Finalizing Knowledge Architecture...")
            
            result = summarize_knowledge(content_input, synth_mode, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Knowledge Node Finalized!", state="complete")
                st.session_state["summary_result"] = result
                st.snow()

# --- Results Presentation ---
res = st.session_state.get("summary_result")
if res:
    st.markdown("---")
    
    col_out1, col_out2 = st.columns([3, 2], gap="large")
    
    with col_out1:
        st.markdown(f"### 🎯 Neural Summary: {res.get('context_audit', 'Tactical Synthesis')}")
        st.write(res.get("summary", "Synthesis complete."))
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚡ Tactical Takeaways")
        for t in res.get("takeaways", []):
            st.success(f"🚀 {t}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🧬 Core Analytical Insights")
        for i in res.get("insights", []):
            st.info(f"💡 {i}")

    with col_out2:
        st.markdown("### 📌 Critical Knowledge Points")
        for point in res.get("key_points", []):
            st.markdown(f"""
            <div class="knowledge-card">
                <div class="knowledge-body">{point}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🧠 Learning Acceleration Swarm")
        for l in res.get("learning_accelerator", []):
            st.warning(f"🎓 {l}")
            
        st.markdown("---")
        # Export logic
        export_text = f"KNOWLEDGE SYNTHESIS BY ProductivityOS\nSOURCE TYPE: {res.get('context_audit')}\n\nSUMMARY:\n{res.get('summary')}\n\nKEY POINTS:\n"
        for p in res.get("key_points", []):
            export_text += f"- {p}\n"
            
        st.download_button(
            label="⬇️ Export Knowledge Brief (.txt)",
            data=export_text,
            file_name=f"Knowledge_Synthesis_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Cognitive Engineering by Harsh Choudhary<br>
    Universal Behavioral Hub Powered by LiteLLM Framework
</div>
""", unsafe_allow_html=True)
