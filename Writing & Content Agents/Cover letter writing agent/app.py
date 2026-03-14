import streamlit as st
import json
import os
import re
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables
load_dotenv()

# Suppress litellm logging for a cleaner console
litellm.suppress_debug_info = True

# --- Page Configuration ---
st.set_page_config(
    page_title="CoverLetter Pro | Advanced Pitch Engine",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
/* Main background and text */
.stApp {
    background-color: #0B0E14; 
    color: #FAFAFA;
}

/* Headers */
h1, h2, h3 {
    color: #FF416C;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
}

/* Custom styling for the main container */
.main-header {
    background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
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
    background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
    color: #FFFFFF !important;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 65, 108, 0.4);
}

/* Text Areas */
.stTextArea textarea {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #334155 !important;
    border-radius: 8px;
}
.stTextArea textarea:focus {
    border-color: #FF416C !important;
    box-shadow: 0 0 0 1px #FF416C !important;
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
    color: #FF416C !important;
    border-bottom: 2px solid #FF416C !important;
}

/* Enhanced Metrics */
div[data-testid="stMetricValue"] {
    color: #FF416C;
}
</style>
""", unsafe_allow_html=True)

# --- Agent Logic ---
def get_system_prompt(tone, length, specific_focus):
    focus_instruction = ""
    if specific_focus:
        focus_instruction = f"\nCRITICAL INSTRUCTION: You MUST heavily highlight the following asset/project/metric naturally within the text: '{specific_focus}'"

    if length == "Short & Punchy (2 paragraphs)":
        length_inst = "Exactly 2 concise, hard-hitting paragraphs. No fluff."
    elif length == "Standard (3-4 paragraphs)":
        length_inst = "Exactly 3 to 4 paragraphs. Hook, Body (proof), Close."
    else:
        length_inst = "Exactly 4 to 5 detailed paragraphs. Elaborate deeply on the technical mapping."

    return f"""
You are a highly advanced Cover Letter Writing Agent.

Your precise mission:
1. Analyze the user's provided resume/background.
2. Analyze the strictly provided target job description.
3. Write a highly persuasive, concise, and role-specific cover letter that bridges the user's experience perfectly to the company's pain points.
4. Adhere strictly to the chosen Tone: {tone}
5. The length must be: {length_inst}
6. Preserve factual accuracy—DO NOT invent metrics or roles the user hasn't listed.
{focus_instruction}

Return strictly valid JSON matching this exact schema:
{{
  "company": "string (the company name extracted or inferred)",
  "role": "string (the role being applied to)",
  "cover_letter": "string (the formatted text of the cover letter)"
}}
"""

def generate_cover_letter_api(resume_text, job_text, model_name, api_key, tone, length, specific_focus):
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

    system_content = get_system_prompt(tone, length, specific_focus)

    prompt = f"""
RESUME / BACKGROUND:
{resume_text}

TARGET JOB DESCRIPTION:
{job_text}

CRITICAL REQUIREMENT: Return ONLY valid JSON format with no Markdown wrappers around the JSON, no thoughts, and no backticks.
"""
    
    response = litellm.completion(
        model=model_name,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4 # slightly higher for creativity
    )
    
    content = response.choices[0].message.content.strip()
    
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
    today = date.today().strftime('%B %d, %Y')
    role = data.get("role", "[Target Role]")
    company = data.get("company", "[Target Company]")
    body = data.get("cover_letter", "")
    
    out = f"Date: {today}\n"
    out += f"Subject: Application for {role} at {company}\n"
    out += "=" * 50 + "\n\n"
    out += body + "\n"
        
    return out

def analyze_keyword_density(jd_text, cv_text):
    """A simplistic visual metric generator showing how many 'JD' words made it into the letter."""
    stop_words = set(["the", "and", "a", "to", "of", "in", "i", "is", "that", "it", "on", "you", "this", "for", "but", "with", "are", "have", "be", "at", "or", "as", "was", "so", "if", "out", "not", "we"])
    
    # Extract words > 4 chars to find 'keywords' loosely
    jd_words = set([w.lower() for w in re.findall(r'[a-zA-Z]{5,}', jd_text)]) - stop_words
    cv_words = set([w.lower() for w in re.findall(r'[a-zA-Z]{5,}', cv_text)]) - stop_words
    
    if not jd_words:
        return 0, [], []
        
    matched = jd_words.intersection(cv_words)
    missing = jd_words - matched
    
    score = int((len(matched) / len(jd_words)) * 100) if len(jd_words) > 0 else 0
    return score, list(matched)[:15], list(missing)[:15]

# --- UI Layout ---

# Sidebar for Settings & Info
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/secured-letter.png", width=64)
    st.title("CoverLetter Pro")
    st.caption("v4.0.0 | Advanced Orchestration")
    
    st.markdown("---")
    
    st.subheader("⚙️ AI Engine Selection")
    
    # Model Selector
    model_options = {
        "Anthropic Claude 3.5 Sonnet (Best Writer)": "claude-3-5-sonnet-20240620",
        "OpenAI GPT-4o (Most Accurate)": "gpt-4o",
        "OpenAI GPT-4o Mini (Fast & Cheap)": "gpt-4o-mini",
        "Google Gemini 1.5 Pro (Deep Context)": "gemini/gemini-1.5-pro",
        "Groq LLaMA 3 70B (Ultra-Fast)": "groq/llama3-70b-8192"
    }
    selected_model_label = st.selectbox("LLM Provider", list(model_options.keys()))
    selected_model = model_options[selected_model_label]
    
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
        f"{provider} Key", 
        value=env_key, 
        type="password", 
        placeholder=f"Enter {provider} key..."
    )
        
    st.markdown("---")
    st.subheader("🎛️ Advanced Tone & Style")
    
    tone_choice = st.selectbox("Preferred Narrative Tone", [
        "Confident & Direct (No fluff, high impact)",
        "Traditional & Formal (Best for Finance/Law)",
        "Story-Driven & Passionate (Best for Startups)",
        "Technical & Analytical (Best for Engineering)"
    ])
    
    length_choice = st.select_slider("Letter Length", options=["Short & Punchy (2 paragraphs)", "Standard (3-4 paragraphs)", "Detailed & Comprehensive"])
    
    focus_choice = st.text_input("🎯 Specific Focus (Optional)", placeholder="E.g. Highlight my 20% revenue growth project")
    
    st.markdown("---")
    st.markdown("© 2026 AI Agent Factory")

# Main Dashboard
st.markdown('<h1 class="main-header">Advanced Pitch Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Feed in constraints, specify your narrative style, and generate a meticulously optimized cover letter proven to cut through the noise.</p>', unsafe_allow_html=True)

page_tabs = st.tabs(["✉️ Drafting Environment", "📊 Semantic Output Analysis"])

# Globals for session state context mapping
if "last_letter" not in st.session_state:
    st.session_state["last_letter"] = None
    st.session_state["last_jd"] = None

with page_tabs[0]:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("1. Ground Truth (Your Resume)")
        resume_input = st.text_area(
            "Raw Experience / Bullet Points", 
            height=280,
            placeholder="E.g.\nBackground: 5 years experience in scalable systems..."
        )

    with col2:
        st.subheader("2. Target Mapping (Job Description)")
        job_input = st.text_area(
            "Full Job Listing", 
            height=280,
            placeholder="E.g.\nCompany: Stripe\nRole: Backend Lead\nRequirements: Define scalable architectures..."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn, col_empty = st.columns([1, 3])
    with col_btn:
        generate_btn = st.button("🚀 Synthesize Letter", use_container_width=True)

    st.markdown("<hr style='border:1px solid #334155; margin-top:1rem; margin-bottom:2rem;'>", unsafe_allow_html=True)

    # Results Area
    if generate_btn:
        if not resume_input or not job_input:
            st.error("⚠️ Please provide your background and the job description to proceed.")
        elif not user_api_key:
            st.error(f"⚠️ Your {provider} API Key is required to power the inference engine.")
        else:
            try:
                with st.spinner(f"⚡ Processing through {provider} Engine... applying Tone: {tone_choice}..."):
                    result_json = generate_cover_letter_api(resume_input, job_input, selected_model, user_api_key, tone_choice, length_choice, focus_choice)
                    st.session_state["last_letter"] = result_json.get("cover_letter", "")
                    st.session_state["last_jd"] = job_input
                    
                st.success("🎯 Synthesis complete! Your highly tailored cover letter is ready.")
                
                tab1, tab2, tab3 = st.tabs(["✉️ Final Document", "💻 Data Payload", "📥 Exports"])
                
                with tab1:
                    st.markdown(f"**To:** Hiring Manager, {result_json.get('company', 'Target Company')}")
                    st.markdown(f"**Regarding:** {result_json.get('role', 'Target Role')} position")
                    st.markdown("---")
                    
                    for paragraph in result_json.get("cover_letter", "").split('\n\n'):
                        st.write(paragraph)
                        
                with tab2:
                    st.json(result_json)
                    
                with tab3:
                    dl_col1, dl_col2, dl_empty = st.columns([1, 1, 2])
                    txt_content = format_text_output(result_json)
                    with dl_col1:
                        st.download_button(
                            label="📄 Download TXT",
                            data=txt_content,
                            file_name=f"CoverLetter_{result_json.get('company', 'Company')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with dl_col2:
                        st.download_button(
                            label="💻 Download JSON",
                            data=json.dumps(result_json, indent=2),
                            file_name=f"CoverLetter_{result_json.get('company', 'Company')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                        
            except Exception as e:
                st.error(f"❌ Synthesis Error: {str(e)}")
                st.info("Check API key validity and billing quotas for the selected provider.")

with page_tabs[1]:
    st.markdown("## 📊 Semantic Resonance Analysis")
    st.markdown("Once you generate a letter, this engine compares the output against the target Job Description to visualize how closely you are hitting their core requirements.")
    
    if st.session_state["last_letter"] and st.session_state["last_jd"]:
        score, matched, missing = analyze_keyword_density(st.session_state["last_jd"], st.session_state["last_letter"])
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("JD Relevancy Score", f"{score}%", "+20% optimal threshold")
        col_m2.metric("Extracted JD Keywords", str(len(matched) + len(missing)))
        col_m3.metric("Letter Length (Words)", str(len(st.session_state["last_letter"].split())))
        
        st.markdown("---")
        
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.markdown("### ✅ Keywords Hit")
            st.caption("These complex terms from the JD successfully made it into your letter.")
            if matched:
                st.markdown("  ".join([f"`{m}`" for m in matched]))
            else:
                st.write("No major keywords matched.")
                
        with col_k2:
            st.markdown("### ❌ Missing Concepts (Optional)")
            st.caption("You might want to manually weave these into your letter if they are crucial hard skills.")
            if missing:
                st.markdown("  ".join([f"`{m}`" for m in missing]))
            else:
                st.write("Perfect alignment! No missing concepts detected.")
    else:
        st.info("⚠️ Generate a cover letter first to view the semantic analysis.")
