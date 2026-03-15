import streamlit as st
import json
import time
import re
from datetime import date

# Safely import AI providers
try:
    from openai import OpenAI, AuthenticationError
except ImportError:
    OpenAI = AuthenticationError = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# --- Page Configuration ---
st.set_page_config(
    page_title="AI FAQ Generator Pro",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #F8FAFC;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
            border-radius: 8px;
            border: 1px solid #CBD5E1;
            transition: all 0.3s ease;
            font-size: 15px;
            background-color: #FFFFFF;
            color: #0F172A;
        }
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #94A3B8;
            opacity: 1;
        }
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox > div > div:focus {
            border-color: #8B5CF6;
            box-shadow: 0 0 0 1px #8B5CF6;
        }
        .stButton button {
            border-radius: 8px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%);
            color: white;
            border: none;
            padding: 0.6rem 1rem;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.4);
            border: none;
            color: white;
        }
        .result-card {
            background: white;
            padding: 35px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #E2E8F0;
            margin-top: 15px;
            margin-bottom: 15px;
        }
        .header-title {
            background: -webkit-linear-gradient(45deg, #5B21B6, #8B5CF6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 3.5rem;
            letter-spacing: -1px;
            margin-bottom: 0px;
        }
        .header-subtitle {
            color: #64748B;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        .provider-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 20px;
            background-color: #F5F3FF;
            color: #6D28D9;
            border: 1px solid #DDD6FE;
        }
        .faq-box {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-left: 4px solid #8B5CF6;
            padding: 24px;
            border-radius: 8px;
            margin-bottom: 16px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .faq-box:hover {
            border-color: #C4B5FD;
            box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.1);
            transform: translateX(2px);
        }
        .question-text {
            color: #5B21B6;
            font-weight: 800;
            font-size: 1.15rem;
            margin-bottom: 12px;
            display: flex;
            align-items: flex-start;
            letter-spacing: -0.2px;
        }
        .question-text::before {
            content: "Q.";
            color: #8B5CF6;
            margin-right: 12px;
            font-weight: 900;
        }
        .answer-text {
            color: #334155;
            font-size: 1.05rem;
            line-height: 1.6;
            padding-left: 36px;
            margin-bottom: 0;
        }
        .answer-text::before {
            content: "A.";
            color: #A78BFA;
            margin-right: 12px;
            font-weight: 800;
            font-size: 1.05rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite Enterprise FAQ Generation Architect. Your exact purpose is to transform a simple list of product details and known user concerns into highly credible, transparent, and direct Frequently Asked Questions (FAQs).

Rules:
- Generate extraordinarily clear, relevant FAQs based on the provided product pipeline and target audience.
- Focus strictly on real user concerns, objections, and pain points.
- Completely avoid fluffy marketing language and sales hype. Don't sound like a salesman.
- Keep answers concise, honest, and highly helpful.
- Structure and format the language to build profound trust and reassure the buyer.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "analysis": "A brief internal thought on how to correctly answer the known concerns honestly but reassuringly.",
  "faqs": [
    {
      "question": "Clear user concern formatted as a conversational question",
      "answer": "Direct, honest, structured, and helpful answer"
    }
  ]
}
"""

def extract_json(text_response):
    try:
        return json.loads(text_response)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?(.*?)```", text_response, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        raise ValueError("Failed to parse output into JSON format")

def process_faq(product, audience, stage, tone, concerns, provider, api_key, model, temp):
    prompt_text = (
        f"Product: {product}\n"
        f"Audience: {audience}\n"
        f"Stage: {stage}\n"
        f"Tone: {tone}\n"
        f"Known Concerns:\n{concerns}\n"
    )
    
    # 1. OpenAI Logic
    if provider == "OpenAI":
        if OpenAI is None:
            raise RuntimeError("OpenAI is not installed. Run `pip install openai`.")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=temp,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    # 2. Anthropic Logic
    elif provider == "Anthropic (Claude)":
        if anthropic is None:
            raise RuntimeError("Anthropic is not installed. Run `pip install anthropic`.")
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            temperature=temp,
            max_tokens=2048
        )
        return extract_json(response.content[0].text)

    # 3. Google Logic (Gemini)
    elif provider == "Google (Gemini)":
        if genai is None:
            raise RuntimeError("Google Generative AI is not installed. Run `pip install google-generativeai`.")
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(
            model_name=model,
            system_instruction=SYSTEM_PROMPT
        )
        response = gemini_model.generate_content(
            prompt_text,
            generation_config=genai.types.GenerationConfig(
                temperature=temp,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)

# --- UI Layout ---
def main():
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Engine Settings")
        
        provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic (Claude)", "Google (Gemini)"])
        
        if provider == "OpenAI":
            api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
            available_models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
        elif provider == "Anthropic (Claude)":
            api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
            available_models = ["claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"]
        else:
            api_key = st.text_input("Google AI API Key", type="password", placeholder="AIza...")
            available_models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp"]
            
        st.markdown("---")
        st.markdown("### 🧠 AI Model")
        model = st.selectbox("Select Model", available_models)
        
        st.markdown("---")
        st.markdown("### 🎛️ Creativity")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.35, step=0.05, help="Low creativity prevents the AI from turning the answers into marketing fluff.")
        
        st.markdown("---")
        st.markdown("*" "AI FAQ Generator Pro v1.0" "*")

    # Main Area
    st.markdown('<div class="header-title">AI FAQ Generator Pro 💬</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Instantly generate transparent, direct, and highly credible FAQs that annihilate buyer objections.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        product_name = st.text_input("📦 Product or Service", placeholder="e.g. AI Agent Productivity Course")
        audience = st.text_input("👥 Target Audience", placeholder="e.g. B2B Founders, Beginners")
        stage = st.selectbox("📍 Customer Journey Stage", ["Pre-purchase", "Post-purchase / Onboarding", "Retention", "SaaS Implementation"])
        tone = st.text_input("🎭 Voice & Tone", value="Clear, professional, and reassuring")
    
    with col2:
        concerns = st.text_area("😟 Known User Concerns & Objections", height=150, placeholder="- Do I need prior experience?\n- Is it fully automated or theoretical?\n- How much time does it take per week?")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("⚡ Synthesize Objection-Handling FAQs", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()
            
        if not product_name.strip() or not concerns.strip():
            st.warning("⚠️ Product Name and Known Concerns are required to generate an accurate FAQ base.")
            st.stop()

        with st.spinner(f"💬 Analyzing objections and drafting credible answers via {model}..."):
            try:
                start_time = time.time()
                result = process_faq(product_name, audience, stage, tone, concerns, provider, api_key, model, temperature)
                delay = time.time() - start_time
                
                st.success(f"✨ FAQ Database Built! Analyzed in {delay:.2f} seconds.")
                
                # --- Result Display ---
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<span class="provider-badge">Logic Engine: {provider}</span>', unsafe_allow_html=True)
                
                with st.expander("🧠 QA Strategist Thought Process", expanded=True):
                    st.info(result.get('analysis', 'No strategic analysis available.'))
                
                st.markdown("### Frequently Asked Questions")
                st.markdown("<br>", unsafe_allow_html=True)

                raw_faqs = result.get('faqs', [])
                if not raw_faqs:
                    st.warning("No FAQs could be mapped.")
                else:
                    for faq in raw_faqs:
                        st.markdown(f"""
                        <div class="faq-box">
                            <div class="question-text">{faq.get('question', 'Unknown Question')}</div>
                            <div class="answer-text">{faq.get('answer', 'No answer provided.')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- Export Options ---
                st.markdown("### 💾 Export Database")
                
                exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 2])
                
                # Txt Format Generation
                txt_output = f"FAQ Database for {product_name}\n"
                txt_output += "=" * (18 + len(product_name)) + "\n\n"
                txt_output += f"Strategist Logic:\n{result.get('analysis', '')}\n\n"
                
                for faq in raw_faqs:
                    txt_output += f"Q: {faq.get('question', '')}\n"
                    txt_output += f"A: {faq.get('answer', '')}\n\n"
                
                json_content = json.dumps(result, indent=2)
                
                with exp_col1:
                    st.download_button(
                        label="📄 Download Formatted TXT",
                        data=txt_output,
                        file_name=f"faqs_{product_name.replace(' ','_')}.txt",
                        mime="text/plain"
                    )
                with exp_col2:
                    st.download_button(
                        label="{ } Download Raw JSON",
                        data=json_content,
                        file_name=f"faqs_{product_name.replace(' ','_')}.json",
                        mime="application/json"
                    )

            except Exception as e:
                import traceback
                st.error(f"❌ An error occurred with {provider}: {str(e)}")
                st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
