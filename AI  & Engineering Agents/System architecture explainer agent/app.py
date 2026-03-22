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
    page_title="System Architecture Explainer | ArchForge",
    page_icon="🏗️",
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
        background: linear-gradient(90deg, #c084fc, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(192, 132, 252, 0.35); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #9333ea 0%, #a855f7 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(168, 85, 247, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #a855f7 0%, #c084fc 100%); }

    /* Output tags */
    .tag-bubble {
        display: inline-block; background-color: #3b0764; border: 1px solid #6b21a8;
        color: #e9d5ff; border-radius: 12px; padding: 4px 12px; font-size: 0.85rem; font-weight: 600;
        margin-right: 8px; margin-bottom: 8px;
    }
    
    .stTextArea textarea { background: #0f172a !important; border: 1px solid #1e293b !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a System Architecture Explainer Agent.

Rules:
- Explain architecture clearly
- Avoid unnecessary jargon
- Highlight component roles and data flow
- Do NOT redesign the system

Return ONLY valid JSON with this schema:
{
  "overview": "High-level summary",
  "components": ["List of component roles"],
  "data_flow": "Description of data traveling through components",
  "design_decisions": ["Implied or stated design decisions"],
  "tradeoffs": ["Potential tradeoffs of this architecture"]
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

def analyze_architecture(text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": text}
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

    if 'arch_result' not in st.session_state:
        st.session_state['arch_result'] = None
        
    if 'text_input' not in st.session_state:
        st.session_state['text_input'] = (
            "The system consists of a web frontend, an API gateway, multiple microservices, a message queue, and a relational database.\n"
            "The frontend communicates with the API gateway, which routes requests to services.\n"
            "Services publish events to the queue for asynchronous processing."
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Arch<span style='color:#c084fc;'>Forge</span></h2>", unsafe_allow_html=True)

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
        st.info("💡 **Tip:** Extract deep design intent, unspoken tradeoffs, and clear operational data-flows from unstructured raw text.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Architecture Intelligence Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Translate raw textual design docs or loose meeting notes into formal system overviews, component listings, and trade-off analysis instantly.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Proposed / Existing Architecture Draft")
    text_input = st.text_area(
        "", 
        height=180, 
        value=st.session_state['text_input'],
        help="Paste a raw paragraph or bullet points explaining the current or proposed architecture."
    )
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🏗️ Deconstruct Architecture"):
            if text_input.strip():
                with st.spinner(f"Analyzing Topologies via {selected_model_label}..."):
                    try:
                        res = analyze_architecture(text_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['arch_result'] = res
                        st.session_state['text_input'] = text_input
                    except Exception as e:
                        st.session_state['arch_result'] = {"error": str(e)}
            else:
                st.warning("Please provide an architecture description to analyze.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['arch_result']:
        res = st.session_state['arch_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            col_l, col_r = st.columns([1.2, 0.8], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown(f"### 🔭 Executive Overview")
                st.info(f"{res.get('overview', 'No overview provided.')}")
                
                st.markdown("### 🔄 Primary Data Flow")
                st.success(f"{res.get('data_flow', 'Unclear data flow.')}")

                st.markdown("### 🧩 Core Components")
                components = res.get("components", [])
                if components:
                    for c in components:
                        st.markdown(f"<span class='tag-bubble'>{c}</span>", unsafe_allow_html=True)
                        
                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                st.markdown("### ⚖️ Implied Trade-offs")
                tradeoffs = res.get("tradeoffs", [])
                if not tradeoffs:
                    st.write("No major trade-offs detected.")
                else:
                    for t in tradeoffs:
                        st.warning(f"{t}")
                        
                st.markdown("### 🎯 Implicit Design Decisions")
                decisions = res.get("design_decisions", [])
                if decisions:
                    for d in decisions:
                        st.markdown(f"- {d}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("#### 📦 Export Schema")
                st.download_button(
                    label="📥 Download architecture_explanation.json",
                    data=json.dumps(res, indent=2),
                    file_name="architecture_explanation.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                txt_export = (f"System Architecture Explanation\\n{'='*55}\\n\\n"
                              f"Overview:\\n{res.get('overview', '')}\\n\\n"
                              f"Components:\\n" + "\\n".join([f"- {c}" for c in res.get('components', [])]) + "\\n\\n"
                              f"Data Flow:\\n{res.get('data_flow', '')}\\n\\n"
                              f"Design Decisions:\\n" + "\\n".join([f"- {d}" for d in res.get('design_decisions', [])]) + "\\n\\n"
                              f"Trade-offs:\\n" + "\\n".join([f"- {t}" for t in res.get('tradeoffs', [])]))
                              
                st.download_button(
                    label="📥 Download architecture_explanation.txt",
                    data=txt_export,
                    file_name="architecture_explanation.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>ArchForge AI © 2026 | Cloud Topology Intelligence Analyst | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
