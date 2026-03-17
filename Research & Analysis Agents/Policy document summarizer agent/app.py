import streamlit as st
import json
from openai import OpenAI
from datetime import date
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="PolicyGuard | AI Policy Summarizer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
        color: #f0fdf4;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.4);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .policy-box {
        background: rgba(16, 185, 129, 0.05);
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    
    h1, h2, h3 {
        color: #ecfdf5 !important;
        letter-spacing: -0.02em;
    }
    
    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.2) !important;
        color: #ecfdf5 !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-size: 1rem;
    }
    
    .metric-label {
        color: #a7f3d0;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Global client initialization
client = None

# Sidebar Content
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/law.png", width=120)
    st.title("Admin Console")
    
    provider = st.selectbox("Intelligence Engine", ["OpenAI", "Groq", "OpenRouter", "DeepSeek", "Local (Ollama)"])
    
    base_urls = {
        "OpenAI": "https://api.openai.com/v1",
        "Groq": "https://api.groq.com/openai/v1",
        "OpenRouter": "https://openrouter.ai/api/v1",
        "DeepSeek": "https://api.deepseek.com",
        "Local (Ollama)": "http://localhost:11434/v1"
    }
    
    default_models = {
        "OpenAI": "gpt-4o-mini",
        "Groq": "mixtral-8x7b-32768",
        "OpenRouter": "anthropic/claude-3-haiku",
        "DeepSeek": "deepseek-chat",
        "Local (Ollama)": "llama3"
    }

    selected_base_url = base_urls.get(provider)
    model_id = st.text_input("Model Signature", value=default_models.get(provider, "gpt-4o-mini"))
    api_key_input = st.text_input("Access Secret", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    
    if api_key_input or provider == "Local (Ollama)":
        client = OpenAI(
            api_key=api_key_input if api_key_input else "nothing",
            base_url=selected_base_url
        )
    
    st.markdown("---")
    st.info("""
    **PolicyGuard Features:**
    - Legal-Intent Preservation
    - Objective Summarization
    - Ambiguity Detection
    - Stakeholder Mapping
    """)

# Helper Function
def summarize_policy_ai(text):
    SYSTEM_PROMPT = """
    You are a Policy Document Summarizer Agent.
    Rules:
    - Summarize clearly and neutrally.
    - Preserve regulatory intent.
    - Avoid advice or subjective interpretation.
    - Highlight scope and obligations.
    - Return JSON ONLY.
    """
    
    schema = {
        "overview": "Brief summary of purpose",
        "scope": "Target entities and data types",
        "key_requirements": ["list", "of", "obligations"],
        "implications": ["list", "of", "consequences"],
        "limitations_or_ambiguities": ["unclear", "sections"]
    }

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\nReturn only valid JSON matching this schema: {json.dumps(schema)}"},
                {"role": "user", "content": text}
            ],
            temperature=0.25,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Engine Fault: {str(e)}")
        return None

# Main UI Integration
st.title("⚖️ PolicyGuard: Regulatory Intelligence")
st.markdown("<p style='font-size:1.2rem; color:#a7f3d0; opacity:0.8;'>Precise thematic synthesis for enterprise policies and regulatory frameworks.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([0.45, 0.55], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📜 Document Input")
    
    input_mode = st.radio("Input Vector", ["Manual Text Entry", "Sample Framework"])
    
    default_text = ""
    if input_mode == "Sample Framework":
        default_text = """Policy Title: Global Remote Work Policy
Jurisdiction: International Operations
Text: This policy governs the terms of remote work for all full-time employees. Employees must maintain a core availability window of 10 AM to 4 PM EST. Secure VPN usage is mandatory. The company reserves the right to terminate remote arrangements with 30 days' notice. Home office expenses are reimbursed up to $500 annually upon submission of valid receipts."""

    policy_input = st.text_area("Policy Context / Regulation Text", value=default_text, height=350, placeholder="Paste policy text here...")
    
    if st.button("🔍 Synthesize Policy"):
        if not policy_input.strip():
            st.warning("Input required for synthesis.")
        elif not client:
            st.error("API Key required to initialize engine.")
        else:
            with st.spinner("Decoding regulatory intent..."):
                result = summarize_policy_ai(policy_input)
                if result:
                    st.session_state['policy_result'] = result
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if 'policy_result' in st.session_state:
        data = st.session_state['policy_result']
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Synthesis Report")
        
        st.markdown("<p class='metric-label'>CORE PURPOSE</p>", unsafe_allow_html=True)
        st.write(data.get("overview", "N/A"))
        
        st.markdown("<p class='metric-label'>APPLICABLE SCOPE</p>", unsafe_allow_html=True)
        st.info(data.get("scope", "N/A"))
        
        tab1, tab2, tab3 = st.tabs(["📋 Obligations", "⚖️ Implications", "🚩 Risks/Gaps"])
        
        with tab1:
            for req in data.get("key_requirements", []):
                st.markdown(f"<div class='policy-box'>• {req}</div>", unsafe_allow_html=True)
        
        with tab2:
            for impl in data.get("implications", []):
                st.markdown(f"• {impl}")
        
        with tab3:
            for limit in data.get("limitations_or_ambiguities", []):
                st.warning(limit)
        
        st.markdown("---")
        st.markdown("### 📥 Extract Intelligence")
        e_col1, e_col2 = st.columns(2)
        
        json_dump = json.dumps(data, indent=2)
        e_col1.download_button("Download JSON", json_dump, "policy_summary.json")
        
        txt_output = f"Policy Intelligence Report - {date.today()}\n" + "="*50 + "\n\n"
        txt_output += f"Overview: {data.get('overview')}\n\nScope: {data.get('scope')}\n\nRequirements:\n"
        txt_output += "\n".join([f"- {r}" for r in data.get('key_requirements', [])])
        
        e_col2.download_button("Download Report", txt_output, "policy_summary.txt")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 500px; color: #a7f3d0; border: 2px dashed rgba(16,185,129,0.2); border-radius: 24px;'>
            <img src='https://img.icons8.com/clouds/200/law.png' width='100' style='opacity: 0.3;'/>
            <p style='margin-top: 20px; font-weight: 300;'>Analytic report will be rendered upon synthesis.</p>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.caption("Engineered by Harsh")
