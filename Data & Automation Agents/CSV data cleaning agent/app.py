import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from agent import AdvancedCSVCleaner, NeuralBatchProcessor, semantic_refine_row

# --- Configure Streamlit ---
st.set_page_config(
    page_title="NeuralData AI v3.0 | Omni-Model Integrity Matrix",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS (V3 Omni-Style) ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #010409, #0d1117, #161b22);
        color: #f8fafc;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    .main-header h1 {
        font-size: 6rem;
        background: linear-gradient(90deg, #0ea5e9, #6366f1, #d946ef);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -6px;
        text-align: center;
        animation: fadeIn 1.5s ease;
    }
    
    .glass-panel {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 40px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 40px 80px -20px rgba(0, 0, 0, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# --- Universal Sidebar Logic ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/data-backup.png", width=64)
    st.markdown("## Integrity Matrix v3.0")
    
    st.markdown("### 🌐 Omni-Model Orchestration")
    MODELS = {
        "OpenAI (GPT-4o)": "gpt-4o",
        "Anthropic (Claude 3.5 Sonnet)": "claude-3-5-sonnet-20240620",
        "Google (Gemini 1.5 Pro)": "gemini/gemini-1.5-pro",
        "Groq (Llama 3 70B)": "groq/llama3-70b-8192",
        "Mistral (Large)": "mistral/mistral-large-latest",
        "Custom Neural Model": "custom"
    }
    
    selected_label = st.selectbox("🤖 Active Neural Hub", list(MODELS.keys()))
    selected_model_id = MODELS[selected_label]
    
    if selected_model_id == "custom":
        selected_model_id = st.text_input("Enter Neural Model ID (LiteLLM)", placeholder="e.g. together_ai/mixtral...")

    # Key Management
    st.markdown("### 🔑 Token Matrix")
    pk_openai = st.text_input("OpenAI Key", type="password")
    pk_anthropic = st.text_input("Anthropic Key", type="password")
    pk_gemini = st.text_input("Gemini Key", type="password")
    pk_groq = st.text_input("Groq Key", type="password")
    
    # Store keys in env for LiteLLM
    if pk_openai: os.environ["OPENAI_API_KEY"] = pk_openai
    if pk_anthropic: os.environ["ANTHROPIC_API_KEY"] = pk_anthropic
    if pk_gemini: os.environ["GEMINI_API_KEY"] = pk_gemini
    if pk_groq: os.environ["GROQ_API_KEY"] = pk_groq
    
    current_key = ""
    if "gpt" in selected_model_id: current_key = pk_openai
    elif "claude" in selected_model_id: current_key = pk_anthropic
    elif "gemini" in selected_model_id: current_key = pk_gemini
    elif "groq" in selected_model_id: current_key = pk_groq
    
    st.markdown("---")
    st.markdown("### 🧪 Rule Matrix")
    if 'rules' not in st.session_state:
        st.session_state.rules = []

    with st.expander("➕ Inject New Logic"):
        r_col = st.text_input("Target Column", placeholder="e.g. email")
        r_op = st.selectbox("Logic", ["range", "regex", "not_null"])
        r_val = st.text_input("Logic Pattern", placeholder="e.g. [0, 100]")
        r_desc = st.text_input("Neural Directive", placeholder="Must be valid email")
        if st.button("Inject Logic"):
            try:
                val = eval(r_val) if "[" in r_val else r_val
                st.session_state.rules.append({"column": r_col, "operator": r_op, "value": val, "description": r_desc})
                st.rerun()
            except:
                st.session_state.rules.append({"column": r_col, "operator": r_op, "value": r_val, "description": r_desc})
                st.rerun()

    for i, r in enumerate(st.session_state.rules):
        st.markdown(f"**{r['column'].upper()}** | `{r['operator']}` | {r['description']}")
        if st.button(f"🗑️ Delete {i}", key=f"del_{i}"):
            st.session_state.rules.pop(i)
            st.rerun()

st.markdown('<div class="main-header"><h1>🧬 NeuralData v3.0</h1><p style="text-align: center;">Advanced Omni-Model Batch Integrity Pipeline</p></div>', unsafe_allow_html=True)

# --- Dataset Interaction Hub ---
uploaded_files = st.file_uploader("📥 Upload CSV Matrices (Supports Multi-Batch)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 Execute Omni-Neural Pipeline", type="primary", use_container_width=True):
        batch_reports = []
        process_progress = st.progress(0)
        
        with st.spinner(f"Interfacing with {selected_model_id}... deconstructing attributes..."):
            for idx, f in enumerate(uploaded_files):
                df = pd.read_csv(f)
                cleaner = AdvancedCSVCleaner(df, f.name)
                for r in st.session_state.rules:
                    cleaner.add_custom_rule(r["column"], r["operator"], r["value"], r["description"])
                
                cleaner.final_pipeline(ai_model=selected_model_id, api_key=current_key)
                batch_reports.append(cleaner.finalize_report())
                process_progress.progress((idx + 1) / len(uploaded_files))
                
                # Save each result for UI retrieval
                st.session_state[f"cleaned_{f.name}"] = cleaner.df.to_csv(index=False)
            
            # Aggregate Review
            score = sum(r['health_score'] for r in batch_reports) / len(batch_reports)
            
            # --- Visual Insights ---
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            col_l, col_r = st.columns([1, 1.5])
            
            with col_l:
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 5rem; font-weight: 900; color: #0ea5e9;">{score:.1f}%</div>
                    <div style="color: #94A3B8; text-transform: uppercase;">Aggregate Health Score</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_r:
                # Dashboard comparison chart
                comp_data = {
                    "File": [r["filename"] for r in batch_reports],
                    "Score": [r["health_score"] for r in batch_reports]
                }
                fig = px.bar(pd.DataFrame(comp_data), x="File", y="Score", color="Score", title="Batch Integrity Distribution")
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#f8fafc")
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Detail Breakdown
            for r in batch_reports:
                with st.expander(f"📄 Audit Log: {r['filename']} ({r['health_score']}%)"):
                    st.json(r)
                    st.download_button(f"📥 Download Cleaned {r['filename']}", 
                                     data=st.session_state[f"cleaned_{r['filename']}"], 
                                     file_name=f"refined_{r['filename']}")

else:
    st.info("👋 Upload one or more CSV files in the sidebar and configure your Token Matrix to begin the Omni-Neural Audit.")
    
    # Tech Showcase
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown("### 🦾 Omni-Intelligence\nPowered by LiteLLM. Support for 100+ models including GPT, Claude, Gemini, and Local LLMs.")
    c2.markdown("### 📊 Batch Matrix\nHigh-velocity batch cleaning for entire data warehouses in seconds.")
    c3.markdown("### 🛠️ Neural Rules\nAdvanced logic directives that allow natural language constraints on structured data.")
    st.markdown('</div>', unsafe_allow_html=True)
