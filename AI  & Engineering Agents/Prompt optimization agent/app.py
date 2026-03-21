import streamlit as st
import json
import os
import litellm
from datetime import date
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PromptForge AI | Multi-Provider Console",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (UNICORN STARTUP AESTHETICS)
# -----------------------------------------------------------------------------
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary-color: #6366f1;
        --secondary-color: #a855f7;
        --bg-color: #0c0e14;
        --card-bg: #161923;
        --text-color: #f1f5f9;
        --border-color: #2e3244;
    }

    /* Reset & Typography */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111420 !important;
        border-right: 1px solid var(--border-color);
        width: 340px !important;
    }

    /* Hide Streamlit Header/Footer */
    header, footer {
        visibility: hidden !important;
    }

    /* Custom Header */
    .main-header {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -1.5px;
    }

    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(22, 25, 35, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8.5px);
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .glass-card:hover { box-shadow: 0 8px 40px rgba(99, 102, 241, 0.15); border-color: rgba(99, 102, 241, 0.3); }

    /* KPI Cards */
    .kpi-card { background: #1a1e2e; border: 1px solid #2e3244; border-radius: 12px; padding: 1.5rem; text-align: left; margin-bottom: 1rem; }
    .kpi-label { font-size: 0.85rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-value { font-size: 1.75rem; font-weight: 700; color: #ffffff; margin-top: 0.5rem; }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600; width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); text-transform: uppercase; letter-spacing: 0.025em;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4);
    }

    /* Badge Tags */
    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; margin-right: 0.5rem; }
    .badge-success { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .badge-info { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. MULTI-PROVIDER CONFIGURATION
# -----------------------------------------------------------------------------
MODEL_PROVIDERS = {
    "🌐 OpenAI": {
        "GPT-4o (Omni)": "gpt-4o",
        "GPT-4o Mini": "gpt-4o-mini",
        "GPT-4 Turbo": "gpt-4-turbo",
    },
    "🎭 Anthropic (Claude)": {
        "Claude 3.5 Sonnet": "claude-3-5-sonnet-20240620",
        "Claude 3 Opus": "claude-3-opus-20240229",
        "Claude 3 Haiku": "claude-3-haiku-20240307",
    },
    "🔶 Google (Gemini)": {
        "Gemini 1.5 Pro": "gemini/gemini-1.5-pro",
        "Gemini 1.5 Flash": "gemini/gemini-1.5-flash",
    },
    "🐋 DeepSeek": {
        "DeepSeek Chat (V3)": "deepseek/deepseek-chat",
        "DeepSeek Coder": "deepseek/deepseek-coder",
    },
    "🚀 xAI (Grok)": {
        "Grok-Beta": "xai/grok-beta",
    },
    "🏠 Local (Ollama)": {
        "Llama 3 (Local)": "ollama/llama3",
        "Mistral (Local)": "ollama/mistral",
        "Gemma (Local)": "ollama/gemma",
    },
    "🔓 Groq (Open Source)": {
        "Llama 3 70B": "groq/llama3-70b-8192",
        "Mixtral 8x7B": "groq/mixtral-8x7b-32768",
    }
}

# -----------------------------------------------------------------------------
# 4. CORE LOGIC
# -----------------------------------------------------------------------------
def optimize_prompt_ai(prompt_text, model_name="gpt-4o-mini", api_key=None):
    SYSTEM_PROMPT = """
    You are a world-class Prompt Engineer and Optimization Agent (PromptForge AI).
    
    Mission: Transform raw, vague prompts into high-performance, structured instructions.
    
    Return ONLY valid JSON with this schema:
    {
      "optimized_prompt": "The full refined prompt text",
      "improvements": ["Improvement 1", "Improvement 2", ...],
      "usage_notes": ["Note 1", "Note 2", ...],
      "score": 0.0 to 1.0 (float)
    }
    """
    
    try:
        kwargs = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.3
        }
        if api_key:
            kwargs["api_key"] = api_key
            
        response = litellm.completion(**kwargs)
        content = response.choices[0].message.content
        
        # Robust JSON extraction
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        if "{" in content:
            content = content[content.find("{"):content.rfind("}")+1]
        
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}

# -----------------------------------------------------------------------------
# 5. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='color: white; margin-bottom: 2.5rem; text-align: center;'>PromptForge <span style='color: #6366f1;'>AI</span></h2>", unsafe_allow_html=True)
        
        st.markdown("### 🧬 AI Provider Engine")
        provider = st.selectbox("Select Cloud Provider", list(MODEL_PROVIDERS.keys()))
        selected_label = st.selectbox("Foundation Model", list(MODEL_PROVIDERS[provider].keys()))
        target_model = MODEL_PROVIDERS[provider][selected_label]
        
        st.markdown("---")
        st.markdown("### 🔑 API Management")
        user_api_key = st.text_input("Custom API Secret", type="password", help="Overrides system keys for the current provider.")
        
        st.markdown("---")
        st.info(f"⚡ Orchestrating via: **{provider.split(' ')[-1]}**")
        st.metric("Neural Sync", "Active", "🟢")

    # Main Content
    st.markdown("<h1 class='main-header'>Multi-Provider Prompt Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Orchestrate industrial-grade AI logic across OpenAI, Gemini, Claude, DeepSeek, and Grok.</p>", unsafe_allow_html=True)

    # Input Area
    input_col, stats_col = st.columns([2, 1])

    with input_col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        raw_prompt = st.text_area("Original Intent", height=320, placeholder="E.g., 'Draft a technical roadmap for an autonomous agent hub'")
        
        if st.button("🚀 Refine with " + provider.split(" ")[-1]):
            if raw_prompt:
                with st.spinner(f"Refining intent using {selected_label}..."):
                    result = optimize_prompt_ai(raw_prompt, model_name=target_model, api_key=user_api_key)
                    st.session_state['result'] = result
            else:
                st.warning("Please enter a prompt to refine.")
        st.markdown("</div>", unsafe_allow_html=True)

    with stats_col:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Intelligence Score</div>", unsafe_allow_html=True)
        score = st.session_state.get('result', {}).get('score', 0.0) if st.session_state.get('result') and "error" not in st.session_state['result'] else 0.0
        st.markdown(f"<div class='kpi-value'>{int(score*100)}%</div>", unsafe_allow_html=True)
        st.progress(score)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>Provider Tier</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value' style='font-size: 1.2rem; transform: translateY(5px);'>{provider.split(' ')[-1]} Enterprise</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Output Section
    if st.session_state.get('result'):
        result = st.session_state['result']
        if "error" in result:
            st.error(f"📡 Orchestration Error: {result['error']}")
        else:
            st.markdown("---")
            res_left, res_right = st.columns([1.2, 0.8])
            
            with res_left:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown(f"#### 💎 Refined Architecture ({provider.split(' ')[-1]})")
                st.code(result['optimized_prompt'], language="markdown")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with res_right:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### ⚡ Strategy Insights")
                for imp in result.get('improvements', []):
                    st.markdown(f"<span class='badge badge-success'>✓</span> {imp}", unsafe_allow_html=True)
                st.markdown("<br>#### 📖 Usage Protocol", unsafe_allow_html=True)
                for note in result.get('usage_notes', []):
                    st.markdown(f"<span class='badge badge-info'>i</span> {note}", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    if 'result' not in st.session_state:
        st.session_state['result'] = None
    main()
