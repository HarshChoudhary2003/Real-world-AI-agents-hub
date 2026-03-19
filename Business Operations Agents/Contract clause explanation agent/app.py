import streamlit as st
import os
import json
from datetime import date
from agent import explain_clause, save_outputs

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
        font-size: 3rem;
        background: -webkit-linear-gradient(45deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
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
    
    # API Key Handling
    api_key_required = model_config["env_var"]
    api_key = st.text_input(f"{api_key_required}", type="password", placeholder=f"Enter {api_key_required}...")
    
    if api_key:
        os.environ[api_key_required] = api_key
        
    st.markdown("---")
    st.markdown("### Agent Capabilities 🧠")
    st.markdown("""
    - **Plain Language Translation**
    - **Legal Meaning Preservation**
    - **Obligation Mapping**
    - **Risk & Watch-out Detection**
    """)
    st.markdown("---")
    st.caption("ClauseClear AI v2.0 • Omni-Model Enterprise Engine")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>📑 ClauseClear AI</h1><p>Translating dense legal clauses into actionable, plain-language insights.</p></div>', unsafe_allow_html=True)

# Main Input Section
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📝 Enter Contract Clause")
    
    default_clause = (
        "Either party may terminate this agreement with thirty (30) days’ written notice.\n"
        "Termination does not relieve either party of obligations accrued prior to termination."
    )
    
    clause_text = st.text_area("Legal clause text to analyze:", value=default_clause, height=150)
    
    analyze_btn = st.button("🔎 Analyze Clause", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if analyze_btn:
    if not os.environ.get(api_key_required):
        st.error(f"🚨 Please enter a valid {api_key_required} in the sidebar to proceed with {selected_model_label}.")
    elif not clause_text.strip():
        st.warning("⚠️ Please enter a clause to analyze.")
    else:
        with st.spinner(f"🤖 Interfacing with {selected_model_label} API... extracting semantics..."):
            try:
                # Call agent logic
                results = explain_clause(clause_text, model_name=model_config["id"])
                
                # Save locally as per agent design
                save_outputs(results)
                
                st.success("✅ Semantic Extraction & Risk Analysis Complete!")
                
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
                    st.download_button("Export as JSON", data=json_data, file_name="clause_explanation.json", mime="application/json")
                with dl_col2:
                    with open("clause_explanation.txt", "r", encoding="utf-8") as txt_f:
                        txt_data = txt_f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name="clause_explanation.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ An error occurred during semantic extraction ({model_config['id']}): {str(e)}")
