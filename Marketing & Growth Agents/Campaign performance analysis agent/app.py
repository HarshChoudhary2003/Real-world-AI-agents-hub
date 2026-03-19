import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from agent import analyze_campaign, save_outputs

# Configure the Streamlit page
st.set_page_config(
    page_title="AdIntel AI | Growth Intelligence Studio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & High-Contrast Growth Gradient */
    .stApp {
        background: linear-gradient(135deg, #020617, #1e1b4b, #4c1d95); /* Deep Navy to Purple */
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        background: -webkit-linear-gradient(45deg, #F472B6, #FB7185, #38BDF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -2px;
    }
    
    .glass-panel {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    
    /* Strategic Insight Cards */
    .insight-card {
        background: rgba(15, 23, 42, 0.75);
        border-top: 4px solid #38BDF8;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .insight-card:hover { transform: translateY(-3px); background: rgba(15, 23, 42, 0.9); border-top-color: #F472B6; }
    .risk-card { border-top-color: #F87171; }
    .opp-card { border-top-color: #34D399; }
    
    .card-title {
        font-weight: 800;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
        color: #94A3B8;
    }

</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier analytical diagnostic depth." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Highly contextual strategic inference." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Massive context & benchmark mapping." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "Real-time performance auditing." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal creative support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bullish.png", width=64)
    st.markdown("## Intelligence Settings")
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
    st.markdown("### Diagnosis Capabilities")
    st.markdown("""
    - **Causal Metric Auditing**
    - **Leaky Bucket Detection**
    - **Efficiency Score Mapping**
    - **Benchmark Sensitivity**
    """)
    st.markdown("---")
    st.caption("AdIntel AI v1.0 • Growth Strategy Hub")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>📈 AdIntel AI</h1><p>Strategic Campaign Performance Audit & Efficiency Extraction</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📊 Define Campaign Dataset")
    
    default_input = (
        "Campaign Objective: Lead generation\n"
        "Platform: Google Ads\n"
        "Metrics:\n"
        "- Impressions: 120,000\n"
        "- Clicks: 3,600\n"
        "- CTR: 3.0%\n"
        "- Conversions: 180\n"
        "- Cost per Conversion: $42\n\n"
        "Comparison:\n"
        "Previous period conversion rate: 2.4%"
    )
    
    campaign_data = st.text_area("Input performance metrics, benchmarks, and context:", value=default_input, height=200)
    generate_btn = st.button("🔎 Run Diagnostic Analysis", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key and not os.environ.get(api_key_required):
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    elif not campaign_data.strip():
        st.warning("⚠️ Please provide campaign data.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id}... auditing budget utility..."):
            try:
                results = analyze_campaign(campaign_data, model_name=actual_model_id, api_key=final_api_key)
                save_outputs(results)
                
                st.success("✅ Growth Intelligence Audit Finalized!")
                
                # --- Top Section: Summary & Score ---
                col1, col2 = st.columns([1.5, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="glass-panel">
                        <h2 style="color: #38BDF8; font-size: 1.5rem; margin-bottom: 0.5rem;">📈 Executive Diagnostic Summary</h2>
                        <p style="font-size: 1.15rem; font-weight: 500;">{results.get('executive_summary', 'N/A')}</p>
                        <div style="border-top: 1px solid rgba(255,255,255,0.1); margin-top: 1.5rem; padding-top: 1rem;">
                            <strong style="color: #F472B6;">Budget Audit:</strong><br>
                            {results.get('budget_utilization_audit', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    score = results.get('efficiency_score', 0)
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = score,
                        title = {'text': "Efficiency Score", 'font': {'size': 24, 'color': '#f8fafc'}},
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        gauge = {
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                            'bar': {'color': "#38BDF8"},
                            'bgcolor': "rgba(0,0,0,0)",
                            'borderwidth': 2,
                            'bordercolor': "rgba(255,255,255,0.2)",
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                                {'range': [50, 80], 'color': 'rgba(234, 179, 8, 0.2)'},
                                {'range': [80, 100], 'color': 'rgba(34, 197, 94, 0.2)'}],
                        }
                    ))
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Inter"})
                    st.plotly_chart(fig, use_container_width=True)

                # --- Bottom Section: 3-Col Split ---
                st.markdown("### 📡 Detailed Strategic Mapping")
                i_col, r_col, o_col = st.columns(3)
                
                with i_col:
                    st.markdown('<div class="insight-card"><div class="card-title">💡 Performance Insights</div>', unsafe_allow_html=True)
                    for item in results.get('key_performance_insights', []): st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with r_col:
                    st.markdown('<div class="insight-card risk-card"><div class="card-title" style="color: #F87171;">⚠️ Leaky Buckets & Risks</div>', unsafe_allow_html=True)
                    for item in results.get('risks_and_leaky_buckets', []): st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with o_col:
                    st.markdown('<div class="insight-card opp-card"><div class="card-title" style="color: #34D399;">💎 Strategic Opportunities</div>', unsafe_allow_html=True)
                    for item in results.get('strategic_opportunities', []): st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # Comparison
                st.markdown(f"""
                <div class="glass-panel" style="border-left: 4px solid #38BDF8;">
                    <h4>📊 Benchmark Synthesis</h4>
                    <p style="font-style: italic;">{results.get('benchmark_comparison', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)

                # Export Controls
                st.markdown("---")
                st.markdown("### 📥 Distribution & Audit Persistence")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"adintel_audit_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("campaign_analysis.txt", "r", encoding="utf-8") as f: txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"adintel_audit_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Intelligence Audit Failure ({actual_model_id}): {str(e)}")
