import streamlit as st
import json
import os
import litellm
import pandas as pd
from datetime import date
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Training Content AI | SkillForge",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (SaaS Elite Edition)
# -----------------------------------------------------------------------------
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    .stApp { background-color: #0f0a1c; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #080512 !important; border-right: 1px solid #1a1233; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #a78bfa, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #c4b5fd; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(46, 30, 89, 0.4);
        border: 1px solid rgba(167, 139, 250, 0.15);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(167, 139, 250, 0.4); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%); }

    .module-box {
        background: rgba(124, 58, 237, 0.15);
        border-left: 4px solid #8b5cf6;
        padding: 16px; margin-bottom: 16px;
        border-radius: 4px 8px 8px 4px; color: #ede9fe;
    }
    .module-title { font-weight: 700; color: #a78bfa; margin-bottom: 8px; font-size: 1.1rem; }
    .module-list { margin-left: 20px; font-size: 0.95rem; line-height: 1.6; }
    
    .stTextArea textarea { background: #080512 !important; border: 1px solid #1a1233 !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an Enterprise Training Content Generator Agent.

Rules:
- Generate modular training content tailored to the audience.
- Identify strict learning objectives.
- Do NOT include assessments unless asked via the brief.

Return ONLY valid JSON with this exact schema:
{
  "learning_objectives": ["Objective 1", "Objective 2"],
  "modules": [
    {
      "title": "Module Title",
      "key_points": ["Instructional Point 1", "Instructional Point 2"]
    }
  ]
}
"""

def extract_json(content_raw: str) -> dict:
    content = str(content_raw)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        start_idx = int(content.find("{"))
        end_idx = int(content.rfind("}")) + 1
        content_str = str(content)
        content = content_str[start_idx:end_idx]
    return json.loads(content)

def generate_training(text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Training Brief:\n{text}"}
        ],
        "temperature": 0.3
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

def build_txt_export(data: dict) -> str:
    export = f"Corporate Enablement Tracker ({date.today()})\\n{'='*65}\\n\\n"
    
    export += "--- CORE LEARNING OBJECTIVES ---\\n"
    for o in data.get("learning_objectives", []):
        export += f"- {o}\\n"
        
    export += "\\n--- TRAINING MODULES ARCHITECTURE ---\\n"
    for m in data.get("modules", []):
        export += f"\\n[MODULE]: {m.get('title', 'Unknown')}\\n"
        for p in m.get("key_points", []):
            export += f"  * {p}\\n"
            
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'training_result' not in st.session_state:
        st.session_state['training_result'] = None
        
    if 'brief_input' not in st.session_state:
        st.session_state['brief_input'] = (
            "Topic: Data Security Awareness\n"
            "Audience: New startup employees (remote context)\n"
            "Objective: Understand basic password hygiene, phishing, and remote data responsibilities"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Skill<span style='color:#a78bfa;'>Forge</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#c4b5fd;font-size:0.8rem;'>Automated Enablement Architect</p>", unsafe_allow_html=True)

        st.markdown("### 🧬 AI Orchestration")
        
        provider_categories = {
            "🌐 OpenAI": {
                "GPT-4o": "gpt-4o",
                "GPT-4o Mini": "gpt-4o-mini"
            },
            "🎭 Anthropic": {
                "Claude 3.5 Sonnet": "claude-3-5-sonnet-20240620",
                "Claude 3 Haiku": "claude-3-haiku-20240307"
            },
            "🔶 Google (Gemini)": {
                "Gemini 1.5 Pro": "gemini/gemini-1.5-pro",
                "Gemini 1.5 Flash": "gemini/gemini-1.5-flash"
            },
            "🐋 DeepSeek": {
                "DeepSeek Chat": "deepseek/deepseek-chat"
            },
            "🚀 xAI": {
                "Grok-Beta": "xai/grok-beta"
            },
            "🏠 Local (Ollama)": {
                "Llama 3": "ollama/llama3",
                "Mistral": "ollama/mistral"
            },
            "🔓 Groq": {
                "Llama 3 70B": "groq/llama3-70b-8192",
                "Mixtral 8x7B": "groq/mixtral-8x7b-32768"
            }
        }
        
        selected_provider = st.selectbox("AI Provider", list(provider_categories.keys()))
        
        model_options = provider_categories[selected_provider]
        selected_model_label = st.selectbox("Intelligence Engine", list(model_options.keys()))
        target_model = model_options[selected_model_label]

        st.markdown("---")
        st.markdown("### 🔑 Authentication")
        
        provider_name = selected_provider.split(" ", 1)[-1].strip()
        if "(Gemini)" in provider_name:
            provider_name = "Google Gemini"
        elif "(Ollama)" in provider_name:
            provider_name = "Ollama"
            
        if "Local" in selected_provider:
            st.info("Local Ollama endpoint selected. No API key required.")
            user_api_key = None
        else:
            user_api_key = st.text_input(f"{provider_name} API Key", type="password", help=f"Required if not pre-configured.")

        st.markdown("---")
        st.success("🎓 **Tip:** Provide high-fidelity objectives. The system scales the technical lexicon based strictly on the 'Audience' variable.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Enterprise Enablement Matrix</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Translate raw corporate objectives into deeply structured, actionable training hierarchies.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Curriculum Brief")
    brief_input = st.text_area("HR / Product Request", height=150, value=st.session_state['brief_input'], label_visibility="collapsed")
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🚀 Architect Curriculum"):
            if brief_input.strip():
                with st.spinner(f"Compiling Learning Hierarchy via {selected_model_label}..."):
                    try:
                        res = generate_training(brief_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['training_result'] = res
                        st.session_state['brief_input'] = brief_input
                    except Exception as e:
                        st.session_state['training_result'] = {"error": str(e)}
            else:
                st.warning("Please provide a training description brief.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['training_result']:
        res = st.session_state['training_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            st.markdown("<hr style='border:1px solid #1a1233;'>", unsafe_allow_html=True)
            col_l, col_r = st.columns([1.5, 0.5], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                st.markdown("### 🎯 Core Learning Objectives")
                for o in res.get("learning_objectives", []):
                    st.markdown(f"✅ **{o}**")
                    
                st.markdown("---")
                st.markdown("### 📚 Deployed Modules")
                for i, m in enumerate(res.get("modules", []), 1):
                    pts_html = "".join([f"<li>{p}</li>" for p in m.get("key_points", [])])
                    
                    st.markdown(f"""
                    <div class='module-box'>
                        <div class='module-title'>Module {i}: {m.get('title', 'Unknown')}</div>
                        <ul class='module-list'>{pts_html}</ul>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Payload Export")
                
                st.download_button(
                    label="📥 Download Matrix JSON",
                    data=json.dumps(res, indent=2),
                    file_name="training_content.json",
                    mime="application/json",
                    use_container_width=True
                )
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download TXT Summary",
                    data=txt_export,
                    file_name="training_content.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>SkillForge AI © 2026 | Objective Enablement Compilation | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
