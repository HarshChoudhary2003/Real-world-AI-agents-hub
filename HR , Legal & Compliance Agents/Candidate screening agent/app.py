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
    page_title="Advanced Candidate Screening | ScreenGenius Pro",
    page_icon="🔎",
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

    .stApp { background-color: #022c22; color: #f8fafc; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #064e3b !important; border-right: 1px solid #065f46; width: 340px !important; }

    .main-header {
        background: linear-gradient(90deg, #34d399, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #d1fae5; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(6, 78, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(52, 211, 153, 0.5); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #10b981 0%, #34d399 100%); }

    /* Advanced Metrics */
    .metric-container {
        display: flex; gap: 1rem; align-items: center; justify-content: space-between;
        background: rgba(2, 44, 34, 0.6); padding: 16px; border-radius: 12px;
        border: 1px solid rgba(16, 185, 129, 0.2); margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem; font-weight: 800; color: #34d399;
    }
    .metric-label {
        font-size: 0.9rem; color: #a7f3d0; text-transform: uppercase; letter-spacing: 1px;
    }
    
    .flag-box {
        background: rgba(220, 38, 38, 0.2);
        border-left: 4px solid #ef4444;
        padding: 12px 16px; margin-bottom: 10px;
        border-radius: 4px 8px 8px 4px; color: #fecaca;
        font-size: 0.95rem;
    }
    
    .stTextArea textarea { background: #022c22 !important; border: 1px solid #065f46 !important; color: #f8fafc !important; border-radius: 12px !important; line-height: 1.6 !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an Advanced Candidate Screening Agent (ATS Intelligence).

Rules:
- Conduct an objective, multi-dimensional forensic analysis of the resume against the job description.
- Never make final hiring decisions, act purely as an analytical engine.
- Identify both explicit skill matches and implicit trajectory matches.
- Highlight specific "red flags" (e.g., gaps in employment, missing critical certifications, mismatched seniority).
- Provide specific, tailored follow-up interview questions to probe the candidate's exact weaknesses.
- Remain neutral and avoid protected attribute bias.

Return ONLY valid JSON with this exact schema:
{
  "scores": {
    "technical_alignment": "Score out of 100",
    "experience_alignment": "Score out of 100",
    "overall_score": "Score out of 100"
  },
  "matched_requirements": ["Strong skill or experience matches"],
  "missing_requirements": ["Critical requirements not found"],
  "red_flags_or_concerns": ["Job gaps, overqualification, underqualification, missing degrees"],
  "custom_interview_probes": ["Question targeting missing requirement 1", "Question targeting red flag 1"],
  "screening_summary": "Objective 2-3 sentence executive summary"
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

def screen_candidate(job_text: str, resume_text: str, model: str, api_key: str | None = None) -> dict:
    prompt = f"Job Description:\n{job_text}\n\nCandidate Resume:\n{resume_text}\n"
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
    export = f"Advanced Candidate Screening Report\\n{'='*65}\\n\\n"
    scores = data.get("scores", {})
    export += "--- INTELLIGENCE SCORES ---\\n"
    export += f"Overall Match:      {scores.get('overall_score', 'N/A')}/100\\n"
    export += f"Technical Affinity: {scores.get('technical_alignment', 'N/A')}/100\\n"
    export += f"Experience Rating:  {scores.get('experience_alignment', 'N/A')}/100\\n\\n"
    export += "--- EXECUTIVE SUMMARY ---\\n"
    export += f"{data.get('screening_summary', '')}\\n\\n"
    export += "--- MATCHED REQUIREMENTS ---\\n"
    for m in data.get("matched_requirements", []): export += f"✅ {m}\\n"
    export += "\\n--- MISSING REQUIREMENTS ---\\n"
    for m in data.get("missing_requirements", []): export += f"❌ {m}\\n"
    export += "\\n--- RED FLAGS / CONCERNS ---\\n"
    for fg in data.get("red_flags_or_concerns", []): export += f"⚠️ {fg}\\n"
    export += "\\n--- RECOMMENDED INTERVIEW PROBES ---\\n"
    for q in data.get("custom_interview_probes", []): export += f"🎤 {q}\\n"
    return export

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    if 'screen_result' not in st.session_state:
        st.session_state['screen_result'] = None
        
    if 'job_input' not in st.session_state:
        st.session_state['job_input'] = (
            "Role: Data Analyst\n"
            "Required Skills:\n"
            "- SQL\n"
            "- Data analysis\n"
            "- Python\n"
            "Experience:\n"
            "- 2+ years in analytics or related role"
        )
        
    if 'resume_input' not in st.session_state:
        st.session_state['resume_input'] = (
            "Experience:\n"
            "- Business analyst for 3 years\n"
            "Skills:\n"
            "- SQL\n"
            "- Excel\n"
            "- Python\n"
            "- Data visualization"
        )

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>Screen<span style='color:#34d399;'>Genius Pro</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#a7f3d0;font-size:0.8rem;'>Advanced Forensic Engine Active</p>", unsafe_allow_html=True)

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
            st.info("Local Ollama endpoint selected. No API key required.")
            user_api_key = None
        else:
            user_api_key = st.text_input(f"{provider_name} API Key", type="password", help=f"Required if not pre-configured.")

        st.markdown("---")
        st.success("✨ **Pro Capabilities Active:** Multi-axis scoring, custom red flag evaluation, and dynamic interview guidance generation.")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Advanced Candidate Forensics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Perform rapid, multi-dimensional analysis. Identify red flags, calculate composite scores, and extract precision interview probes instantly.</p>", unsafe_allow_html=True)

    # Input Section
    col_req, col_res = st.columns(2, gap="large")
    with col_req:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 The Requisition (Job Specifications)")
        job_input = st.text_area("Job Description", height=200, value=st.session_state['job_input'], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 👤 The Candidate (Resume / CV Data)")
        resume_input = st.text_area("Candidate Resume", height=200, value=st.session_state['resume_input'], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    
    col_btn, _, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🔎 Execute Deep Matrix Scan"):
            if job_input.strip() and resume_input.strip():
                with st.spinner(f"Running Advanced Heuristics via {selected_model_label}..."):
                    try:
                        res = screen_candidate(job_input, resume_input, model=target_model, api_key=user_api_key if user_api_key else None)
                        st.session_state['screen_result'] = res
                        st.session_state['job_input'] = job_input
                        st.session_state['resume_input'] = resume_input
                    except Exception as e:
                        st.session_state['screen_result'] = {"error": str(e)}
            else:
                st.warning("Please provide both the Job Description and Resume.")

    # ── Outputs ───────────────────────────────────────────────
    if st.session_state['screen_result']:
        res = st.session_state['screen_result']

        if "error" in res:
            st.error(f"🔴 AI Error: {res['error']}")
        else:
            st.markdown("<hr style='border:1px solid #065f46;'>", unsafe_allow_html=True)
            col_l, col_r = st.columns([1.4, 0.6], gap="large")

            scores = res.get("scores", {})

            with col_l:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                st.markdown("### 🧠 Executive Summary")
                st.info(f"{res.get('screening_summary', 'No summary provided.')}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### ✅ Matched Requirements")
                    if not res.get("matched_requirements"): st.write("None.")
                    for m in res.get("matched_requirements", []): st.markdown(f"- **{m}**")

                with c2:
                    st.markdown("#### ❌ Critical Missing Traits")
                    if not res.get("missing_requirements"): st.write("None.")
                    for m in res.get("missing_requirements", []): st.markdown(f"- **{m}**")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### ⚠️ Red Flags / HR Concerns")
                flags = res.get("red_flags_or_concerns", [])
                if not flags:
                    st.success("No behavioral or temporal red flags detected.")
                else:
                    for fg in flags:
                        st.markdown(f"<div class='flag-box'>{fg}</div>", unsafe_allow_html=True)
                        
                st.markdown("#### 🎤 Custom Interview Probes")
                st.caption("Suggested questions based on gaps and red flags:")
                for q in res.get("custom_interview_probes", []):
                    st.markdown(f"- {q}")

                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### Algorithmic Scoring")
                
                st.markdown(f"""
                <div class='metric-container'>
                    <span class='metric-label'>Overall Fit</span>
                    <span class='metric-value'>{scores.get('overall_score', 'N/A')}</span>
                </div>
                <div class='metric-container'>
                    <span class='metric-label'>Technical</span>
                    <span class='metric-value'>{scores.get('technical_alignment', 'N/A')}</span>
                </div>
                <div class='metric-container'>
                    <span class='metric-label'>Experience</span>
                    <span class='metric-value'>{scores.get('experience_alignment', 'N/A')}</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Export Diagnostics")
                st.download_button(
                    label="📥 Download JSON Artifact",
                    data=json.dumps(res, indent=2),
                    file_name="advanced_screening_results.json",
                    mime="application/json",
                    use_container_width=True
                )
                txt_export = build_txt_export(res)
                st.download_button(
                    label="📥 Download TXT Dossier",
                    data=txt_export,
                    file_name="advanced_screening_results.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>ScreenGenius Pro AI © 2026 | Multi-Dimensional Candidate ATS | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
