import streamlit as st
import json
import os
from datetime import date

# Import API Clients
from openai import OpenAI
import anthropic
import groq
import google.generativeai as genai

# -----------------------------------------------------------------------------
# CONSTANTS & CONFIG
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an elite, enterprise-grade Web Research Expert Agent.

Rules:
- Synthesize complex information from diverse web domains and knowledge sources.
- Focus strictly on high relevance, absolute factual accuracy, and credibility.
- Do NOT copy text verbatim; synthesize and paraphrase professionally.
- Clearly separate established facts, emerging trends, and unresolved questions.
- Provide actionable, executive-level insights.

Return ONLY valid JSON strictly matching this schema (do not wrap in markdown tags like ```json):

{
  "summary": "High-level executive summary (2-3 paragraphs)",
  "key_findings": ["Actionable finding 1", "Actionable finding 2", "..."],
  "trends": ["Emerging trend 1", "Emerging trend 2", "..."],
  "open_questions": ["Critical unknown 1", "Critical unknown 2", "..."]
}
"""

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Web Research Agent | LiveOS",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS FOR PREMIUM UI
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Main container and text */
    .main {
        background-color: #0E1117;
        color: #E0E6ED;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8F9FA !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    
    /* Cards and containers */
    .stAlert {
        background-color: #1E2329;
        border: 1px solid #30363D;
        border-radius: 8px;
        color: #E0E6ED;
    }
    
    /* Metrics / Callouts */
    .metric-card {
        background-color: #161A20;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161A20;
        border-right: 1px solid #30363D;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #2F81F7;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1F6AE0;
        box-shadow: 0 4px 12px rgba(47, 129, 247, 0.3);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #0D1117;
        border: 1px solid #30363D;
        color: #E0E6ED;
        border-radius: 6px;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #2F81F7;
        box-shadow: 0 0 0 1px #2F81F7;
    }
    
    /* Custom divider */
    hr {
        border-color: #30363D;
    }
    
    /* Badge */
    .enterprise-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        background-color: rgba(47, 129, 247, 0.1);
        color: #2F81F7;
        border: 1px solid rgba(47, 129, 247, 0.2);
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def conduct_research(api_provider, api_key, model, temp, prompt_text):
    if api_provider == "OpenAI":
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=temp,
            response_format={ "type": "json_object" }
        )
        content = response.choices[0].message.content
        return json.loads(content)
        
    elif api_provider == "Anthropic":
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            temperature=temp,
            max_tokens=4000
        )
        content = response.content[0].text
        # Extract JSON from potential markdown tags since Anthropic doesn't have a strict JSON mode flag
        start = content.find('{')
        end = content.rfind('}') + 1
        return json.loads(content[start:end])
        
    elif api_provider == "Groq":
        client = groq.Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=temp,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
        
    elif api_provider == "Google Gemini":
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(
            model_name=model,
            system_instruction=SYSTEM_PROMPT,
            generation_config={"temperature": temp, "response_mime_type": "application/json"}
        )
        response = model_instance.generate_content(prompt_text)
        return json.loads(response.text)

def handle_research(api_provider, api_key, model, temp, prompt):
    if not api_key:
        st.error(f"Please enter your {api_provider} API key in the sidebar.")
        return

    with st.spinner("Initiating autonomous intelligence gathering..."):
        try:
            research_data = conduct_research(api_provider, api_key, model, temp, prompt)
            st.session_state['research_results'] = research_data
            st.toast('Research completed successfully!', icon='✅')
        except Exception as e:
            st.error(f"Analysis Failed: {str(e)}")

# -----------------------------------------------------------------------------
# MAIN APP
# -----------------------------------------------------------------------------
def main():
    # --- Sidebar Configuration ---
    with st.sidebar:
        st.image("https://img.icons8.com/nolan/96/artificial-intelligence.png", width=60)
        st.title("System Config")
        st.markdown("Configure intelligence engine parameters.")
        
        st.divider()
        st.subheader("Agent Settings")
        api_provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic", "Groq", "Google Gemini"], index=0)
        
        st.divider()
        st.subheader("Authentication")
        api_key = st.text_input(f"{api_provider} API Key", type="password", help="Enter your API key securely here. It is not stored.")
        
        st.divider()
        st.subheader("Model Configuration")
        
        if api_provider == "OpenAI":
            model_options = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
        elif api_provider == "Anthropic":
            model_options = ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
        elif api_provider == "Groq":
            model_options = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it", "gemma-7b-it"]
        elif api_provider == "Google Gemini":
            model_options = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"]
            
        selected_model = st.selectbox("LLM Architecture", model_options, index=0)
        
        temperature = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.3, step=0.05, 
                                help="Lower values produce more factual, grounded output; higher values allow more creative synthesis.")
        
        st.divider()
        st.markdown("<p style='font-size: 0.8rem; color: #8b949e;'>v3.0 Multi-Model Enterprise Build</p>", unsafe_allow_html=True)

    # --- Header ---
    st.markdown("<h1>Web Research Agent <span class='enterprise-badge'>ENTERPRISE</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; color: #8b949e; margin-bottom: 2rem;'>An autonomous intelligence assistant designed to synthesize complex information into actionable executive summaries, key findings, and dynamic market trends.</p>", unsafe_allow_html=True)

    # --- Main Content Structure ---
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown("### Research Parameters")
        
        default_prompt = (
            "Topic: AI Agents in Enterprise Productivity\n"
            "Scope: High-level executive overview\n"
            "Focus Areas: Automation, ROI, Security risks\n"
            "Timeframe: Last 12 months"
        )
        
        research_prompt = st.text_area(
            "Define Objective & Scope", 
            value=default_prompt,
            height=250,
            help="Provide clear constraints: Topic, Scope, Focus Areas, and required Depth."
        )
        
        if st.button("Deploy Research Agent 🚀"):
            handle_research(api_provider, api_key, selected_model, temperature, research_prompt)

    with col2:
        st.markdown("### Intelligence Dashboard")
        
        if 'research_results' in st.session_state:
            data = st.session_state['research_results']
            
            # Use tabs for a cleaner UI
            tab_summary, tab_findings, tab_raw = st.tabs(["Executive Summary", "Detailed Analysis", "Raw Data (JSON)"])
            
            with tab_summary:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown("#### The Synthesis")
                st.write(data.get("summary", "No summary provided."))
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Download Text
                text_output = f"Executive Intelligence Report ({date.today()})\n"
                text_output += "=" * 50 + "\n\n"
                text_output += "Summary:\n" + data.get("summary", "") + "\n\n"
                text_output += "Key Findings:\n" + "\n".join([f"- {k}" for k in data.get("key_findings", [])]) + "\n\n"
                text_output += "Trends:\n" + "\n".join([f"- {t}" for t in data.get("trends", [])]) + "\n\n"
                text_output += "Open Questions:\n" + "\n".join([f"- {q}" for q in data.get("open_questions", [])]) + "\n"
                
                st.download_button(
                    label="📄 Export Executive Briefing (.txt)",
                    data=text_output,
                    file_name="executive_briefing.txt",
                    mime="text/plain"
                )

            with tab_findings:
                # Key Findings
                st.markdown("#### Key Findings")
                for finding in data.get("key_findings", []):
                    st.info(finding, icon="💎")
                
                # Trends
                st.markdown("#### Emerging Trends")
                for trend in data.get("trends", []):
                    st.success(trend, icon="📈")
                
                # Open Questions
                st.markdown("#### Critical Open Questions")
                for q in data.get("open_questions", []):
                    st.warning(q, icon="❓")

            with tab_raw:
                st.json(data)
                
                st.download_button(
                    label="💾 Export Raw Data (.json)",
                    data=json.dumps(data, indent=2),
                    file_name="intelligence_data.json",
                    mime="application/json"
                )
        else:
            st.info("System is standing by. Define parameters and deploy the agent to view intelligence metrics.")

if __name__ == "__main__":
    main()