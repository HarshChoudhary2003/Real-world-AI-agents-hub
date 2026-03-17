import streamlit as st
import json
from openai import OpenAI
from datetime import date
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="PolicyGuard Ultra | Advanced Regulatory Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Hyper-Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;600;700&display=swap');
    
    :root {
        --primary-emerald: #10b981;
        --deep-forest: #064e3b;
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 0% 0%, #064e3b 0%, #022c22 100%);
        color: #ecfdf5;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        background: linear-gradient(90deg, #34d399 0%, #a7f3d0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.6rem;
        border-radius: 14px;
        font-weight: 600;
        letter-spacing: 0.02em;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }

    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 25px rgba(16, 185, 129, 0.4);
        color: white;
    }

    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 28px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        transition: border 0.3s ease;
    }
    
    .glass-card:hover {
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .obligation-box {
        background: rgba(16, 185, 129, 0.08);
        border-left: 5px solid #10b981;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.95rem;
    }

    .metric-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        padding: 0.4rem 1rem;
        border-radius: 100px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .risk-high { color: #ef4444; font-weight: 700; }
    .risk-medium { color: #f59e0b; font-weight: 700; }
    .risk-low { color: #10b981; font-weight: 700; }

    .stTextArea textarea {
        background: rgba(0, 0, 0, 0.3) !important;
        color: #ecfdf5 !important;
        border-radius: 18px !important;
        border: 1px solid var(--glass-border) !important;
        padding: 1rem !important;
    }

    .sidebar-brand {
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Global Client
client = None

# Sidebar Content
with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <img src='https://img.icons8.com/clouds/200/law.png' width='120'/>
        <h2 style='font-size: 1.5rem;'>PolicyGuard Ultra</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("Neural Engine")
    provider = st.selectbox("Intelligence Vector", ["OpenAI", "Groq", "OpenRouter", "DeepSeek", "Ollama"])
    model_id = st.text_input("Intelligence Signature", value="gpt-4o")
    api_key_input = st.text_input("Neural Access Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    
    if api_key_input:
        client = OpenAI(api_key=api_key_input)
        if provider == "Groq": client.base_url = "https://api.groq.com/openai/v1"
        if provider == "OpenRouter": client.base_url = "https://openrouter.ai/api/v1"
    
    st.markdown("---")
    st.markdown("### 🧬 Advanced Capabilities")
    st.info("""
    - **Deep Risk Quantification**
    - **Strategic Impact Mapping**
    - **Stakeholder DNA Audit**
    - **Ambiguity Indexing**
    """)

def analyze_policy_ultra(text):
    SYSTEM_PROMPT = """
    You are an Advanced Policy Intelligence Agent. Deconstruct documents into structured intelligence.
    Schema:
    {
      "metadata": {"title": "", "jurisdiction": "", "date": "", "issuer": ""},
      "summary": {"overview": "", "scope": ""},
      "framework": {"obligations": [], "stakeholders": [], "deadlines": []},
      "risk": {"level": "High|Medium|Low", "score": 0-100, "threats": [], "ambiguities": []},
      "strategy": ["Impact 1", "Impact 2"]
    }
    Rules: Objective, Neutral, JSON ONLY.
    """
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Engine Failure: {str(e)}")
        return None

# Main UI
st.title("⚖️ PolicyGuard Ultra: Advanced Synthesis")
st.markdown("<p style='font-size:1.2rem; color:#a7f3d0; opacity:0.7;'>High-fidelity neural deconstruction of regulatory frameworks and enterprise policies.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([0.4, 0.6], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📡 Intelligence Ingestion")
    
    sample_text = """Policy Title: Enterprise Data Governance Framework
Jurisdiction: United States & European Union (GDPR overlap)
Effective Date: Q3 2026
Issuer: Global Security & Compliance Office

Text: This framework mandates the classification of all internal and external data. 'Level 4' datasets (highly sensitive) must be encrypted using AES-256 and stored exclusively on sovereign clouds within their jurisdiction. Employees must undergo biannual training. Non-compliance results in a temporary suspension of access and potential audits. The definition of 'highly sensitive' remains subject to the CISO's discretion, which may change quarterly based on the threat landscape."""

    policy_input = st.text_area("Regulatory Source / Policy Text", value=sample_text, height=450)
    
    if st.button("🧠 Synthesize Intelligence"):
        if not policy_input.strip():
            st.warning("Input required.")
        elif not client:
            st.error("Neural Access Key missing.")
        else:
            with st.spinner("Executing deep neural synthesis..."):
                intel = analyze_policy_ultra(policy_input)
                if intel:
                    st.session_state['intel'] = intel
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if 'intel' in st.session_state:
        data = st.session_state['intel']
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # Metadata Header
        m = data['metadata']
        st.subheader(f"🛡️ Report: {m.get('title', 'Unknown Policy')}")
        st.markdown(f"<span class='metric-badge'>{m.get('issuer')}</span> <span class='metric-badge'>{m.get('jurisdiction')}</span>", unsafe_allow_html=True)
        
        # Summary
        st.markdown("#### 📝 Executive Digest")
        st.write(data['summary']['overview'])
        
        # Risk Visualization
        st.markdown("---")
        risk_col, score_col = st.columns(2)
        with risk_col:
            risk_level = data['risk']['level']
            color = "#ef4444" if risk_level == "High" else "#f59e0b" if risk_level == "Medium" else "#10b981"
            st.markdown(f"#### Risk Profile: <span style='color:{color}'>{risk_level}</span>", unsafe_allow_html=True)
            for threat in data['risk']['threats']:
                st.markdown(f"• {threat}")
        
        with score_col:
            score = data['risk']['score']
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                title = {'text': "Compliance Risk Score", 'font': {'color': "#34d399", 'size': 16}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': "#34d399"},
                    'bar': {'color': "#10b981"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "rgba(255,255,255,0.1)",
                    'steps': [
                        {'range': [0, 40], 'color': "rgba(16, 185, 129, 0.1)"},
                        {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.1)"},
                        {'range': [70, 100], 'color': "rgba(239, 68, 68, 0.1)"}]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        # Tabs for Deep Dive
        tab1, tab2, tab3 = st.tabs(["📋 Obligations", "👥 Stakeholders", "🚩 Ambiguities"])
        
        with tab1:
            for obs in data['framework']['obligations']:
                st.markdown(f"<div class='obligation-box'>{obs}</div>", unsafe_allow_html=True)
        
        with tab2:
            st.write("Applicable Entities & Roles")
            for person in data['framework']['stakeholders']:
                st.info(person)
        
        with tab3:
            if data['risk']['ambiguities']:
                for amb in data['risk']['ambiguities']:
                    st.warning(amb)
            else:
                st.write("No major ambiguities detected.")

        st.markdown("---")
        st.markdown("### 📥 Intelligence Export")
        e1, e2 = st.columns(2)
        e1.download_button("Export JSON Intelligence", json.dumps(data, indent=2), "policy_ultra.json")
        e2.download_button("Export Final Report", f"POLICY REPORT\n{json.dumps(data, indent=2)}", "policy_report.txt")
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 600px; color: #a7f3d0; border: 2px dashed rgba(16,185,129,0.1); border-radius: 30px;'>
            <img src='https://img.icons8.com/clouds/200/law.png' width='120' style='opacity: 0.2;'/>
            <p style='margin-top: 20px; font-weight: 300;'>Analytic report will be rendered upon architectural synthesis.</p>
        </div>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.caption("Engineered by Harsh Choudhary | V2.0 Ultra")
