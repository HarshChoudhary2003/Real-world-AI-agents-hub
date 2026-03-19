import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from agent import analyze_campaign_v3, save_outputs_v3

# Configure the Streamlit page
st.set_page_config(
    page_title="AdIntel AI v3.0 | Neural Growth Architecture",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Neural Intelligence Deep Gradient */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #1e1b4b, #020617);
        color: #f8fafc;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        margin-bottom: 3.5rem;
        animation: fadeInDown 1s cubic-bezier(0.22, 1, 0.36, 1);
    }
    
    .main-header h1 {
        font-size: 4.5rem;
        background: linear-gradient(90deg, #0ea5e9, #6366f1, #d946ef);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -3px;
    }
    
    .glass-panel {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px 0 rgba(0, 0, 0, 0.6);
    }
    
    /* Strategic Action Cards */
    .action-card {
        background: rgba(15, 23, 42, 0.85);
        border-left: 6px solid #6366f1;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        transition: all 0.4s ease;
    }
    
    .action-card:hover {
        transform: translateX(10px) scale(1.02);
        background: rgba(15, 23, 42, 1);
        border-left-color: #d946ef;
    }
    
    .urgency-badge {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 900;
        padding: 0.2rem 0.8rem;
        border-radius: 30px;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    
    .critical { background: #ef4444; color: white; }
    .high { background: #f97316; color: white; }
    .medium { background: #3b82f6; color: white; }

    /* Creative Pivot Card */
    .pivot-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(14, 165, 233, 0.2);
        padding: 1.25rem;
        border-radius: 14px;
        margin-bottom: 1.25rem;
    }
    
    .dimension-label {
        font-size: 0.75rem;
        color: #0ea5e9;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier neural audit and scaling logic." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Expert in creative pivot inference." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Multi-dimensional performance mapping." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "High-velocity intelligence audits." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal creative support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.markdown("## Intelligence Matrix v3.0")
    selected_model_label = st.selectbox("🌐 Select AI Engine", list(MODELS.keys()))
    model_config = MODELS[selected_model_label]
    st.caption(f"_{model_config['doc']}_")
    
    is_custom = model_config["id"] == "custom"
    actual_model_id = st.text_input("Active Logic Hub", value=model_config["id"] if not is_custom else "", placeholder="e.g. together_ai/mixtral...")
    api_key_required = model_config["env_var"] if not is_custom else "API Key"
    
    api_key = st.text_input(f"{api_key_required}", type="password", placeholder=f"Enter {api_key_required}...")
    if not is_custom and api_key:
        os.environ[api_key_required] = api_key
        
    st.markdown("---")
    st.markdown("### Neural Capabilities")
    st.markdown("""
    - **Creative Performance Pivot**
    - **Spend Velocity Forecast Matrix**
    - **Diminishing Returns Audit**
    - **Strategic Next-Action Engine**
    - **Market Benchmark Context**
    """)
    st.markdown("---")
    st.caption("AdIntel AI v3.0 • Neural Growth Matrix")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>🤖 AdIntel AI</h1><p>Next-Generation Neural Growth Intelligence & Creative Pivoting</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📊 Dataset Integrity Hub")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        metrics_raw = {
            "Dimension": ["Total Spend", "Impressions", "Clicks", "Conversions", "Cost/Lead (CPL)", "CTR (%)", "CVR (%)"],
            "Value": [12500, 450000, 8200, 410, 30.48, 1.82, 5.0]
        }
        df_metrics = pd.DataFrame(metrics_raw)
        st.markdown("##### Core Performance Matrix")
        edited_df = st.data_editor(df_metrics, hide_index=True, use_container_width=True)
    
    with col2:
        performance_context = st.text_area("Operational Context & Scaling Goals:", 
            value="Target CPA: $25\nBudget Limit: $20,000\nPlatform: Google Ads Search\nCreative: High-text static images targeting mid-level managers.", height=155)

    generate_btn = st.button("🧠 Execute Neural Intelligence Audit", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    # Combine data
    metrics_str = edited_df.to_string(index=False)
    combined_prompt = f"Performance Metrics:\n{metrics_str}\n\nStrategic Context:\n{performance_context}"
    
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key and not os.environ.get(api_key_required):
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    else:
        with st.spinner(f"🌐 Interfacing with {actual_model_id} Neural Engine... deconstructing attribution signals..."):
            try:
                results = analyze_campaign_v3(combined_prompt, model_name=actual_model_id, api_key=final_api_key)
                save_outputs_v3(results)
                
                st.success("✅ Neural Growth Matrix v3.0 Finalized!")
                
                # --- Row 1: Dashboard Hub ---
                st.markdown("### 🚦 Strategic Growth Dashboard")
                dash_col1, dash_col2, dash_col3, dash_col4 = st.columns(4)
                
                with dash_col1:
                    score = results.get('efficiency_score', 0)
                    st.metric("Efficiency Score", f"{score}%", help="Neural confidence in budget utility.")
                with dash_col2:
                    v = results.get('forecasting_projection', {})
                    st.metric("Proj. EOM Spend", v.get('projected_eom_spend'), delta_color="inverse")
                with dash_col3:
                    st.metric("Proj. Conversions", v.get('projected_eom_conversions'), delta="Forward Look")
                with dash_col4:
                    st.metric("Pacing Status", v.get('pacing_status'))

                st.markdown("<br>", unsafe_allow_html=True)
                
                # --- Row 2: Diagnostic Split ---
                l_col, r_col = st.columns([1.5, 1])
                
                with l_col:
                    st.markdown("### ⚡ Strategic Next-Action Engine")
                    for action in results.get('strategic_next_actions', []):
                        u_class = action.get('urgency', 'medium').lower()
                        st.markdown(f"""
                        <div class="action-card">
                            <span class="urgency-badge {u_class}">{action.get('urgency')}</span>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC;">{action.get('action')}</div>
                            <div style="font-size: 0.9rem; color: #CBD5E1; margin-top: 0.5rem;">Expected ROI Impact: <strong>{action.get('expected_impact')}</strong></div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="glass-panel" style="padding: 1.5rem; border-left: 5px solid #d946ef;">
                        <h4 style="color: #d946ef;">📉 Diminishing Returns Audit</h4>
                        <p style="font-size: 1rem; color: #E2E8F0;">{results.get('diminishing_returns_audit', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with r_col:
                    st.markdown("### 🛠️ Creative Performance Pivot")
                    for cp in results.get('creative_pivot_roadmap', []):
                        st.markdown(f"""
                        <div class="pivot-card">
                            <div class="dimension-label">{cp.get('dimension')}</div>
                            <div style="margin-bottom: 0.5rem; font-size: 0.85rem; color: #94A3B8;">Current: <s>{cp.get('current_state')}</s></div>
                            <div style="font-weight: 700; color: #38BDF8; font-size: 1rem;">Pivot: {cp.get('pivot_suggestion')}</div>
                            <div style="font-size: 0.8rem; font-style: italic; margin-top: 0.5rem; color: #CBD5E1;">Rationale: {cp.get('rationale')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("### 🏛️ Market Benchmark Synthesis")
                    st.info(results.get('industry_benchmark_context', 'N/A'))
                    
                    st.markdown("### 💸 Leaky Buckets")
                    for l in results.get('leaky_bucket_audit', []):
                        st.error(f"Leakage: {l}")

                # --- Row 3: Visual Projections ---
                st.markdown("---")
                st.markdown("### 📊 Performance Correlation Visualizer")
                # Dummy Plotly for v3 visuals
                df_viz = edited_df.copy()
                fig = px.bar(df_viz, x='Dimension', y='Value', color='Value', 
                            color_continuous_scale=[[0, '#0ea5e9'], [0.5, '#6366f1'], [1, '#d946ef']],
                            template='plotly_dark')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

                # --- Exports ---
                st.markdown("### 📥 Neural Strategy Export")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON Intelligence", data=json_data, file_name=f"adintel_neural_v3_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("campaign_analysis.txt", "r", encoding="utf-8") as f: txt_data = f.read()
                    st.download_button("Export as Strategic TXT", data=txt_data, file_name=f"adintel_neural_v3_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Neural Audit Architectural Failure ({actual_model_id}): {str(e)}")
