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
    page_title="AI API Documentation Agent | DocForge",
    page_icon="📖",
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

    .stApp { background-color: #0f111a; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #161925 !important; border-right: 1px solid #1e2430; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(22, 25, 37, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(16, 185, 129, 0.35); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #10b981 0%, #34d399 100%); }

    /* Docs elements */
    .endpoint-banner {
        background: #1e293b;
        border-left: 5px solid #10b981;
        border-radius: 8px; padding: 1.2rem;
        font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 700;
        margin-bottom: 1.5rem; color: #10b981;
    }
    .doc-section-title {
        text-transform: uppercase; font-size: 0.85rem; font-weight: 700; color: #64748b;
        letter-spacing: 1px; margin-top: 1.5rem; border-bottom: 1px solid #334155; padding-bottom: 0.5rem; margin-bottom: 1rem;
    }
    
    .stTextArea textarea { background: #0f111a !important; border: 1px solid #1e2430 !important; color: #f1f5f9 !important; border-radius: 12px !important; font-family: 'JetBrains Mono', monospace !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an API Documentation Agent.

Rules:
- Generate clear, structured REST API documentation
- Use precise technical language
- Include examples and error references
- Do NOT invent endpoints

Return ONLY valid JSON with this schema:
{
  "endpoint": "METHOD /path",
  "overview": "Clear description of the API functionality",
  "request": {"field_name": "type and description"},
  "response": {"field_name": "type and description"},
  "examples": ["{ 'json': 'example' }"],
  "errors": ["400: Bad Request"]
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
        content = content[start_idx:end_idx]
    return json.loads(content)

def generate_docs(spec_text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": spec_text}
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

    if 'docs_result' not in st.session_state:
        st.session_state['docs_result'] = None
        
    if 'spec_input' not in st.session_state:
        st.session_state['spec_input'] = (
            "Endpoint: POST /users\n"
            "Description: Create a new user\n"
            "Authentication: Bearer token\n\n"
            "Request Body:\n- name (string, required)\n- email (string, required)\n\n"
            "Response:\n- id (string)\n- name (string)\n- email (string)\n\n"
            "Errors:\n- 400 Bad Request\n- 401 Unauthorized"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Doc<span style='color:#10b981;'>Forge</span></h2>", unsafe_allow_html=True)

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
        st.info("💡 **Tip:** Generate production-ready Markdown and JSON schemas from mere loose notes.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>API Documentation Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Transform messy notes and structural requirements into deterministic, developer-ready API contracts.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Rough API Specifications")
    spec_input = st.text_area(
        "", 
        height=220, 
        value=st.session_state['spec_input'],
        help="Paste your rough endpoint notes. The AI will formalize it."
    )
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("⚙️ Compile Documentation"):
            if spec_input.strip():
                with st.spinner(f"Architecting Docs via {selected_label.split('—')[-1].strip() if '—' in selected_label else selected_label}..."):
                    try:
                        res = generate_docs(spec_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['docs_result'] = res
                        st.session_state['spec_input'] = spec_input
                    except Exception as e:
                        st.session_state['docs_result'] = {"error": str(e)}
            else:
                st.warning("Please provide specifications.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['docs_result']:
        res = st.session_state['docs_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            col_l, col_r = st.columns([1.3, 0.7], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                # Render beautiful docs
                st.markdown(f"<div class='endpoint-banner'>{res.get('endpoint', 'METHOD /unknown')}</div>", unsafe_allow_html=True)
                st.markdown(f"**{res.get('overview', '')}**")
                
                # Request
                req_data = res.get("request", {})
                if req_data:
                    st.markdown("<div class='doc-section-title'>Request Parameters</div>", unsafe_allow_html=True)
                    req_df = pd.DataFrame([{"Field": k, "Type/Constraint": v} for k, v in req_data.items()])
                    st.table(req_df)

                # Response
                res_data = res.get("response", {})
                if res_data:
                    st.markdown("<div class='doc-section-title'>Response Schema</div>", unsafe_allow_html=True)
                    res_df = pd.DataFrame([{"Field": k, "Type": v} for k, v in res_data.items()])
                    st.table(res_df)
                    
                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                st.markdown("<div class='doc-section-title'>Example Payloads</div>", unsafe_allow_html=True)
                for ex in res.get("examples", []):
                    st.code(ex, language="json")
                
                st.markdown("<div class='doc-section-title'>Error Constraints</div>", unsafe_allow_html=True)
                for err in res.get("errors", []):
                    st.markdown(f"- `{err}`")
                
                st.markdown("<div class='doc-section-title'>Exports</div>", unsafe_allow_html=True)
                docs_json = json.dumps(res, indent=2)
                st.download_button(
                    label="📥 Download JSON Spec",
                    data=docs_json,
                    file_name="api_docs.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                md_content = f"# {res.get('endpoint')}\\n\\n{res.get('overview')}\\n\\n## Schema\\n**Request:**\\n{json.dumps(res.get('request'), indent=2)}\\n\\n**Response:**\\n{json.dumps(res.get('response'), indent=2)}"
                st.download_button(
                    label="📥 Download Markdown",
                    data=md_content,
                    file_name="api_docs.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>DocForge AI © 2026 | Automated Rest Documentation Intelligence | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
