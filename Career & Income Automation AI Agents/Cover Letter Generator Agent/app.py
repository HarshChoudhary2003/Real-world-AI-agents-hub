import streamlit as st
import time
from agent import generate_cover_letter, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Cover Letter AI Generator", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism) ---
st.markdown("""
<style>
/* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    color: #f8fafc;
}

/* Glassmorphism Title Card */
.title-container {
    padding: 3rem;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 2rem;
    text-align: center;
}

.title-container h1 {
    font-size: 3.5rem;
    background: linear-gradient(to right, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.title-container p {
    font-size: 1.2rem;
    color: #94a3b8;
}

/* Input Card Styling */
.stTextArea label, .stTextInput label, .stSelectbox label {
    font-weight: 600;
    color: #38bdf8 !important;
    font-size: 1.1rem;
    margin-bottom: 10px;
}

.stTextArea textarea, .stTextInput input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.1) !important;
}

/* Generate Button Call-to-Action */
.stButton button {
    width: 100%;
    height: 3.5rem;
    font-size: 1.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 12px;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5);
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
}

/* AI Response Card */
.response-card {
    background: rgba(30, 41, 59, 0.7);
    padding: 2rem;
    border-radius: 16px;
    border-left: 5px solid #38bdf8;
    margin-top: 2rem;
}

/* Footer & Sub-labels */
.footer {
    text-align: center;
    color: #64748b;
    margin-top: 5rem;
    font-size: 0.9rem;
    padding-bottom: 2rem;
}

/* Custom Dividers */
hr {
    border: 0;
    height: 1px;
    background: linear-gradient(to right, rgba(0,0,0,0), rgba(56,189,248,0.5), rgba(0,0,0,0));
    margin: 3rem 0;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar: AI Configuration ---
with st.sidebar:
    st.markdown("### 🤖 Intelligence Brain")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    model_choice = st.selectbox("Select Model", SUPPORTED_MODELS[provider])
    
    st.markdown("---")
    st.markdown("### 🔑 API Configuration")
    
    # Dynamic Key Placeholder based on provider
    provider_key_map = {
        "OpenAI": "OPENAI_API_KEY",
        "Google (Gemini)": "GEMINI_API_KEY",
        "Groq": "GROQ_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY"
    }
    
    user_api_key = st.text_input(
        f"{provider} API Key", 
        type="password", 
        help=f"Paste your {provider} key here. We use LiteLLM for universal routing."
    )
    
    st.info("Your key is used for this session only and is not stored.")
    st.markdown("---")
    st.markdown("#### 🛠️ Quick Steps")
    st.markdown("1. Enter API Key\n2. Paste Resume & Job Desc\n3. Click Generate")

# --- Header ---
st.markdown("""
    <div class="title-container">
        <h1>CareerOS Cover Letter AI</h1>
        <p>Multi-Model Intelligence Hub for Career Success ⚡</p>
    </div>
""", unsafe_allow_html=True)

# --- Main Interface ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📄 Step 1: Your Context")
    resume = st.text_area(
        "Paste Your Resume", 
        height=300, 
        placeholder="Copy paste your resume content here..."
    )
    
    company = st.text_input(
        "🏢 Target Company Name", 
        placeholder="e.g. Google, Tesla, a high-growth startup..."
    )

with col2:
    st.markdown("### 🧾 Step 2: Job Details")
    job_desc = st.text_area(
        "Job Description", 
        height=300, 
        placeholder="Paste the requirements and role description from the job posting..."
    )
    
    # Custom Selectors for Tone & Focus
    st.markdown("### ⚙️ Optimization Preferences")
    sel_col1, sel_col2, sel_col3 = st.columns(3)
    with sel_col1:
        tone = st.selectbox(
            "Communication Tone", 
            ["Professional", "Confident & Bold", "Creative", "Short & Punchy", "Friendly"]
        )
    with sel_col2:
        focus = st.selectbox(
            "Strategy Focus", 
            ["Overall Fit", "Technical Expertise", "Leadership & Impact", "Growth & Culture"]
        )
    with sel_col3:
        num_variants = st.select_slider(
            "Variations",
            options=[1, 2, 3],
            value=1
        )

# --- Generate Action ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Craft My Cover Letters"):
    if not resume or not job_desc:
        st.error("⚠️ Please provide both your resume and the job description to continue.")
    else:
        results = []
        with st.status(f"🧠 Generating {num_variants} Curated Variations...", expanded=True) as status:
            for i in range(1, num_variants + 1):
                st.write(f"✍️ Synthesizing Variation #{i}...")
                letter = generate_cover_letter(
                    resume=resume, 
                    job_description=job_desc, 
                    model=model_choice,
                    company=company if company else "the company",
                    tone=tone,
                    focus=focus,
                    variation_index=i,
                    api_key=user_api_key if user_api_key else None
                )
                results.append(letter)
            status.update(label=f"✅ Success! {num_variants} Variations Generated.", state="complete", expanded=False)
        
        # Display Output
        st.markdown("---")
        
        if num_variants > 1:
            tabs = st.tabs([f"📄 Variation {i}" for i in range(1, num_variants + 1)])
            for i, tab in enumerate(tabs):
                with tab:
                    st.text_area(f"Cover Letter {i+1}", value=results[i], height=500, key=f"out_{i}")
                    st.download_button(
                        f"⬇️ Download Variation {i+1}",
                        results[i],
                        file_name=f"Letter_V{i+1}_{company}.txt",
                        mime="text/plain",
                        key=f"dl_{i}"
                    )
        else:
            st.markdown("### ✉️ Final Tailored Cover Letter")
            st.text_area("Draft Copy", value=results[0], height=500, key="output_letter")
            st.download_button(
                label="⬇️ Download as Text File",
                data=results[0],
                file_name=f"CoverLetter_{company}.txt",
                mime="text/plain",
                use_container_width=True
            )

# --- Footer ---
st.markdown("""
    <div class="footer">
        Powered by OpenAI GPT-4o-mini & CareerOS Intelligence Hub Core<br>
        Built by Antigravity Agent • career-growth-suite v2.0
    </div>
""", unsafe_allow_html=True)
