import streamlit as st
import json
import time
import re
from datetime import date

# Safely import AI providers so the app doesn't crash if one is missing
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
    page_title="AI Tone Alchemist Pro",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #FAFAFD;
        }
        .stTextArea textarea {
            border-radius: 12px;
            border: 2px solid #E2E8F0;
            transition: border-color 0.3s ease;
            font-size: 16px;
        }
        .stTextArea textarea:focus {
            border-color: #6366F1;
            box-shadow: 0 0 0 1px #6366F1;
        }
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            border: none;
            color: white;
        }
        .result-card {
            background: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            border: 1px solid #F1F5F9;
            margin-top: 10px;
        }
        .header-title {
            background: -webkit-linear-gradient(45deg, #4f46e5, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem;
        }
        .provider-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 8px;
            background-color: #EEF2FF;
            color: #4F46E5;
        }
    </style>
""", unsafe_allow_html=True)

# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite Enterprise Tone Rewriting Architect. Your absolute sole purpose is to flawlessly rewrite text into a given target tone, while maintaining 100% semantic equivalence to the original message.

CRITICAL DIRECTIVES:
1. SEMANTIC FIDELITY: You must preserve EVERY original fact, constraint, and nuanced meaning. Do NOT hallucinate, infer, or inject new information whatsoever.
2. TONE PRECISION: Immerse the rewriting entirely in the requested target tone. Calibrate vocabulary, sentence structure, and pacing to match flawlessly.
3. ZERO FLUFF: Eliminate robotic AI clichés (e.g., "In conclusion", "It is important to remember"). Ensure the output flows naturally as if written by a world-class human copywriter.
4. NO OMISSIONS: Do not drop any original detail, no matter how small or seemingly insignificant.

Return ONLY valid JSON with this exact schema (no markdown formatting other than the JSON block):
{
  "analysis": "A brief 1-sentence internal thought process on how you bridged the original meaning to the target tone without losing facts.",
  "rewritten_text": "The final flawless rewritten text.",
  "tone_applied": "The exact tone you successfully applied."
}
"""

def extract_json(text_response):
    """Fallback utility to extract JSON from markdown wrappers if models don't return raw JSON"""
    try:
        # First attempt: parse raw text
        return json.loads(text_response)
    except json.JSONDecodeError:
        # Second attempt: find JSON block using regex
        match = re.search(r"```(?:json)?(.*?)```", text_response, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        raise ValueError("Failed to parse output into JSON context")

def process_rewrite(text, target_tone, provider, api_key, model, temp):
    prompt_with_tone = f"Target Tone: {target_tone}\n\nOriginal Text:\n{text}"
    
    # 1. OpenAI Logic
    if provider == "OpenAI":
        if OpenAI is None:
            raise RuntimeError("OpenAI is not installed. Run `pip install openai`.")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_with_tone}
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
                {"role": "user", "content": prompt_with_tone}
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
            prompt_with_tone,
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
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1, 
                              help="Higher values make the output more creative, lower values make it more focused.")
        
        st.markdown("---")
        st.markdown("*" "AI Tone Alchemist Pro v2.0.0" "*")

    # Main Area
    st.markdown('<h1 class="header-title">AI Tone Alchemist Pro 🎭</h1>', unsafe_allow_html=True)
    st.markdown("Transform your content instantly into any desired tone while preserving the core message. Perfect for enterprise communications, marketing drafts, and sensitive emails.")
    
    st.markdown("### 📝 Original Content")
    original_text = st.text_area("Paste your text here:", height=150, placeholder="Example: I need this task done by tomorrow. This delay is causing problems.", label_visibility="collapsed")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 Target Tone")
        predefined_tone = st.selectbox("Choose a preset tone:", [
            "Professional and Calm",
            "Empathetic and Supportive",
            "Authoritative and Direct",
            "Persuasive and Enthusiastic",
            "Friendly and Casual",
            "Diplomatic and Polite",
            "Humorous and Witty",
            "Custom"
        ], label_visibility="collapsed")
    
    with col2:
        if predefined_tone == "Custom":
            st.markdown("### ✍️ Custom Tone")
            target_tone = st.text_input("Enter your custom tone:", placeholder="e.g., Pirate, Shakespearean, Gen Z slang", label_visibility="collapsed")
        else:
            st.markdown("### ✨ Selected Tone")
            target_tone = predefined_tone
            st.text_input("Selected tone:", disabled=True, value=target_tone, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✨ Transform Tone", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()
            
        if not original_text.strip():
            st.warning("⚠️ Please provide some text to rewrite.")
            st.stop()
            
        if not target_tone.strip():
            st.warning("⚠️ Please specify a target tone.")
            st.stop()

        with st.spinner(f"🔮 Alchemizing your text using {model}..."):
            try:
                start_time = time.time()
                result = process_rewrite(original_text, target_tone, provider, api_key, model, temperature)
                end_time = time.time()
                
                delay = end_time - start_time
                
                st.success(f"✨ Rewriting complete! (Took {delay:.2f}s)")
                
                # Display Results
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<span class="provider-badge">Powered by {provider}</span>', unsafe_allow_html=True)
                
                with st.expander("🧠 AI Thought Process", expanded=False):
                    st.caption(f"_{result.get('analysis', 'Analysis not available.')}_")
                
                st.markdown("#### 🌟 Rewritten Text")
                st.info(result['rewritten_text'])
                
                st.markdown("#### 🎭 Applied Tone")
                st.caption(f"_{result['tone_applied']}_")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Export Options
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 💾 Export Results")
                
                exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 2])
                
                # Setup files for download
                txt_content = f"Tone-Rewritten Text ({date.today()})\nPowered by: {provider} ({model})\n{'=' * 45}\nOriginal Tone Objective: {target_tone}\n\n{result['rewritten_text']}"
                json_content = json.dumps(result, indent=2)
                
                with exp_col1:
                    st.download_button(
                        label="📄 Download TXT",
                        data=txt_content,
                        file_name=f"rewritten_{date.today()}.txt",
                        mime="text/plain"
                    )
                with exp_col2:
                    st.download_button(
                        label="{ } Download JSON",
                        data=json_content,
                        file_name=f"rewritten_{date.today()}.json",
                        mime="application/json"
                    )
                    
            except Exception as e:
                st.error(f"❌ An error occurred with {provider}: {str(e)}")

if __name__ == "__main__":
    main()
