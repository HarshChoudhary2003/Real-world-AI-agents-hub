import streamlit as st
import os
import json
from datetime import date
from agent import generate_ad_copy, save_outputs

# Configure the Streamlit page
st.set_page_config(
    page_title="AdForge AI v2.0 | Advanced Creative Growth Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
<style>
    /* Global Styles & Animated Sunset Growth Gradient */
    .stApp {
        background: linear-gradient(-45deg, #1e1b4b, #4c1d95, #831843, #9d174d);
        background-size: 400% 400%;
        animation: gradientAnimation 15s ease infinite;
        color: #f8fafc;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        text-align: center;
        margin-bottom: 2.5rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header h1 {
        font-size: 4rem;
        background: -webkit-linear-gradient(45deg, #F97316, #FB7185, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -2.5px;
    }
    
    .glass-panel {
        background: rgba(15, 23, 42, 0.55);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 16px 48px 0 rgba(0, 0, 0, 0.45);
    }
    
    /* Persona Reaction Cards */
    .persona-card {
        background: rgba(30, 41, 59, 0.6);
        border-left: 4px solid #FB7185;
        padding: 1.25rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .persona-card:hover {
        transform: scale(1.02);
        background: rgba(30, 41, 59, 0.85);
    }

    /* Ad Variation Strategy Card */
    .ad-card-variant {
        background: rgba(15, 23, 42, 0.75);
        border-top: 4px solid #8B5CF6;
        padding: 1.5rem;
        border-radius: 16px;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .ad-card-variant:hover {
        transform: translateY(-8px);
        border-top-color: #F97316;
        box-shadow: 0 10px 40px rgba(249, 115, 22, 0.15);
    }
    
    .hook-tag {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 800;
        color: #F97316;
        border: 1px solid rgba(249, 115, 22, 0.4);
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
    }
    
    .overlay-bubble {
        background: rgba(255, 255, 255, 0.05);
        border: 1px dashed rgba(255, 255, 255, 0.2);
        padding: 0.75rem 1rem;
        border-radius: 10px;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        color: #E2E8F0;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Define Model Providers ---
MODELS = {
    "OpenAI (GPT-4o)": { "id": "gpt-4o", "env_var": "OPENAI_API_KEY", "doc": "Premier semantic reasoning & creative logic." },
    "Anthropic (Claude 3.5 Sonnet)": { "id": "claude-3-5-sonnet-20240620", "env_var": "ANTHROPIC_API_KEY", "doc": "Highly persuasive buyer-intent analysis." },
    "Google (Gemini 1.5 Pro)": { "id": "gemini/gemini-1.5-pro", "env_var": "GEMINI_API_KEY", "doc": "Massive context-driven campaign mapping." },
    "Groq (Llama 3 70B)": { "id": "groq/llama3-70b-8192", "env_var": "GROQ_API_KEY", "doc": "High-velocity multivariate testing." },
    "Custom (Omni-Model)": { "id": "custom", "env_var": "API_KEY", "doc": "Universal creative support." }
}

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bullhorn.png", width=64)
    st.markdown("## Global Campaign Config")
    selected_model_label = st.selectbox("🌐 Select AI Engine", list(MODELS.keys()))
    model_config = MODELS[selected_model_label]
    st.caption(f"_{model_config['doc']}_")
    
    is_custom = model_config["id"] == "custom"
    actual_model_id = st.text_input("Model Key", value=model_config["id"] if not is_custom else "", placeholder="e.g. together_ai/mixtral...")
    api_key_required = model_config["env_var"] if not is_custom else "API Key"
    
    api_key = st.text_input(f"{api_key_required}", type="password", placeholder=f"Enter {api_key_required}...")
    if not is_custom and api_key:
        os.environ[api_key_required] = api_key
        
    st.markdown("---")
    st.markdown("### Advanced Capabilities v2.0")
    st.markdown("""
    - **Buyer Persona Simulation**
    - **Psy-Engine Hook Selection**
    - **Causal Creative Audit**
    - **Visual Identity Strategy**
    """)
    st.markdown("---")
    st.caption("AdForge AI • Growth Studio")

# --- UI Layout ---
st.markdown('<div class="main-header"><h1>🎨 AdForge AI</h1><p>Strategic Creative Growth Architecture & Persona Simulation</p></div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📣 Strategic Campaign Inputs")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        product_name = st.text_input("Product/Service Name", placeholder="e.g. AI Workflow Automation Platform")
        target_audience = st.text_input("Target Audience Persona", placeholder="e.g. Operations managers at mid-sized companies")
    with col2:
        platform = st.selectbox("Advertising Platform", ["LinkedIn Ads", "Meta Ads (FB/IG)", "X (Twitter) Ads", "Google Search Ads", "YouTube Ads"])
        brand_tone = st.selectbox("Brand Voice Tone", ["Professional & Confident", "Disruptive & Bold", "Warm & Empathetic", "Clever & Witty", "Minimalist & Direct"])

    objective = st.text_input("Core Campaign Objective", placeholder="e.g. Drive demo sign-ups for Q4")
    
    campaign_data_combined = f"Product: {product_name}\nTarget Audience: {target_audience}\nPlatform: {platform}\nObjective: {objective}\nBrand Tone: {brand_tone}"
    
    generate_btn = st.button("🔥 Forge Strategic Creative Variations", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# Action Logic
if generate_btn:
    final_api_key = api_key if api_key else (os.environ.get(api_key_required) if not is_custom else "")
    
    if not final_api_key and not os.environ.get(api_key_required):
        st.error(f"🚨 Please provide a valid {api_key_required} in the sidebar.")
    elif not product_name:
        st.warning("⚠️ Please provide product details.")
    else:
        with st.spinner(f"🤖 Interfacing with {actual_model_id}... simulating persona reactions..."):
            try:
                results = generate_ad_copy(campaign_data_combined, model_name=actual_model_id, api_key=final_api_key)
                save_outputs(results)
                
                st.success("✅ Creative Strategy Finalized!")
                
                # --- Highlights & Headlines Section ---
                st.markdown("### 🏺 High-Engagement Headlines")
                h_cols = st.columns(len(results.get('headlines', [1, 2, 3])))
                for idx, h in enumerate(results.get('headlines', [])):
                    with h_cols[idx % len(h_cols)]:
                        st.markdown(f'<div style="background: rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.4); padding: 1rem; border-radius: 12px; font-weight: 700; text-align: center;">{h}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # --- Main Analysis Split ---
                l_col, r_col = st.columns([1.8, 1.2])
                
                with l_col:
                    st.markdown("### 📽️ Creative Identity Variants")
                    for idx, v in enumerate(results.get('primary_copy_variations', [])):
                        st.markdown(f"""
                        <div class="ad-card-variant">
                            <span class="hook-tag">HOOK: {v.get('viral_hook', 'N/A')}</span>
                            <h4 style="color: #F8FAFC; margin-bottom: 0.75rem;">{v.get('variation_name', 'N/A')}</h4>
                            <div style="line-height: 1.7; color: #CBD5E1; font-size: 1.05rem;">
                                {v.get('text', 'N/A')}
                            </div>
                        </div><br>
                        """, unsafe_allow_html=True)

                with r_col:
                    st.markdown("### 👥 Persona Simulation")
                    for p in results.get('persona_simulations', []):
                        st.markdown(f"""
                        <div class="persona-card">
                            <div style="color: #FB7185; font-weight: 800; font-size: 0.85rem; text-transform: uppercase;">Simulated React: {p.get('persona')}</div>
                            <div style="font-size: 0.95rem; margin-top: 0.5rem; color: #E2E8F0;">{p.get('likely_reaction')}</div>
                            <div style="font-size: 0.85rem; font-style: italic; margin-top: 0.5rem; color: #F97316;">Value Hook: {p.get('perceived_value')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("### 🖼️ Visual Identity Overlays")
                    for overlay in results.get('image_text_overlays', []):
                        st.markdown(f'<div class="overlay-bubble">{overlay}</div>', unsafe_allow_html=True)

                # --- CTAs & Downloads ---
                st.markdown("---")
                cta_html = " ".join([f'<span style="background: #F97316; color: white; padding: 0.4rem 1rem; border-radius: 6px; font-weight: 800; margin-right: 0.5rem; font-size: 0.85rem;">{c}</span>' for c in results.get('calls_to_action', [])])
                st.markdown(f"**⚡ Multi-Stage CTAs:** {cta_html}", unsafe_allow_html=True)
                
                st.markdown("### 📥 Strategy Download")
                json_data = json.dumps(results, indent=2)
                dl_col1, dl_col2, _ = st.columns([1, 1, 2])
                with dl_col1:
                    st.download_button("Export as JSON", data=json_data, file_name=f"adforge_strategy_{date.today()}.json", mime="application/json")
                with dl_col2:
                    with open("ad_copy.txt", "r", encoding="utf-8") as f:
                        txt_data = f.read()
                    st.download_button("Export as TXT", data=txt_data, file_name=f"adforge_strategy_{date.today()}.txt", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Creative Forge Architectural Failure ({actual_model_id}): {str(e)}")
