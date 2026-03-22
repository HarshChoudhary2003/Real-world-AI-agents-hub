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
    page_title="AI Test Case Agent | TestForge",
    page_icon="🧪",
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

    .stApp { background-color: #0d1117; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #facc15, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(22, 27, 34, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(250, 204, 21, 0.35); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ca8a04 0%, #eab308 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(234, 179, 8, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #eab308 0%, #facc15 100%); }

    /* Test elements */
    .test-case-item {
        background: #1e293b;
        border-left: 4px solid #facc15;
        border-radius: 6px; padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .test-desc { font-weight: 600; font-size: 1.05rem; color: #f8fafc; margin-bottom: 0.5rem; }
    .test-io { color: #94a3b8; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }
    
    .stTextArea textarea { background: #0d1117 !important; border: 1px solid #30363d !important; color: #f1f5f9 !important; border-radius: 12px !important; font-family: 'JetBrains Mono', monospace !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Test Case Generation Agent.

Rules:
- Generate meaningful test cases
- Cover normal and edge cases
- Align with Python unittest style
- Do NOT invent behavior

Return ONLY valid JSON with this schema:
{
  "test_cases": [
    {
      "description": "Short description of the case",
      "inputs": {"a": 10, "b": 2},
      "expected": "5.0 or ValueError"
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
        content = str(content)[start_idx:end_idx]
    return json.loads(content)

def generate_tests(code_text: str, model: str, api_key: str | None = None) -> dict:
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

def build_test_file_content(data: dict) -> str:
    content = "import unittest\\n\\n"
    content += "# NOTE: Adjust this import to match your actual file hierarchy\\n"
    content += "from source_code import module_function\\n\\n"
    content += "class TestGeneratedSuite(unittest.TestCase):\\n"
    
    for i, t in enumerate(data.get("test_cases", []), 1):
        content += f"    def test_case_{i}(self):\\n"
        content += f"        \"\"\"{t.get('description', '')}\"\"\"\\n"
        
        expected = str(t.get('expected', ''))
        inputs = t.get('inputs', {})
        
        if "Exception" in expected or "Error" in expected:
            content += f"        with self.assertRaises(ValueError):\\n"
            content += f"            module_function(**{inputs})\\n\\n"
        else:
            content += f"        self.assertEqual(module_function(**{inputs}), {expected})\\n\\n"
    
    if not data.get("test_cases"):
        content += "    pass\\n"
    return content

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'tests_result' not in st.session_state:
        st.session_state['tests_result'] = None
        
    if 'code_input' not in st.session_state:
        st.session_state['code_input'] = (
            "def divide(a, b):\n"
            "    if b == 0:\n"
            "        raise ValueError(\"Division by zero\")\n"
            "    return a / b\n"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Test<span style='color:#facc15;'>Forge</span></h2>", unsafe_allow_html=True)

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
        st.info("💡 **Tip:** Neural test generation prevents regressions and secures architectural limits.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Automated Test Generation Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Scan source code deterministically to orchestrate comprehensive edge case testing suites instantly.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Target Source Code")
    code_input = st.text_area(
        "", 
        height=240, 
        value=st.session_state['code_input'],
        help="Paste the Python module / function you want to rigorously test."
    )
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🧪 Synthesize Testing Suite"):
            if code_input.strip():
                with st.spinner(f"Simulating Edge Cases via {selected_model_label}..."):
                    try:
                        res = generate_tests(code_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['tests_result'] = res
                        st.session_state['code_input'] = code_input
                    except Exception as e:
                        st.session_state['tests_result'] = {"error": str(e)}
            else:
                st.warning("Please provide code to analyze.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['tests_result']:
        res = st.session_state['tests_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            col_l, col_r = st.columns([1.1, 0.9], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 🔍 Generated Test Cases")
                
                tests = res.get("test_cases", [])
                if not tests:
                    st.info("No test cases generated. Ensure the code is valid.")
                else:
                    for i, t in enumerate(tests, 1):
                        st.markdown(f"""
                        <div class='test-case-item'>
                            <div class='test-desc'>🛡️ Block {i}: {t.get('description', '')}</div>
                            <div class='test-io'>Args Payload: {t.get('inputs', {})}</div>
                            <div class='test-io'>Expected Ret: {t.get('expected', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Export Files")
                
                st.markdown("#### Test Suite (`unittest`)")
                py_code = build_test_file_content(res)
                st.download_button(
                    label="📥 Download generated_tests.py",
                    data=py_code,
                    file_name="generated_tests.py",
                    mime="text/plain",
                    use_container_width=True
                )
                
                st.markdown("<hr style='border:1px solid #1e293b; margin:1rem 0;'>", unsafe_allow_html=True)
                
                st.markdown("#### JSON Reporting")
                report = {"date": str(date.today()), "tests": res.get("test_cases", [])}
                st.download_button(
                    label="📥 Download test_cases_report.json",
                    data=json.dumps(report, indent=2),
                    file_name="test_cases_report.json",
                    mime="application/json",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>TestForge AI © 2026 | Code Assurance Integrity Pipelines | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
