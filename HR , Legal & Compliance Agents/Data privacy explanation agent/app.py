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
    page_title="Data Privacy AI | PrivacyForge",
    page_icon="🛡️",
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

    .stApp { background-color: #0c1a1f; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #060d10 !important; border-right: 1px solid #142a33; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #2dd4bf, #0d9488);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #99f6e4; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(20, 42, 51, 0.4);
        border: 1px solid rgba(45, 212, 191, 0.15);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(45, 212, 191, 0.4); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(20, 184, 166, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #14b8a6 0%, #2dd4bf 100%); }

    .detail-box {
        background: rgba(13, 148, 136, 0.15);
        border-left: 4px solid #14b8a6;
        padding: 16px; margin-bottom: 12px;
        border-radius: 4px 8px 8px 4px; color: #ccfbf1;
        font-size: 0.95rem; line-height: 1.5;
    }
    
    .stTextArea textarea { background: #060d10 !important; border: 1px solid #142a33 !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Data Privacy Explanation Agent.

Rules:
- Explain specific privacy regulations clearly based on the provided scenario.
- Preserve the exact regulatory intent (e.g., GDPR, CCPA).
- Do NOT provide formal legal advice.
- Focus strictly on practical understanding, obligations, and individual rights.

Return ONLY valid JSON with this exact schema:
{
  "explanation": "Clear, plain-English overview of the regulatory constraints",
  "key_obligations": ["List of what the company must implement"],
  "individual_rights": ["List of rights the end-user has"],
  "practical_implications": ["Actionable corporate next steps"]
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

def explain_privacy(text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Operational Scenario:\n{text}"}
        ],
        "temperature": 0.2
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

def build_txt_export(data: dict) -> str:
    export = f"Data Privacy Analysis Record ({date.today()})\\n{'='*65}\\n\\n"
    export += f"Regulatory Explanation:\\n{data.get('explanation', 'None')}\\n\\n"
    
    export += "--- KEY CORPORATE OBLIGATIONS ---\\n"
    for o in data.get("key_obligations", []):
        export += f"- {o}\\n"
        
    export += "\\n--- INDIVIDUAL USER RIGHTS ---\\n"
    for r in data.get("individual_rights", []):
        export += f"- {r}\\n"

    export += "\\n--- PRACTICAL BUSINESS IMPLICATIONS ---\\n"
    for p in data.get("practical_implications", []):
        export += f"- {p}\\n"
        
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'privacy_result' not in st.session_state:
        st.session_state['privacy_result'] = None
        
    if 'scenario_input' not in st.session_state:
        st.session_state['scenario_input'] = (
            "Scenario: Collecting email addresses for a marketing newsletter from EU users.\n"
            "Regulation Focus: GDPR"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Privacy<span style='color:#2dd4bf;'>Forge</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#99f6e4;font-size:0.8rem;'>Automated Cyber Law Explainer</p>", unsafe_allow_html=True)

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
        st.warning("🛡️ **Notice:** All outputs are AI-driven regulatory overviews meant for operational logic parsing, not formal legal council mapping.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Cyber Compliance & Privacy Logic</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Map product decisions and codebase telemetry changes directly against GDPR, CCPA, and HIPAA architectures.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Define Operational Feature")
    scenario_input = st.text_area("What are you building or collecting?", height=120, value=st.session_state['scenario_input'], label_visibility="collapsed")
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🛡️ Execute Privacy Audit"):
            if scenario_input.strip():
                with st.spinner(f"Querying Regulatory Architecture via {selected_model_label}..."):
                    try:
                        res = explain_privacy(scenario_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['privacy_result'] = res
                        st.session_state['scenario_input'] = scenario_input
                    except Exception as e:
                        st.session_state['privacy_result'] = {"error": str(e)}
            else:
                st.warning("Please provide a feature scenario to audit.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['privacy_result']:
        res = st.session_state['privacy_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            st.markdown("<hr style='border:1px solid #142a33;'>", unsafe_allow_html=True)
            col_l, col_r = st.columns([1.5, 0.5], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 🧠 Regulatory Explanation")
                st.info(f"{res.get('explanation', 'No explanation generated.')}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### ✅ Required Corporate Obligations")
                    for o in res.get("key_obligations", []):
                        st.markdown(f"<div class='detail-box'>⚓ {o}</div>", unsafe_allow_html=True)
                        
                with c2:
                    st.markdown("#### ⚖️ Retained Individual Rights")
                    for r in res.get("individual_rights", []):
                        st.markdown(f"<div class='detail-box'>👤 {r}</div>", unsafe_allow_html=True)
                        
                st.markdown("#### 🛠️ Practical Implementation Code (Business Impact)")
                for p in res.get("practical_implications", []):
                    st.markdown(f"- {p}")

                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Payload Export")
                
                st.download_button(
                    label="📥 Download JSON Matrix",
                    data=json.dumps(res, indent=2),
                    file_name="privacy_explanation.json",
                    mime="application/json",
                    use_container_width=True
                )
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download TXT Summary",
                    data=txt_export,
                    file_name="privacy_explanation.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>PrivacyForge AI © 2026 | Objective Data Ordinance Parsing | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
