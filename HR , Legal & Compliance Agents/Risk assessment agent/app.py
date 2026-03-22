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
    page_title="Risk Assessment AI | RiskForge",
    page_icon="⚠️",
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

    .stApp { background-color: #0f1115; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #08090b !important; border-right: 1px solid #1f2329; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #fcd34d; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(26, 30, 37, 0.6);
        border: 1px solid rgba(245, 158, 11, 0.15);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(245, 158, 11, 0.4); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); }

    .risk-box {
        background: rgba(20, 24, 30, 0.8);
        border-left: 4px solid #f59e0b;
        padding: 16px;
        margin-bottom: 20px;
        border-radius: 4px 8px 8px 4px;
        color: #f8fafc;
        font-size: 0.95rem;
    }
    
    .level-tag {
        display: inline-block; padding: 4px 10px; border-radius: 6px;
        font-weight: 700; font-size: 0.8rem; text-transform: uppercase;
        margin-left: 10px;
    }
    .level-low { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid #10b981; }
    .level-medium { background: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid #f59e0b; }
    .level-high { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid #ef4444; }
    .level-extreme { background: rgba(153, 27, 27, 0.2); color: #fca5a5; border: 1px solid #dc2626; box-shadow: 0 0 10px rgba(220, 38, 38, 0.5); }
    
    .stTextArea textarea { background: #08090b !important; border: 1px solid #1f2329 !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are a Risk Assessment Agent.

Rules:
- Identify and critically assess operational, legal, or technical risks based on the scenario.
- Estimate 'likelihood' and 'impact'.
- Suggest highly actionable mitigations.
- Be realistic and balanced.

Return ONLY valid JSON with this exact schema:
{
  "risks": [
    {
      "risk": "Clear description of the identified risk",
      "likelihood": "Low, Medium, or High",
      "impact": "Low, Medium, High, or Critical",
      "risk_level": "Overall risk classification (Low, Medium, High, Extreme)",
      "mitigation": "Targeted mitigation to reduce this risk"
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
        content_str = str(content)
        content = content_str[start_idx:end_idx]
    return json.loads(content)

def assess_risk(text: str, model: str, api_key: str | None = None) -> dict:
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
    export = f"Risk Assessment Log ({date.today()})\\n{'='*65}\\n\\n"
    risks = data.get("risks", [])
    if not risks:
        return export + "No major risks identified.\\n"
        
    for i, r in enumerate(risks, 1):
        export += f"Risk {i}: {r.get('risk', 'Unknown')}\\n"
        export += f" - Likelihood: {r.get('likelihood', 'N/A')}\\n"
        export += f" - Impact:     {r.get('impact', 'N/A')}\\n"
        export += f" - Risk Level: {r.get('risk_level', 'N/A')}\\n"
        export += f" - Mitigation: {r.get('mitigation', 'None')}\\n\\n"
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'risk_result' not in st.session_state:
        st.session_state['risk_result'] = None
        
    if 'scenario_input' not in st.session_state:
        st.session_state['scenario_input'] = (
            "Scenario: Launching a new customer data analytics feature\n"
            "Details:\n"
            "- Collects user behavior data\n"
            "- Integrates with third-party analytics tools\n"
            "- Targets EU customers"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Risk<span style='color:#f59e0b;'>Forge</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#fcd34d;font-size:0.8rem;'>Automated Threat Matrix</p>", unsafe_allow_html=True)

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
        st.warning("⚠️ **Notice:** This matrix maps operational hypotheses. High-consequence deployment decisions must still be confirmed by physical strategy boards.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Enterprise Threat & Risk Matrix</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Instantly deconstruct proposals, pinpointing likelihood ratios and required mitigations automatically.</p>", unsafe_allow_html=True)

    # Input Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Strategic Payload")
    scenario_input = st.text_area("Scenario Context", height=200, value=st.session_state['scenario_input'], label_visibility="collapsed")
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🔎 Execute Threat Analysis"):
            if scenario_input.strip():
                with st.spinner(f"Evaluating Risk Surface via {selected_model_label}..."):
                    try:
                        res = assess_risk(scenario_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['risk_result'] = res
                        st.session_state['scenario_input'] = scenario_input
                    except Exception as e:
                        st.session_state['risk_result'] = {"error": str(e)}
            else:
                st.warning("Please provide a scenario string to evaluate.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['risk_result']:
        res = st.session_state['risk_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            st.markdown("<hr style='border:1px solid #1f2329;'>", unsafe_allow_html=True)
            col_l, col_r = st.columns([1.5, 0.5], gap="large")

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 🛑 Detected Contingencies")
                
                risks = res.get("risks", [])
                if not risks:
                    st.success("No critical operational risks logged against this process.")
                else:
                    for r in risks:
                        level = str(r.get("risk_level", "Medium")).lower()
                        t_class = "level-medium"
                        if "low" in level: t_class = "level-low"
                        elif "extreme" in level: t_class = "level-extreme"
                        elif "high" in level: t_class = "level-high"
                        
                        st.markdown(f"""
                        <div class='risk-box'>
                            <h4 style="margin-top:0; color:white;">{r.get('risk', 'Unknown Risk')} <span class='level-tag {t_class}'>{level.upper()} RISK</span></h4>
                            <strong>Likelihood:</strong> {r.get('likelihood', 'N/A')} | <strong>Impact:</strong> {r.get('impact', 'N/A')}<br>
                            <hr style='border-color: rgba(245, 158, 11, 0.2); margin: 10px 0;'>
                            <strong>🛡️ Required Mitigation:</strong> {r.get('mitigation', 'None suggested')}
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Payload Export")
                
                st.download_button(
                    label="📥 Download Matrix JSON",
                    data=json.dumps(res, indent=2),
                    file_name="risk_assessment.json",
                    mime="application/json",
                    use_container_width=True
                )
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download Master TXT",
                    data=txt_export,
                    file_name="risk_assessment.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>RiskForge AI © 2026 | Objective Threat Matrices | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
