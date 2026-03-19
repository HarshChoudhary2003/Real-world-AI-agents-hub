import streamlit as st
import os
import json
from datetime import date
from agent import generate_sop, save_outputs

# Configure the Streamlit page
st.set_page_config(
    page_title="SOPFlow AI | Internal Operations Architect",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Glassmorphism */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #064e3b); /* Emerald Operational Dark Gradient */
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
        background: -webkit-linear-gradient(45deg, #10B981, #34D399);
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
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Procedure Step Timeline */
    .step-box {
        background: rgba(15, 23, 42, 0.7);
        border-left: 4px solid #10B981;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: transform 0.2s ease;
    }
    
    .step-box:hover {
        transform: translateX(5px);
        background: rgba(16, 185, 129, 0.1);
    }
    
    .step-number {
        background: #10B981;
        color: white;
        min-width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .sop-title-chip {
        display: inline-block;
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        padding: 0.25rem 1rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier instructional precision." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Contextually deep standardizations." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Robust architectural mapping." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "Lightning-fast procedural generation." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/rules.png", width=64)
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
    - **Step-by-Step Standardization**
    - **Role & Responsibility Mapping**
    - **Operational Compliance Engine**
    - **Multi-Output Format Support**
    """)
    st.markdown("---")
    st.caption("SOPFlow AI v1.0 • Operations Reliability Engine")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>📋 SOPFlow AI</h1><p>Architecting robust Standard Operating Procedures for enterprise teams.</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📝 Define Process Parameters")
    
    default_input = (
        "Process Name: New Employee IT Onboarding\n"
        "Team: IT Operations\n"
        "Purpose:\nEnsure new hires receive system access on day one.\n\n"
        "Steps:\n"
        "- Receive onboarding request from HR\n"
        "- Create company email account\n"
        "- Provision laptop and software\n"
        "- Grant access to internal tools\n"
        "Constraints:\nAccess must be approved by manager"
    )
    
    process_data = st.text_area("Initial process description and constraints:", value=default_input, height=200)
    generate_btn = st.button("🏗️ Build Standard Operating Procedure", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key:
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    elif not process_data.strip():
        st.warning("⚠️ Please provide a process description.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id}... standardizing operations..."):
            try:
                # Call agent
                results = generate_sop(process_data, model_name=actual_model_id, api_key=final_api_key)
                save_outputs(results)
                
                st.success("✅ Standard Operating Procedure Finalized!")
                
                # SOP Header
                st.markdown(f'<div class="sop-title-chip">SOP-2024-{date.today().strftime("%m%d")}</div>', unsafe_allow_html=True)
                st.markdown(f"## {results.get('title', 'N/A')}")
                
                col1, col2 = st.columns([1.2, 0.8])
                
                with col1:
                    st.markdown(f"""
                    <div class="glass-panel">
                        <h4 style="color: #10B981;">🎯 Purpose & Scope</h4>
                        <p><strong>Purpose:</strong> {results.get('purpose', 'N/A')}</p>
                        <p><strong>Scope:</strong> {results.get('scope', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 🛠️ Step-by-Step Procedure")
                    for idx, step in enumerate(results.get('procedure_steps', []), start=1):
                        st.markdown(f"""
                        <div class="step-box">
                            <div class="step-number">{idx}</div>
                            <div>{step}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="glass-panel">
                        <h4 style="color: #10B981;">👥 Roles & Responsibilities</h4>
                        {"".join([f'<p>• {r}</p>' for r in results.get("roles_and_responsibilities", [])])}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="glass-panel" style="border-top: 4px solid #F59E0B;">
                        <h4 style="color: #FBBF24;">📝 Structural Review Notes</h4>
                        <p>{results.get('review_notes', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Download Buttons
                st.markdown("---")
                st.markdown("### 📥 Document Distribution")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"sop_export_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("sop.txt", "r", encoding="utf-8") as f:
                        txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"sop_export_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ SOP Architectural Failure ({actual_model_id}): {str(e)}")
