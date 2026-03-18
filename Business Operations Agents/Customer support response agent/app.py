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
    page_title="SupportCraft AI",
    page_icon="🛡️",
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
            background: linear-gradient(135deg, #1a0a2e 0%, #16213e 50%, #0f3460 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
            border-radius: 10px;
            border: 1px solid rgba(167, 139, 250, 0.25);
            transition: all 0.3s ease;
            font-size: 15px;
            background: rgba(15, 23, 42, 0.8);
            color: #e2e8f0;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #a78bfa;
            box-shadow: 0 0 0 1px #a78bfa, 0 0 20px rgba(167, 139, 250, 0.15);
        }
        .stButton button {
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 50%, #c4b5fd 100%);
            color: #020617;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        }
        .stButton button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(167, 139, 250, 0.5);
            color: #020617;
        }
        .header-title {
            background: linear-gradient(135deg, #a78bfa, #c4b5fd, #818cf8);
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
        .response-card {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(167, 139, 250, 0.15);
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 20px;
            backdrop-filter: blur(12px);
        }
        .analysis-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            margin: 4px;
        }
        .priority-critical { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
        .priority-high { background: rgba(249, 115, 22, 0.15); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.3); }
        .priority-medium { background: rgba(234, 179, 8, 0.15); color: #fbbf24; border: 1px solid rgba(234, 179, 8, 0.3); }
        .priority-low { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
        .sentiment-badge { background: rgba(167, 139, 250, 0.1); color: #c4b5fd; border: 1px solid rgba(167, 139, 250, 0.2); }
        .email-preview {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(167, 139, 250, 0.15);
            border-radius: 12px;
            padding: 28px;
            margin: 16px 0;
            font-size: 0.95rem;
            line-height: 1.7;
            color: #e2e8f0;
        }
        .email-subject {
            color: #a78bfa;
            font-weight: 800;
            font-size: 1.1rem;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(167, 139, 250, 0.15);
        }
        .step-item {
            background: rgba(167, 139, 250, 0.06);
            border-left: 3px solid #a78bfa;
            padding: 12px 18px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 8px;
            color: #e2e8f0;
            font-size: 0.92rem;
        }
        .internal-note {
            background: rgba(234, 179, 8, 0.06);
            border: 1px solid rgba(234, 179, 8, 0.15);
            border-radius: 10px;
            padding: 20px;
            margin-top: 16px;
        }
        .tag-chip {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            margin: 2px;
            background: rgba(167, 139, 250, 0.08);
            color: #c4b5fd;
            border: 1px solid rgba(167, 139, 250, 0.15);
        }
    </style>
""", unsafe_allow_html=True)


# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite Customer Support Response Agent for Enterprise Teams.

Rules:
- Craft highly professional, empathetic, and clear customer support responses.
- Analyze the customer's tone, urgency, and core issue before responding.
- Match the appropriate tone (formal, friendly, apologetic, solution-focused).
- Provide actionable next steps and resolution paths.
- Include escalation recommendations when appropriate.
- Never use generic filler language or robotic templates.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "ticket_analysis": {
    "core_issue": "The primary customer problem",
    "sentiment": "Customer sentiment (frustrated, confused, urgent, neutral, positive)",
    "priority": "low | medium | high | critical",
    "category": "Category of the support ticket"
  },
  "response": {
    "subject_line": "Professional email subject line",
    "greeting": "Personalized opening",
    "body": "The main response body with empathy, acknowledgment, and solution",
    "next_steps": ["Array of concrete next steps"],
    "closing": "Professional closing statement"
  },
  "internal_notes": {
    "escalation_needed": false,
    "escalation_reason": "Why escalation is or isn't needed",
    "follow_up_date": "Suggested follow-up timeframe",
    "knowledge_base_tags": ["Tags for internal categorization"]
  }
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


def process_ticket(customer, email, subject, message, product, tier, history, tone_pref,
                   provider_name, api_key, model, temp):
    prompt_text = (
        f"Customer: {customer}\n"
        f"Email: {email}\n"
        f"Subject: {subject}\n"
        f"Message: {message}\n"
        f"Product: {product}\n"
        f"Account Tier: {tier}\n"
        f"Previous Interactions: {history}\n"
        f"Preferred Response Tone: {tone_pref}\n"
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
        st.markdown("### 🛡️ Response Engine")

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
        st.markdown("### 🎛️ Tone Calibration")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05,
                                help="Lower = more formal and precise. Higher = warmer and more creative.")

        st.markdown("---")
        st.markdown("*SupportCraft AI v1.0*")

    # Main Area
    st.markdown('<div class="header-title">SupportCraft AI 🛡️</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">AI-powered customer support response engine. Analyze tickets, craft empathetic responses, and resolve issues faster.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 📧 Ticket Information")
        customer = st.text_input("👤 Customer Name", placeholder="e.g. John Smith")
        email = st.text_input("📧 Customer Email", placeholder="e.g. john@example.com")
        subject = st.text_input("📋 Ticket Subject", placeholder="e.g. Billing issue — charged twice")
        product = st.text_input("📦 Product/Service", placeholder="e.g. Premium SaaS Platform")
        tier = st.selectbox("🏷️ Account Tier", ["Free", "Starter", "Professional", "Enterprise", "Custom"])

    with col2:
        st.markdown("#### 💬 Customer Message")
        message = st.text_area("Customer's Message", height=150,
                               placeholder="Paste the customer's support message here...")
        history = st.text_area("📜 Previous Interaction History (Optional)", height=60,
                               placeholder="e.g. Last contacted 8 months ago for onboarding")
        tone_pref = st.selectbox("🎭 Response Tone",
                                 ["Empathetic & Professional", "Warm & Friendly",
                                  "Formal & Corporate", "Solution-Focused & Direct",
                                  "Apologetic & Reassuring"])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Generate Professional Response", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()

        if not message.strip():
            st.warning("⚠️ Customer message is required to generate a response.")
            st.stop()

        with st.spinner(f"🛡️ Analyzing ticket and crafting response via {model}..."):
            try:
                start_time = time.time()
                result = process_ticket(customer, email, subject, message, product, tier,
                                        history, tone_pref, provider, api_key, model, temperature)
                delay = time.time() - start_time

                st.success(f"✨ Response Crafted! Generated in {delay:.2f}s")

                analysis = result.get("ticket_analysis", {})
                resp = result.get("response", {})
                notes = result.get("internal_notes", {})

                # --- Ticket Analysis ---
                st.markdown("### 🔍 Ticket Analysis")
                analysis_cols = st.columns(4)

                priority = analysis.get("priority", "medium")
                priority_class = f"priority-{priority}"

                with analysis_cols[0]:
                    st.markdown(f'<span class="analysis-badge {priority_class}">⚡ {priority.upper()}</span>',
                                unsafe_allow_html=True)
                    st.caption("Priority")

                with analysis_cols[1]:
                    st.markdown(f'<span class="analysis-badge sentiment-badge">💬 {analysis.get("sentiment", "N/A")}</span>',
                                unsafe_allow_html=True)
                    st.caption("Sentiment")

                with analysis_cols[2]:
                    st.markdown(f'<span class="analysis-badge sentiment-badge">📂 {analysis.get("category", "N/A")}</span>',
                                unsafe_allow_html=True)
                    st.caption("Category")

                with analysis_cols[3]:
                    esc = "🔴 YES" if notes.get("escalation_needed") else "🟢 NO"
                    st.markdown(f'<span class="analysis-badge sentiment-badge">🔔 {esc}</span>',
                                unsafe_allow_html=True)
                    st.caption("Escalation")

                st.info(f"**Core Issue:** {analysis.get('core_issue', 'N/A')}")

                # --- Email Preview ---
                st.markdown("### ✉️ Generated Response")
                st.markdown(f"""
                <div class="email-preview">
                    <div class="email-subject">RE: {resp.get('subject_line', subject)}</div>
                    <p>{resp.get('greeting', '')}</p>
                    <p>{resp.get('body', '')}</p>
                    <p><em>{resp.get('closing', '')}</em></p>
                </div>
                """, unsafe_allow_html=True)

                # --- Next Steps ---
                if resp.get("next_steps"):
                    st.markdown("### 📋 Next Steps for Customer")
                    for step in resp["next_steps"]:
                        st.markdown(f'<div class="step-item">✅ {step}</div>', unsafe_allow_html=True)

                # --- Internal Notes ---
                st.markdown("### 🔒 Internal Team Notes")
                st.markdown(f"""
                <div class="internal-note">
                    <strong>Escalation:</strong> {"Required — " + notes.get("escalation_reason", "") if notes.get("escalation_needed") else "Not needed — " + notes.get("escalation_reason", "")}<br>
                    <strong>Follow-up Date:</strong> {notes.get("follow_up_date", "N/A")}<br>
                    <strong>KB Tags:</strong> {"".join([f'<span class="tag-chip">{t}</span>' for t in notes.get("knowledge_base_tags", [])])}
                </div>
                """, unsafe_allow_html=True)

                # --- Export ---
                st.markdown("---")
                st.markdown("### 💾 Export Response")

                full_email = f"Subject: RE: {resp.get('subject_line', subject)}\n\n"
                full_email += f"{resp.get('greeting', '')}\n\n"
                full_email += f"{resp.get('body', '')}\n\n"
                if resp.get("next_steps"):
                    full_email += "Next Steps:\n"
                    for step in resp["next_steps"]:
                        full_email += f"  - {step}\n"
                    full_email += "\n"
                full_email += f"{resp.get('closing', '')}\n"

                json_content = json.dumps(result, indent=2)

                exp_col1, exp_col2, exp_col3, _ = st.columns([1, 1, 1, 1])
                with exp_col1:
                    st.download_button("📧 Download Email TXT", full_email,
                                       f"support_response_{customer.replace(' ', '_')}.txt", "text/plain")
                with exp_col2:
                    st.download_button("{ } Download JSON", json_content,
                                       f"support_response_{customer.replace(' ', '_')}.json", "application/json")
                with exp_col3:
                    st.code(full_email, language=None)

            except Exception as e:
                import traceback
                st.error(f"❌ Response generation failed: {str(e)}")
                st.code(traceback.format_exc())

    st.markdown("---")
    st.caption("SupportCraft AI • Powered by LiteLLM Multi-Provider Relay")

if __name__ == "__main__":
    main()
