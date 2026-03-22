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
    page_title="AI Code Refactoring Agent | CleanCode",
    page_icon="🛠️",
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp { background-color: #0d1117; color: #e6edf3; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #8b949e; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(88, 166, 255, 0.35); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(35, 134, 54, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%); }

    /* Report elements */
    .change-item {
        background: #1c2128;
        border-left: 4px solid #bc8cff;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        color: #e6edf3;
    }
    .behavior-banner {
        background: rgba(35, 134, 54, 0.15);
        border: 1px solid rgba(35, 134, 54, 0.4);
        border-radius: 10px; padding: 1.5rem; text-align: center; margin-bottom: 1.5rem;
        color: #3fb950; font-weight: 700; font-size: 1.2rem;
    }
    .stTextArea textarea { background: #0d1117 !important; border: 1px solid #30363d !important; color: #e6edf3 !important; border-radius: 12px !important; font-family: 'JetBrains Mono', monospace !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Code Refactoring Agent.

Rules:
- Improve readability and structure
- Preserve behavior exactly
- Follow Python best practices (PEP 8)
- Explain changes clearly

Return ONLY valid JSON with this schema:
{
  "refactored_code": "string with the new python code",
  "changes_summary": ["string change 1", "string change 2"],
  "behavior_preserved": true
}
"""

def extract_json(content_raw: str) -> dict:
    content = str(content_raw)
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        start_idx = content.find("{")
        end_idx = content.rfind("}") + 1
        content = content[start_idx:end_idx]
    return json.loads(content)

def refactor_code(code_text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": code_text}
        ],
        "temperature": 0.2
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'refactored_result' not in st.session_state:
        st.session_state['refactored_result'] = None
        
    if 'code_input' not in st.session_state:
        st.session_state['code_input'] = "def calc(a, b):\n    x = a * b\n    y = a * b\n    return x + y\n"

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Clean<span style='color:#58a6ff;'>Code</span></h2>", unsafe_allow_html=True)

        st.markdown("### 🧬 AI Orchestration")
        provider_map = {
            "🌐 OpenAI — GPT-4o":          "gpt-4o",
            "🌐 OpenAI — GPT-4o Mini":     "gpt-4o-mini",
            "🎭 Claude 3.5 Sonnet":        "claude-3-5-sonnet-20240620",
            "🎭 Claude 3 Haiku":           "claude-3-haiku-20240307",
            "🔶 Gemini 1.5 Pro":           "gemini/gemini-1.5-pro",
            "🔶 Gemini 1.5 Flash":         "gemini/gemini-1.5-flash",
            "🐋 DeepSeek Chat":            "deepseek/deepseek-chat",
            "🚀 Grok-Beta":                "xai/grok-beta",
            "🏠 Llama 3 (Ollama)":         "ollama/llama3",
            "🏠 Mistral (Ollama)":         "ollama/mistral",
            "🔓 Llama 3 70B (Groq)":       "groq/llama3-70b-8192",
            "🔓 Mixtral 8x7B (Groq)":      "groq/mixtral-8x7b-32768",
        }
        selected_label = st.selectbox("Intelligence Engine", list(provider_map.keys()))
        target_model   = provider_map[selected_label]

        st.markdown("---")
        st.markdown("### 🔑 Authentication")
        user_api_key = st.text_input("Custom API Key (Optional)", type="password")

        st.markdown("---")
        st.info("💡 **Tip:** The agent verifies its modifications to ensure logic stability and best practices formatting.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Code Refactoring Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Upload or paste messy code, and the AI will analyze, clean, and provide a detailed change report.</p>", unsafe_allow_html=True)

    # IDE Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Original Source Code")
    code_input = st.text_area(
        "", 
        height=250, 
        value=st.session_state['code_input']
    )
    
    if st.button("🛠️ Initiate Refactoring"):
        if code_input.strip():
            with st.spinner(f"Refactoring via {selected_label.split('—')[-1].strip() if '—' in selected_label else selected_label}..."):
                try:
                    res = refactor_code(code_input, model=target_model, api_key=user_api_key if user_api_key else None)
                    st.session_state['refactored_result'] = res
                    st.session_state['code_input'] = code_input # save to preserve
                except Exception as e:
                    st.session_state['refactored_result'] = {"error": str(e)}
        else:
            st.warning("Please provide code to refactor.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['refactored_result']:
        res = st.session_state['refactored_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            col_l, col_r = st.columns([1.2, 0.8], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### ✨ Refactored Output")
                st.code(res.get("refactored_code", "No code generated"), language="python")

                # Export
                if st.download_button(
                    label="📥 Download refactored_code.py",
                    data=res.get("refactored_code", ""),
                    file_name="refactored_code.py",
                    mime="text/plain",
                    use_container_width=True
                ):
                    pass
                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📊 Refactoring Report")
                
                # Behavior preserved badge
                if res.get("behavior_preserved", False):
                    st.markdown("<div class='behavior-banner'>✅ Behavior Preserved</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='behavior-banner' style='background: rgba(248,81,73,0.15); border-color: rgba(248,81,73,0.4); color: #f85149;'>⚠️ Behavior Changed or Unverified</div>", unsafe_allow_html=True)

                st.markdown("#### Changes Applied:")
                for c in res.get("changes_summary", []):
                    st.markdown(f"<div class='change-item'>{c}</div>", unsafe_allow_html=True)

                report_json = json.dumps({
                    "date": str(date.today()),
                    "changes_summary": res.get("changes_summary", []),
                    "behavior_preserved": res.get("behavior_preserved", False)
                }, indent=2)

                st.download_button(
                    label="📥 Download Report JSON",
                    data=report_json,
                    file_name="refactoring_report.json",
                    mime="application/json",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#8b949e;'>CleanCode AI © 2026 | Code Transformation Architecture | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
