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
    page_title="Performance Review AI | ReviewForge",
    page_icon="📈",
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

    .stApp { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(96, 165, 250, 0.35); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%); }

    .feedback-box {
        background: rgba(30, 64, 175, 0.15);
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        margin-bottom: 12px;
        border-radius: 4px 8px 8px 4px;
        color: #e2e8f0;
    }
    
    .stTextArea textarea { background: #020617 !important; border: 1px solid #1e293b !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Performance Review Agent.

Rules:
- Generate balanced, evidence-based reviews.
- Use professional, constructive language.
- Avoid biased or inflammatory phrasing.
- Do NOT assign compensation decisions.

Return ONLY valid JSON with this schema:
{
  "summary": "Executive overview of performance",
  "strengths": ["List of core strengths"],
  "areas_for_improvement": ["Constructive feedback areas"],
  "development_recommendations": ["Actionable steps"]
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

def generate_review(input_text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": input_text}
        ],
        "temperature": 0.3
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

def build_txt_export(data: dict) -> str:
    export = f"Performance Review Report ({date.today()})\\n{'='*55}\\n\\n"
    export += f"Summary:\\n{data.get('summary', '')}\\n\\n"
    
    export += "Strengths:\\n"
    for s in data.get("strengths", []):
        export += f"- {s}\\n"
        
    export += "\\nAreas for Improvement:\\n"
    for a in data.get("areas_for_improvement", []):
        export += f"- {a}\\n"
        
    export += "\\nDevelopment Recommendations:\\n"
    for d in data.get("development_recommendations", []):
        export += f"- {d}\\n"
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'review_result' not in st.session_state:
        st.session_state['review_result'] = None
        
    if 'perf_input' not in st.session_state:
        st.session_state['perf_input'] = (
            "Employee Role: Software Engineer\n"
            "Review Period: Q2\n"
            "Goals:\n"
            "- Deliver authentication feature\n"
            "- Improve code quality\n"
            "Manager Notes:\n"
            "- Delivered feature on time\n"
            "- Improved test coverage\n"
            "- Occasionally missed documentation updates"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Review<span style='color:#60a5fa;'>Forge</span></h2>", unsafe_allow_html=True)

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
        st.info("💡 **Tip:** Neural modeling prevents inflammatory or biased feedback automatically.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Performance Review Architect</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Transform brief management notes into polished, objective, and legally sound professional performance appraisals.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Manager's Unstructured Notes")
    perf_input = st.text_area(
        "", 
        height=180, 
        value=st.session_state['perf_input'],
        help="Paste crude bullet points regarding performance, goals, and observations."
    )
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("📈 Architect Review Payload"):
            if perf_input.strip():
                with st.spinner(f"Synthesizing Professional Tone via {selected_model_label}..."):
                    try:
                        res = generate_review(perf_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['review_result'] = res
                        st.session_state['perf_input'] = perf_input
                    except Exception as e:
                        st.session_state['review_result'] = {"error": str(e)}
            else:
                st.warning("Please provide performance notes.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['review_result']:
        res = st.session_state['review_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            col_l, col_r = st.columns([1.3, 0.7], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 🧠 Executive Summary")
                st.info(f"{res.get('summary', 'No summary provided.')}")
                
                t1, t2, t3 = st.tabs(["🌟 Strengths", "📈 Growth Areas", "🗺️ Action Plan"])
                
                with t1:
                    for s in res.get("strengths", []):
                        st.markdown(f"<div class='feedback-box'>{s}</div>", unsafe_allow_html=True)
                        
                with t2:
                    for a in res.get("areas_for_improvement", []):
                        st.markdown(f"<div class='feedback-box'>{a}</div>", unsafe_allow_html=True)

                with t3:
                    for d in res.get("development_recommendations", []):
                        st.markdown(f"<div class='feedback-box'>{d}</div>", unsafe_allow_html=True)
                        
                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Export Logic")
                
                st.download_button(
                    label="📥 Download review.json",
                    data=json.dumps(res, indent=2),
                    file_name="performance_review.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download review.txt",
                    data=txt_export,
                    file_name="performance_review.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>ReviewForge AI © 2026 | Constructive Appraisal Engine | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
