import streamlit as st
import os
import json
from datetime import date
from agent import compare_vendors, save_outputs

# Configure the Streamlit page
st.set_page_config(
    page_title="VendorFlow AI | Strategic Vendor Comparison",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Glassmorphism */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #2D1B69); /* Deep Purple/Indigo Gradient */
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
        background: -webkit-linear-gradient(45deg, #A78BFA, #818CF8);
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
    .vendor-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(167, 139, 250, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .vendor-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(167, 139, 250, 0.15);
        border-color: rgba(167, 139, 250, 0.5);
    }
    
    .vendor-header {
        color: #A78BFA;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }
    
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .tag {
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .tag-strength { background: rgba(34, 197, 94, 0.15); color: #4ADE80; border: 1px solid rgba(74, 222, 128, 0.3); }
    .tag-weakness { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(248, 113, 113, 0.3); }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Highest analytical capability." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Context-aware business logic." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Deep data synthesis." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "Extreme inference speed." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/commercial.png", width=64)
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
    - **Omni-Model Analysis**
    - **Objective Vendor Scoring**
    - **Strategic Trade-off Mapping**
    - **Premium Data Exports**
    """)
    st.markdown("---")
    st.caption("VendorFlow AI v1.0 • Strategic Asset Analysis")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>⚖️ VendorFlow AI</h1><p>Strategic, cross-dimensional vendor landscape analysis.</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📝 Define Comparison Scope")
    
    default_input = (
        "Vendors:\n- Vendor A\n- Vendor B\n- Vendor C\n\n"
        "Criteria:\n- Cost\n- Feature completeness\n- Support quality\n- Scalability\n- Compliance readiness\n\n"
        "Business Priority:\nOperational reliability and long-term scalability"
    )
    
    comparison_text = st.text_area("Vendor data and criteria:", value=default_input, height=200)
    compare_btn = st.button("🔎 Run Comparison Intelligence", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if compare_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key:
        st.error(f"🚨 Please enter a valid {api_key_required} in the sidebar.")
    elif not comparison_text.strip():
        st.warning("⚠️ Please provide vendor data to analyze.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id}... analyzing vendor parameters..."):
            try:
                # Call agent
                results = compare_vendors(comparison_text, model_name=actual_model_id, api_key=final_api_key)
                save_outputs(results)
                
                st.success("✅ Vendor Intelligence Report Compiled!")
                
                # Summary Section
                st.markdown(f"""
                <div class="glass-panel">
                    <h3>📈 Executive Summary</h3>
                    <p>{results.get('summary', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Vendor Grid
                st.markdown("### 🤝 Vendor Breakdown")
                cols = st.columns(len(results.get('vendors', [1, 2, 3]))) # Dynamic columns based on count
                
                for idx, vendor in enumerate(results.get('vendors', [])):
                    col_to_use = cols[idx % len(cols)]
                    with col_to_use:
                        st.markdown(f"""
                        <div class="vendor-card">
                            <div class="vendor-header">{vendor.get('name', 'N/A')}</div>
                            <div style="margin-bottom: 0.5rem; font-weight: 600; font-size: 0.9rem;">Strengths</div>
                            <div class="tag-container">
                                {' '.join([f'<span class="tag tag-strength">{s}</span>' for s in vendor.get('strengths', [])])}
                            </div>
                            <div style="margin-bottom: 0.5rem; font-weight: 600; font-size: 0.9rem;">Weaknesses</div>
                            <div class="tag-container">
                                {' '.join([f'<span class="tag tag-weakness">{w}</span>' for w in vendor.get('weaknesses', [])])}
                            </div>
                            <div style="font-size: 0.9rem; color: #94A3B8; margin-top: 1rem;">
                                <strong>Notes:</strong> {vendor.get('notes', 'N/A')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Trade-offs
                st.markdown(f"""
                <div class="glass-panel" style="border-left: 4px solid #F43F5E;">
                    <h3>⚡ Strategic Trade-offs</h3>
                    {''.join([f'<p>• {t}</p>' for t in results.get('key_tradeoffs', [])])}
                </div>
                """, unsafe_allow_html=True)

                # Download Buttons
                st.markdown("### 📥 Report Export")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"vendor_analysis_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("vendor_comparison.txt", "r", encoding="utf-8") as f:
                        txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"vendor_analysis_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Analysis Failed ({actual_model_id}): {str(e)}")
