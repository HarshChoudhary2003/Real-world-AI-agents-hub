import streamlit as st
import json
import os
import time
import re
from datetime import date
from litellm import completion
from dotenv import load_dotenv

# Page Config
st.set_page_config(
    page_title="CRM DataForge AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load context
load_dotenv()

# --- Premium Custom CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        .main {
            background: linear-gradient(135deg, #020617 0%, #0c1222 50%, #0f172a 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
            border-radius: 10px;
            border: 1px solid rgba(56, 189, 248, 0.2);
            transition: all 0.3s ease;
            font-size: 15px;
            background: rgba(15, 23, 42, 0.8);
            color: #e2e8f0;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 0 1px #38bdf8, 0 0 20px rgba(56, 189, 248, 0.15);
        }
        .stButton button {
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 50%, #7dd3fc 100%);
            color: #020617;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
        }
        .stButton button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.5);
            color: #020617;
        }
        .header-title {
            background: linear-gradient(135deg, #38bdf8, #0ea5e9, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 3.2rem;
            letter-spacing: -1.5px;
            margin-bottom: 0px;
            line-height: 1.1;
        }
        .header-subtitle {
            color: #64748b;
            font-size: 1.15rem;
            margin-bottom: 30px;
            line-height: 1.5;
        }
        .enrichment-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(56, 189, 248, 0.15);
            padding: 28px;
            border-radius: 16px;
            margin-bottom: 20px;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
        }
        .enrichment-card:hover {
            border-color: rgba(56, 189, 248, 0.35);
            box-shadow: 0 8px 32px rgba(56, 189, 248, 0.1);
            transform: translateY(-2px);
        }
        .metric-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            margin: 4px;
            background: rgba(56, 189, 248, 0.1);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }
        .score-display {
            font-size: 4rem;
            font-weight: 900;
            text-align: center;
            line-height: 1;
            margin: 10px 0;
        }
        .score-label {
            text-align: center;
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .section-title {
            color: #38bdf8;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .tag-chip {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            margin: 3px;
            background: rgba(14, 165, 233, 0.08);
            color: #7dd3fc;
            border: 1px solid rgba(125, 211, 252, 0.15);
        }
        .dm-card {
            background: rgba(56, 189, 248, 0.05);
            border-left: 3px solid #38bdf8;
            padding: 16px 20px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 10px;
        }
        .provider-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            background: rgba(56, 189, 248, 0.1);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
""", unsafe_allow_html=True)


# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite CRM Data Enrichment Agent for Enterprise Sales Teams.

Rules:
- Analyze the provided company/contact information and enrich it with actionable intelligence.
- Generate industry classification, company size estimates, technology stack guesses, and buying signals.
- Identify potential decision-makers' roles and engagement strategies.
- Provide concrete, data-driven enrichment — avoid vague or generic insights.
- Score the lead readiness from 1-10.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "enriched_profile": {
    "company_name": "Name of the company",
    "industry": "Classified industry vertical",
    "estimated_size": "Employee range estimate",
    "tech_stack_signals": ["Likely technologies used"],
    "buying_signals": ["Observed or inferred buying intent signals"],
    "pain_points": ["Likely business challenges"],
    "recommended_approach": "Tailored outreach strategy"
  },
  "decision_makers": [
    {
      "role": "Title/Role",
      "engagement_tip": "How to engage this persona"
    }
  ],
  "lead_score": 7,
  "enrichment_summary": "Brief strategic summary of findings"
}
"""

# Provider Data
PROVIDERS = {
    "OpenAI": {
        "models": ["openai/gpt-4o-mini", "openai/gpt-4o", "openai/gpt-3.5-turbo"],
        "env_key": "OPENAI_API_KEY"
    },
    "Anthropic": {
        "models": ["anthropic/claude-3-5-sonnet-20240620", "anthropic/claude-3-haiku-20240307", "anthropic/claude-3-opus-20240229"],
        "env_key": "ANTHROPIC_API_KEY"
    },
    "Google (Gemini)": {
        "models": ["gemini/gemini-1.5-flash", "gemini/gemini-1.5-pro", "gemini/gemini-pro"],
        "env_key": "GEMINI_API_KEY"
    },
    "Groq": {
        "models": ["groq/llama-3.1-70b-versatile", "groq/llama-3.1-8b-instant", "groq/mixtral-8x7b-32768"],
        "env_key": "GROQ_API_KEY"
    },
    "Mistral": {
        "models": ["mistral/mistral-large-latest", "mistral/mistral-small-latest"],
        "env_key": "MISTRAL_API_KEY"
    },
    "DeepSeek": {
        "models": ["deepseek/deepseek-chat", "deepseek/deepseek-coder"],
        "env_key": "DEEPSEEK_API_KEY"
    },
    "OpenRouter": {
        "models": ["openrouter/auto", "openrouter/anthropic/claude-3.5-sonnet", "openrouter/google/gemini-pro-1.5"],
        "env_key": "OPENROUTER_API_KEY"
    }
}


def extract_json(text_response):
    try:
        return json.loads(text_response)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text_response, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Failed to parse output into JSON format")


def process_enrichment(company_info, contact_info, source, notes, provider_name, api_key, model, temp):
    prompt_text = (
        f"Company: {company_info}\n"
        f"Contact: {contact_info}\n"
        f"Source: {source}\n"
        f"Notes:\n{notes}\n"
    )

    env_key = PROVIDERS[provider_name]["env_key"]
    if api_key:
        os.environ[env_key] = api_key

    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        temperature=temp,
    )

    return extract_json(response.choices[0].message.content)


