import streamlit as st
import time
from agent import fetch_jobs, calculate_match_score, SUPPORTED_MODELS

# --- Page Config ---
st.set_page_config(
    page_title="Job Finder Agent", 
    page_icon="🔍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Premium Glassmorphism & Card System) ---
# (Styles remain same)
st.markdown("""
<style>
/* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #020617 100%);
    color: #f8fafc;
}

/* Glassmorphism Title Card */
.title-container {
    padding: 2.5rem;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 2.5rem;
    text-align: center;
}

.title-container h1 {
    font-size: 3.2rem;
    background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}

.title-container p {
    font-size: 1.1rem;
    color: #94a3b8;
}

/* Input Fields */
.stTextInput input, .stTextArea textarea {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    color: #f8fafc !important;
    border-radius: 10px !important;
}

/* Premium Job Card */
.job-card {
    background: rgba(30, 41, 59, 0.4);
    padding: 1.8rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.job-card:hover {
    transform: translateY(-5px);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    background: rgba(30, 41, 59, 0.6);
}

.match-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    padding: 0.4rem 0.8rem;
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 700;
}

.score-high { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.score-mid { background: rgba(234, 179, 8, 0.15); color: #fbbf24; border: 1px solid rgba(234, 179, 8, 0.3); }
.score-low { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }

.company-logo {
    width: 50px;
    height: 50px;
    border-radius: 8px;
    margin-right: 1rem;
    object-fit: contain;
    background: white;
    padding: 2px;
}

/* CTA Button */
.stButton button {
    width: 100%;
    height: 3.2rem;
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    color: white;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    transition: all 0.4s ease;
}

.stButton button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(79, 70, 229, 0.4);
}

.footer {
    text-align: center;
    color: #475569;
    margin-top: 5rem;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🔐 API Keys")
    rapid_key = st.text_input("RapidAPI (JSearch) Key", type="password", help="Get from rapidapi.com/jsearch")
    
    st.markdown("---")
    st.markdown("### 🧬 AI Match Core")
    provider = st.selectbox("AI Provider", list(SUPPORTED_MODELS.keys()))
    match_model = st.selectbox("Intelligence Model", SUPPORTED_MODELS[provider])
    
    user_api_key = st.text_input(
        f"{provider} API Key", 
        type="password", 
        help=f"Paste your {provider} key here for AI matching."
    )
    
    st.info("The match score compares your resume directly with the job description.")

# --- Header ---
st.markdown("""
<div class="title-container">
    <h1>Job Finder Agent</h1>
    <p>Discover opportunities and calculate relevance with AI in real-time. ⚡</p>
</div>
""", unsafe_allow_html=True)

# --- Main Layout ---
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("### 🔍 Search Profile")
    search_role = st.text_input("💼 Target Job Role", placeholder="e.g. Senior Frontend Engineer")
    search_loc = st.text_input("📍 Preferred Location", placeholder="e.g. Remote / New York")
    
with col2:
    st.markdown("### 📄 Personal Context (Optional)")
    user_resume = st.text_area("Paste Resume", height=152, placeholder="Paste your resume here to see AI match scores for every listing...")

# --- Search Logic ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Scrape Live Jobs Pipeline"):
    if not search_role or not search_loc:
        st.error("⚠️ Please specify a Role and Location to search.")
    else:
        with st.status("🔍 Connecting to Recruitment Nodes...", expanded=True) as status:
            st.write("🌐 Fetching global career data...")
            time.sleep(1)
            jobs_data = fetch_jobs(search_role, search_loc, api_key=rapid_key if rapid_key else None)
            
            if isinstance(jobs_data, dict) and "error" in jobs_data:
                status.update(label=f"❌ Error", state="error")
                st.error(jobs_data["error"])
            else:
                status.update(label=f"✅ Found {len(jobs_data)} High-Sync Results", state="complete")
                st.session_state["found_jobs"] = jobs_data
                st.session_state["triggered_search"] = True

# --- Results Rendering ---
if st.session_state.get("triggered_search") and "found_jobs" in st.session_state:
    st.markdown("---")
    st.markdown(f"### 🎯 Results for: {search_role} in {search_loc}")
    
    for idx, job in enumerate(st.session_state["found_jobs"]):
        # Match Score Calculation
        match_score = None
        match_analysis = None
        
        if user_resume and (user_api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")):
            # Placeholder for premium "Compute Match" button per job 
            # Or run it automatically for top results
            if idx < 3: # Auto-calculate for top 3 to save tokens
                match_score, match_analysis = calculate_match_score(
                    user_resume, 
                    job["description"], 
                    model=match_model, 
                    api_key=user_api_key if user_api_key else None
                )
        
        # Determine CSS Class for badge
        badge_class = "score-low"
        if match_score:
            if match_score >= 80: badge_class = "score-high"
            elif match_score >= 60: badge_class = "score-mid"

        # Render Job Card
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <div class="match-badge {badge_class}">Match Score: {match_score if match_score else "??"}%</div>
                <div style="display: flex; align-items: center;">
                    <img src="{job['logo'] if job['logo'] else 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'}" class="company-logo">
                    <div>
                        <h4 style="margin: 0; color: #fff;">{job['title']}</h4>
                        <p style="margin: 0; color: #6366f1; font-weight: 600;">{job['company']}</p>
                    </div>
                </div>
                <p style="margin: 0.8rem 0; font-size: 0.9rem; color: #94a3b8;">
                    📍 {job['location']} | 📅 Posted {job['posted_at']}
                </p>
                <div style="margin-top: 1rem; color: #cbd5e1; font-size: 0.85rem;">
                    {match_analysis if match_analysis else "Paste resume and provide API keys in sidebar to unlock AI match scoring for this listing."}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action Buttons for the Card
            btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 6])
            with btn_col1:
                st.link_button("🔗 Apply Now", job["link"], use_container_width=True)
            with btn_col2:
                # Custom trigger to pass job description to Agent #2 (Cover Letter)
                if st.button("✉️ Draft Cover Letter", key=f"cl_{idx}", use_container_width=True):
                    st.info(f"Feature Link Incoming: Copying job description for {job['company']}...")
                    st.session_state["target_job_desc"] = job["description"]
                    st.session_state["target_company"] = job["company"]
                    st.success("Redirecting to Cover Letter Generator... (Navigate manually or use Master Hub)")

# --- Footer ---
st.markdown("""
<div class="footer">
    Driven by CareerOS JSearch API Framework • AI-Model: GPT-4o-mini<br>
    Architected by Antigravity Agent
</div>
""", unsafe_allow_html=True)
