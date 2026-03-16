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
    page_title="NewsFlow | News Aggregation Agent",
    page_icon="📰",
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
        background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
        color: #f8fafc;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #0284c7 100%);
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
        box-shadow: 0 10px 15px -3px rgba(56, 189, 248, 0.4);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .theme-card {
        background: rgba(56, 189, 248, 0.05);
        border-left: 4px solid #38bdf8;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
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
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        background: rgba(56, 189, 248, 0.1);
        color: #7dd3fc;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Global client initialization placeholder
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a News Aggregation Agent.

Rules:
- Aggregate and synthesize news objectively based on user input.
- Group related stories by theme.
- Avoid sensationalism or opinion.
- Focus on relevance and clarity.

Return ONLY valid JSON with this schema:
{
  "summary": "High-level digest of all key themes",
  "themes": [
    {
      "theme": "Theme Name",
      "key_developments": ["Development 1", "Development 2"]
    }
  ]
}
"""

def aggregate_news(text):
    model = st.session_state.get('model_id', 'gpt-4o-mini')
    if client is None:
        st.error("AI Client is not initialized. Please check settings in the sidebar.")
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
    st.image("https://img.icons8.com/clouds/200/news.png", width=120)
    st.title("Settings")
    
    provider = st.selectbox("Select Provider", ["OpenAI", "Groq", "OpenRouter", "DeepSeek", "Local (Ollama/LM Studio)", "Custom"])
    
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
    - **Multi-Source Synthesis**
    - **Thematic Grouping**
    - **Neutral Intelligence**
    - **Cross-Model Support**
    """)
    st.caption("Developed by Antigravity Agent Lab")

# Main UI
st.title("📰 NewsFlow: Intelligence Aggregator")
st.markdown("<p style='font-size:1.2rem; color:#94a3b8;'>Real-time thematic synthesis for enterprise news and market events.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🎯 Aggregation Parameters")
    
    input_method = st.radio("Input Mode", ["Custom Specification", "Daily Enterprise Brief (Sample)"])
    
    if input_method == "Custom Specification":
        topics = st.text_input("Focus Topics", placeholder="AI Regulation, Semiconductor Market, Fed Policy")
        geography = st.text_input("Geography", value="Global")
        time_frame = st.selectbox("Time Window", ["Daily", "Weekly", "Monthly", "Custom"])
        scope = st.text_area("Additional Context/Sources", placeholder="Focus on financial impacts and mergers...")
        input_text = f"Topics: {topics}\nGeography: {geography}\nTime: {time_frame}\nContext: {scope}"
    else:
        sample = """Topics: AI, enterprise technology, regulation
Time Window: Daily
Geography: Global
Sources: Major news outlets and industry publications"""
        input_text = st.text_area("Sample Input:", value=sample, height=200)

    if st.button("🛰️ Aggregate Intelligence"):
        if not input_text.strip():
            st.warning("Please specify topics.")
        elif client is None:
            st.error("API Key is required in the sidebar.")
        else:
            with st.spinner("Synthesizing global signals..."):
                digest = aggregate_news(input_text)
                if digest:
                    st.session_state['news_digest'] = digest
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if 'news_digest' in st.session_state:
        data = st.session_state['news_digest']
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📂 News Digest")
        st.markdown(f"<div class='status-badge'>Compiled on {date.today()}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 📝 Executive Summary")
        st.write(data.get("summary", ""))
        
        st.markdown("#### 🧩 Thematic Breakdown")
        for theme in data.get("themes", []):
            with st.container():
                st.markdown(f"<div class='theme-card'><strong>{theme['theme']}</strong>", unsafe_allow_html=True)
                for dev in theme.get("key_developments", []):
                    st.markdown(f"• {dev}")
                st.markdown("</div>", unsafe_allow_html=True)
                
        st.markdown("---")
        st.markdown("### 📥 Export Intelligence")
        col_ex1, col_ex2 = st.columns(2)
        
        json_str = json.dumps(data, indent=2)
        col_ex1.download_button("Download JSON", data=json_str, file_name="news_digest.json")
        
        txt_out = f"News Intelligence Digest ({date.today()})\n" + "="*50 + "\n\n"
        txt_out += f"Summary:\n{data['summary']}\n\n"
        for t in data['themes']:
            txt_out += f"Theme: {t['theme']}\n"
            txt_out += "\n".join([f"- {d}" for d in t['key_developments']]) + "\n\n"
            
        col_ex2.download_button("Download Text", data=txt_out, file_name="news_digest.txt")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #64748b; border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px; padding: 4rem;'>
            <img src='https://img.icons8.com/fluency/96/news.png' width='80' style='opacity: 0.5; margin-bottom: 20px;'/>
            <p>Intelligence digest will appear here after synthesis.</p>
        </div>
        """, unsafe_allow_html=True)
