import streamlit as st
import time
import os
import sys
import json
from datetime import datetime

# Local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import process_meeting, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Meeting Intelligence Architect", 
    page_icon="📝", 
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
    background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
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
}

.stat-val { font-size: 1.6rem; font-weight: 800; color: #38bdf8; }
.stat-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; margin-top: 0.5rem; }

/* Tactical Blocks */
.tactical-card {
    background: rgba(15, 23, 42, 0.6);
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 5px solid #818cf8;
    margin-bottom: 1.2rem;
}
.tactical-title { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; }
.tactical-body { color: #94a3b8; font-size: 0.95rem; line-height: 1.6; }

/* Action Items Table-like UI */
.action-item {
    background: rgba(15, 23, 42, 0.4);
    padding: 1rem;
    border-radius: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.action-priority { font-size: 0.7rem; font-weight: 800; text-transform: uppercase; padding: 2px 8px; border-radius: 4px; }
.priority-high { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.priority-medium { background: rgba(99, 102, 241, 0.2); color: #818cf8; }
.priority-low { background: rgba(34, 197, 94, 0.2); color: #4ade80; }

/* Input Fields */
.stTextArea textarea {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
}

/* Control Buttons */
.stButton button {
    width: 100%;
    height: 3.5rem;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(56, 189, 248, 0.3);
}

.footer { text-align: center; color: #475569; margin-top: 5rem; font-size: 0.85rem; padding-bottom: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Configuration ---
with st.sidebar:
    st.markdown("### 🧬 AI Intelligence Swarm")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    ai_model = st.selectbox("Neural Model", SUPPORTED_MODELS[provider])
    user_api_key = st.text_input(f"{provider} API Key", type="password")
    
    st.markdown("---")
    st.markdown("#### 📁 Tactical Feeds")
    uploaded_file = st.file_uploader("Import Transcript (.txt/md)", type=["txt", "md"])
    if uploaded_file:
        st.success("Transcript Ingested.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Meeting Intelligence Agent</h1>
    <p>ProductivityOS: Tactical Deconstruction of Unstructured Temporal Logs 🚀</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard Overviews ---
col_v1, col_v2, col_v3, col_v4 = st.columns(4)
with col_v1:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Enabled</div>
        <div class="stat-label">Sentiment Audit</div>
    </div>""", unsafe_allow_html=True)
with col_v2:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Surgical</div>
        <div class="stat-label">Task Extraction</div>
    </div>""", unsafe_allow_html=True)
with col_v3:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">Active</div>
        <div class="stat-label">Follow-up Engine</div>
    </div>""", unsafe_allow_html=True)
with col_v4:
    st.markdown("""<div class="stat-box">
        <div class="stat-val">7.8s</div>
        <div class="stat-label">Synthesis Latency</div>
    </div>""", unsafe_allow_html=True)

# --- Input Area ---
st.markdown("### 📑 Transcript Data Feed")
default_text = ""
if uploaded_file:
    default_text = uploaded_file.read().decode("utf-8")

transcript_input = st.text_area(
    "Paste Raw Meeting Notes / Unstructured Transcript", 
    height=300, 
    value=default_text,
    placeholder="Alice: We need to finish the API by Friday.\nBob: I will handle the auth layer.\nCharlie: Let's use PostgreSQL for the database..."
)

proc_btn = st.button("🚀 Synthesize Meeting Intelligence")

# --- Generation Logic ---
if proc_btn:
    if not transcript_input:
        st.error("⚠️ Data Feed error: No transcript detected.")
    else:
        with st.status("🧠 Processing Neural Clusters...", expanded=True) as status:
            st.write("🌌 Deconstructing narrative nodes...")
            time.sleep(1)
            st.write("🔬 Extracting action items and decisions...")
            time.sleep(1)
            st.write("📊 Finalizing Tactical Architecture...")
            
            result = process_meeting(transcript_input, ai_model, user_api_key if user_api_key else None)
            
            if "error" in result:
                status.update(label="❌ Synthesis Failed", state="error")
                st.error(result["error"])
            else:
                status.update(label="✅ Meeting Intelligence Finalized!", state="complete")
                st.session_state["meeting_result"] = result
                st.snow()

# --- Results Presentation ---
res = st.session_state.get("meeting_result")
if res:
    st.markdown("---")
    
    col_out1, col_out2 = st.columns([3, 2], gap="large")
    
    with col_out1:
        st.markdown("### 🎯 Executive Summary")
        st.write(res.get("summary", "Synthesis complete."))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### ✅ Action Node Registry")
        for item in res.get("action_items", []):
            p_class = f"priority-{item.get('priority', 'medium').lower()}"
            st.markdown(f"""
            <div class="action-item">
                <div>
                    <span style="font-weight: 700; color: #f8fafc;">{item.get('task', 'No Task')}</span><br>
                    <span style="font-size: 0.8rem; color: #64748b;">ASSIGNED: {item.get('owner', 'Unassigned')} | DEADLINE: {item.get('deadline', 'TBD')}</span>
                </div>
                <span class="action-priority {p_class}">{item.get('priority', 'Medium')}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("### 📊 Strategic Decisions")
        for d in res.get("decisions", []):
            st.success(f"📌 {d}")

    with col_out2:
        st.markdown("### 🧠 Sentiment Audit")
        s_val = res.get("sentiment_analysis", "Neutral")
        st.info(f"🎭 Status: {s_val}")
        
        st.markdown("### 📌 Key Extraction Points")
        for point in res.get("key_points", []):
            st.markdown(f"- {point}")
            
        st.markdown("### 🔁 Persistent Follow-ups")
        for f in res.get("follow_ups", []):
            st.markdown(f"- {f}")
            
        st.markdown("### 🚀 Next Meeting Architecture")
        for tip in res.get("next_meeting_agenda", []):
            st.markdown(f"📝 {tip}")
            
        st.markdown("---")
        # Export logic
        export_text = f"SUMMARY\n{res.get('summary')}\n\nACTION ITEMS\n"
        for item in res.get("action_items", []):
            export_text += f"- [{item.get('priority')}] {item.get('task')} ({item.get('owner')})\n"
            
        st.download_button(
            label="⬇️ Export Tactical Brief (.txt)",
            data=export_text,
            file_name="Meeting_Architecture_Brief.txt",
            mime="text/plain"
        )

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by ProductivityOS Swarm • Strategic Engineering by Harsh Choudhary<br>
    LiteLLM Platform • Execution Node Active
</div>
""", unsafe_allow_html=True)
