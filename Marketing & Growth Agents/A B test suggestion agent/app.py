import streamlit as st
import os
import json
from datetime import date
from agent import suggest_tests, save_outputs

# Configure the Streamlit page
st.set_page_config(
    page_title="OptiTest AI | Hypothesis Engine Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Amber Core Theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b, #334155); /* Slate and Deep Navy Gradient */
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .main-header h1 {
        font-size: 3.8rem;
        background: -webkit-linear-gradient(45deg, #F59E0B, #D97706, #FB7185);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -2px;
    }
    
    .glass-panel {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
    }
    
    /* Experiment Cards */
    .test-card {
        background: rgba(15, 23, 42, 0.7);
        border-top: 4px solid #F59E0B;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .test-card:hover {
        transform: translateY(-5px);
        background: rgba(15, 23, 42, 0.9);
        box-shadow: 0 8px 30px rgba(245, 158, 11, 0.1);
    }
    
    .test-id {
        color: #F59E0B;
        font-weight: 800;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    /* ICE Score Visuals */
    .ice-bar-container {
        display: flex;
        gap: 10px;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .ice-pill {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        color: #F59E0B;
    }
    
    .metric-tag {
        display: inline-block;
        padding: 2px 8px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 4px;
        font-size: 0.75rem;
        color: #94A3B8;
        margin-right: 5px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier strategic optimization & reasoning." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Expert in conversion psychology & bias." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Context-aware multivariate mapping." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "High-velocity multivariate iteration." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal creative support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/test-partial_passed.png", width=64)
    st.markdown("## Optimization Config")
    selected_model_label = st.selectbox("🌐 Select AI Engine", list(MODELS.keys()))
    model_config = MODELS[selected_model_label]
    st.caption(f"_{model_config['doc']}_")
    
    is_custom = model_config["id"] == "custom"
    actual_model_id = st.text_input("Model Identifier", value=model_config["id"] if not is_custom else "", placeholder="e.g. together_ai/mixtral...")
    api_key_required = model_config["env_var"] if not is_custom else "API Key"
    
    api_key = st.text_input(f"{api_key_required}", type="password", placeholder=f"Enter {api_key_required}...")
    if not is_custom and api_key:
        os.environ[api_key_required] = api_key
        
    st.markdown("---")
    st.markdown("### Neural Strategy Engine")
    st.markdown("""
    - **ICE Scoring Framework**
    - **Hypothesis Architecture**
    - **Variable Control Matrix**
    - **Confidence Simulation**
    """)
    st.markdown("---")
    st.caption("OptiTest AI v1.0 • Growth Optimization Engine")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>🧪 OptiTest AI</h1><p>Strategic A/B Testing Architecture & Growth Psychology Engine</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 🔍 Performance Context & Metrics")
    
    default_input = (
        "Context:\nLanding page conversion rate is lower than expected.\n\n"
        "Metrics:\n- Conversion Rate: 1.8%\n- Industry Benchmark: 2.5%\n\n"
        "Goal:\nIncrease form submissions\n\n"
        "Constraints:\nBrand messaging must remain professional and compliant."
    )
    
    performance_data = st.text_area("Provide campaign context, conversion metrics, and primary goals:", value=default_input, height=180)
    generate_btn = st.button("🛠️ Forge Experiment Suggestions", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key and not os.environ.get(api_key_required):
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    elif not performance_data.strip():
        st.warning("⚠️ Please provide performance data.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id}... architecting experiments..."):
            try:
                results = suggest_tests(performance_data, model_name=actual_model_id, api_key=final_api_key)
                save_outputs(results)
                
                st.success("✅ A/B Testing Roadmap Finalized!")
                
                # --- Strategic Overview Section ---
                st.markdown(f"""
                <div class="glass-panel" style="border-left: 4px solid #F59E0B;">
                    <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">📡 Optimization Strategic Vision</h3>
                    <p style="font-size: 1.1rem; color: #CBD5E1;">{results.get('strategic_overview', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # --- Experiment Roadmap Grid ---
                st.markdown("### 🗺️ Experiment Roadmaps")
                tests = results.get('tests', [])
                for i, test in enumerate(tests):
                    # Create two columns per row
                    if i % 2 == 0: col_a, col_b = st.columns(2)
                    
                    with (col_a if i % 2 == 0 else col_b):
                        st.markdown(f"""
                        <div class="test-card">
                            <div class="test-id">{test.get('test_id')} | {test.get('element_to_change')}</div>
                            <h4 style="color: #F8FAFC; margin-bottom: 0.75rem;">Hypothesis</h4>
                            <p style="font-size: 0.95rem; color: #E2E8F0; line-height: 1.6;">{test.get('hypothesis', 'N/A')}</p>
                            
                            <h4 style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; margin-top: 1rem;">Variation Details</h4>
                            <p style="font-size: 0.9rem; color: #CBD5E1;">{test.get('variation_details', 'N/A')}</p>
                            
                            <div style="margin-top: 0.8rem;">
                                {''.join([f'<span class="metric-tag">{m}</span>' for m in test.get('success_metrics', [])])}
                            </div>
                            
                            <div class="ice-bar-container">
                                <span class="ice-pill">I: {test.get('ice_score', {}).get('impact')}/10</span>
                                <span class="ice-pill">C: {test.get('ice_score', {}).get('confidence')}/10</span>
                                <span class="ice-pill">E: {test.get('ice_score', {}).get('ease')}/10</span>
                                <span class="ice-pill" style="border-color: #F59E0B; background: rgba(245, 158, 11, 0.4); color: white;">TOTAL: {test.get('ice_score', {}).get('total', 0)}</span>
                                <span class="ice-pill" style="border-color: #94A3B8; color: #94A3B8;">⌛ {test.get('estimated_runtime_weeks', 'N/A')}w</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # --- Variable Control Matrix ---
                st.markdown("### 🧬 Optimization Integrity Audit")
                for test in tests:
                    st.info(f"**Variable Control Matrix ({test.get('test_id')}):** {test.get('variable_control', 'N/A')}")

                # --- Exports ---
                st.markdown("---")
                st.markdown("### 📥 Distribution Studio")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"optitest_roadmap_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("ab_test_suggestions.txt", "r", encoding="utf-8") as f: txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"optitest_roadmap_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Strategy Forge Architectural Failure ({actual_model_id}): {str(e)}")
