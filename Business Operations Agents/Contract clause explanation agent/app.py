import streamlit as st
import os
import json
import time
from datetime import date
from agent import explain_clause, save_outputs, extract_text_from_pdf

# Configure the Streamlit page
st.set_page_config(
    page_title="ClauseClear AI | Contract Clause Explainer",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Glassmorphism */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
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
        background: -webkit-linear-gradient(45deg, #38BDF8, #818CF8);
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
    
    /* Result Cards */
    .result-card {
        background: rgba(15, 23, 42, 0.7);
        border-left: 4px solid #38BDF8;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15);
    }
    
    .result-title {
        color: #38BDF8;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .warning-card {
        border-left-color: #F43F5E;
    }
    .warning-card .result-title {
        color: #F43F5E;
    }
    
    .list-item {
        margin-bottom: 0.5rem;
        display: flex;
        align-items: flex-start;
    }
    
    .list-icon {
        color: #818CF8;
        margin-right: 0.75rem;
        font-size: 1.1rem;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": {
        "id": "gpt-4o",
        "env_var": "OPENAI_API_KEY",
        "doc": "Highest reasoning capabilities for complex clauses."
    },
    "Anthropic (Claude 3.5 Sonnet)": {
        "id": "claude-3-5-sonnet-20240620",
        "env_var": "ANTHROPIC_API_KEY",
        "doc": "Excellent contextual window for dense legal docs."
    },
    "Google (Gemini 1.5 Pro)": {
        "id": "gemini/gemini-1.5-pro",
        "env_var": "GEMINI_API_KEY",
        "doc": "Native ecosystem integration with extensive token context."
    },
    "Groq (Llama 3 70B)": {
        "id": "groq/llama3-70b-8192",
        "env_var": "GROQ_API_KEY",
        "doc": "Lightning-fast inference speed for immediate feedback."
    },
    "Custom (Omni-Model Support)": {
        "id": "custom",
        "env_var": "CUSTOM_API_KEY",
        "doc": "Input ANY LiteLLM supported model (e.g. huggingface/..., bedrock/...) and its explicit API key."
    }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/contract.png", width=64)
    st.markdown("## Configuration ⚙️")
    
    # Model Selection
    selected_model_label = st.selectbox("🌐 Select AI Engine", list(MODELS.keys()))
    model_config = MODELS[selected_model_label]
    
    st.caption(f"_{model_config['doc']}_")
    
    is_custom = model_config["id"] == "custom"
    
    if is_custom:
        custom_model_id = st.text_input("Custom Model String", placeholder="e.g. together_ai/mixtral-8x7b-32768")
        actual_model_id = custom_model_id
        api_key_required = "API Key"
    else:
        actual_model_id = model_config["id"]
        api_key_required = model_config["env_var"]
        
    # API Key Handling
    api_key = st.text_input(f"{api_key_required}", type="password", placeholder=f"Enter {api_key_required}...")
    
    # Let session state or os handle the custom key gracefully, but litellm takes kwargs later
    if not is_custom and api_key:
        os.environ[api_key_required] = api_key
        
    st.markdown("---")
    st.markdown("### Agent Capabilities 🧠")
    st.markdown("""
    - **Omni-Model Support**
    - **PDF & Plain Text Analysis**
    - **High-Fidelity Legal Semantic Mapping**
    - **Structural Outcome Forecasting**
    """)
    st.markdown("---")
    st.caption("ClauseClear AI v2.5 • Advanced Legal Intel")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>📑 ClauseClear AI</h1><p>Translating dense legal clauses into actionable, plain-language insights.</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    # Mode Selection
    analysis_mode = st.radio("Choose Analysis Mode", ["Single Clause Input", "Batch Document Upload (PDF/TXT)"], horizontal=True)
    
    clause_text = ""
    
    if analysis_mode == "Single Clause Input":
        default_clause = (
            "Either party may terminate this agreement with thirty (30) days’ written notice.\n"
            "Termination does not relieve either party of obligations accrued prior to termination."
        )
        clause_text = st.text_area("Legal clause text to analyze:", value=default_clause, height=150)
    else:
        uploaded_file = st.file_uploader("Upload Contract (PDF or TXT)", type=["pdf", "txt"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                with st.spinner("Extracting text from PDF..."):
                    clause_text = extract_text_from_pdf(uploaded_file)
            else:
                clause_text = uploaded_file.read().decode("utf-8")
            st.info(f"📄 Successfully loaded {len(clause_text)} characters.")
            if st.checkbox("Show extracted text"):
                st.text_area("Extracted Content", value=clause_text, height=150)

    analyze_btn = st.button("🔎 Analyze Intelligence", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if analyze_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key:
        st.error(f"🚨 Please enter a valid {api_key_required} in the sidebar to proceed with {selected_model_label}.")
    elif is_custom and not actual_model_id.strip():
        st.error("🚨 Please enter a valid Custom Model String (e.g., 'anthropic/claude-3-haiku-20240307').")
    elif not clause_text.strip():
        st.warning("⚠️ Please provide a clause or document to analyze.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id} API... performing semantic extraction..."):
            try:
                # Call agent logic
                results = explain_clause(clause_text, model_name=actual_model_id, api_key=final_api_key)
                
                # Save locally as per agent design
                save_outputs(results)
                
                st.success("✅ Deep Semantic Analysis Complete!")
                
                # Presentation Layer
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">📖 Plain Language Explanation</div>
                        <p>{results.get('plain_language_explanation', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="result-card"><div class="result-title">🤝 Obligations & Rights</div>', unsafe_allow_html=True)
                    for item in results.get('obligations_and_rights', []):
                        st.markdown(f'<div class="list-item"><span class="list-icon">▪</span><span>{item}</span></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="result-card"><div class="result-title">💡 Practical Implications</div>', unsafe_allow_html=True)
                    for item in results.get('practical_implications', []):
                        st.markdown(f'<div class="list-item"><span class="list-icon">▪</span><span>{item}</span></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="result-card warning-card"><div class="result-title">⚠️ Risks / Watch-outs</div>', unsafe_allow_html=True)
                    for item in results.get('risks_or_watchouts', []):
                        st.markdown(f'<div class="list-item"><span class="list-icon">▪</span><span>{item}</span></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Download Buttons
                st.markdown("### 📥 Export Capabilities")
                json_data = json.dumps(results, indent=2)
                
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"clause_analysis_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("clause_explanation.txt", "r", encoding="utf-8") as txt_f:
                        txt_data = txt_f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"clause_analysis_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ An error occurred during semantic extraction ({actual_model_id}): {str(e)}")
