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
    page_title="Policy Compliance AI | ComplianceGuard",
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

    .stApp { background-color: #0f0a0a; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #1a0f0f !important; border-right: 1px solid #331515; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #f87171, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #fca5a5; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(30, 20, 20, 0.6);
        border: 1px solid rgba(239, 68, 68, 0.15);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(239, 68, 68, 0.4); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #b91c1c 0%, #ef4444 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #ef4444 0%, #f87171 100%); }

    .violation-box {
        background: rgba(185, 28, 28, 0.1);
        border-left: 4px solid #ef4444;
        padding: 12px 16px;
        margin-bottom: 20px;
        border-radius: 4px 8px 8px 4px;
        color: #fecaca;
        font-size: 0.95rem;
    }
    
    .status-tag {
        display: inline-block; padding: 6px 12px; border-radius: 20px;
        font-weight: 700; font-size: 1rem; text-transform: uppercase;
        margin-bottom: 20px;
    }
    .status-compliant { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
    .status-noncompliant { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
    .status-partial { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
    
    .stTextArea textarea { background: #1a0f0f !important; border: 1px solid #331515 !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Policy Compliance Checker Agent.

Rules:
- Evaluate the provided content strictly against the provided policy rules.
- Identify violations directly tied to explicit policies.
- Classify the severity of each violation (Low, Medium, High, Critical).
- Explain findings transparently and impartially.
- If completely compliant, clearly state that.

Return ONLY valid JSON with this exact schema:
{
  "compliance_status": "Compliant, Partial, or Non-Compliant",
  "violations": [
    {
      "rule": "The specific policy rule violated",
      "severity": "Severity string level",
      "explanation": "Why this content violates the rule"
    }
  ],
  "guidance": ["Steps to remediate and achieve compliance"]
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

def check_compliance(policy_text: str, content_text: str, model: str, api_key: str | None = None) -> dict:
    prompt = f"Policy Elements:\n{policy_text}\n\nContent to Audit:\n{content_text}\n"
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

def build_txt_export(data: dict) -> str:
    export = f"Compliance Audit Report ({date.today()})\\n{'='*65}\\n\\n"
    status = data.get("compliance_status", "N/A")
    export += f"Status: {status}\\n\\n"
    
    viol = data.get("violations", [])
    if viol:
        export += "--- VIOLATIONS ---\\n"
        for v in viol:
            export += f"- Rule broken: {v.get('rule', 'Unknown')}\\n"
            export += f"  Severity: {v.get('severity', 'None')}\\n"
            export += f"  Explanation: {v.get('explanation', 'None')}\\n\\n"
    else:
        export += "--- VIOLATIONS ---\\nNone.\\n\\n"
        
    export += "--- REMEDIATION GUIDANCE ---\\n"
    for g in data.get("guidance", []):
        export += f"- {g}\\n"
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'audit_result' not in st.session_state:
        st.session_state['audit_result'] = None
        
    if 'policy_input' not in st.session_state:
        st.session_state['policy_input'] = (
            "Policy: Data Privacy\n"
            "Rules:\n"
            "- No sharing of personal email addresses\n"
            "- No storage of credit card numbers\n"
            "- All user data must be anonymized"
        )
        
    if 'content_input' not in st.session_state:
        st.session_state['content_input'] = (
            "User contact list includes names and email addresses."
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Compliance<span style='color:#f87171;'>Guard</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#fca5a5;font-size:0.8rem;'>Automated Risk & Penalty Prevention</p>", unsafe_allow_html=True)

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
        st.error("⚠️ **Notice:** Audits do not constitute formal legal counsel. Always verify explicitly high-risk flag detections with compliance officers.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Internal Policy Enforcement</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Scan documents, emails, and code structures dynamically against formal HR & Legal boundary rules.</p>", unsafe_allow_html=True)

    # Input Section
    col_req, col_res = st.columns(2, gap="large")
    with col_req:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🛡️ Core Policy Matrix")
        policy_input = st.text_area("Policy Rules", height=200, value=st.session_state['policy_input'], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📄 Target Document/Content")
        content_input = st.text_area("Content to check", height=200, value=st.session_state['content_input'], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("⚖️ Execute Compliance Audit"):
            if policy_input.strip() and content_input.strip():
                with st.spinner(f"Auditing via {selected_model_label}..."):
                    try:
                        res = check_compliance(policy_input, content_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['audit_result'] = res
                        st.session_state['policy_input'] = policy_input
                        st.session_state['content_input'] = content_input
                    except Exception as e:
                        st.session_state['audit_result'] = {"error": str(e)}
            else:
                st.warning("Please provide both the Policy matrix and the Target Content.")

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['audit_result']:
        res = st.session_state['audit_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            st.markdown("<hr style='border:1px solid #331515;'>", unsafe_allow_html=True)
            col_l, col_r = st.columns([1.3, 0.7], gap="large")

            status = res.get("compliance_status", "Unknown").lower()
            tag_class = "status-noncompliant"
            if status == "compliant": tag_class = "status-compliant"
            elif status == "partial": tag_class = "status-partial"

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='status-tag {tag_class}'>STATUS: {status.upper()}</div>", unsafe_allow_html=True)
                
                viol = res.get("violations", [])
                st.markdown("### 🛑 Detected Violations")
                if not viol:
                    st.success("No violations detected against the provided policy matrix.")
                else:
                    for v in viol:
                        st.markdown(f"""
                        <div class='violation-box'>
                            <strong>Rule Violated:</strong> {v.get('rule', 'N/A')}<br>
                            <strong>Risk Severity:</strong> {v.get('severity', 'N/A')}<br>
                            <hr style='border-color: rgba(239, 68, 68, 0.2); margin: 8px 0;'>
                            <strong>Evidence:</strong> {v.get('explanation', 'None provided')}
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("### 🗺️ Remediation Guidance")
                for g in res.get("guidance", []):
                    st.markdown(f"- {g}")

                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Audit Export")
                
                st.download_button(
                    label="📥 Download Audit JSON",
                    data=json.dumps(res, indent=2),
                    file_name="compliance_report.json",
                    mime="application/json",
                    use_container_width=True
                )
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download Audit TXT",
                    data=txt_export,
                    file_name="compliance_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#94a3b8;'>ComplianceGuard AI © 2026 | Enterprise Liability Engine | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
