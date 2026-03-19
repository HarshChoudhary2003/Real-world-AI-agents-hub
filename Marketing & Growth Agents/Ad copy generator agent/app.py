import streamlit as st
import os
import json
from datetime import date
from agent import generate_ad_copy, save_outputs

# Configure the Streamlit page
st.set_page_config(
    page_title="AdForge AI | Creative Growth Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Glassmorphism */
    .stApp {
        background: linear-gradient(135deg, #1e1b4b, #4c1d95, #831843); /* Indigo to Deep Rose Gradient */
        color: #f8fafc;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        background: -webkit-linear-gradient(45deg, #F97316, #EC4899, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    .glass-panel {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }
    
    /* Ad Variation Cards */
    .ad-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(236, 72, 153, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .ad-card:hover {
        transform: translateY(-5px);
        background: rgba(30, 41, 59, 0.9);
        border-color: #EC4899;
        box-shadow: 0 8px 30px rgba(236, 72, 153, 0.15);
    }
    
    .card-label {
        color: #F97316;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .headline-bubble {
        background: rgba(139, 92, 246, 0.15);
        color: #C084FC;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .cta-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: #EC4899;
        color: white;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-top: 0.5rem;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier creative copywriting." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Highly persuasive narrative logic." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Context-aware ad generation." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "Lightning-fast iteration speed." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bullhorn.png", width=64)
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
    st.markdown("### Studio Capabilities 🧠")
    st.markdown("""
    - **Psychology-Driven variations**
    - **Multi-Platform Adaptation**
    - **A/B Testing Ready Output**
    - **CTA Optimization Engine**
    """)
    st.markdown("---")
    st.caption("AdForge AI v1.0 • Growth Engineering Studio")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>🎨 AdForge AI</h1><p>Strategic ad creative studio for high-conversion growth campaigns.</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📣 Campaign Context")
    
    default_input = (
        "Product: AI Workflow Automation Platform\n"
        "Target Audience: Operations managers at mid-sized companies\n"
        "Platform: LinkedIn Ads\n"
        "Objective: Drive demo sign-ups\n"
        "Brand Tone: Professional, clear, and confident"
    )
    
    campaign_data = st.text_area("Define your campaign parameters:", value=default_input, height=180)
    generate_btn = st.button("✨ Forge Ad Copy Variations", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key and not os.environ.get(api_key_required):
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    elif not campaign_data.strip():
        st.warning("⚠️ Please provide campaign context.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id}... crafting variations..."):
            try:
                # Call agent
                results = generate_ad_copy(campaign_data, model_name=actual_model_id, api_key=final_api_key)
                save_outputs(results)
                
                st.success("✅ Creative Variations Forged Successfully!")
                
                # Headlines Section
                st.markdown("### 🏮 Strategic Headlines")
                h_col1, h_col2, h_col3 = st.columns(3)
                headlines = results.get('headlines', [])
                for i, h in enumerate(headlines):
                    col = [h_col1, h_col2, h_col3][i % 3]
                    with col:
                        st.markdown(f'<div class="headline-bubble">{h}</div>', unsafe_allow_html=True)
                
                # Variation Cards
                st.markdown("### 🎞️ Ad Body Variations")
                v_cols = st.columns(len(results.get('primary_copy_variations', [1, 2])))
                for idx, variant in enumerate(results.get('primary_copy_variations', [])):
                    with v_cols[idx % len(v_cols)]:
                        st.markdown(f"""
                        <div class="ad-card">
                            <div class="card-label">{variant.get('variation_name', f'Variation {idx+1}')}</div>
                            <div style="font-size: 1.05rem; line-height: 1.6; color: #E2E8F0;">
                                {variant.get('text', 'N/A')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # CTAs
                st.markdown("### ⚡ Optimized CTAs")
                cta_html = "".join([f'<span class="cta-tag">{cta}</span>' for cta in results.get('calls_to_action', [])])
                st.markdown(f'<div style="margin-bottom: 2rem;">{cta_html}</div>', unsafe_allow_html=True)

                # Download Buttons
                st.markdown("---")
                st.markdown("### 📥 Distribution Studio")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"adforge_copy_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("ad_copy.txt", "r", encoding="utf-8") as f:
                        txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"adforge_copy_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Creative Forge Failure ({actual_model_id}): {str(e)}")
