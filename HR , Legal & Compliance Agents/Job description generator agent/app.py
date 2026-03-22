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
    page_title="Job Description Generator | TalentForge",
    page_icon="💼",
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

    .stApp { background-color: #0b1120; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #1e293b; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
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
    .glass-card:hover { border-color: rgba(56, 189, 248, 0.35); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(56, 189, 248, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #38bdf8 0%, #7dd3fc 100%); }

    /* Output tags */
    .jd-section-title {
        color: #38bdf8;
        font-weight: 700;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 0.5rem;
    }
    
    .stTextArea textarea { background: #0f172a !important; border: 1px solid #1e293b !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Job Description Generator Agent.

Rules:
- Generate clear, inclusive job descriptions
- Avoid biased language
- Structure content professionally
- Do NOT invent unrealistic requirements

Return ONLY valid JSON with this schema:

{
  "role_overview": "Paragraph describing the role",
  "responsibilities": ["List of responsibilities"],
  "required_qualifications": ["List of requirements"],
  "preferred_qualifications": ["List of nice to haves"],
  "benefits": ["List of inferred or standard benefits"]
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

def generate_jd(text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": text}
        ],
        "temperature": 0.3
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

def build_txt_export(data: dict) -> str:
    export = f"Job Description Generated\\n{'='*55}\\n\\n"
    export += f"Role Overview:\\n{data.get('role_overview', '')}\\n\\n"
    export += "Responsibilities:\\n" + "\\n".join([f"- {r}" for r in data.get('responsibilities', [])]) + "\\n\\n"
    export += "Required Qualifications:\\n" + "\\n".join([f"- {q}" for q in data.get('required_qualifications', [])]) + "\\n\\n"
    if data.get('preferred_qualifications'):
        export += "Preferred Qualifications:\\n" + "\\n".join([f"- {p}" for p in data.get('preferred_qualifications', [])]) + "\\n\\n"
    if data.get('benefits'):
        export += "Benefits:\\n" + "\\n".join([f"- {b}" for b in data.get('benefits', [])]) + "\\n"
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'jd_result' not in st.session_state:
        st.session_state['jd_result'] = None
        
    if 'role_input' not in st.session_state:
        st.session_state['role_input'] = (
            "Role: AI Product Manager\n"
            "Team: Enterprise AI Platform\n"
            "Seniority: Senior\n"
            "Location: Remote\n\n"
            "Responsibilities:\n"
            "- Define AI product roadmap\n"
            "- Collaborate with engineering and stakeholders\n"
            "- Drive product delivery\n\n"
            "Required Skills:\n"
            "- Product management experience\n"
            "- AI/ML fundamentals"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Talent<span style='color:#38bdf8;'>Forge</span></h2>", unsafe_allow_html=True)

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
        
        selected_label = f"{selected_provider} — {selected_model_label}"

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
        st.info("💡 **Tip:** Eradicate biased verbiage and dynamically scale talent requisitions effortlessly.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>AI Job Description Architect</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Transform brief role requirements into expansive, inclusive, and highly professional job descriptions instantly.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Rough Role Brief")
    role_input = st.text_area(
        "", 
        height=220, 
        value=st.session_state['role_input'],
        help="Paste basic bullet points regarding the title, requirements, and responsibilities."
    )
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("💼 Synthesize Description"):
            if role_input.strip():
                with st.spinner(f"Architecting Requisition via {selected_model_label}..."):
                    try:
                        res = generate_jd(role_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['jd_result'] = res
                        st.session_state['role_input'] = role_input
                    except Exception as e:
                        st.session_state['jd_result'] = {"error": str(e)}
            else:
                st.warning("Please provide a role brief to expand upon.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['jd_result']:
        res = st.session_state['jd_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            col_l, col_r = st.columns([1.3, 0.7], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                st.markdown("<div class='jd-section-title'>Role Overview</div>", unsafe_allow_html=True)
                st.write(f"{res.get('role_overview', '')}")
                
                st.markdown("<div class='jd-section-title'>Responsibilities</div>", unsafe_allow_html=True)
                for r in res.get("responsibilities", []):
                    st.markdown(f"- {r}")

                st.markdown("<div class='jd-section-title'>Required Qualifications</div>", unsafe_allow_html=True)
                for req in res.get("required_qualifications", []):
                    st.markdown(f"- {req}")

                if res.get("preferred_qualifications"):
                    st.markdown("<div class='jd-section-title'>Preferred Qualifications</div>", unsafe_allow_html=True)
                    for pref in res.get("preferred_qualifications", []):
                        st.markdown(f"- {pref}")

                if res.get("benefits"):
                    st.markdown("<div class='jd-section-title'>Value & Benefits</div>", unsafe_allow_html=True)
                    for b in res.get("benefits", []):
                        st.markdown(f"- {b}")
                        
                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Export Requisition")
                
                st.download_button(
                    label="📥 Download job_description.json",
                    data=json.dumps(res, indent=2),
                    file_name="job_description.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download job_description.txt",
                    data=txt_export,
                    file_name="job_description.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>TalentForge AI © 2026 | Inclusive Requisition Intelligence | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
