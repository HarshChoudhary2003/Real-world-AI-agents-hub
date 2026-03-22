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
    page_title="Interview Question Generator | QuestForge",
    page_icon="🎙️",
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

    .stApp { background-color: #1e1b4b; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #111827 !important; border-right: 1px solid #374151; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #fde68a; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(17, 24, 39, 0.6);
        border: 1px solid rgba(251, 191, 36, 0.15);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(251, 191, 36, 0.5); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); }

    .q-box {
        background: rgba(31, 41, 55, 0.5);
        border-left: 4px solid #f59e0b;
        padding: 12px 16px;
        margin-bottom: 12px;
        border-radius: 4px 8px 8px 4px;
        color: #f3f4f6;
    }
    
    .stTextArea textarea { background: #111827 !important; border: 1px solid #374151 !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an Interview Question Generator Agent.

Rules:
- Generate fair, role-relevant questions tailored to the seniority and skills listed.
- Avoid illegal or biased topics explicitly.
- Include behavioral and technical questions.
- Do NOT provide answers to the questions.

Return ONLY valid JSON with this schema:
{
  "behavioral_questions": ["question 1", "question 2"],
  "technical_questions": ["question 1", "question 2"],
  "scenario_questions": ["question 1", "question 2"]
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

def generate_questions(role_text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": role_text}
        ],
        "temperature": 0.3
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

def build_txt_export(data: dict) -> str:
    export = f"Interview Questions ({date.today()})\\n{'='*55}\\n\\n"
    
    export += "Behavioral Questions:\\n"
    for q in data.get("behavioral_questions", []):
        export += f"- {q}\\n"
        
    export += "\\nTechnical Questions:\\n"
    for q in data.get("technical_questions", []):
        export += f"- {q}\\n"
        
    export += "\\nScenario-Based Questions:\\n"
    for q in data.get("scenario_questions", []):
        export += f"- {q}\\n"
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'quest_result' not in st.session_state:
        st.session_state['quest_result'] = None
        
    if 'role_input' not in st.session_state:
        st.session_state['role_input'] = (
            "Role: Backend Software Engineer\n"
            "Seniority: Mid-level\n"
            "Key Skills:\n"
            "- Python\n"
            "- APIs\n"
            "- Databases\n"
            "- System design"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Quest<span style='color:#f59e0b;'>Forge</span></h2>", unsafe_allow_html=True)

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
            st.info("Local Ollama endpoint selected. No API key required (make sure your service is running).")
            user_api_key = None
        else:
            user_api_key = st.text_input(f"{provider_name} API Key", type="password", help=f"Required if not pre-configured. Enter your {provider_name} API Key here.")

        st.markdown("---")
        st.info("💡 **Tip:** Generated questions automatically avoid illegal HR topics and focus solely on operational competency.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Automated Interview Matrix</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Synthesize deeply technical and fair behavioral questions tailored precisely to the requisition profile.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 💼 Requisition Context")
    role_input = st.text_area(
        "", 
        height=180, 
        value=st.session_state['role_input'],
        help="Detail the role, seniority, and required technical stack."
    )
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🎙️ Compile Interview Script"):
            if role_input.strip():
                with st.spinner(f"Orchestrating Questions via {selected_model_label}..."):
                    try:
                        res = generate_questions(role_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['quest_result'] = res
                        st.session_state['role_input'] = role_input
                    except Exception as e:
                        st.session_state['quest_result'] = {"error": str(e)}
            else:
                st.warning("Please provide target role parameters.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['quest_result']:
        res = st.session_state['quest_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            col_l, col_r = st.columns([1.3, 0.7], gap="large")

            with col_l:
                t1, t2, t3 = st.tabs(["⚙️ Technical", "🧠 Behavioral", "🌐 Scenarios"])
                
                with t1:
                    st.markdown("### Technical Validation")
                    for q in res.get("technical_questions", []):
                        st.markdown(f"<div class='q-box'>{q}</div>", unsafe_allow_html=True)
                        
                with t2:
                    st.markdown("### Behavioral Mapping")
                    for q in res.get("behavioral_questions", []):
                        st.markdown(f"<div class='q-box'>{q}</div>", unsafe_allow_html=True)

                with t3:
                    st.markdown("### Dynamic Scenarios")
                    for q in res.get("scenario_questions", []):
                        st.markdown(f"<div class='q-box'>{q}</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Export Script")
                
                st.download_button(
                    label="📥 Download interview_questions.json",
                    data=json.dumps(res, indent=2),
                    file_name="interview_questions.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download interview_questions.txt",
                    data=txt_export,
                    file_name="interview_questions.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>QuestForge AI © 2026 | Technical Requisition Evaluator | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