# --- UI Layout ---
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### 🛡️ Intelligence Engine")

        provider = st.selectbox("LLM Provider", list(PROVIDERS.keys()))
        env_key_name = PROVIDERS[provider]["env_key"]
        api_key = st.text_input(f"{provider} API Key", type="password", value=os.getenv(env_key_name, ""))

        if api_key:
            os.environ[env_key_name] = api_key
            st.success("🔗 Connection Active")
        else:
            st.warning("🔑 Key Required")

        st.markdown("---")
        st.markdown("### 🧠 Model Selection")
        model = st.selectbox("Intelligence Model", PROVIDERS[provider]["models"])

        st.markdown("---")
        st.markdown("### 🎛️ Precision Tuning")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05,
                                help="Lower = more factual enrichment. Higher = more creative insights.")

        st.markdown("---")
        st.markdown("*CRM DataForge AI v1.0*")

    # Main Area
    st.markdown('<div class="header-title">CRM DataForge AI 🧬</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Transform raw CRM records into rich, actionable intelligence with AI-powered data enrichment.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 📋 Lead Information")
        company_info = st.text_input("🏢 Company Name & Website",
                                     placeholder="e.g. Acme Corp — acmecorp.io")
        contact_info = st.text_input("👤 Contact Name & Title",
                                     placeholder="e.g. Jane Doe, VP of Engineering")
        source = st.selectbox("📍 Lead Source",
                              ["LinkedIn Inbound", "Website Form", "Referral", "Cold Outreach",
                               "Conference/Event", "Content Download", "Free Trial Signup", "Other"])

    with col2:
        st.markdown("#### 📝 Additional Context")
        notes = st.text_area("🔍 Notes & Known Context", height=180,
                             placeholder="- Expressed interest in AI automation\n- Currently using legacy workflow systems\n- Team size approximately 200 engineers\n- Budget cycle starts Q1")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Enrich & Analyze Lead", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()

        if not company_info.strip():
            st.warning("⚠️ Company information is required for enrichment.")
            st.stop()

        with st.spinner(f"🧬 Enriching CRM data via {model}..."):
            try:
                start_time = time.time()
                result = process_enrichment(company_info, contact_info, source, notes,
                                            provider, api_key, model, temperature)
                delay = time.time() - start_time

                st.success(f"✨ Enrichment Complete! Processed in {delay:.2f}s")

                profile = result.get("enriched_profile", {})
                lead_score = result.get("lead_score", 0)

                # --- Score Display ---
                score_col, info_col = st.columns([1, 3])

                with score_col:
                    score_color = "#22c55e" if lead_score >= 7 else "#eab308" if lead_score >= 4 else "#ef4444"
                    st.markdown(f"""
                    <div class="enrichment-card" style="text-align: center;">
                        <div class="score-label">Lead Score</div>
                        <div class="score-display" style="color: {score_color};">{lead_score}</div>
                        <div class="score-label">out of 10</div>
                    </div>
                    """, unsafe_allow_html=True)

                with info_col:
                    st.markdown(f"""
                    <div class="enrichment-card">
                        <span class="provider-badge">{provider} • {model.split('/')[-1]}</span>
                        <h3 style="color: #f1f5f9; margin: 12px 0 6px 0;">{profile.get('company_name', company_info)}</h3>
                        <span class="metric-badge">📊 {profile.get('industry', 'N/A')}</span>
                        <span class="metric-badge">👥 {profile.get('estimated_size', 'N/A')}</span>
                        <p style="color: #94a3b8; margin-top: 14px; font-size: 0.95rem; line-height: 1.6;">{result.get('enrichment_summary', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Detailed Enrichment ---
                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.markdown('<div class="section-title">🔧 Tech Stack Signals</div>', unsafe_allow_html=True)
                    tech_html = "".join([f'<span class="tag-chip">{t}</span>' for t in profile.get("tech_stack_signals", [])])
                    st.markdown(f'<div class="enrichment-card">{tech_html if tech_html else "<em>No signals detected</em>"}</div>', unsafe_allow_html=True)

                    st.markdown('<div class="section-title">🎯 Buying Signals</div>', unsafe_allow_html=True)
                    for signal in profile.get("buying_signals", []):
                        st.markdown(f"- ✅ {signal}")

                with detail_col2:
                    st.markdown('<div class="section-title">⚠️ Pain Points</div>', unsafe_allow_html=True)
                    for pain in profile.get("pain_points", []):
                        st.markdown(f"- 🔴 {pain}")

                    st.markdown('<div class="section-title">🗺️ Recommended Approach</div>', unsafe_allow_html=True)
                    st.info(profile.get("recommended_approach", "No recommendation available."))

                # --- Decision Makers ---
                st.markdown('<div class="section-title">👥 Decision Maker Map</div>', unsafe_allow_html=True)
                for dm in result.get("decision_makers", []):
                    st.markdown(f"""
                    <div class="dm-card">
                        <strong style="color: #38bdf8;">{dm.get('role', 'Unknown Role')}</strong><br>
                        <span style="color: #94a3b8;">{dm.get('engagement_tip', '')}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Export ---
                st.markdown("---")
                st.markdown("### 💾 Export Intelligence Report")

                txt_output = f"CRM Enrichment Report — {profile.get('company_name', company_info)}\n"
                txt_output += "=" * 60 + "\n\n"
                txt_output += f"Industry: {profile.get('industry', 'N/A')}\n"
                txt_output += f"Size: {profile.get('estimated_size', 'N/A')}\n"
                txt_output += f"Lead Score: {lead_score}/10\n\n"
                txt_output += f"Summary:\n{result.get('enrichment_summary', '')}\n\n"
                txt_output += f"Recommended Approach:\n{profile.get('recommended_approach', '')}\n\n"
                txt_output += "Tech Stack:\n"
                for t in profile.get("tech_stack_signals", []):
                    txt_output += f"  - {t}\n"
                txt_output += "\nBuying Signals:\n"
                for s in profile.get("buying_signals", []):
                    txt_output += f"  - {s}\n"
                txt_output += "\nPain Points:\n"
                for p in profile.get("pain_points", []):
                    txt_output += f"  - {p}\n"
                txt_output += "\nDecision Makers:\n"
                for dm in result.get("decision_makers", []):
                    txt_output += f"  - {dm.get('role', '')}: {dm.get('engagement_tip', '')}\n"

                json_content = json.dumps(result, indent=2)

                exp_col1, exp_col2, _ = st.columns([1, 1, 2])
                with exp_col1:
                    st.download_button("📄 Download TXT Report", txt_output,
                                       f"crm_enrichment_{company_info.replace(' ', '_')}.txt", "text/plain")
                with exp_col2:
                    st.download_button("{ } Download JSON", json_content,
                                       f"crm_enrichment_{company_info.replace(' ', '_')}.json", "application/json")

            except Exception as e:
                import traceback
                st.error(f"❌ Enrichment failed: {str(e)}")
                st.code(traceback.format_exc())

    st.markdown("---")
    st.caption(f"CRM DataForge AI • Powered by LiteLLM Multi-Provider Relay")

if __name__ == "__main__":
    main()
