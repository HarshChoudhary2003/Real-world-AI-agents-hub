import streamlit as st
import os
import json
from datetime import date
from agent import generate_insights, save_outputs

# Configure the Streamlit page
st.set_page_config(
    page_title="InsightCore AI | Strategic KPI Analytics",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Glassmorphism */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e3a8a); /* Data Intelligence Deep Blue Gradient */
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
    
    /* Metrics Highlighting */
    .insight-card {
        background: rgba(15, 23, 42, 0.7);
        border-top: 4px solid #38BDF8;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-5px);
        background: rgba(56, 189, 248, 0.05);
        border-color: #60A5FA;
    }
    
    .risk-card { border-top-color: #F87171; }
    .opp-card { border-top-color: #34D399; }
    .focus-card { border-top-color: #FBBF24; }
    
    .card-title {
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
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
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier analytical depth." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Excellent business logic mapping." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Massive context processing." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "Real-time inference speed." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/line-chart.png", width=64)
    st.markdown("## Configuration ⚙️")
    
    selected_model_label = st.selectbox("🌐 Select AI Engine", list(MODELS.keys()))
    model_config = MODELS[selected_model_label]
    st.caption(f"_{model_config['doc']}_")
    
    is_custom = model_config["id"] == "custom"
    if is_custom:
        custom_model_id = st.text_input("Custom Model String", placeholder="e.g. together_ai/mixtral...")
        actual_model_id = custom_model_id
        api_key_required = "API Key"
    else:
        actual_model_id = model_config["id"]
        api_key_required = model_config["env_var"]
        
    api_key = st.text_input(f"{api_key_required}", type="password", placeholder=f"Enter {api_key_required}...")
    if not is_custom and api_key:
        os.environ[api_key_required] = api_key
        
    st.markdown("---")
    st.markdown("### Agent Capabilities 🧠")
    st.markdown("""
    - **Contextual KPI Decoding**
    - **Trend & Anomaly Detection**
    - **Strategic Risk Forecasting**
    - **Growth Opportunity Mapping**
    """)
    st.markdown("---")
    st.caption("InsightCore AI v1.0 • Strategic KPI Studio")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>💹 InsightCore AI</h1><p>Decoding performance metrics into strategic narrative intelligence.</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📊 Enter Performance Data")
    
    default_input = (
        "KPIs:\n"
        "- Monthly Active Users: 120,000 (↑ 8% MoM)\n"
        "- Churn Rate: 3.2% (↑ 0.5%)\n"
        "- Revenue Growth: 12% QoQ\n"
        "- Customer Support Tickets: 1,450 (↓ 10%)\n\n"
        "Targets:\n"
        "- Churn Rate Target: < 3%\n\n"
        "Business Context:\n"
        "Recent product update and pricing changes"
    )
    
    kpi_data = st.text_area("Input raw KPI metrics and business context:", value=default_input, height=200)
    generate_btn = st.button("🔎 Generate Intelligence Report", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key:
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    elif not kpi_data.strip():
        st.warning("⚠️ Please provide KPI data to analyze.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id}... decoding metrics..."):
            try:
                # Call agent
                results = generate_insights(kpi_data, model_name=actual_model_id, api_key=final_api_key)
                save_outputs(results)
                
                st.success("✅ Strategic Narrative Compilation Complete!")
                
                # Executive Summary
                st.markdown(f"""
                <div class="glass-panel">
                    <h2 style="color: #38BDF8; font-size: 1.5rem; margin-bottom: 1rem;">📈 Strategic Executive Summary</h2>
                    <p style="font-size: 1.1rem; line-height: 1.6;">{results.get('executive_summary', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Grid Layout for Insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="insight-card"><div class="card-title">📡 Key Trends</div>', unsafe_allow_html=True)
                    for item in results.get('key_trends', []):
                        st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="insight-card risk-card"><div class="card-title" style="color: #F87171;">⚠️ Identified Risks</div>', unsafe_allow_html=True)
                    for item in results.get('risks', []):
                        st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="insight-card opp-card"><div class="card-title" style="color: #34D399;">💡 Growth Opportunities</div>', unsafe_allow_html=True)
                    for item in results.get('opportunities', []):
                        st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="insight-card focus-card"><div class="card-title" style="color: #FBBF24;">🎯 Critical Focus Areas</div>', unsafe_allow_html=True)
                    for item in results.get('focus_areas', []):
                        st.markdown(f"• {item}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # Export Controls
                st.markdown("---")
                st.markdown("### 📥 Insight Distribution")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"kpi_insights_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("kpi_insights.txt", "r", encoding="utf-8") as f:
                        txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"kpi_insights_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Insight Synthesis Failure ({actual_model_id}): {str(e)}")
