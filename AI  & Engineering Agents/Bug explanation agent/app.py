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
    page_title="AI Bug Explanation Agent | BugSentinel",
    page_icon="🐛",
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

    .stApp { background-color: #0b0f19; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #121827 !important; border-right: 1px solid #1e293b; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #f43f5e, #fb923c);
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
    .glass-card:hover { border-color: rgba(244, 63, 94, 0.35); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #e11d48 0%, #f43f5e 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(225, 29, 72, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #f43f5e 0%, #fb7185 100%); }

    /* Bug elements */
    .explanation-item {
        background: #1e293b;
        border-left: 4px solid #f43f5e;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        color: #f8fafc;
        font-size: 1rem;
    }
    .root-cause-banner {
        background: rgba(244, 63, 94, 0.15);
        border: 1px solid rgba(244, 63, 94, 0.3);
        border-radius: 10px; padding: 1.5rem; margin-bottom: 1.5rem;
        color: #fb7185; font-weight: 600; font-size: 1.1rem;
    }
    .focus-item {
        color: #cbd5e1; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }

    .stTextArea textarea { background: #0b0f19 !important; border: 1px solid #1e293b !important; color: #f8fafc !important; border-radius: 12px !important; font-family: 'JetBrains Mono', monospace !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Bug Explanation Agent.

Rules:
- Explain bugs clearly
- Identify root cause
- Reference code where relevant
- Do NOT provide a full fix

Return ONLY valid JSON with this schema:
{
  "explanation": "Clear explanation of why it failed",
  "root_cause": "The exact conceptual gap or error",
  "affected_code": ["function add_values", "variable result"],
  "debugging_focus": ["Check variable types", "Verify input sources"]
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

def explain_bug(error_text: str, code_text: str, model: str, api_key: str | None = None) -> dict:
    prompt = f"Error:\\n{error_text}\\n\\nCode:\\n{code_text}"
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt}
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

    if 'bug_result' not in st.session_state:
        st.session_state['bug_result'] = None
        
    if 'code_input' not in st.session_state:
        st.session_state['code_input'] = "def add_values(a, b):\\n    return a + b\\n\\nresult = add_values(5, \"10\")\\n"
        
    if 'error_input' not in st.session_state:
        st.session_state['error_input'] = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Bug<span style='color:#f43f5e;'>Sentinel</span></h2>", unsafe_allow_html=True)

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
        selected_label = st.selectbox("Diagnostic Engine", list(provider_map.keys()))
        target_model   = provider_map[selected_label]

        st.markdown("---")
        st.markdown("### 🔑 Authentication")
        user_api_key = st.text_input("Custom API Key (Optional)", type="password")

        st.markdown("---")
        st.info("💡 **Tip:** The agent diagnoses the root cause without writing the exact code fix, forcing the developer to learn.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Bug Diagnosis Forensics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>A neural proxy to explain tracebacks, identify conceptual failures, and prescribe debugging focuses.</p>", unsafe_allow_html=True)

    # Input Section
    col_code, col_err = st.columns(2, gap="large")
    with col_code:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📝 Failing Code Snippet")
        code_input = st.text_area(
            "Paste the code context here", 
            height=200, 
            value=st.session_state['code_input']
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_err:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚠️ Stack Trace / Exception")
        error_input = st.text_area(
            "Paste the terminal output or traceback here", 
            height=200, 
            value=st.session_state['error_input']
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Action Button
    st.markdown("<div style='max-width:300px; margin:0 auto 2rem;'>", unsafe_allow_html=True)
    if st.button("🦠 Launch Diagnosis Sequences"):
        if code_input.strip() and error_input.strip():
            with st.spinner(f"Analyzing via {selected_label.split('—')[-1].strip() if '—' in selected_label else selected_label}..."):
                try:
                    res = explain_bug(error_input, code_input, model=target_model, api_key=user_api_key if user_api_key else None)
                    st.session_state['bug_result'] = res
                    st.session_state['code_input'] = code_input # save to preserve
                    st.session_state['error_input'] = error_input
                except Exception as e:
                    st.session_state['bug_result'] = {"error": str(e)}
        else:
            st.warning("Please provide both code and error details.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['bug_result']:
        res = st.session_state['bug_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 🔍 Root Cause Analysis")
            st.markdown(f"<div class='root-cause-banner'>{res.get('root_cause', 'Unknown')}</div>", unsafe_allow_html=True)
            
            col_l, col_r = st.columns([1.2, 0.8], gap="large")

            with col_l:
                st.markdown("#### 💡 Explanation")
                st.markdown(f"<div class='explanation-item'>{res.get('explanation', 'None provided')}</div>", unsafe_allow_html=True)
                
                # Export
                report_json = json.dumps(res, indent=2)
                st.download_button(
                    label="📥 Download Diagnostic Report JSON",
                    data=report_json,
                    file_name="bug_explanation.json",
                    mime="application/json",
                    use_container_width=True
                )

            with col_r:
                st.markdown("#### 🎯 Affected Vectors")
                for c in res.get("affected_code", []):
                    st.markdown(f"- <span class='focus-item'>{c}</span>", unsafe_allow_html=True)
                
                st.markdown("#### 🔦 Debugging Focus")
                for d in res.get("debugging_focus", []):
                    st.markdown(f"- <span class='focus-item'>{d}</span>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>BugSentinel AI © 2026 | Debugging Intelligence Architectures | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
