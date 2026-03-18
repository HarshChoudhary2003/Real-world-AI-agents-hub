import streamlit as st
import json
import os
from datetime import date
from litellm import completion
from dotenv import load_dotenv

# Page Config
st.set_page_config(
    page_title="Market Trend Intelligence Pro",
    page_icon="📈",
    layout="wide",
)

# Load context
load_dotenv()

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
        color: #f8fafc;
    }
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
        color: white;
    }
    .trend-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }
    .trend-title {
        color: #60a5fa;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .implication-box {
        background: rgba(96, 165, 250, 0.1);
        border-left: 4px solid #60a5fa;
        padding: 0.75rem 1rem;
        margin-top: 1rem;
        font-size: 0.95rem;
    }
    .sidebar .sidebar-content {
        background: #0f172a;
    }
    .stSelectbox label, .stTextInput label {
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Provider Data
PROVIDERS = {
    "OpenAI": {
        "models": ["openai/gpt-4o-mini", "openai/gpt-4o", "openai/o1-preview", "openai/gpt-3.5-turbo"],
        "env_key": "OPENAI_API_KEY"
    },
    "Anthropic": {
        "models": ["anthropic/claude-3-5-sonnet-20240620", "anthropic/claude-3-haiku-20240307", "anthropic/claude-3-opus-20240229"],
        "env_key": "ANTHROPIC_API_KEY"
    },
    "Google (Gemini)": {
        "models": ["gemini/gemini-1.5-flash", "gemini/gemini-1.5-pro", "gemini/gemini-pro"],
        "env_key": "GEMINI_API_KEY"
    },
    "Groq": {
        "models": ["groq/llama-3.1-70b-versatile", "groq/llama-3.1-8b-instant", "groq/mixtral-8x7b-32768"],
        "env_key": "GROQ_API_KEY"
    },
    "Mistral": {
        "models": ["mistral/mistral-large-latest", "mistral/mistral-small-latest", "mistral/pixtral-12b-2409"],
        "env_key": "MISTRAL_API_KEY"
    },
    "Perplexity": {
        "models": ["perplexity/llama-3.1-sonar-large-128k-online", "perplexity/llama-3.1-sonar-small-128k-online"],
        "env_key": "PERPLEXITY_API_KEY"
    },
    "Cohere": {
        "models": ["cohere/command-r-plus", "cohere/command-r"],
        "env_key": "COHERE_API_KEY"
    },
    "DeepSeek": {
        "models": ["deepseek/deepseek-chat", "deepseek/deepseek-coder"],
        "env_key": "DEEPSEEK_API_KEY"
    },
    "OpenRouter": {
        "models": ["openrouter/auto", "openrouter/anthropic/claude-3.5-sonnet", "openrouter/google/gemini-pro-1.5"],
        "env_key": "OPENROUTER_API_KEY"
    }
}

# Sidebar for configuration
with st.sidebar:
    st.title("🛡️ API Control Center")
    
    selected_provider = st.selectbox("LLM Provider", list(PROVIDERS.keys()))
    selected_model = st.selectbox("Intelligence Model", PROVIDERS[selected_provider]["models"])
    
    env_key_name = PROVIDERS[selected_provider]["env_key"]
    api_key = st.text_input(f"{selected_provider} API Key", type="password", value=os.getenv(env_key_name, ""))
    
    if api_key:
        os.environ[env_key_name] = api_key
        st.success(f"Connection Active")
    else:
        st.warning(f"Key Required")

    st.markdown("---")
    st.markdown("### 🛠️ Agentic Tuning")
    temperature = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.35)
    max_tokens = st.number_input("Max Output Tokens", 500, 4000, 2000)
    top_p = st.slider("Top P", 0.0, 1.0, 1.0)

# Main UI
st.title("📈 TrendSynthetix AI")
st.markdown("##### Enterprise Market Intelligence | Multi-Model Architecture")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Market Context")
    default_input = """Market: Enterprise AI
Time Horizon: Mid-term (2–3 years)
Sources: News, analyst reports, industry commentary
Geography: Global"""
    
    input_text = st.text_area("Define Scope:", value=default_input, height=300)
    
    if st.button("🚀 Synthesize Trends"):
        if not api_key:
            st.error(f"Missing {selected_provider} API Key!")
        else:
            with st.spinner(f"Requesting {selected_model}..."):
                try:
                    SYSTEM_PROMPT = """
                    You are a Market Trend Summarization Agent.
                    Rules:
                    - Identify meaningful market trends
                    - Distinguish trends from isolated events
                    - Avoid speculation and hype
                    - Highlight implications and uncertainty
                    - Return ONLY valid JSON with 'overview', 'trends' (array of {trend, description, implications}), and 'risks_and_uncertainties' (array).
                    """
                    
                    response = completion(
                        model=selected_model,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": input_text}
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p
                    )
                    
                    content = response.choices[0].message.content
                    # Advanced JSON extraction
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        content = json_match.group(0)
                    
                    st.session_state['trends_data'] = json.loads(content)
                    st.success("Intelligence report generated!")
                except Exception as e:
                    st.error(f"Generation Error: {str(e)}")

with col2:
    st.subheader("🔍 Intelligence Report")
    
    if 'trends_data' in st.session_state:
        data = st.session_state['trends_data']
        
        st.write(f"**Market Overview:** {data.get('overview', 'N/A')}")
        
        # Visualization
        import pandas as pd
        trends_list = data.get('trends', [])
        if trends_list:
            df = pd.DataFrame([
                {
                    "Trend": t.get("trend"),
                    "Impact": t.get("impact", 5),
                    "Confidence": t.get("confidence", 5)
                } for t in trends_list
            ])
            st.markdown("### 📊 Trend Matrix (Impact vs Confidence)")
            st.scatter_chart(df, x="Confidence", y="Impact", color="Trend", size="Impact")

        for trend in trends_list:
            st.markdown(f"""
            <div class="trend-card">
                <div class="trend-title">{trend.get('trend', 'Trend')}</div>
                <div style="margin-bottom: 0.5rem;">
                    <span style="background:#1e293b; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">Impact: {trend.get('impact', 'N/A')}/10</span>
                    <span style="background:#1e293b; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-left: 5px;">Confidence: {trend.get('confidence', 'N/A')}/10</span>
                </div>
                <div>{trend.get('description', '')}</div>
                <div class="implication-box">
                    <strong>Implications:</strong> {trend.get('implications', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if data.get('risks_and_uncertainties'):
            with st.expander("⚠️ Risks & Strategic Uncertainties"):
                for risk in data.get('risks_and_uncertainties', []):
                    st.markdown(f"- {risk}")
                
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.download_button("📥 JSON", json.dumps(data, indent=2), "trends.json", "application/json")
        with col_ex2:
            st.download_button("📄 TXT", str(data), "trends.txt", "text/plain")
    else:
        st.info("System Ready. Select a model and provide context to begin synthesis.")

st.markdown("---")
st.caption(f"Connected to {selected_model} via LiteLLM Relay")


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
