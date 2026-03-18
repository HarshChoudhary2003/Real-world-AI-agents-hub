import streamlit as st
import json
import time
import re
import pandas as pd
from datetime import date

# Safely import AI providers so the app doesn't crash if one is missing
try:
    from openai import OpenAI, AuthenticationError
except ImportError:
    OpenAI = AuthenticationError = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# --- Page Configuration ---
st.set_page_config(
    page_title="AI SEO Architect Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #FAFAFD;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
            border-radius: 12px;
            border: 2px solid #E2E8F0;
            transition: border-color 0.3s ease;
            font-size: 15px;
            background-color: #FFFFFF;
        }
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox > div > div:focus {
            border-color: #10B981;
            box-shadow: 0 0 0 1px #10B981;
        }
        .stButton button {
            border-radius: 8px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            width: 100%;
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            color: white;
            border: none;
            padding: 0.6rem 1rem;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
            border: none;
            color: white;
        }
        .result-card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border: 1px solid #F1F5F9;
            margin-top: 15px;
            margin-bottom: 15px;
        }
        .header-title {
            background: -webkit-linear-gradient(45deg, #059669, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 3.5rem;
            letter-spacing: -1px;
            margin-bottom: 0px;
        }
        .header-subtitle {
            color: #64748B;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        .provider-badge {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 15px;
            background-color: #ECFDF5;
            color: #059669;
            border: 1px solid #A7F3D0;
        }
        .metric-card {
            background-color: #FFFFFF;
            border: 2px solid #E2E8F0;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #059669;
        }
        .metric-label {
            font-size: 0.85rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- AI Core Logic ---
SYSTEM_PROMPT = """
You are an Elite Enterprise SEO Strategist & Data Analyst. Your explicit purpose is to transform a seed keyword into a highly structured, data-rich SEO keyword cluster suitable for a Fortune 500 content strategy.

CRITICAL DIRECTIVES:
1. RELEVANCE & PRECISION: Expand the seed keyword into terms specifically tailored to the provided Audience, Intent, and Industry.
2. METRIC ESTIMATION: As an elite AI, you must intelligently estimate key SEO metrics for each keyword based on global industry standards. Provide estimates for Intent, Search Volume (High/Medium/Low), Competition (High/Medium/Low), and an estimated CPC (e.g. "$4.50").
3. NO HALLUCINATION FLUFF: Do not pad results with fake words. Keep exactly to real-world search terminology.
4. CLUSTER ARCHITECTURE: 
   - Primary: High volume, broad "head" terms. 
   - Supporting: Latent Semantic Indexing (LSI) terms.
   - Long Tail: Highly specific, low competition phrases perfect for quick rankings.
   - Questions: Exactly matched "People Also Ask" queries for FAQ schemas.

Return ONLY valid JSON exactly matching this schema (with no other markdown outside the JSON block):
{
  "analysis": "A sophisticated 2-3 sentence strategic rationale explaining WHY this specific cluster will drive traffic and conversions for the target audience.",
  "metrics": {
    "total_keywords_found": 0,
    "average_competition": "Medium",
    "search_intent_match": "Informational"
  },
  "primary_keywords": [
    {"keyword": "example term", "intent": "Commercial", "volume": "High", "competition": "High", "cpc": "$5.00"}
  ],
  "supporting_keywords": [
    {"keyword": "example term", "intent": "Informational", "volume": "Medium", "competition": "Medium", "cpc": "$2.50"}
  ],
  "long_tail_keywords": [
    {"keyword": "example term", "intent": "Transactional", "volume": "Low", "competition": "Low", "cpc": "$1.20"}
  ],
  "question_keywords": [
    {"keyword": "example question", "intent": "Informational", "volume": "Medium", "competition": "Medium", "cpc": "$0.00"}
  ]
}
"""

def extract_json(text_response):
    try:
        return json.loads(text_response)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?(.*?)```", text_response, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
        raise ValueError("Failed to parse output into JSON format")

def process_keywords(seed, content_type, audience, intent, industry, provider, api_key, model, temp):
    prompt_text = (
        f"Seed Keyword: {seed}\n"
        f"Content Type: {content_type}\n"
        f"Audience: {audience}\n"
        f"Search Intent: {intent}\n"
        f"Industry: {industry}\n"
    )
    
    # 1. OpenAI Logic
    if provider == "OpenAI":
        if OpenAI is None:
            raise RuntimeError("OpenAI is not installed. Run `pip install openai`.")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ],
            temperature=temp,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    # 2. Anthropic Logic
    elif provider == "Anthropic (Claude)":
        if anthropic is None:
            raise RuntimeError("Anthropic is not installed. Run `pip install anthropic`.")
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            temperature=temp,
            max_tokens=2500
        )
        return extract_json(response.content[0].text)

    # 3. Google Logic (Gemini)
    elif provider == "Google (Gemini)":
        if genai is None:
            raise RuntimeError("Google Generative AI is not installed. Run `pip install google-generativeai`.")
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(
            model_name=model,
            system_instruction=SYSTEM_PROMPT
        )
        response = gemini_model.generate_content(
            prompt_text,
            generation_config=genai.types.GenerationConfig(
                temperature=temp,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)

# --- UI Layout ---
def main():
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Engine Settings")
        
        provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic (Claude)", "Google (Gemini)"])
        
        if provider == "OpenAI":
            api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
            available_models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
        elif provider == "Anthropic (Claude)":
            api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
            available_models = ["claude-3-5-sonnet-20240620", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"]
        else:
            api_key = st.text_input("Google AI API Key", type="password", placeholder="AIza...")
            available_models = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp"]
            
        st.markdown("---")
        st.markdown("### 🧠 AI Model")
        model = st.selectbox("Select Model", available_models)
        
        st.markdown("---")
        st.markdown("### 🎛️ Creativity")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1, help="Lowered creativity forces the AI to stick strictly to pure data-driven keywords instead of inventing fluff.")
        
        st.markdown("---")
        st.markdown("*" "AI SEO Architect Pro v3.0 (Enterprise Build)" "*")

    # Main Area
    st.markdown('<div class="header-title">AI SEO Architect Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Enterprise-grade Semantic SEO Expansion & Strategy Dashboard</div>', unsafe_allow_html=True)
    
    # Input Area Frame
    with st.container():
        col_main1, col_main2 = st.columns([1.5, 1])
        with col_main1:
            seed_kw = st.text_input("🌱 Target Seed Keyword", placeholder="e.g. AI Agents, CRM Software, Organic Coffee")
        with col_main2:
            industry = st.text_input("🏢 Industry Segment", placeholder="e.g. B2B SaaS, E-commerce, Healthcare")
            
        col_sub1, col_sub2, col_sub3 = st.columns(3)
        with col_sub1:
            audience = st.text_input("👥 Target Audience", placeholder="e.g. C-Level Execs, Gamers")
        with col_sub2:
            search_intent = st.selectbox("🔍 Search Intent Focus", ["Informational (How, What)", "Navigational (Brand)", "Commercial (Best, Top)", "Transactional (Buy, Pricing)"])
        with col_sub3:
            content_type = st.selectbox("📄 Content Container", ["Blog Post Framework", "Pillar Page", "Product Landing Page", "Silo Structure"])

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("⚡ Generate Enterprise SEO Architecture", use_container_width=True):
        if not api_key:
            st.error(f"⚠️ Please enter your {provider} API key in the sidebar.")
            st.stop()
            
        if not seed_kw.strip():
            st.warning("⚠️ Please provide a Target Seed Keyword.")
            st.stop()
            
        if not audience.strip() or not industry.strip():
            st.warning("⚠️ Target Audience or Industry Segment is missing. These are required for Enterprise-level context.")
            st.stop()

        with st.spinner(f"🔍 Synthesizing High-Value SERP Intent via {model}..."):
            try:
                start_time = time.time()
                result = process_keywords(seed_kw, content_type, audience, search_intent, industry, provider, api_key, model, temperature)
                end_time = time.time()
                
                delay = end_time - start_time
                st.success(f"✨ Architecture Deployment Complete! Synthesized in {delay:.2f} seconds.")
                
                # --- Result Dashboard ---
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(f'<span class="provider-badge">Core Engine: {provider}</span>', unsafe_allow_html=True)
                
                # Top Metrics Layer
                met = result.get("metrics", {})
                total_kws = met.get("total_keywords_found", sum([len(result.get(k, [])) for k in ["primary_keywords", "supporting_keywords", "long_tail_keywords", "question_keywords"]]))
                
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{total_kws}</div><div class="metric-label">Keywords Found</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{met.get("average_competition", "Medium")}</div><div class="metric-label">Avg. Competition</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{met.get("search_intent_match", "Mixed")}</div><div class="metric-label">Dominant Intent</div></div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                with st.expander("🧠 AI Strategic Outline", expanded=True):
                    st.info(result.get('analysis', 'No detailed analysis provided.'))
                
                st.markdown("<br>", unsafe_allow_html=True)

                # Dataframe rendering helper
                def render_table(title, subtitle, json_key):
                    st.markdown(f"#### {title}")
                    st.caption(subtitle)
                    data = result.get(json_key, [])
                    if data:
                        df = pd.DataFrame(data)
                        if not df.empty:
                            # Standardize columns to look professional in UI
                            if "keyword" in df.columns:
                                df.rename(columns={"keyword": "Keyword"}, inplace=True)
                            if "intent" in df.columns:
                                df.rename(columns={"intent": "Intent"}, inplace=True)
                            if "volume" in df.columns:
                                df.rename(columns={"volume": "Volume (Est)"}, inplace=True)
                            if "competition" in df.columns:
                                df.rename(columns={"competition": "Competition (Est)"}, inplace=True)
                            if "cpc" in df.columns:
                                df.rename(columns={"cpc": "CPC (Est)"}, inplace=True)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.write("No keywords generated for this section.")
                    else:
                        st.write("No keywords generated for this section.")
                    st.markdown("<br>", unsafe_allow_html=True)

                # Render Dataframes
                render_table("🥇 Primary Focus Keywords", "High-volume, highly competitive head terms to target centrally.", "primary_keywords")
                render_table("🥈 Semantic LSI Keywords", "Contextual terms to weave throughout the semantic content cluster.", "supporting_keywords")
                render_table("🎯 Long-Tail Opportunities", "Ultra-specific, low-competition phrases perfect for quick wins.", "long_tail_keywords")
                render_table("❓ FAQ / PAA Injections", "Targeted queries specifically mapped for H2/H3 tags and FAQ schemas.", "question_keywords")

                st.markdown('</div>', unsafe_allow_html=True)
                
                # Export Options
                st.markdown("### 💾 Export Keyword Plan")
                
                csv_col1, csv_col2 = st.columns([1, 4])
                
                # Consolidate ALL keywords into one big CSV for enterprise export
                all_kws = []
                for cat_name, key in [("Primary", "primary_keywords"), ("Supporting", "supporting_keywords"), ("Long Tail", "long_tail_keywords"), ("Question", "question_keywords")]:
                    for item in result.get(key, []):
                        if isinstance(item, dict):
                            item["Category"] = cat_name
                            all_kws.append(item)
                
                if all_kws:
                    full_df = pd.DataFrame(all_kws)
                    col_order = ["Category", "keyword", "intent", "volume", "competition", "cpc"]
                    # keep only existing columns, handle missing gracefully
                    col_order = [c for c in col_order if c in full_df.columns]
                    full_df = full_df[col_order]
                    csv_data = full_df.to_csv(index=False).encode('utf-8')
                    
                    with csv_col1:
                        st.download_button(
                            label="📊 Download CSV Dataset",
                            data=csv_data,
                            file_name=f"Enterprise_SEO_Plan_{seed_kw.replace(' ','_')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                with csv_col2:
                    st.download_button(
                        label="{ } Download Raw JSON",
                        data=json.dumps(result, indent=2),
                        file_name=f"Enterprise_SEO_Plan_{seed_kw.replace(' ','_')}.json",
                        mime="application/json",
                        use_container_width=False
                    )

            except Exception as e:
                import traceback
                st.error(f"❌ An error occurred with the AI Pipeline: {str(e)}")
                st.code(traceback.format_exc())

if __name__ == "__main__":
    main()


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
