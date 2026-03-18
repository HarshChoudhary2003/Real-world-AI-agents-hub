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
    page_title="StreamBrief | YouTube Summary Agent",
    page_icon="🎬",
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
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
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
        box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.4);
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
        border-left: 4px solid #ef4444;
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
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        background: rgba(239, 68, 68, 0.1);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Global client initialization placeholder
client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a YouTube Video Summary Agent.

Rules:
- Summarize video content clearly and faithfully
- Remove filler and repetition
- Preserve key ideas and structure
- Avoid personal interpretation

Return ONLY valid JSON with this schema:
{
  "overview": "Concise high-level summary",
  "key_points": ["Point 1", "Point 2"],
  "examples_or_insights": ["Insight 1", "Insight 2"],
  "final_takeaway": "Actionable conclusion or main message"
}
"""

def summarize_video(text):
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
    st.image("https://img.icons8.com/clouds/200/youtube-play--v1.png", width=120)
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
    - **Transcript Synthesis**
    - **Filler Extraction**
    - **Key-Insight Mapping**
    - **Multi-Model Support**
    """)
    st.caption("Developed by Antigravity Agent Lab")

# Main UI
st.title("🎬 StreamBrief: Video Summarizer")
st.markdown("<p style='font-size:1.2rem; color:#94a3b8;'>Turn long videos into structured intelligence in seconds.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📝 Input Transcript")
    
    input_method = st.radio("Input Source", ["Paste Transcript", "Sample Text"])
    
    if input_method == "Paste Transcript":
        input_text = st.text_area("Paste video transcript or notes:", height=300, placeholder="Title: ... \n[00:00] Intro...")
    else:
        sample = """Video Title: How AI Agents are Changing Software
Transcript:
In this video, we explore the shift from passive software to agentic systems. 
AI agents are no longer just responding to prompts; they are planning, using tools, and achieving goals.
We look at examples like AutoGPT and specialized coding agents. 
The main takeaway is that developers need to think about 'handing off' agency to these models safely."""
        input_text = st.text_area("Sample Input:", value=sample, height=300)

    if st.button("⚡ Synthesize Summary"):
        if not input_text.strip():
            st.warning("Please provide a transcript.")
        elif client is None:
            st.error("API Key is required in the sidebar.")
        else:
            with st.spinner("Parsing video logic..."):
                summary = summarize_video(input_text)
                if summary:
                    st.session_state['video_summary'] = summary
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if 'video_summary' in st.session_state:
        data = st.session_state['video_summary']
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Structured Summary")
        st.markdown(f"<div class='status-badge'>Generated on {date.today()}</div>", unsafe_allow_html=True)
        
        st.markdown("#### 📖 Overview")
        st.write(data.get("overview", ""))
        
        st.markdown("#### 🎯 Key Points")
        for point in data.get("key_points", []):
            st.markdown(f"• {point}")
            
        if data.get("examples_or_insights"):
            st.markdown("#### 💡 Insights")
            for insight in data.get("examples_or_insights", []):
                st.markdown(f"- {insight}")
                
        st.markdown("#### 🏁 Final Takeaway")
        st.success(data.get("final_takeaway", ""))
        
        st.markdown("---")
        st.markdown("### 📥 Export Details")
        col_ex1, col_ex2 = st.columns(2)
        
        json_str = json.dumps(data, indent=2)
        col_ex1.download_button("Download JSON", data=json_str, file_name="video_summary.json")
        
        txt_out = f"YouTube Summary ({date.today()})\n" + "="*50 + "\n\n"
        txt_out += f"Overview:\n{data['overview']}\n\nPoints:\n"
        txt_out += "\n".join([f"- {p}" for p in data['key_points']])
        txt_out += f"\n\nTakeaway: {data['final_takeaway']}"
        col_ex2.download_button("Download Text", data=txt_out, file_name="video_summary.txt")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #64748b; border: 2px dashed rgba(255,255,255,0.1); border-radius: 20px; padding: 4rem;'>
            <img src='https://img.icons8.com/fluency/96/youtube-play--v1.png' width='80' style='opacity: 0.5; margin-bottom: 20px;'/>
            <p>Video intelligence will appear here.</p>
        </div>
        """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
