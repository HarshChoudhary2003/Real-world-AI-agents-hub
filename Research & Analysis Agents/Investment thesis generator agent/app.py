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
    page_title="CapitalMind | Investment Thesis Generator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #f1f5f9 !important;
    }
    
    .main {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.6rem;
        border-radius: 8px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        box-shadow: 0 4px 15px rgba(217, 119, 6, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(217, 119, 6, 0.5);
        border: none;
    }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
    }
    
    .thesis-metric {
        background: rgba(245, 158, 11, 0.05);
        border-right: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-size: 1.1rem;
    }
    
    .badge-gold {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        background: rgba(245, 158, 11, 0.1);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.2);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Global Client
client = None

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/money-bag.png", width=120)
    st.title("Settings")
    
    provider = st.selectbox("Intelligence Provider", ["OpenAI", "Groq", "Anthropic", "Local (Ollama)"])
    model_id = st.text_input("Model ID", value="gpt-4o-mini")
    api_key_input = st.text_input("API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    
    if api_key_input:
        client = OpenAI(api_key=api_key_input)
        if provider == "Groq":
            client.base_url = "https://api.groq.com/openai/v1"
        elif provider == "Local (Ollama)":
            client.base_url = "http://localhost:11434/v1"
            client.api_key = "ollama"

    st.markdown("---")
    st.info("""
    **Analytical Frameworks:**
    - First-Principles Synthesis
    - Risk-Adjusted Forecasting
    - Macro-Micro Logic Mapping
    - Multi-Catalyst Detection
    """)

# Helper
def generate_thesis_ai(context):
    SYSTEM_PROMPT = """
    You are an Investment Thesis Generator Agent.
    Rules:
    - Build structured, analytical theses.
    - Separate rationale, catalysts, and risks.
    - Neutral, evidence-driven tone.
    - Return JSON ONLY.
    """
    
    schema = {
        "thesis_summary": "Core summary",
        "rationale": "Logical bridge",
        "catalysts": ["catalyst 1", "catalyst 2"],
        "risks": ["risk 1", "risk 2"],
        "conclusion": "Final synthesis"
    }

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\nReturn JSON matching schema: {json.dumps(schema)}"},
                {"role": "user", "content": context}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Execution Error: {str(e)}")
        return None

# Main UI
st.title("💰 CapitalMind: Thesis Architecture")
st.markdown("<p style='font-size:1.2rem; color:#94a3b8;'>Formulating high-conviction, evidence-driven investment frameworks with neural intelligence.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([0.45, 0.55], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🎯 Investment Context")
    
    asset = st.text_input("Target Asset/Company", placeholder="e.g., SpaceX, Ethereum, NVIDIA")
    sector = st.selectbox("Primary Sector", ["Artificial Intelligence", "SaaS", "Biotech", "Green Tech", "Crypto/Web3", "Semiconductors", "Consumer Tech", "Other"])
    horizon = st.select_slider("Investment Horizon", options=["1 Year", "2 Years", "3-5 Years", "5-10 Years", "Indefinite"])
    
    assumptions = st.text_area("Key Assumptions & Inputs", height=200, placeholder="Define the core beliefs driving this investment...")
    
    input_text = f"Asset: {asset}\nSector: {sector}\nHorizon: {horizon}\nContext: {assumptions}"
    
    if st.button("🚀 Architect Thesis"):
        if not asset or not assumptions:
            st.warning("Please define asset and context.")
        elif not client:
            st.error("API Key required.")
        else:
            with st.spinner("Synthesizing market signals..."):
                result = generate_thesis_ai(input_text)
                if result:
                    st.session_state['thesis_result'] = result
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if 'thesis_result' in st.session_state:
        data = st.session_state['thesis_result']
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='badge-gold'>CONFIRMED THESIS - {date.today()}</div>", unsafe_allow_html=True)
        
        st.subheader("📝 Executive Summary")
        st.write(data.get("thesis_summary", "N/A"))
        
        st.subheader("🏛️ Core Rationale")
        st.markdown(f"<div class='thesis-metric'>{data.get('rationale', 'N/A')}</div>", unsafe_allow_html=True)
        
        t1, t2 = st.tabs(["🚀 Catalysts", "🛡️ Risk Matrix"])
        
        with t1:
            for cat in data.get("catalysts", []):
                st.markdown(f"• **{cat}**")
        
        with t2:
            for risk in data.get("risks", []):
                st.error(risk)
                
        st.markdown("---")
        st.subheader("🏁 Strategic Conclusion")
        st.info(data.get("conclusion", "N/A"))
        
        st.markdown("---")
        st.markdown("### 📥 Extract Intelligence")
        e_col1, e_col2 = st.columns(2)
        
        json_out = json.dumps(data, indent=2)
        e_col1.download_button("Download JSON", json_out, "investment_thesis.json")
        
        txt_out = f"Investment Thesis Report: {asset}\n" + "="*50 + "\n\n"
        txt_out += f"Summary: {data.get('thesis_summary')}\n\nRationale: {data.get('rationale')}\n\n"
        txt_out += "Catalysts:\n" + "\n".join([f"- {c}" for c in data.get('catalysts', [])]) + "\n\n"
        txt_out += "Risks:\n" + "\n".join([f"- {r}" for r in data.get('risks', [])]) + "\n\n"
        txt_out += f"Conclusion: {data.get('conclusion')}"
        
        e_col2.download_button("Download Report", txt_out, "investment_thesis.txt")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 500px; color: #64748b; border: 2px dashed rgba(255,255,255,0.05); border-radius: 16px;'>
            <img src='https://img.icons8.com/clouds/200/bullish.png' width='100' style='opacity: 0.2;'/>
            <p style='margin-top: 20px;'>Intelligence report will be rendered upon architectural synthesis.</p>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh Choudhary")
