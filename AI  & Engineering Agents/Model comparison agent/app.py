import streamlit as st
import json
import os
import litellm
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ModelMind AI | Multi-Provider Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (PREMIUM SaaS AESTHETICS)
# -----------------------------------------------------------------------------
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary-color: #0ea5e9;
        --secondary-color: #6366f1;
        --bg-color: #0c0e14;
        --card-bg: #161923;
        --text-color: #f1f5f9;
        --border-color: #2e3244;
    }

    /* Reset & Typography */
    .stApp { background-color: var(--bg-color); color: var(--text-color); font-family: 'Inter', sans-serif; }

    /* Hide Streamlit Header/Footer */
    header, footer { visibility: hidden !important; }

    /* Custom Header */
    .main-header {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
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
    }

    /* KPI Cards */
    .kpi-card { background: #1a1e2e; border: 1px solid #2e3244; border-radius: 12px; padding: 1.5rem; text-align: left; }
    .kpi-label { font-size: 0.8rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; }
    .kpi-value { font-size: 1.5rem; font-weight: 700; color: #ffffff; margin-top: 0.5rem; }

    /* Recommendation Banner */
    .recommendation-banner {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%);
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Badge Tags */
    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; margin-right: 0.5rem; margin-bottom: 0.5rem; }
    .badge-success { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .badge-error { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. MULTI-PROVIDER CONFIGURATION
# -----------------------------------------------------------------------------
MODEL_PROVIDERS = {
    "🌐 OpenAI": {
        "GPT-4o": "gpt-4o",
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
    },
    "🔓 Groq (Open Source)": {
        "Llama 3 70B": "groq/llama3-70b-8192",
        "Mixtral 8x7B": "groq/mixtral-8x7b-32768",
    }
}

# -----------------------------------------------------------------------------
# 4. CORE LOGIC
# -----------------------------------------------------------------------------
def analyze_models_ai(input_text, orchestrator="gpt-4o", api_key=None):
    SYSTEM_PROMPT = """
    You are a world-class AI Infrastructure Architect (ModelMind AI).
    
    Mission: Compare candidate models for a specific task and evaluate trade-offs.
    
    Return ONLY valid JSON with this schema:
    {
      "comparison_summary": "High-level architectural assessment",
      "models": [
        {
          "model_name": "Full name",
          "strengths": ["...", "..."],
          "weaknesses": ["...", "..."],
          "scores": {
            "Accuracy": 0-100,
            "Latency": 0-100,
            "Cost": 0-100,
            "Consistency": 0-100
          },
          "verdict": "One-liner verdict"
        }
      ],
      "recommended_model": "The winner",
      "recommendation_rationale": "Why this model wins"
    }
    """
    
    try:
        kwargs = {
            "model": orchestrator,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": input_text}
            ],
            "temperature": 0.3
        }
        if api_key:
            kwargs["api_key"] = api_key
            
        response = litellm.completion(**kwargs)
        content = response.choices[0].message.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "{" in content:
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
        st.markdown("<h2 style='text-align: center; color: white;'>ModelMind AI</h2>", unsafe_allow_html=True)
        
        st.markdown("### 🧬 Provider Console")
        provider = st.selectbox("Orchestration Provider", list(MODEL_PROVIDERS.keys()))
        selected_label = st.selectbox("Select Orchestrator", list(MODEL_PROVIDERS[provider].keys()))
        target_model = MODEL_PROVIDERS[provider][selected_label]
        
        st.markdown("---")
        st.markdown("### 🔑 API Management")
        user_api_key = st.text_input("Custom API Key", type="password")
        
        st.markdown("---")
        st.info(f"Orchestrating via: **{provider.split(' ')[-1]}**")

    # Main Content
    st.markdown("<h1 class='main-header'>Cross-Provider Model Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Perform industrial-grade trade-off analysis across OpenAI, Claude, Gemini, DeepSeek, Grok, and more.</p>", unsafe_allow_html=True)

    # Input Canvas
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    input_text = st.text_area("Define Task & Candidate Models", height=200, placeholder="E.g., Task: Video analytics, Models: GPT-4o vs Gemini 1.5 Pro")
    
    if st.button("🚀 Analyze Trade-offs"):
        if input_text:
            with st.spinner(f"Orchestrating comparison via {selected_label}..."):
                result = analyze_models_ai(input_text, orchestrator=target_model, api_key=user_api_key)
                st.session_state['comparison'] = result
        else:
            st.warning("Please define a task.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Comparison Results
    if st.session_state.get('comparison'):
        result = st.session_state['comparison']
        if "error" in result:
            st.error(f"📡 Analysis Failed: {result['error']}")
        else:
            st.markdown("---")
            # Recommendation
            st.markdown(f"""
            <div class='recommendation-banner'>
                <h2 style='color: #38bdf8; margin: 0;'>Recommended: {result['recommended_model']}</h2>
                <p style='color: #94a3b8; font-size: 1.1rem;'>{result['recommendation_rationale']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Radar Chart
            categories = ['Accuracy', 'Latency', 'Cost', 'Consistency']
            fig = go.Figure()
            for model in result['models']:
                model_scores = [model['scores'].get(cat, 0) for cat in categories]
                fig.add_trace(go.Scatterpolar(r=model_scores + [model_scores[0]], theta=categories + [categories[0]], fill='toself', name=model['model_name']))

            fig.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, range=[0, 100], color='#94a3b8')), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'))
            
            radar_col, cards_col = st.columns([1, 1.2])
            with radar_col:
                st.plotly_chart(fig, use_container_width=True)
            
            with cards_col:
                for model in result['models']:
                    st.markdown(f"<div class='kpi-card' style='margin-bottom: 1rem;'>", unsafe_allow_html=True)
                    st.markdown(f"**{model['model_name']}**")
                    st.write(f"Verdict: {model['verdict']}")
                    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    if 'comparison' not in st.session_state:
        st.session_state['comparison'] = None
    main()
