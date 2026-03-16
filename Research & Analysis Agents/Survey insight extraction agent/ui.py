import streamlit as st
import json
import os
from datetime import date
from agent import run_multi_model_analysis

# Premium Page Configuration
st.set_page_config(
    page_title="Survey Insight Agent Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Sellable" Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Outfit', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
        color: #f8fafc;
    }
    
    .main-header {
        font-weight: 800;
        background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    
    .badge {
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 2rem;
        display: inline-block;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    
    .card {
        background: rgba(30, 41, 59, 0.4);
        padding: 2rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }
    
    .theme-card {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #38bdf8;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1.2rem;
        transition: transform 0.2s;
    }
    
    .theme-card:hover {
        transform: translateX(10px);
        background: rgba(30, 41, 59, 0.8);
    }
    
    .sentiment-positive { color: #4ade80; background: rgba(74, 222, 128, 0.1); padding: 2px 8px; border-radius: 4px; }
    .sentiment-neutral { color: #fbbf24; background: rgba(251, 191, 36, 0.1); padding: 2px 8px; border-radius: 4px; }
    .sentiment-negative { color: #f87171; background: rgba(248, 113, 113, 0.1); padding: 2px 8px; border-radius: 4px; }
    
    /* Input Styling */
    .stTextArea textarea {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1px solid #1e293b !important;
        border-radius: 1rem !important;
    }
    
    .stButton>button {
        background: linear-gradient(to right, #38bdf8, #818cf8) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Provider Logic Mapping
MODELS = {
    "OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
    "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
    "Google Gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
    "Groq": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
}

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Neural Config")
    
    provider = st.selectbox("Intelligence Provider", list(MODELS.keys()))
    model = st.selectbox("Specific Model", MODELS[provider])
    
    env_key_name = f"{provider.split()[0].upper()}_API_KEY"
    api_key = st.text_input(f"{provider} API Key", type="password", value=os.getenv(env_key_name, ""))
    
    st.divider()
    st.caption("v2.0 • Pro Edition")

# Main UI
st.markdown('<h1 class="main-header">Survey Insight Agent Pro</h1>', unsafe_allow_html=True)
st.markdown('<span class="badge">Multi-Model Operational Engine</span>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Primary Data Stream")
    
    default_input = """Survey Goal: Understand learner feedback on AI Agent course
Audience: Course participants
Responses:
- The hands-on projects were extremely helpful.
- I found the pacing intense but rewarding.
- Some topics could use more real-world examples.
- Loved the daily structure and independence of lessons.
- Too much content to absorb in some weeks."""
    
    survey_text = st.text_area("Input survey responses (Text/CSV format):", value=default_input, height=400)
    
    if st.button("🚀 Execute Neural Extraction", use_container_width=True):
        if not api_key:
            st.error(f"Error: {provider} API Key is required for processing.")
        else:
            with st.spinner(f"Routing through {provider} {model}..."):
                try:
                    # Execute analysis via the multi-model router in agent.py
                    insights = run_multi_model_analysis(provider, model, api_key, survey_text)
                    st.session_state['insights'] = insights
                    st.toast("Neural analysis complete!", icon="✅")
                except Exception as e:
                    st.error(f"Neural Error: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if 'insights' in st.session_state:
        insights = st.session_state['insights']
        
        # Summary Area
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏮 Executive Intelligence")
        st.write(insights.get("summary", "No summary generated."))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Theme Navigation
        st.subheader("🎯 Key Signals & Themes")
        for theme in insights.get("themes", []):
            with st.markdown(f'<div class="theme-card">', unsafe_allow_html=True):
                st.markdown(f"### {theme['theme']}")
                sentiment = theme['sentiment'].lower()
                sentiment_class = "sentiment-positive" if "pos" in sentiment else "sentiment-negative" if "neg" in sentiment else "sentiment-neutral"
                st.markdown(f"**Sentiment Analysis:** <span class='{sentiment_class}'>{theme['sentiment']}</span>", unsafe_allow_html=True)
                
                with st.expander("View Evidence Examples"):
                    for ex in theme['examples']:
                        st.markdown(f"- {ex}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Optional Insights
        c_alt1, c_alt2 = st.columns(2)
        with c_alt1:
            if insights.get("outliers"):
                with st.expander("🛸 Minority Signals", expanded=True):
                    for outlier in insights["outliers"]:
                        st.markdown(f"- {outlier}")
        with c_alt2:
            if insights.get("suggested_follow_ups"):
                with st.expander("❓ Optimization Steps", expanded=True):
                    for q in insights["suggested_follow_ups"]:
                        st.markdown(f"- {q}")
                    
        # Export options
        st.divider()
        col_json, col_txt = st.columns(2)
        with col_json:
            st.download_button("📥 Export JSON", data=json.dumps(insights, indent=2), file_name="survey_insights.json", use_container_width=True)
        with col_txt:
            # Generate TXT content
            txt_content = f"Survey Insights Pro ({date.today()})\n{'='*30}\n\nSummary: {insights.get('summary', '')}\n\n"
            for t in insights.get('themes', []):
                txt_content += f"Theme: {t['theme']}\nSentiment: {t['sentiment']}\nExamples:\n"
                txt_content += "\n".join([f"- {e}" for e in t.get('examples', [])]) + "\n\n"
            st.download_button("📝 Export TXT", data=txt_content, file_name="survey_insights.txt", use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding-top: 100px; color: #64748b;">
            <img src="https://cdn-icons-png.flaticon.com/512/2040/2040441.png" width="100" style="opacity: 0.2;">
            <p style="margin-top: 20px;">Ready for command. Select provider and upload data to begin.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption(f"Operational Node: {provider} {model} | HarshChoudhary2003/Real-world-AI-agents-hub")
