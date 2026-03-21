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
    page_title="NeuralData AI v2.0 | Batch Integrity Matrix",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS (Updated for V2) ---
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #050a1b, #0c1a3a, #010409);
        color: #f8fafc;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    .main-header h1 {
        font-size: 5.5rem;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #d946ef);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -5px;
        text-align: center;
    }
    
    .glass-panel {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 35px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.7);
    }
    
    .rule-card {
        background: rgba(15, 23, 42, 0.85);
        border-right: 6px solid #818cf8;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
    }
    
    .health-gauge-bg {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 50%;
        width: 15rem;
        height: 15rem;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 4px solid #38bdf8;
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Logic ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/data-backup.png", width=64)
    st.markdown("## Integrity Matrix v2.0")
    
    mode = st.radio("🛠️ Operation Mode", ["Single Hub", "Neural Batch Matrix"])
    
    st.markdown("---")
    st.markdown("### 🧬 AI Processing Config")
    MODELS = {
        "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY" },
        "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY" }
    }
    selected_model = st.selectbox("🌐 Engine", list(MODELS.keys()))
    api_key = st.text_input("🔑 API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 🛠️ Custom Neural Rules")
    if 'rules' not in st.session_state:
        st.session_state.rules = []

    with st.expander("➕ Add Logic Directive"):
        r_col = st.text_input("Column Target", placeholder="e.g. age")
        r_op = st.selectbox("Operator", ["range", "regex", "not_null", "custom"])
        r_val = st.text_input("Value/Pattern", placeholder="e.g. [18, 99]")
        r_desc = st.text_input("Rationale", placeholder="Must be adults")
        if st.button("Inject Logic"):
            try:
                # Handle range input conversion
                val = eval(r_val) if "[" in r_val else r_val
                st.session_state.rules.append({"column": r_col, "operator": r_op, "value": val, "description": r_desc})
                st.rerun()
            except:
                st.error("Invalid range format. Use [min, max]")
                
    for i, r in enumerate(st.session_state.rules):
        st.markdown(f"""
        <div class="rule-card">
            <span style="color: #818cf8; font-weight: 800;">{r['column'].upper()}</span>: {r['operator']} 
            <br><small style="color: #94A3B8;">{r['description']}</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Nuke Rule {i}", key=f"del_{i}"):
            st.session_state.rules.pop(i)
            st.rerun()

st.markdown('<div class="main-header"><h1>🧬 NeuralData v2.0</h1><p style="text-align: center;">Advanced Multi-Cloud Batch Integrity Matrix</p></div>', unsafe_allow_html=True)

# --- Implementation ---
if mode == "Single Hub":
    uploaded_file = st.file_uploader("📥 Upload CSV for Audit", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### 📊 Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)
        
        if st.button("🚀 Execute Neural Pipeline", type="primary", use_container_width=True):
            with st.spinner("Processing..."):
                cleaner = AdvancedCSVCleaner(df, uploaded_file.name)
                for r in st.session_state.rules:
                    cleaner.add_custom_rule(r["column"], r["operator"], r["value"], r["description"])
                
                cleaner.final_pipeline(
                    ai_provider=selected_model.split(" ")[0].lower() if api_key else None,
                    ai_model=MODELS[selected_model]["id"] if api_key else None,
                    api_key=api_key
                )
                report = cleaner.finalize_report()
                
                # --- Quick Metrics ---
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Integrity", f"{report['health_score']}%")
                m2.metric("Duplicates Nuked", report["duplicates_removed"])
                m3.metric("Rule Violations", len(report["rule_violations"]))
                m4.metric("AI Semantic Fixes", len(report["llm_refinements"]))
                
                st.markdown("### 🛡️ Audit Log")
                for v in report["rule_violations"]:
                    st.warning(f"Row {v.get('row', 'N/A')}: {v['column']} failed '{v['rule']}'")
                
                st.download_button("Download Cleaned CSV", data=cleaner.df.to_csv(index=False), file_name=f"neural_v2_{uploaded_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    uploaded_files = st.file_uploader("📥 Upload Batch (Multi-CSV)", type=["csv"], accept_multiple_files=True)
    if uploaded_files:
        if st.button("🚀 Execute Neural Batch Matrix", type="primary", use_container_width=True):
            batch_reports = []
            cleaned_zip_files = [] # For demo we just track them
            
            with st.spinner("Processing Neural Batch..."):
                for f in uploaded_files:
                    df = pd.read_csv(f)
                    cleaner = AdvancedCSVCleaner(df, f.name)
                    for r in st.session_state.rules:
                        cleaner.add_custom_rule(r["column"], r["operator"], r["value"], r["description"])
                    
                    cleaner.final_pipeline(
                        ai_provider=selected_model.split(" ")[0].lower() if api_key else None,
                        ai_model=MODELS[selected_model]["id"] if api_key else None,
                        api_key=api_key
                    )
                    report = cleaner.finalize_report()
                    batch_reports.append(report)
                
                # Aggregate Review
                avg_health = sum(r['health_score'] for r in batch_reports) / len(batch_reports)
                
                st.markdown(f"""
                <div class="health-gauge-bg">
                    <div style="text-align: center;">
                        <span style="font-size: 3.5rem; font-weight: 900; color: #38bdf8;">{avg_health:.1f}%</span>
                        <br><span style="color: #94A3B8; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 2px;">Aggregate Score</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📂 Batch File Audit Matrix")
                for r in batch_reports:
                    with st.expander(f"📄 {r['filename']} | Score: {r['health_score']}%"):
                        st.write(f"Duplicates: {r['duplicates_removed']}")
                        st.write(f"Violations: {len(r['rule_violations'])}")
                        st.json(r)
                
                st.success(f"Batch Processing Complete. Processed {len(uploaded_files)} matrices.")
