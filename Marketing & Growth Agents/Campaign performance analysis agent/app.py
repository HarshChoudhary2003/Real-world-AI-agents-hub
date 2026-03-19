import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from agent import analyze_campaign_advanced, save_outputs_advanced

# Configure the Streamlit page
st.set_page_config(
    page_title="AdIntel AI v2.0 | Strategic Growth Studio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Futuristic Growth Gradient */
    .stApp {
        background: linear-gradient(135deg, #020617, #0f172a, #1e1b4b, #312e81);
        color: #f8fafc;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header h1 {
        font-size: 4rem;
        background: -webkit-linear-gradient(45deg, #F472B6, #FB7185, #38BDF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -2.5px;
    }
    
    .glass-panel {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 16px 48px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Forecasting Cards */
    .forecast-card {
        background: rgba(30, 41, 59, 0.7);
        border-bottom: 4px solid #38BDF8;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
    }
    
    .forecast-label {
        color: #94A3B8;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .forecast-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0.5rem 0;
    }
    
    .pacing-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        text-transform: uppercase;
    }

    /* Anomaly Cards */
    .anomaly-card {
        background: rgba(15, 23, 42, 0.8);
        border-left: 4px solid #FB7185;
        padding: 1.25rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .anomaly-title {
        color: #FB7185;
        font-weight: 800;
        font-size: 0.9rem;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier diagnostic logic and forecasting." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Expert in root-cause & bias detection." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "High-context attribution mapping." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "Real-time spend velocity audits." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal creative support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bullish.png", width=64)
    st.markdown("## Intelligence Core")
    selected_model_label = st.selectbox("🌐 Select AI Engine", list(MODELS.keys()))
    model_config = MODELS[selected_model_label]
    st.caption(f"_{model_config['doc']}_")
    
    is_custom = model_config["id"] == "custom"
    actual_model_id = st.text_input("Active Model", value=model_config["id"] if not is_custom else "", placeholder="e.g. together_ai/mixtral...")
    api_key_required = model_config["env_var"] if not is_custom else "API Key"
    
    api_key = st.text_input(f"{api_key_required}", type="password", placeholder=f"Enter {api_key_required}...")
    if not is_custom and api_key:
        os.environ[api_key_required] = api_key
        
    st.markdown("---")
    st.markdown("### Diagnosis Capabilities v2.0")
    st.markdown("""
    - **Multi-Touch Attribution Audit**
    - **Spend Velocity Forecasting**
    - **Anomaly Root-Cause Detection**
    - **Portfolio Rebalancing Logic**
    """)
    st.markdown("---")
    st.caption("AdIntel AI • Growth Engineering")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>📈 AdIntel AI</h1><p>Strategic Strategic Growth Studio & Multi-Channel Audit Engine</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📊 Performance Dataset Audit")
    
    default_input = (
        "Campaign Objective: Lead generation\n"
        "Platform: Google Ads / Meta Ads / LinkedIn Ads\n"
        "Timeframe: Last 30 Days\n\n"
        "Raw Metrics:\n"
        "- Total Spend: $12,500 (Budget Limit: $20,000)\n"
        "- Impressions: 450,000\n"
        "- Clicks: 8,200\n"
        "- Conversions: 410\n"
        "- Cost per Lead: $30.48\n\n"
        "Context:\n"
        "- Scaling target: $25 CPA\n"
        "- Primary metric of concern: CTR remains high but Landing Page Conversion fell 12% last week."
    )
    
    campaign_metrics = st.text_area("Provide raw metrics, budget constraints, and operational context:", value=default_input, height=220)
    generate_btn = st.button("🔥 Run Strategic Intelligence Diagnostic", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key and not os.environ.get(api_key_required):
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    elif not campaign_metrics.strip():
        st.warning("⚠️ Please provide performance metrics.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id}... forecasting spend velocity..."):
            try:
                results = analyze_campaign_advanced(campaign_metrics, model_name=actual_model_id, api_key=final_api_key)
                save_outputs_advanced(results)
                
                st.success("✅ Growth Intelligence Audit Finalized!")
                
                # --- Top Forecasting Row ---
                st.markdown("### ⏳ Spend Velocity & EOM Forecasting")
                v = results.get('spend_velocity', {})
                f_col1, f_col2, f_col3 = st.columns(3)
                
                with f_col1:
                    st.markdown(f"""
                    <div class="forecast-card">
                        <div class="forecast-label">Projected EOM Spend</div>
                        <div class="forecast-value">{v.get('projected_eom_spend', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with f_col2:
                    st.markdown(f"""
                    <div class="forecast-card" style="border-bottom-color: #34D399;">
                        <div class="forecast-label">Projected EOM Conversions</div>
                        <div class="forecast-value">{v.get('projected_eom_conversions', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with f_col3:
                    p_status = v.get('pacing_status', 'N/A')
                    b_color = "#38BDF8" if "On-track" in p_status else ("#F59E0B" if "Under" in p_status else "#FB7185")
                    st.markdown(f"""
                    <div class="forecast-card" style="border-bottom-color: {b_color};">
                        <div class="forecast-label">Current Pacing Status</div>
                        <div class="forecast-value" style="font-size: 1.5rem; text-transform: uppercase;">{p_status}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                
                # --- Diagnostic Logic Split ---
                l_col, r_col = st.columns([1.5, 1])
                
                with l_col:
                    st.markdown("### ⚠️ Anomaly & Root-Cause Analysis")
                    for a in results.get('anomaly_detection', []):
                        st.markdown(f"""
                        <div class="anomaly-card">
                            <div class="anomaly-title">{a.get('metric')} Diagnostic</div>
                            <div style="font-size: 1.1rem; margin-top: 0.5rem; color: #F8FAFC; font-weight: 500;">{a.get('observation')}</div>
                            <div style="font-size: 0.9rem; font-style: italic; margin-top: 0.5rem; color: #94A3B8;">Root-Cause Hypothesis: {a.get('root_cause_hypothesis')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("### 🧬 Attribution Perspective")
                    for attr in results.get('attribution_insights', []):
                        st.markdown(f"**{attr.get('model')}:** {attr.get('interpretation')}")

                with r_col:
                    score = results.get('efficiency_score', 0)
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = score,
                    title = {'text': "Efficiency Score", 'font': {'size': 24, 'color': '#f8fafc'}},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#F472B6"},
                            'bgcolor': "rgba(0,0,0,0)",
                            'borderwidth': 2,
                            'bordercolor': "rgba(255,255,255,0.2)",
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                                {'range': [80, 100], 'color': 'rgba(34, 197, 94, 0.2)'}],
                        }
                    ))
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Outfit"})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("### 💸 Portfolio Rebalancing")
                    for r in results.get('rebalancing_suggestions', []):
                        st.success(f"**REBALANCE:** {r}")

                # --- Exports & Persistence ---
                st.markdown("---")
                st.markdown("### 📥 Strategic Audit Export")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"adintel_strategic_v2_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("campaign_analysis.txt", "r", encoding="utf-8") as f: txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"adintel_strategic_v2_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Intelligence Audit Architectural Failure ({actual_model_id}): {str(e)}")
