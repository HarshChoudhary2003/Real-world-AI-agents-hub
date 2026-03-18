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
    page_title="LeadScore AI",
    page_icon="🎯",
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
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #0f172a 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
            border-radius: 10px;
            border: 1px solid rgba(251, 146, 60, 0.2);
            transition: all 0.3s ease;
            font-size: 15px;
            background: rgba(15, 23, 42, 0.8);
            color: #e2e8f0;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #fb923c;
            box-shadow: 0 0 0 1px #fb923c, 0 0 20px rgba(251, 146, 60, 0.15);
        }
        .stButton button {
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #ea580c 0%, #fb923c 50%, #fdba74 100%);
            color: #020617;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0 4px 15px rgba(234, 88, 12, 0.3);
        }
        .stButton button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(251, 146, 60, 0.5);
            color: #020617;
        }
        .header-title {
            background: linear-gradient(135deg, #fb923c, #f97316, #fdba74);
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
        .score-ring {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            border: 6px solid;
        }
        .score-ring-hot { border-color: #22c55e; background: rgba(34, 197, 94, 0.05); }
        .score-ring-warm { border-color: #fb923c; background: rgba(251, 146, 60, 0.05); }
        .score-ring-cool { border-color: #3b82f6; background: rgba(59, 130, 246, 0.05); }
        .score-ring-cold { border-color: #64748b; background: rgba(100, 116, 139, 0.05); }
        .score-number {
            font-size: 3.5rem;
            font-weight: 900;
            line-height: 1;
        }
        .score-label {
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 4px;
        }
        .bant-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(251, 146, 60, 0.12);
            border-radius: 14px;
            padding: 22px;
            backdrop-filter: blur(12px);
            text-align: center;
            transition: all 0.3s ease;
        }
        .bant-card:hover {
            border-color: rgba(251, 146, 60, 0.3);
            transform: translateY(-3px);
        }
        .bant-score {
            font-size: 2rem;
            font-weight: 900;
            color: #fb923c;
        }
        .bant-title {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #94a3b8;
            margin-bottom: 8px;
        }
        .bant-assessment {
            font-size: 0.85rem;
            color: #cbd5e1;
            margin-top: 10px;
            line-height: 1.4;
        }
        .flag-green {
            background: rgba(34, 197, 94, 0.06);
            border-left: 3px solid #22c55e;
            padding: 12px 18px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 8px;
            color: #86efac;
            font-size: 0.9rem;
        }
        .flag-red {
            background: rgba(239, 68, 68, 0.06);
            border-left: 3px solid #ef4444;
            padding: 12px 18px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 8px;
            color: #fca5a5;
            font-size: 0.9rem;
        }
        .action-card {
            background: rgba(251, 146, 60, 0.08);
            border: 1px solid rgba(251, 146, 60, 0.2);
            border-radius: 14px;
            padding: 24px;
            margin-top: 16px;
        }
        .talking-point {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(251, 146, 60, 0.1);
            padding: 12px 18px;
            border-radius: 10px;
            margin-bottom: 8px;
            color: #e2e8f0;
            font-size: 0.9rem;
        }
        .classification-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        .class-hot { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
        .class-warm { background: rgba(251, 146, 60, 0.15); color: #fb923c; border: 1px solid rgba(251, 146, 60, 0.3); }
        .class-cool { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
        .class-cold { background: rgba(100, 116, 139, 0.15); color: #94a3b8; border: 1px solid rgba(100, 116, 139, 0.3); }
    </style>
""", unsafe_allow_html=True)


# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite Lead Qualification Agent for Enterprise Sales Teams.

Rules:
- Analyze the provided lead information and qualify them using the BANT framework (Budget, Authority, Need, Timeline).
- Score each lead on a 1-100 scale based on qualification strength.
- Classify leads as: Hot (80-100), Warm (50-79), Cool (25-49), or Cold (0-24).
- Identify red flags and green flags in the lead data.
- Provide a tailored next-action recommendation for the sales team.
- Be brutally honest — false positives waste sales resources.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "qualification": {
    "lead_name": "Lead contact name",
    "company": "Company name",
    "score": 75,
    "classification": "Hot | Warm | Cool | Cold",
    "bant": {
      "budget": {"score": 8, "assessment": "Budget assessment details"},
      "authority": {"score": 7, "assessment": "Authority assessment details"},
      "need": {"score": 9, "assessment": "Need assessment details"},
      "timeline": {"score": 6, "assessment": "Timeline assessment details"}
    }
  },
  "green_flags": ["Positive indicators"],
  "red_flags": ["Warning signals or concerns"],
  "recommended_action": "Specific next step for the sales team",
  "talking_points": ["Key discussion points for the next call"],
  "disqualification_risks": ["Factors that could disqualify this lead"],
  "summary": "Executive summary of the qualification"
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
        "models": ["openrouter/auto", "openrouter/anthropic/claude-3.5-sonnet"],
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


def process_lead(lead_name, company, source, budget_info, authority_info,
                 need_info, timeline_info, notes,
                 provider_name, api_key, model, temp):
    prompt_text = (
        f"Lead: {lead_name}\n"
        f"Company: {company}\n"
        f"Source: {source}\n"
        f"Budget: {budget_info}\n"
        f"Authority: {authority_info}\n"
        f"Need: {need_info}\n"
        f"Timeline: {timeline_info}\n"
        f"Additional Notes:\n{notes}\n"
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
        st.markdown("### 🎯 Qualification Engine")

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
        st.markdown("### 🎛️ Analysis Depth")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.25, 0.05,
                                help="Lower = stricter qualification. Higher = more generous scoring.")

        st.markdown("---")
        st.markdown("*LeadScore AI v1.0*")

    # Main Area
    st.markdown('<div class="header-title">LeadScore AI 🎯</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">AI-powered BANT lead qualification. Score, classify, and strategize your next sales move with precision intelligence.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 👤 Lead Information")
        lead_name = st.text_input("👤 Contact Name & Title",
                                  placeholder="e.g. Sarah Chen, Director of Operations")
        company = st.text_input("🏢 Company & Stage",
                                placeholder="e.g. GrowthTech Solutions (Series B, 150 employees)")
        source = st.selectbox("📍 Lead Source",
                              ["Demo Request", "Website Form", "LinkedIn Inbound",
                               "Referral", "Conference/Event", "Cold Outreach",
                               "Content Download", "Free Trial Signup", "Webinar Attendee", "Other"])

    with col2:
        st.markdown("#### 📊 BANT Data")
        budget_info = st.text_input("💰 Budget Information",
                                    placeholder="e.g. $50K-$100K allocated for automation tools")
        authority_info = st.text_input("👔 Authority Level",
                                      placeholder="e.g. Director-level, signing authority up to $75K")
        need_info = st.text_input("🔥 Need / Pain Point",
                                  placeholder="e.g. Reduce manual data entry for 25 operations staff")
        timeline_info = st.text_input("⏰ Timeline",
                                      placeholder="e.g. Decision expected within 6 weeks, evaluating 3 vendors")

    notes = st.text_area("📝 Additional Context (Optional)", height=80,
                         placeholder="Any extra context: previous interactions, current tools, competitors being evaluated...")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Qualify & Score Lead", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()

        if not lead_name.strip() or not company.strip():
            st.warning("⚠️ Lead name and company are required for qualification.")
            st.stop()

        with st.spinner(f"🎯 Qualifying lead via {model}..."):
            try:
                start_time = time.time()
                result = process_lead(lead_name, company, source, budget_info,
                                      authority_info, need_info, timeline_info, notes,
                                      provider, api_key, model, temperature)
                delay = time.time() - start_time

                st.success(f"✨ Qualification Complete! Analyzed in {delay:.2f}s")

                qual = result.get("qualification", {})
                score = qual.get("score", 0)
                classification = qual.get("classification", "Cold")
                bant = qual.get("bant", {})

                # --- Score Display ---
                score_col, details_col = st.columns([1, 2])

                # Score color mapping
                class_lower = classification.lower()
                score_color_map = {"hot": "#22c55e", "warm": "#fb923c", "cool": "#3b82f6", "cold": "#64748b"}
                class_css_map = {"hot": "class-hot", "warm": "class-warm", "cool": "class-cool", "cold": "class-cold"}
                ring_css_map = {"hot": "score-ring-hot", "warm": "score-ring-warm", "cool": "score-ring-cool", "cold": "score-ring-cold"}
                score_color = score_color_map.get(class_lower, "#64748b")

                with score_col:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 20px;">
                        <div class="score-ring {ring_css_map.get(class_lower, 'score-ring-cold')}">
                            <div class="score-number" style="color: {score_color};">{score}</div>
                            <div class="score-label" style="color: {score_color};">/ 100</div>
                        </div>
                        <br>
                        <span class="classification-badge {class_css_map.get(class_lower, 'class-cold')}">🏷️ {classification}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with details_col:
                    st.markdown(f"""
                    <div class="action-card">
                        <h3 style="color: #fb923c; margin-top: 0;">📋 Executive Summary</h3>
                        <p style="color: #e2e8f0; line-height: 1.6;">{result.get('summary', '')}</p>
                        <h4 style="color: #fb923c; margin-top: 16px;">🚀 Recommended Action</h4>
                        <p style="color: #fdba74; font-weight: 600;">{result.get('recommended_action', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # --- BANT Breakdown ---
                st.markdown("### 📊 BANT Qualification Breakdown")
                bant_cols = st.columns(4)

                bant_labels = {"budget": "💰 Budget", "authority": "👔 Authority", "need": "🔥 Need", "timeline": "⏰ Timeline"}

                for i, (key, label) in enumerate(bant_labels.items()):
                    with bant_cols[i]:
                        item = bant.get(key, {})
                        bant_score = item.get("score", 0)
                        st.markdown(f"""
                        <div class="bant-card">
                            <div class="bant-title">{label}</div>
                            <div class="bant-score">{bant_score}/10</div>
                            <div class="bant-assessment">{item.get('assessment', 'N/A')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                # --- Flags ---
                flag_col1, flag_col2 = st.columns(2)

                with flag_col1:
                    st.markdown("### ✅ Green Flags")
                    for flag in result.get("green_flags", []):
                        st.markdown(f'<div class="flag-green">✅ {flag}</div>', unsafe_allow_html=True)

                with flag_col2:
                    st.markdown("### 🔴 Red Flags")
                    red_flags = result.get("red_flags", [])
                    if red_flags:
                        for flag in red_flags:
                            st.markdown(f'<div class="flag-red">⚠️ {flag}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown("No red flags detected. ✨")

                # --- Talking Points ---
                talking_points = result.get("talking_points", [])
                if talking_points:
                    st.markdown("### 💬 Talking Points for Next Call")
                    for tp in talking_points:
                        st.markdown(f'<div class="talking-point">💡 {tp}</div>', unsafe_allow_html=True)

                # --- Disqualification Risks ---
                risks = result.get("disqualification_risks", [])
                if risks:
                    with st.expander("⚠️ Disqualification Risks"):
                        for risk in risks:
                            st.markdown(f"- 🔴 {risk}")

                # --- Export ---
                st.markdown("---")
                st.markdown("### 💾 Export Qualification Report")

                txt_output = f"Lead Qualification Report — {qual.get('lead_name', lead_name)}\n"
                txt_output += "=" * 60 + "\n\n"
                txt_output += f"Company: {qual.get('company', company)}\n"
                txt_output += f"Score: {score}/100 ({classification})\n\n"
                txt_output += "BANT Analysis:\n"
                for key in ["budget", "authority", "need", "timeline"]:
                    item = bant.get(key, {})
                    txt_output += f"  {key.upper()} ({item.get('score', 'N/A')}/10): {item.get('assessment', '')}\n"
                txt_output += f"\nRecommended Action: {result.get('recommended_action', '')}\n"
                txt_output += f"\nSummary: {result.get('summary', '')}\n"
                txt_output += "\nGreen Flags:\n"
                for f in result.get("green_flags", []):
                    txt_output += f"  ✅ {f}\n"
                txt_output += "\nRed Flags:\n"
                for f in result.get("red_flags", []):
                    txt_output += f"  🔴 {f}\n"

                json_content = json.dumps(result, indent=2)

                exp_col1, exp_col2, _ = st.columns([1, 1, 2])
                with exp_col1:
                    st.download_button("📄 Download TXT Report", txt_output,
                                       f"lead_qual_{lead_name.replace(' ', '_')}.txt", "text/plain")
                with exp_col2:
                    st.download_button("{ } Download JSON", json_content,
                                       f"lead_qual_{lead_name.replace(' ', '_')}.json", "application/json")

            except Exception as e:
                import traceback
                st.error(f"❌ Qualification failed: {str(e)}")
                st.code(traceback.format_exc())

    st.markdown("---")
    st.caption("LeadScore AI • Powered by LiteLLM Multi-Provider Relay")

if __name__ == "__main__":
    main()
