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
    page_title="Legal Clause Summary AI | BriefForge",
    page_icon="⚖️",
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
        background: linear-gradient(90deg, #fbbf24, #d97706);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #fde68a; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(251, 191, 36, 0.15);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(251, 191, 36, 0.4); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #d97706 0%, #fbbf24 100%);
        color: #0f172a; border: none; border-radius: 8px; font-weight: 700; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(251, 191, 36, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #fbbf24 0%, #fcd34d 100%); color: #020617; }

    .highlight-box {
        background: rgba(217, 119, 6, 0.15);
        border-left: 4px solid #f59e0b;
        padding: 16px; margin-bottom: 12px;
        border-radius: 4px 8px 8px 4px; color: #fef3c7;
        font-size: 0.95rem; line-height: 1.5;
    }
    
    .stTextArea textarea { background: #020617 !important; border: 1px solid #1e293b !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Legal Clause Summarization Agent.

Rules:
- Summarize legal clauses clearly into everyday professional language.
- Preserve the exact original contractual meaning.
- Highlight crucial obligations and risks.
- Do NOT provide formal legal advice.

Return ONLY valid JSON with this exact schema:
{
  "summary": "Clear, plain-English translation",
  "key_obligations": ["List of obligations"],
  "risks_or_conditions": ["List of risks or specific conditions"]
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

def summarize_clause(text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Legal Clause:\n{text}"}
        ],
        "temperature": 0.2
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

def build_txt_export(data: dict) -> str:
    export = f"Legal Clause Brief ({date.today()})\\n{'='*65}\\n\\n"
    export += f"Executive Summary:\\n{data.get('summary', 'None')}\\n\\n"
    
    export += "--- KEY OBLIGATIONS ---\\n"
    for o in data.get("key_obligations", []):
        export += f"- {o}\\n"
        
    export += "\\n--- RISKS & CONDITIONS ---\\n"
    for r in data.get("risks_or_conditions", []):
        export += f"- {r}\\n"
        
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'legal_result' not in st.session_state:
        st.session_state['legal_result'] = None
        
    if 'clause_input' not in st.session_state:
        st.session_state['clause_input'] = (
            "The Company shall not be liable for any indirect, incidental, special, or consequential damages arising out of or related to the use of the Service, even if advised of the possibility of such damages."
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Brief<span style='color:#fbbf24;'>Forge</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#fde68a;font-size:0.8rem;'>Automated Legal Clause Summarization</p>", unsafe_allow_html=True)

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
        st.warning("⚖️ **Disclaimer:** Summaries are AI-generated plain English interpretations and do not replace formal legal advice.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Legal Brief Synthesis</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Instantly translate dense legalese into plain English while explicitly isolating key contract risks.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📜 Target Clause")
    clause_input = st.text_area("Contract Extractor", height=150, value=st.session_state['clause_input'], label_visibility="collapsed")
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("⚖️ Translate Legalese"):
            if clause_input.strip():
                with st.spinner(f"Extracting clause mechanics via {selected_model_label}..."):
                    try:
                        res = summarize_clause(clause_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['legal_result'] = res
                        st.session_state['clause_input'] = clause_input
                    except Exception as e:
                        st.session_state['legal_result'] = {"error": str(e)}
            else:
                st.warning("Please paste a legal clause to evaluate.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['legal_result']:
        res = st.session_state['legal_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            st.markdown("<hr style='border:1px solid #1e293b;'>", unsafe_allow_html=True)
            col_l, col_r = st.columns([1.5, 0.5], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 🧠 Executive Translation")
                st.info(f"{res.get('summary', 'No summary generated.')}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### ✅ Key Obligations")
                    obs = res.get("key_obligations", [])
                    if obs:
                        for o in obs:
                            st.markdown(f"<div class='highlight-box'>⚓ {o}</div>", unsafe_allow_html=True)
                    else:
                        st.write("No distinct obligations identified.")
                        
                with c2:
                    st.markdown("#### ⚠️ Risks or Conditions")
                    risks = res.get("risks_or_conditions", [])
                    if risks:
                        for r in risks:
                            st.markdown(f"<div class='highlight-box'>⚠️ {r}</div>", unsafe_allow_html=True)
                    else:
                        st.write("No extreme conditioning risks identified.")

                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Brief Export")
                
                st.download_button(
                    label="📥 Download Brief JSON",
                    data=json.dumps(res, indent=2),
                    file_name="legal_summary.json",
                    mime="application/json",
                    use_container_width=True
                )
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download Brief TXT",
                    data=txt_export,
                    file_name="legal_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>BriefForge AI © 2026 | Objective Legal Translation Matrix | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
