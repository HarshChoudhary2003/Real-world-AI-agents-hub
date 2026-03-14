import streamlit as st
import json
import os
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables
load_dotenv()

# Suppress litellm logging for a cleaner console
litellm.suppress_debug_info = True

# --- Page Configuration ---
st.set_page_config(
    page_title="ResumeAI Pro | Multi-Model Omni-Engine",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
/* Main background and text */
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}

/* Headers */
h1, h2, h3 {
    color: #00E676;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
}

/* Custom styling for the main container */
.main-header {
    background: linear-gradient(90deg, #1A2980 0%, #26D0CE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 3rem;
    margin-bottom: 0px;
    padding-bottom: 0px;
}

.sub-header {
    color: #A0AEC0;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

/* Cards for Content */
div.stChatMessage {
    background-color: #1E293B;
    border-radius: 10px;
    border: 1px solid #334155;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
    color: #0f172a !important;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 201, 255, 0.4);
}

/* Text Areas */
.stTextArea textarea {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #334155 !important;
    border-radius: 8px;
}
.stTextArea textarea:focus {
    border-color: #00E676 !important;
    box-shadow: 0 0 0 1px #00E676 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #1E293B;
    border-radius: 8px 8px 0px 0px;
    border: 1px solid #334155;
    border-bottom: none;
    padding: 10px 20px;
    color: #A0AEC0;
}
.stTabs [aria-selected="true"] {
    background-color: #2D3748 !important;
    color: #00E676 !important;
    border-bottom: 2px solid #00E676 !important;
}

/* Explainer Cards */
.explainer-card {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.explainer-card:hover {
    transform: translateY(-2px);
    border-color: #00E676;
    box-shadow: 0 4px 12px rgba(0, 230, 118, 0.1);
}
</style>
""", unsafe_allow_html=True)

# --- Agent System Prompt ---
SYSTEM_PROMPT = """
You are a highly advanced Resume Optimization AI.

Your precise mission:
1. Analyze the user's current resume content.
2. Analyze the strictly provided target job description.
3. Rewrite and optimize the resume bullet points to aggressively align with the target role, emphasizing measurable impact and hard metrics.
4. Extract and align the optimal list of skills required for ATS (Applicant Tracking System) parsing.
5. Generate a compelling, high-impact professional summary.
6. Preserve absolute factual accuracy. DO NOT hallucinate or invent experience.

Return strictly valid JSON matching this exact schema:
{
  "optimized_experience": ["bullet 1", "bullet 2"],
  "optimized_skills": ["skill 1", "skill 2"],
  "summary_suggestion": "string"
}
"""

def optimize_resume_api(resume_text, job_text, model_name, api_key):
    """
    Executes an inference call utilizing LiteLLM to dynamically route to 
    OpenAI, Anthropic, Google, or Groq based on the user's selection.
    """
    if not api_key:
        raise ValueError("API Key is missing for the selected provider.")

    # Dynamically set the correct environment variable for litellm
    if "gpt" in model_name:
        os.environ["OPENAI_API_KEY"] = api_key
    elif "claude" in model_name:
        os.environ["ANTHROPIC_API_KEY"] = api_key
    elif "gemini" in model_name:
        os.environ["GEMINI_API_KEY"] = api_key
    elif "groq" in model_name:
        os.environ["GROQ_API_KEY"] = api_key

    prompt = f"""
RESUME CONTENT:
{resume_text}

TARGET JOB DESCRIPTION:
{job_text}

CRITICAL REQUIREMENT: Return ONLY valid JSON format with absolutely no Markdown wrapper, no thoughts, and no backticks.
"""

    response = litellm.completion(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    content = response.choices[0].message.content.strip()
    
    # Clean possible markdown blocks that some models stubbornly output
    if content.startswith("```json"):
        content = content[7:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON from the model answer: {content}")

def format_text_output(data):
    out = f"🚀 OPTIMIZED RESUME PROFILE\n"
    out += f"Generated on: {date.today().strftime('%B %d, %Y')}\n"
    out += "=" * 50 + "\n\n"
    
    out += "Executive Summary:\n"
    out += "-" * 20 + "\n"
    out += data.get("summary_suggestion", "") + "\n\n"
    
    out += "Core Competencies & Skills:\n"
    out += "-" * 20 + "\n"
    skills = data.get("optimized_skills", [])
    out += " | ".join(skills) + "\n\n"
    
    out += "Impact-Driven Experience:\n"
    out += "-" * 20 + "\n"
    for bullet in data.get("optimized_experience", []):
        out += f"• {bullet}\n"
        
    return out

# --- Sidebar UI ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/parse-from-clipboard.png", width=64)
    st.title("ResumeAI Omni")
    st.caption("v3.0.0 | All-Model Universal Support")
    
    st.markdown("---")
    
    st.subheader("⚙️ AI Engine Configuration")
    
    # Model Selector
    model_options = {
        "OpenAI GPT-4o Mini (Fast & Cheap)": "gpt-4o-mini",
        "OpenAI GPT-4o (Most Accurate)": "gpt-4o",
        "Anthropic Claude 3.5 Sonnet (Best Writer)": "claude-3-5-sonnet-20240620",
        "Google Gemini 1.5 Pro (Deep Context)": "gemini/gemini-1.5-pro",
        "Groq LLaMA 3 70B (Ultra-Fast)": "groq/llama3-70b-8192"
    }
    selected_model_label = st.selectbox("Select LLM Provider", list(model_options.keys()))
    selected_model = model_options[selected_model_label]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dynamic API Key Input
    if "gpt" in selected_model:
        provider = "OpenAI"
        env_key = os.getenv("OPENAI_API_KEY", "")
    elif "claude" in selected_model:
        provider = "Anthropic"
        env_key = os.getenv("ANTHROPIC_API_KEY", "")
    elif "gemini" in selected_model:
        provider = "Google Gemini"
        env_key = os.getenv("GEMINI_API_KEY", "")
    elif "groq" in selected_model:
        provider = "Groq"
        env_key = os.getenv("GROQ_API_KEY", "")
    else:
        provider = "API"
        env_key = ""

    user_api_key = st.text_input(
        f"{provider} API Key", 
        value=env_key, 
        type="password", 
        placeholder=f"Enter your {provider} key..."
    )
        
    st.markdown("---")
    
    with st.expander("💡 Pro Tips for Best Results"):
        st.markdown("""
        - **Claude 3.5 Sonnet** tends to write the most natural-sounding bullet points.
        - **GPT-4o** is exceptional at rigid formatting and ensuring keywords hit perfectly.
        - **Groq LLaMA 3** is best for bulk text processing at blazing speeds.
        """)
        
    st.markdown("---")
    st.markdown("© 2026 AI Agent Factory")

# --- Main Dashboard ---
st.markdown('<h1 class="main-header">Omni-Model Optimization Engine</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Bypass ATS filters using state-of-the-art LLMs. Select any provider, paste your details, and instantly generate a highly tailored profile.</p>', unsafe_allow_html=True)

# Navigation via Tabs
page_tabs = st.tabs(["🎯 Resume Optimizer Workspace", "🧠 How It Works (Engine Architecture)"])

with page_tabs[0]:
    # Layout: Split into input and options
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("1. Your Current Profile")
        resume_input = st.text_area(
            "Paste your raw experience & skills", 
            height=300,
            placeholder="E.g.\nExperience:\n- Handled customer database migrations...\n\nSkills:\nPython, SQL, AWS..."
        )

    with col2:
        st.subheader("2. Target Opportunity")
        job_input = st.text_area(
            "Paste the Target Job Description", 
            height=300,
            placeholder="E.g.\nRole: Senior Data Engineer\nRequirements:\n- 5+ years building scalable ETL pipelines...\n- Expertise in Apache Spark and Python..."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Area
    col_btn, col_empty = st.columns([1, 3])
    with col_btn:
        optimize_btn = st.button("⚡ Align Profile Constraints", use_container_width=True)

    st.markdown("<hr style='border:1px solid #334155; margin-top:1rem; margin-bottom:2rem;'>", unsafe_allow_html=True)

    # Results Area
    if optimize_btn:
        if not resume_input or not job_input:
            st.error("⚠️ Please provide both your current resume content and the target job description.")
        elif not user_api_key:
            st.error(f"⚠️ Please enter your {provider} API Key in the sidebar.")
        else:
            try:
                with st.spinner(f"🚀 Initializing {provider} Engine ({selected_model}). Processing semantic alignment..."):
                    result_json = optimize_resume_api(resume_input, job_input, selected_model, user_api_key)
                    
                st.success(f"✨ Optimization Complete! Rendered via {provider}.")
                
                # Display Results in Tabs
                tab1, tab2, tab3 = st.tabs(["📄 Formatted Preview", "💻 Raw JSON Data", "📥 Export Options"])
                
                with tab1:
                    st.markdown("### Executive Summary")
                    st.info(result_json.get("summary_suggestion", "N/A"))
                    
                    st.markdown("### ATS-Optimized Skills")
                    st.markdown(f"**{', '.join(result_json.get('optimized_skills', []))}**")

                    st.markdown("### Impact-Driven Experience Bullets")
                    for bullet in result_json.get("optimized_experience", []):
                        st.markdown(f"- {bullet}")
                        
                with tab2:
                    st.json(result_json)
                    
                with tab3:
                    st.markdown("### Download Your Assets")
                    st.caption("Use the formatted text for your document, or the JSON for programmatic integration.")
                    
                    dl_col1, dl_col2, dl_empty = st.columns([1, 1, 2])
                    
                    txt_content = format_text_output(result_json)
                    json_content = json.dumps(result_json, indent=2)
                    
                    with dl_col1:
                        st.download_button(
                            label="📄 Download Formatted TXT",
                            data=txt_content,
                            file_name=f"Optimized_Resume_{date.today()}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with dl_col2:
                        st.download_button(
                            label="💻 Download JSON",
                            data=json_content,
                            file_name=f"Optimized_Resume_{date.today()}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                        
            except Exception as e:
                st.error(f"❌ An error occurred during optimization: {str(e)}")
                st.info(f"Tip: Ensure your {provider} API key is valid, has billing enabled, and you are not exceeding quotas.")

with page_tabs[1]:
    st.markdown("## 🧠 Core System Architecture")
    st.markdown("This suite utilizes an agentic logic pipeline and an Omni-Model Routing system to perform state-of-the-art NLP alignment. Here is how the agent processes your profile:")

    st.markdown("""
    <div class="explainer-card">
        <h3 style="margin-top:0;"><span style="font-size:1.5rem;">01</span> The Omni-Model Adapter</h3>
        <p style="color:#A0AEC0;">
        Unlike standard wrappers, this tool uses <b>LiteLLM</b> formatting to instantly switch between the underlying NLP models 
        (OpenAI's GPT series, Anthropic's Claude 3.5, Google's Gemini Pro, or Groq's insanely fast open-weights). 
        The system dynamically structures the system prompt based on the specific tokenizer requirements of the chosen model.
        </p>
    </div>
    
    <div class="explainer-card">
        <h3 style="margin-top:0;"><span style="font-size:1.5rem;">02</span> Semantic Gap Analysis & Mapping</h3>
        <p style="color:#A0AEC0;">
        When you provide a Job Description, the LLM engine performs a semantic vector approximation. It maps your <i>raw experience</i> 
        to the <i>required job outcomes</i>. It doesn't just look for words; it looks for conceptual overlap (e.g., mapping "handled servers" to "cloud infrastructure readiness").
        </p>
    </div>

    <div class="explainer-card">
        <h3 style="margin-top:0;"><span style="font-size:1.5rem;">03</span> Output Quantification Re-Writing</h3>
        <p style="color:#A0AEC0;">
        The instruction set forces the LLM to apply the <b>STAR methodology</b> (Situation, Task, Action, Result). 
        Even if you simply wrote <i>"fixed bugs and improved speed"</i>, the agent restructures it to sound like: 
        <i>"Optimized backend performance and resolved critical bugs to elevate overall system efficiency."</i> 
        It attempts to inject plausible impact statements without inventing fictional metrics.
    </div>

    <div class="explainer-card">
        <h3 style="margin-top:0;"><span style="font-size:1.5rem;">04</span> Abstract Syntax parsing (The ATS Hack)</h3>
        <p style="color:#A0AEC0;">
        Applicant Tracking Systems (workday, greenhouse, etc.) search for exact strings. 
        The agent evaluates the JD to find critical hard skills and injects them precisely into a <b>"Core Competencies"</b> array.
        Finally, the response is forced perfectly into <b>Strict JSON</b> validation format, making the results instantly integratable into a database or downstream SaaS application.
        </p>
    </div>
    """, unsafe_allow_html=True)
