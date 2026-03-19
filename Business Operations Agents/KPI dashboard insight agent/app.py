import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
from datetime import date
from agent import generate_insights, save_outputs

# Configure the Streamlit page
st.set_page_config(
    page_title="InsightCore AI | Strategic KPI Intelligence",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Glassmorphism */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        background: -webkit-linear-gradient(45deg, #38BDF8, #60A5FA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -2px;
    }
    
    .glass-panel {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    
    .metric-bubble {
        background: rgba(15, 23, 42, 0.7);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .insight-card {
        background: rgba(15, 23, 42, 0.7);
        border-top: 4px solid #38BDF8;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover { transform: translateY(-3px); background: rgba(56, 189, 248, 0.05); }
    .risk-card { border-top-color: #F87171; }
    .opp-card { border-top-color: #34D399; }
    .focus-card { border-top-color: #FBBF24; }
    
    .card-title {
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier causal analytics." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Dynamic business intuition." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Massive data synthesis." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "Lightning-fast intelligence." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/line-chart.png", width=64)
    st.markdown("## Global Engine Settings")
    selected_model_label = st.selectbox("🌐 Select AI Engine", list(MODELS.keys()))
    model_config = MODELS[selected_model_label]
    st.caption(f"_{model_config['doc']}_")
    
    is_custom = model_config["id"] == "custom"
    actual_model_id = st.text_input("Model ID", value=model_config["id"] if not is_custom else "", placeholder="e.g. together_ai/mixtral...")
    api_key_required = model_config["env_var"] if not is_custom else "API Key"
    
    api_key = st.text_input(f"{api_key_required}", type="password", placeholder=f"Enter {api_key_required}...")
    if not is_custom and api_key:
        os.environ[api_key_required] = api_key
        
    st.markdown("---")
    st.markdown("### Agent Architecture v2.0")
    st.markdown("""
    - **Causality Detection Engine**
    - **Interactive CSV Dashboard**
    - **Plotly Data Visualization**
    - **Advanced Risk Attribution**
    """)
    st.markdown("---")
    st.caption("InsightCore AI • Powered by LiteLLM")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>💹 InsightCore AI</h1><p>Strategic causal analytics for multi-dimensional performance metrics.</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    # Mode selection
    analysis_mode = st.radio("Choose Analysis Mode", ["Manual Metric Entry", "CSV Document Analysis"], horizontal=True)
    
    kpi_raw = ""
    
    if analysis_mode == "Manual Metric Entry":
        default_input = (
            "KPIs:\n- Monthly Active Users: 120,000 (↑ 8% MoM)\n- Churn Rate: 3.2% (↑ 0.5%)\n- Revenue Growth: 12% QoQ\n- Customer Support Tickets: 1,450 (↓ 10%)\n\n"
            "Business Context: Recent product update and pricing changes"
        )
        kpi_raw = st.text_area("Input performance metrics and context:", value=default_input, height=200)
    else:
        uploaded_csv = st.file_uploader("Upload KPI CSV File", type=["csv"])
        if uploaded_csv:
            df = pd.read_csv(uploaded_csv)
            st.session_state['df'] = df
            st.markdown("### 📊 Metrics Editor")
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            kpi_raw = f"KPI CSV DATA:\n{edited_df.to_string()}\n\nBusiness Context: Batch analytics from CSV upload."
            
            # Simple visualization
            st.markdown("### 📈 Tactical Trend Preview")
            if not edited_df.empty:
                numeric_cols = edited_df.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 1:
                    fig = px.bar(edited_df, x=edited_df.columns[0], y=numeric_cols, template="plotly_dark", barmode="group", color_discrete_sequence=px.colors.sequential.Teal)
                    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True)

    generate_btn = st.button("🚀 Generate Advanced Narrative Intelligence", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key and not os.environ.get(api_key_required):
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    elif not kpi_raw.strip():
        st.warning("⚠️ Please provide KPI data to analyze.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id} AI... performing causal mapping..."):
            try:
                results = generate_insights(kpi_raw, model_name=actual_model_id, api_key=final_api_key)
                save_outputs(results)
                
                st.success("✅ Multi-Dimensional Strategic Analysis Finalized!")
                
                # Executive Summary Header
                st.markdown(f"""
                <div class="glass-panel">
                    <h2 style="color: #38BDF8; margin-bottom: 0.5rem;">📈 Strategic Executive Summary</h2>
                    <p style="font-size: 1.25rem; font-weight: 500;">{results.get('executive_summary', 'N/A')}</p>
                    <p style="font-size: 1rem; color: #94A3B8; line-height: 1.6; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1rem; margin-top: 1.5rem;">{results.get('detailed_analysis', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Grid
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="insight-card"><div class="card-title">📡 Key Trends</div>', unsafe_allow_html=True)
                    for item in results.get('key_trends', []): st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="insight-card ris-card risk-card"><div class="card-title" style="color: #F87171;">⚠️ Strategic Risks</div>', unsafe_allow_html=True)
                    for item in results.get('risks', []): st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="insight-card focus-card"><div class="card-title" style="color: #FBBF24;">💹 Causality & Attribution</div>', unsafe_allow_html=True)
                    for item in results.get('causality_mapping', []): st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="insight-card opp-card"><div class="card-title" style="color: #34D399;">💡 Untapped Growth Opportunities</div>', unsafe_allow_html=True)
                    for item in results.get('opportunities', []): st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Download
                st.markdown("### 📥 Distribution & Persistence")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"kpi_intelligence_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("kpi_insights.txt", "r", encoding="utf-8") as f: txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"kpi_intelligence_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Analysis Architectural Failure ({actual_model_id}): {str(e)}")
