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
    page_title="SalesFollowAI Pro",
    page_icon="🤝",
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
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #020617 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
            border-radius: 10px;
            border: 1px solid rgba(14, 165, 233, 0.2);
            transition: all 0.3s ease;
            font-size: 15px;
            background: rgba(15, 23, 42, 0.8);
            color: #e2e8f0;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #0ea5e9;
            box-shadow: 0 0 0 1px #0ea5e9, 0 0 20px rgba(14, 165, 233, 0.15);
        }
        .stButton button {
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 50%, #38bdf8 100%);
            color: #020617;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3);
        }
        .stButton button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(14, 165, 233, 0.5);
            color: #020617;
        }
        .header-title {
            background: linear-gradient(135deg, #38bdf8, #0ea5e9, #0284c7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 3.2rem;
            letter-spacing: -1.5px;
            margin-bottom: 0px;
            line-height: 1.1;
        }
        .header-subtitle {
            color: #94a3b8;
            font-size: 1.15rem;
            margin-bottom: 30px;
            line-height: 1.5;
        }
        .message-preview {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(14, 165, 233, 0.2);
            border-radius: 16px;
            padding: 35px;
            margin-bottom: 20px;
            backdrop-filter: blur(12px);
            font-size: 1.05rem;
            line-height: 1.7;
            color: #f1f5f9;
            transition: all 0.3s ease;
        }
        .message-preview:hover {
            border-color: rgba(14, 165, 233, 0.4);
            box-shadow: 0 8px 32px rgba(14, 165, 233, 0.1);
        }
        .section-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #38bdf8;
            margin-bottom: 4px;
            margin-top: 16px;
            opacity: 0.8;
            display: block;
            border-bottom: 1px dashed rgba(56, 189, 248, 0.3);
            padding-bottom: 4px;
        }
        .section-label:first-child {
            margin-top: 0;
        }
        .cta-highlight {
            background: rgba(56, 189, 248, 0.1);
            border-left: 3px solid #38bdf8;
            padding: 10px 16px;
            border-radius: 0 8px 8px 0;
            margin: 12px 0;
            font-weight: 600;
            color: #e0f2fe;
        }
        .tone-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            background: rgba(14, 165, 233, 0.1);
            color: #38bdf8;
            border: 1px solid rgba(14, 165, 233, 0.2);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)


# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite Sales Follow-Up Agent for Enterprise Teams.

