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
    page_title="Audit Prep AI | AuditForge",
    page_icon="📋",
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
    section[data-testid="stSidebar"] { background-color: #050810 !important; border-right: 1px solid #1e293b; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #818cf8, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #a5b4fc; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(129, 140, 248, 0.15);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(129, 140, 248, 0.4); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%); }

    .gap-box {
        background: rgba(225, 29, 72, 0.1);
        border-left: 4px solid #e11d48;
        padding: 12px; margin-bottom: 8px;
        border-radius: 4px 8px 8px 4px; color: #ffe4e6;
        font-size: 0.95rem;
    }
    .fix-box {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        padding: 12px; margin-bottom: 8px;
        border-radius: 4px 8px 8px 4px; color: #d1fae5;
        font-size: 0.95rem;
    }
    .check-box {
        background: rgba(99, 102, 241, 0.1);
        border-left: 4px solid #6366f1;
        padding: 12px; margin-bottom: 8px;
        border-radius: 4px 8px 8px 4px; color: #e0e7ff;
        font-size: 0.95rem;
    }
    
    .stTextArea textarea { background: #050810 !important; border: 1px solid #1e293b !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an Enterprise Audit Preparation Agent.

Rules:
- Assess readiness directly against the provided audit schema (e.g., SOC 2, ISO 27001).
- Output specific Missing Evidence Checklists.
- Output Identified Operational Gaps.
- Output Actionable Remediation steps to resolve the gaps immediately.
- Be highly professional, rigorous, and direct.

Return ONLY valid JSON with this exact schema:
{
  "readiness_summary": "High-level current state",
  "evidence_checklist": ["Required Log 1", "Required PDF 2"],
  "identified_gaps": ["Crucial Missing Item 1", "Past Finding Unresolved"],
  "remediation_actions": ["Direct Action 1", "Direct Action 2"]
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

def prepare_audit(text: str, model: str, api_key: str | None = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Audit Matrix Input:\n{text}"}
        ],
        "temperature": 0.2
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

def build_txt_export(data: dict) -> str:
    export = f"Audit Readiness Matrix ({date.today()})\\n{'='*65}\\n\\n"
    export += f"Executive Readiness:\\n{data.get('readiness_summary', 'None')}\\n\\n"
    
    export += "--- EVIDENCE TO PROCURE ---\\n"
    for e in data.get("evidence_checklist", []):
        export += f"[ ] {e}\\n"
        
    export += "\\n--- OPERATIONAL GAPS DETECTED ---\\n"
    for g in data.get("identified_gaps", []):
        export += f"! {g}\\n"

    export += "\\n--- REMEDIATION DIRECTIVES ---\\n"
    for r in data.get("remediation_actions", []):
        export += f"-> {r}\\n"
        
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'audit_result' not in st.session_state:
        st.session_state['audit_result'] = None
        
    if 'audit_input' not in st.session_state:
        st.session_state['audit_input'] = (
            "Audit Type: SOC 2\n"
            "Scope: Data security and access controls\n"
            "Past Findings:\n"
            "- Incomplete access review documentation\n"
            "- Delayed incident response reporting"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Audit<span style='color:#818cf8;'>Forge</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#a5b4fc;font-size:0.8rem;'>Automated Compliance Architect</p>", unsafe_allow_html=True)

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
        st.success("📋 **Tip:** Supply past findings & exact framework tags (ISO27001/SOC2) for precision gap extraction.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Enterprise Readiness Forensics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Instantly generate required document telemetry, expose unresolved compliance gaps, and output remediation workflows prior to strict auditing.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Internal Audit State")
    audit_input = st.text_area("Provide framework type and known gaps", height=150, value=st.session_state['audit_input'], label_visibility="collapsed")
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🔎 Scan Readiness Deficiencies"):
            if audit_input.strip():
                with st.spinner(f"Simulating Auditor Parsing via {selected_model_label}..."):
                    try:
                        res = prepare_audit(audit_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['audit_result'] = res
                        st.session_state['audit_input'] = audit_input
                    except Exception as e:
                        st.session_state['audit_result'] = {"error": str(e)}
            else:
                st.warning("Please provide system context to audit.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['audit_result']:
        res = st.session_state['audit_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            st.markdown("<hr style='border:1px solid #1e293b;'>", unsafe_allow_html=True)
            col_l, col_r = st.columns([1.5, 0.5], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 🧠 Executive Readiness Summary")
                st.info(f"{res.get('readiness_summary', 'No summary generated.')}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### 🚫 Identified System Gaps")
                    for g in res.get("identified_gaps", []):
                        st.markdown(f"<div class='gap-box'>⚠ {g}</div>", unsafe_allow_html=True)
                        
                    st.markdown("#### 🛠️ Direct Remediation Code")
                    for r in res.get("remediation_actions", []):
                        st.markdown(f"<div class='fix-box'>✓ {r}</div>", unsafe_allow_html=True)
                        
                with c2:
                    st.markdown("#### 📋 Evidence Telemetry To Procure")
                    for e in res.get("evidence_checklist", []):
                        st.markdown(f"<div class='check-box'>🗂 {e}</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Payload Export")
                
                st.download_button(
                    label="📥 Download Audit JSON",
                    data=json.dumps(res, indent=2),
                    file_name="audit_readiness.json",
                    mime="application/json",
                    use_container_width=True
                )
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download Audit TXT",
                    data=txt_export,
                    file_name="audit_readiness.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>AuditForge AI © 2026 | Objective Compliance Forensics | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
