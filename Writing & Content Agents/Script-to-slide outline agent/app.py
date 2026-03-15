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
    page_title="AI Presentation Architect Pro",
    page_icon="📽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #FAFAFD;
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
            border-color: #0D9488;
            box-shadow: 0 0 0 1px #0D9488;
        }
        .stButton button {
            border-radius: 8px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #0F766E 0%, #14B8A6 100%);
            color: white;
            border: none;
            padding: 0.6rem 1rem;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.4);
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
            margin-bottom: 30px;
        }
        .header-title {
            background: -webkit-linear-gradient(45deg, #0F766E, #2DD4BF);
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
            background-color: #F0FDFA;
            color: #0F766E;
            border: 1px solid #CCFBF1;
        }
        .slide-deck-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .slide-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-top: 5px solid #0D9488;
            padding: 24px;
            border-radius: 8px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        .slide-card:hover {
            border-color: #CBD5E1;
            box-shadow: 0 8px 15px -3px rgba(13, 148, 136, 0.15);
            transform: translateY(-3px);
        }
        .slide-number {
            color: #94A3B8;
            font-weight: 800;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        .slide-title {
            color: #0F172A;
            font-weight: 800;
            font-size: 1.25rem;
            margin-bottom: 15px;
            line-height: 1.3;
        }
        .slide-bullets {
            color: #334155;
            font-size: 1.05rem;
            line-height: 1.6;
            margin-top: auto;
        }
        .slide-bullets li {
            margin-bottom: 8px;
            padding-left: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite Enterprise Presentation & Slide Deck Architect. Your purpose is to ingest long-form speeches, scripts, or blogs, and effortlessly convert them into a structured, highly persuasive slide deck outline.

Rules:
- Transform the script into a visually digestible slide outline.
- Strictly allocate ONE main idea or narrative beat per slide. DO NOT overcrowd slides.
- Keep bullets extremely punchy and concise limit 5-7 words per bullet if possible.
- Do NOT include full sentences or paragraphs on the slides. The text on the slide supports the speaker's script, it doesn't replace it.
- Optimize the flow for a high-converting, professional, and visually engaging presentation.

Return ONLY valid JSON with this exact schema (no markdown formatting blocks):
{
  "analysis": "A brief internal thought on pacing, presentation arc, and cognitive load balancing across the slides.",
  "slides": [
    {
      "slide_number": 1,
      "title": "Clear, Punchy Slide Title",
      "bullets": ["Action-oriented bullet 1", "Data-driven bullet 2"]
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

def build_slides(script, context, provider, api_key, model, temp):
    prompt_text = (
        f"Input Script / Context Info: {context}\n\n"
        f"Full Underlying Script Data:\n{script}\n"
    )
    
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

    elif provider == "Anthropic (Claude)":
        if anthropic is None:
            raise RuntimeError("Anthropic is not installed.")
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            temperature=temp,
            max_tokens=3000
        )
        return extract_json(response.content[0].text)

    elif provider == "Google (Gemini)":
        if genai is None:
            raise RuntimeError("Google Generative AI is not installed.")
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
        st.markdown("### ⚙️ Architecture Engine")
        
        provider = st.selectbox("AI Logic Provider", ["OpenAI", "Anthropic (Claude)", "Google (Gemini)"])
        
        if provider == "OpenAI":
            api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
            available_models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
        elif provider == "Anthropic (Claude)":
            api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
            available_models = ["claude-3-5-haiku-20241022", "claude-3-5-sonnet-20240620", "claude-3-opus-20240229"]
        else:
            api_key = st.text_input("Google AI API Key", type="password", placeholder="AIza...")
            available_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
            
        st.markdown("---")
        st.markdown("### 🧠 Neural Processor")
        model = st.selectbox("Select Model", available_models)
        
        st.markdown("---")
        st.markdown("### 🎛️ Narration Variability")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.35, step=0.05)
        
        st.markdown("---")
        st.markdown("*" "Presentation Architect Pro v2.0" "*")

    # Main Area
    st.markdown('<div class="header-title">Presentation Architect Pro 📽️</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Cut the bloat. Convert dense scripts into visually striking, punchy slide decks to maximize audience impact.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### 1. Context & Pacing")
        context = st.text_area("Event / Presentation Context", placeholder="e.g. A 10-minute keynote to investors outlining our Q3 strategy.", height=150)
        
    with col2:
        st.markdown("#### 2. Raw Script Material")
        script = st.text_area("Full Speech, Script, or Blog Payload", height=150, placeholder="Paste the entire text you plan to speak, or the massive unorganized document here...")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("⚡ Synthesize Presentation Deck", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()
            
        if len(script.strip()) < 10:
            st.warning("⚠️ Please provide a substantial block of text or script to synthesize.")
            st.stop()

        with st.spinner(f"📽️ Analyzing narrative rhythm and mapping slides via {model}..."):
            try:
                start_time = time.time()
                result = build_slides(script, context, provider, api_key, model, temperature)
                delay = time.time() - start_time
                
                st.success(f"✨ Deck Architected! Compiled in {delay:.2f} seconds.")
                
                # --- Result Display ---
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<span class="provider-badge">Mapped via: {provider}</span>', unsafe_allow_html=True)
                
                with st.expander("🧠 Architect's Pacing Analysis", expanded=True):
                    st.info(result.get('analysis', 'No strategic analysis available.'))
                
                st.markdown("### Constructed Slide Deck")
                
                slides = result.get('slides', [])
                if not slides:
                    st.warning("No slides could be extracted.")
                else:
                    # Generate CSS Grid of Slide Cards
                    html_blocks = '<div class="slide-deck-container">'
                    for s in slides:
                        bullets_html = "".join([f"<li>{b}</li>" for b in s.get('bullets', [])])
                        html_blocks += f'''
                        <div class="slide-card">
                            <div class="slide-number">SLIDE {s.get("slide_number", "?")}</div>
                            <div class="slide-title">{s.get("title", "Untitled")}</div>
                            <ul class="slide-bullets">{bullets_html}</ul>
                        </div>
                        '''
                    html_blocks += "</div>"
                    st.markdown(html_blocks, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- Export Options ---
                st.markdown("### 💾 Export Slide Deck")
                
                exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 2])
                
                # Txt Format Generation
                txt_output = f"Presentation Slide Deck\n"
                txt_output += "=" * 30 + "\n\n"
                txt_output += f"Architect's Pacing Notes:\n{result.get('analysis', '')}\n\n"
                
                for s in slides:
                    txt_output += "-" * 30 + "\n"
                    txt_output += f"SLIDE {s.get('slide_number', '?')}\n"
                    txt_output += f"TITLE: {s.get('title', '')}\n"
                    for b in s.get("bullets", []):
                        txt_output += f"• {b}\n"
                    txt_output += "\n"
                
                json_content = json.dumps(result, indent=2)
                
                with exp_col1:
                    st.download_button(
                        label="📄 Download Formatted TXT",
                        data=txt_output,
                        file_name="slide_deck_outline.txt",
                        mime="text/plain"
                    )
                with exp_col2:
                    st.download_button(
                        label="{ } Download Raw JSON",
                        data=json_content,
                        file_name="slide_deck_outline.json",
                        mime="application/json"
                    )

            except Exception as e:
                import traceback
                st.error(f"❌ An error occurred with {provider}: {str(e)}")
                st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