Rules:
- Reference prior interaction intelligently, making it clear you listened.
- Be professional, consultative, and articulate.
- Highlight specific value tailored to their role and context.
- Include a single, clear next step (Call to Action).
- Avoid high-pressure sales tactics or artificial urgency.
- Ensure the overall tone precisely matches the user's instructions.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "opening": "Professional opening greeting and well-wishes",
  "interaction_reference": "Direct and appreciative reference to the previous discussion",
  "value_reinforcement": "Reiteration of value discussed and how it solves their challenges",
  "call_to_action": "Clear next step, meeting request, or timeline",
  "closing": "Professional closing sign-off"
}
"""

# Provider Data
PROVIDERS = {
    "OpenAI": {
        "models": ["openai/gpt-4o-mini", "openai/gpt-4o", "openai/gpt-3.5-turbo"],
        "env_key": "OPENAI_API_KEY"
    },
    "Anthropic": {
        "models": ["anthropic/claude-3-5-sonnet-20240620", "anthropic/claude-3-haiku-20240307"],
        "env_key": "ANTHROPIC_API_KEY"
    },
    "Google (Gemini)": {
        "models": ["gemini/gemini-1.5-flash", "gemini/gemini-1.5-pro"],
        "env_key": "GEMINI_API_KEY"
    },
    "Groq": {
        "models": ["groq/llama-3.1-70b-versatile", "groq/llama-3.1-8b-instant", "groq/mixtral-8x7b-32768"],
        "env_key": "GROQ_API_KEY"
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


def generate_draft(context, role, objective, tone, provider_name, api_key, model, temp):
    prompt_text = (
        f"Previous Interaction:\n{context}\n\n"
        f"Prospect Role: {role}\n"
        f"Follow-Up Objective: {objective}\n"
        f"Tone: {tone}\n"
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
        st.markdown("### 🤝 Engagement Engine")

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
        model = st.selectbox("Drafting Model", PROVIDERS[provider]["models"])

        st.markdown("---")
        st.markdown("### 🎛️ Creativity Tuning")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.35, 0.05,
                                help="Higher values create more unique phrasing, lower values stick strictly to templates.")

        st.markdown("---")
        st.markdown("*SalesFollowAI Pro v1.0*")

    # Main Area
    st.markdown('<div class="header-title">SalesFollowAI Pro 🤝</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Generate high-converting, consultative follow-up messages tailored to prospect roles and past interactions.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 📝 Meeting Context")
        context = st.text_area("Previous Interaction Notes", height=150,
                               placeholder="e.g. Demo call discussing workflow automation use cases. They were specifically interested in API integrations and saving manual data entry hours.")
        
        role = st.text_input("👤 Prospect Role", placeholder="e.g. Director of Operations")

    with col2:
        st.markdown("#### 🎯 Outreach Strategy")
        objective = st.text_input("🏁 Follow-Up Objective", placeholder="e.g. Schedule next technical deep-dive")
        
        tone = st.selectbox("🎭 Message Tone",
                                 ["Professional and consultative", "Warm and enthusiastic",
                                  "Direct and action-oriented", "Educational and thought-provoking",
                                  "Casual and friendly"])
        
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡ Generate Sales Follow-Up", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()

        if not context.strip():
            st.warning("⚠️ Previous interaction context is required to draft an effective follow-up.")
            st.stop()

        with st.spinner(f"🤝 Drafting your follow-up via {model}..."):
            try:
                start_time = time.time()
                result = generate_draft(context, role, objective, tone,
                                        provider, api_key, model, temperature)
                delay = time.time() - start_time

                st.success(f"✨ Message Drafted! Generated in {delay:.2f}s")

                opening = result.get("opening", "")
                interaction = result.get("interaction_reference", "")
                value = result.get("value_reinforcement", "")
                cta = result.get("call_to_action", "")
                closing = result.get("closing", "")

                # --- Message Display ---
                st.markdown("### ✉️ Final Message Preview")
                
                st.markdown(f'<span class="tone-badge">{tone} Tone</span>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="message-preview">
                    <span class="section-label">Opening</span>
                    {opening}<br><br>
                    <span class="section-label">Context Check</span>
                    {interaction}<br><br>
                    <span class="section-label">Value Proposition</span>
                    {value}<br>
                    <div class="cta-highlight">
                        <span class="section-label" style="border:none; margin-top:0; padding:0;">Next Step</span>
                        {cta}
                    </div>
                    <span class="section-label">Closing</span>
                    {closing}
                </div>
                """, unsafe_allow_html=True)

                # --- Export ---
                st.markdown("---")
                st.markdown("### 💾 Export Message")

                full_email = f"{opening}\n\n{interaction}\n\n{value}\n\n{cta}\n\n{closing}"
                
                json_content = json.dumps(result, indent=2)

                exp_col1, exp_col2, exp_col3, _ = st.columns([1, 1, 1, 1])
                with exp_col1:
                    st.download_button("📧 Download As TXT", full_email,
                                       f"sales_followup_{date.today()}.txt", "text/plain")
                with exp_col2:
                    st.download_button("{ } Download RAW JSON", json_content,
                                       f"sales_followup_{date.today()}.json", "application/json")
                with exp_col3:
                    st.code(full_email, language="text")

            except Exception as e:
                import traceback
                st.error(f"❌ Message generation failed: {str(e)}")
                st.code(traceback.format_exc())

    st.markdown("---")
    st.caption("SalesFollowAI Pro • Powered by LiteLLM Multi-Provider Relay")

if __name__ == "__main__":
    main()
