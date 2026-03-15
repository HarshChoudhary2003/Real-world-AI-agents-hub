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
You are an elite Competitive Analysis Agent.

Rules:
- Compare competitors objectively and rigorously.
- Identify specific strengths, weaknesses, and market positioning.
- Avoid subjective or promotional language; remain neutral and analytical.
- Focus on strategic, actionable insights for market differentiation.

Return ONLY valid JSON with this schema:

{
  "overview": "High-level summary of the competitive landscape",
  "competitors": [
    {
      "name": "Competitor Name",
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "positioning": "Strategic market positioning description"
    }
  ],
  "gaps_and_opportunities": ["Opportunity 1", "Gap 2"]
}
"""

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Competitive Analysis Agent | LiveOS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS FOR PREMIUM UI
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #E0E6ED;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        color: #F8F9FA !important;
        font-weight: 600 !important;
    }
    .stAlert {
        background-color: #1E2329;
        border: 1px solid #30363D;
        border-radius: 8px;
    }
    .metric-card {
        background-color: #161A20;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .competitor-card {
        background-color: #0D1117;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .competitor-card:hover {
        border-color: #2F81F7;
        transform: translateY(-2px);
    }
    .stButton>button {
        background-color: #2F81F7;
        color: white;
        width: 100%;
    }
    .enterprise-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        background-color: rgba(47, 129, 247, 0.1);
        color: #2F81F7;
        border: 1px solid rgba(47, 129, 247, 0.2);
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def conduct_analysis(api_provider, api_key, model, temp, prompt_text):
    if api_provider == "OpenAI":
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt_text}],
            temperature=temp,
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    # ... (Similar implementations for Anthropic, Groq, Gemini as in Web Research Agent)
    elif api_provider == "Anthropic":
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model, system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=temp, max_tokens=4000
        )
        content = response.content[0].text
        start, end = content.find('{'), content.rfind('}') + 1
        return json.loads(content[start:end])
    elif api_provider == "Groq":
        client = groq.Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt_text}],
            temperature=temp, response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    elif api_provider == "Google Gemini":
        genai.configure(api_key=api_key)
        m = genai.GenerativeModel(model_name=model, system_instruction=SYSTEM_PROMPT, generation_config={"temperature": temp, "response_mime_type": "application/json"})
        response = m.generate_content(prompt_text)
        return json.loads(response.text)

# -----------------------------------------------------------------------------
# MAIN APP
# -----------------------------------------------------------------------------
def main():
    with st.sidebar:
        st.title("🛡️ Intelligence Config")
        api_provider = st.selectbox("Intelligence Source", ["OpenAI", "Anthropic", "Groq", "Google Gemini"], index=0)
        api_key = st.text_input(f"{api_provider} API Key", type="password")
        
        if api_provider == "OpenAI": model_options = ["gpt-4o", "gpt-4o-mini"]
        elif api_provider == "Anthropic": model_options = ["claude-3-5-sonnet-20240620"]
        elif api_provider == "Groq": model_options = ["llama3-70b-8192"]
        elif api_provider == "Google Gemini": model_options = ["gemini-1.5-pro"]
        
        selected_model = st.selectbox("Neural Architecture", model_options)
        temperature = st.slider("Analytical Variance", 0.0, 1.0, 0.35)

    st.markdown("<h1>Competitive Analysis Agent <span class='enterprise-badge'>ENTERPRISE</span></h1>", unsafe_allow_html=True)
    st.markdown("Deconstruct the market landscape with autonomous intelligence.")

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("Analysis Parameters")
        default_input = "Primary Company: AI Agent Productivity Course\nIndustry: Online education\nCompetitors:\n- Generic AI courses\n- No-code automation courses\n- Traditional productivity coaching\nFocus: Differentiation and positioning"
        context = st.text_area("Market Context", value=default_input, height=300)
        
        if st.button("Generate Tactical Briefing 🚀"):
            if not api_key:
                st.error("API Key required.")
            else:
                with st.spinner("Decoding competitor DNA..."):
                    try:
                        results = conduct_analysis(api_provider, api_key, selected_model, temperature, context)
                        st.session_state['comp_results'] = results
                        st.toast("Intelligence synthesized.", icon="✅")
                    except Exception as e:
                        st.error(f"Synthesis failed: {e}")

    with col2:
        st.subheader("Market Intelligence Dashboard")
        if 'comp_results' in st.session_state:
            data = st.session_state['comp_results']
            
            tab1, tab2, tab3 = st.tabs(["Strategic Overview", "Competitor Matrix", "Raw Intelligence"])
            
            with tab1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.markdown("#### Landscape Summary")
                st.write(data.get("overview", ""))
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("#### Strategic Gaps & Opportunities")
                for gap in data.get("gaps_and_opportunities", []):
                    st.warning(gap, icon="💡")
                    
            with tab2:
                for comp in data.get("competitors", []):
                    with st.container():
                        st.markdown(f"<div class='competitor-card'>", unsafe_allow_html=True)
                        st.markdown(f"### {comp.get('name')}")
                        st.markdown(f"**Positioning:** {comp.get('positioning')}")
                        sc1, sc2 = st.columns(2)
                        with sc1:
                            st.markdown("##### Strengths")
                            for s in comp.get('strengths', []): st.write(f"- {s}")
                        with sc2:
                            st.markdown("##### Weaknesses")
                            for w in comp.get('weaknesses', []): st.write(f"- {w}")
                        st.markdown("</div>", unsafe_allow_html=True)
            
            with tab3:
                st.json(data)
        else:
            st.info("Standing by for market parameters.")

if __name__ == "__main__":
    main()
