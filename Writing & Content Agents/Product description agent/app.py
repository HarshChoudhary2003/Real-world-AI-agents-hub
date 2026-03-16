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
    page_title="Product Copywriter Pro",
    page_icon="✍️",
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
            border-color: #2563EB;
            box-shadow: 0 0 0 1px #2563EB;
        }
        .stButton button {
            border-radius: 8px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #1E40AF 0%, #2563EB 100%);
            color: white;
            border: none;
            padding: 0.6rem 1rem;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
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
            background: -webkit-linear-gradient(45deg, #1E3A8A, #3B82F6);
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
            background-color: #EFF6FF;
            color: #1E40AF;
            border: 1px solid #BFDBFE;
        }
        .benefit-chip {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            padding: 12px 18px;
            border-radius: 8px;
            margin-bottom: 12px;
            font-size: 15px;
            display: flex;
            align-items: center;
            color: #334155;
            transition: all 0.2s ease;
        }
        .benefit-chip:hover {
            border-color: #CBD5E1;
            background: #FFFFFF;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .benefit-chip::before {
            content: '✔️';
            margin-right: 12px;
            color: #2563EB;
        }
        .cta-box {
            background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            font-weight: 800;
            font-size: 1.3rem;
            color: #FFFFFF;
            margin-top: 30px;
            box-shadow: 0 4px 6px -1px rgba(30, 58, 138, 0.4);
            letter-spacing: 0.5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite Enterprise Product Description Architect and Conversion Copywriter. Your exact purpose is to transform a simple list of product details into a high-converting, benefit-driven product description.

Rules:
- Write clear, incredibly persuasive, benefit-driven product descriptions.
- Expertly map every provided feature to a tangible real-world outcome for the user.
- Avoid all hype, exaggeration, or unsupported magic claims.
- Adapt your tone perfectly to the target audience requested.
- Make the reading experience highly scannable and professional.

Return ONLY valid JSON with this exact schema (no markdown blocks around it):
{
  "analysis": "A brief internal thought on how to correctly map these specific features to this specific audience's pain points.",
  "product_name": "The Product Name (Polished if needed)",
  "description": "A compelling 2-3 paragraph primary product description.",
  "key_benefits": ["Tangible Benefit 1", "Tangible Benefit 2", "Tangible Benefit 3"],
  "ideal_for": "A short, precise description of the ideal buyer avatar.",
  "cta": "A powerful, actionable Call to Action (CTA) phrase."
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

def process_description(product_name, category, audience, features, use_case, tone, provider, api_key, model, temp):
    prompt_text = (
        f"Product Name: {product_name}\n"
        f"Category: {category}\n"
        f"Audience: {audience}\n"
        f"Core Features:\n{features}\n"
        f"Primary Use Case:\n{use_case}\n"
        f"Tone: {tone}\n"
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
        st.markdown("### ⚙️ Copywriter Engine")
        
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
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.4, step=0.1)
        
        st.markdown("---")
        st.markdown("*" "Product Copywriter Pro v3.0" "*")

    # Main Area
    st.markdown('<div class="header-title">Product Copywriter Pro ✍️</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Transform basic product specs into high-converting, benefit-driven product page copy instantly.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        product_name = st.text_input("🏷️ Product Name", placeholder="e.g. AI Agent Productivity Course")
        category = st.selectbox("📁 Category", ["Online Education", "SaaS Software", "E-commerce Product", "Consulting Service", "B2B Hardware"])
        audience = st.text_input("👥 Target Audience", placeholder="e.g. Professionals and Founders")
        tone = st.selectbox("🎭 Tone of Voice", ["Professional and Confident", "Energetic and Exciting", "Authoritative and Direct", "Friendly and Approachable", "Luxury and Exclusive"])
    
    with col2:
        features = st.text_area("✨ Core Features (One per line)", height=100, placeholder="- 100 hands-on AI agent projects\n- No prerequisites\n- Practical, real-world focus")
        use_case = st.text_area("🌟 Primary Use Case", height=100, placeholder="Help learners apply AI agents to daily work to save 10+ hours a week.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("⚡ Generate High-Converting Copy", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()
            
        if not product_name.strip() or not features.strip():
            st.warning("⚠️ Product Name and Core Features are required to generate copy.")
            st.stop()

        with st.spinner(f"✍️ Architecting value propositions via {model}..."):
            try:
                start_time = time.time()
                result = process_description(product_name, category, audience, features, use_case, tone, provider, api_key, model, temperature)
                delay = time.time() - start_time
                
                st.success(f"✨ Copywriting Complete! Generated in {delay:.2f} seconds.")
                
                # --- Result Display ---
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<span class="provider-badge">Written with: {provider}</span>', unsafe_allow_html=True)
                
                with st.expander("🧠 Copywriter's Analysis", expanded=False):
                    st.info(result.get('analysis', 'No strategic analysis available.'))
                
                # Title
                st.markdown(f"<h2>{result.get('product_name', product_name)}</h2>", unsafe_allow_html=True)
                
                # Primary Description
                st.markdown(f"**The Pitch:**\n\n{result.get('description', '')}")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Key Benefits
                st.markdown("#### The Benefits")
                for benefit in result.get('key_benefits', []):
                    st.markdown(f'<div class="benefit-chip">{benefit}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Ideal For
                st.markdown(f"**Ideal For:** _{result.get('ideal_for', '')}_")
                
                # CTA
                st.markdown(f'<div class="cta-box">{result.get("cta", "")}</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- Export Options ---
                st.markdown("### 💾 Export Copy")
                
                exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 2])
                
                # Txt Format Generation
                txt_output = f"{result.get('product_name', product_name)}\n"
                txt_output += "=" * 45 + "\n\n"
                txt_output += f"Copywriter Analysis:\n{result.get('analysis', '')}\n\n"
                txt_output += f"Description:\n{result.get('description', '')}\n\n"
                txt_output += "Key Benefits:\n"
                for b in result.get('key_benefits', []):
                    txt_output += f"- {b}\n"
                txt_output += f"\nIdeal For:\n{result.get('ideal_for', '')}\n\n"
                txt_output += f"Call To Action:\n{result.get('cta', '')}\n"
                
                json_content = json.dumps(result, indent=2)
                
                with exp_col1:
                    st.download_button(
                        label="📄 Download TXT Draft",
                        data=txt_output,
                        file_name=f"product_copy_{product_name.replace(' ','_')}.txt",
                        mime="text/plain"
                    )
                with exp_col2:
                    st.download_button(
                        label="{ } Download JSON Payload",
                        data=json_content,
                        file_name=f"product_copy_{product_name.replace(' ','_')}.json",
                        mime="application/json"
                    )

            except Exception as e:
                import traceback
                st.error(f"❌ An error occurred with {provider}: {str(e)}")
                st.code(traceback.format_exc())

if __name__ == "__main__":
    main()


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
