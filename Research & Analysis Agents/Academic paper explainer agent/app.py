import streamlit as st
import json
from openai import OpenAI
from datetime import date
import os
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="ScholarAI | Academic Paper Explainer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
    }
    
    h1, h2, h3 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .sidebar .sidebar-content {
        background: #0f172a;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        background: rgba(59, 130, 246, 0.1);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Global client initialization placeholder
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an Academic Paper Explainer Agent.

Rules:
- Explain academic research clearly and accurately for a non-expert audience.
- Preserve technical meaning, nuance, and critical limitations.
- Avoid speculation, exaggeration, or marketing "fluff".
- Structure the response with clear headings.

Return ONLY valid JSON with this schema:
{
  "summary": "High-level plain-English summary",
  "research_question": "What specifically is being studied?",
  "methodology": "How was the research conducted?",
  "key_findings": ["Finding 1", "Finding 2"],
  "implications": ["Impact 1", "Impact 2"],
  "limitations": ["Limitation 1", "Limitation 2"]
}
"""

def explain_paper(text):
    model = st.session_state.get('model_id', 'gpt-4o-mini')
    
    if client is None:
        st.error("AI Client is not initialized. Please provide an API key or check your settings in the sidebar.")
        return None
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"AI Generation Error: {str(e)}")
        return None

# Sidebar Content
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/education.png", width=120)
    st.title("Settings")
    
    provider = st.selectbox("Select Provider", ["OpenAI", "Groq", "OpenRouter", "DeepSeek", "Local (Ollama/LM Studio)", "Custom"])
    
    # Provider-specific configurations
    base_urls = {
        "OpenAI": "https://api.openai.com/v1",
        "Groq": "https://api.groq.com/openai/v1",
        "OpenRouter": "https://openrouter.ai/api/v1",
        "DeepSeek": "https://api.deepseek.com",
        "Local (Ollama/LM Studio)": "http://localhost:11434/v1",
        "Custom": ""
    }
    
    default_models = {
        "OpenAI": "gpt-4o-mini",
        "Groq": "mixtral-8x7b-32768",
        "OpenRouter": "anthropic/claude-3-haiku",
        "DeepSeek": "deepseek-chat",
        "Local (Ollama/LM Studio)": "llama3",
        "Custom": "model-id"
    }

    selected_base_url = base_urls.get(provider)
    if provider == "Custom":
        selected_base_url = st.text_input("Base URL", placeholder="https://your-api.com/v1")
    
    model_id = st.text_input("Model ID", value=default_models.get(provider, "gpt-4o-mini"))
    
    api_key_input = st.text_input("API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    
    if api_key_input or provider == "Local (Ollama/LM Studio)":
        client = OpenAI(
            api_key=api_key_input if api_key_input else "ollama",
            base_url=selected_base_url if selected_base_url else None
        )
        st.session_state['model_id'] = model_id
    
    st.markdown("---")
    st.markdown("### 🚀 Capabilities")
    st.info("""
    - **Plain Language Translation**
    - **Methodology Extraction**
    - **Critical Findings Recap**
    - **Implication Analysis**
    """)
    st.markdown("---")
    st.caption("Developed by Antigravity Agent Lab")

# Main UI
st.title("🎓 ScholarAI: Research Explainer")
st.markdown("<p style='font-size:1.2rem; color:#94a3b8;'>Transform complex academic papers into crystal-clear insights in seconds.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📄 Input Paper Content")
    
    input_method = st.radio("Choose Input Method", ["Paste Text", "Sample Text"])
    
    if input_method == "Paste Text":
        input_text = st.text_area("Paste the abstract or full paper text here:", height=300, placeholder="Title: ... \nAbstract: ...")
    else:
        sample = """Paper Title: Attention Is All You Need
Abstract:
The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."""
        input_text = st.text_area("Sample Input:", value=sample, height=300)

    if st.button("✨ Generate AI Explanation"):
        if not input_text.strip():
            st.warning("Please provide some text to analyze.")
        elif not os.getenv("OPENAI_API_KEY"):
            st.error("API Key is required. Please set it in the sidebar.")
        else:
            with st.spinner("Decoding complex research..."):
                explanation = explain_paper(input_text)
                if explanation:
                    st.session_state['explanation'] = explanation
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if 'explanation' in st.session_state:
        data = st.session_state['explanation']
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💡 AI Insights")
        
        st.markdown(f"<div class='status-badge'>Generated on {date.today()}</div>", unsafe_allow_html=True)
        
        with st.expander("📝 Summary", expanded=True):
            st.write(data.get("summary", ""))
            
        with st.expander("🔍 Research Question", expanded=True):
            st.write(data.get("research_question", ""))
            
        with st.expander("🛠 Methodology", expanded=True):
            st.write(data.get("methodology", ""))
            
        tabs = st.tabs(["🎯 Key Findings", "🌍 Implications", "⚠️ Limitations"])
        
        with tabs[0]:
            for item in data.get("key_findings", []):
                st.markdown(f"• {item}")
                
        with tabs[1]:
            for item in data.get("implications", []):
                st.markdown(f"• {item}")
                
        with tabs[2]:
            for item in data.get("limitations", []):
                st.markdown(f"• {item}")
                
        st.markdown("---")
        
        # Output options
        st.markdown("### 📥 Export Results")
        col_ex1, col_ex2 = st.columns(2)
        
        json_str = json.dumps(data, indent=2)
        col_ex1.download_button(
            label="Download JSON",
            data=json_str,
            file_name="paper_explanation.json",
            mime="application/json"
        )
        
        txt_output = f"Academic Paper Explanation ({date.today()})\n" + "="*55 + "\n\n"
        txt_output += f"Summary:\n{data['summary']}\n\n"
        txt_output += f"Research Question:\n{data['research_question']}\n\n"
        txt_output += f"Methodology:\n{data['methodology']}\n\n"
        txt_output += "Key Findings:\n" + "\n".join([f"- {k}" for k in data['key_findings']]) + "\n\n"
        txt_output += "Implications:\n" + "\n".join([f"- {i}" for i in data['implications']]) + "\n\n"
        txt_output += "Limitations:\n" + "\n".join([f"- {l}" for l in data['limitations']])
        
        col_ex2.download_button(
            label="Download Text",
            data=txt_output,
            file_name="paper_explanation.txt",
            mime="text/plain"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #64748b; border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px; padding: 4rem;'>
            <img src='https://img.icons8.com/fluency/96/brain--v1.png' width='80' style='opacity: 0.5; margin-bottom: 20px;'/>
            <p>Intelligence results will appear here after generation.</p>
        </div>
        """, unsafe_allow_html=True)
