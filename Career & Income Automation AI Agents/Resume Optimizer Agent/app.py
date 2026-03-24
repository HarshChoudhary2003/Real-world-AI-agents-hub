import streamlit as st
import json
import os
from openai import OpenAI
from google import generativeai as genai
from dotenv import load_dotenv

# Page Config
st.set_page_config(
    page_title="Resume Forge | ATS Optimization",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- UI State ---
if "provider" not in st.session_state:
    st.session_state.provider = "OpenAI"
if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"
if "match_score" not in st.session_state:
    st.session_state.match_score = 0
if "optimized_data" not in st.session_state:
    st.session_state.optimized_data = None

# --- Providers & Models Mappings ---
LLM_MANIFEST = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
    "Google Gemini": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
}

# --- SaaS Premium UI (Vercel/Linear Style) ---
def inject_premium_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@700;800&display=swap');
        
        :root {
            --bg-main: #020202;
            --bg-card: #0a0a0a;
            --accent: #5e5ce6; /* Linear Blue */
            --border: #1f1f1f;
            --text-primary: #ffffff;
            --text-secondary: #888888;
        }

        .main { background: var(--bg-main); color: var(--text-primary); }
        [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid var(--border); }
        [data-testid="stHeader"] { background: transparent; }
        footer { visibility: hidden; }
        .stDeployButton { display: none; }

        h1, h2, h3, p, span, div { font-family: 'Inter', sans-serif !important; }
        
        /* KPI Cards */
        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s ease;
        }
        .kpi-card:hover { border-color: #444; transform: translateY(-2px); }
        .kpi-label { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }
        .kpi-value { font-size: 1.8rem; font-weight: 800; color: var(--text-primary); }

        /* Resume Output Box */
        .resume-box {
            background: #050505;
            border: 1px solid var(--border);
            padding: 2rem;
            border-radius: 8px;
            font-size: 0.95rem;
            line-height: 1.6;
            color: #ddd;
            font-family: 'Inter', sans-serif !important;
            white-space: pre-wrap;
        }

        /* Keyword Badge */
        .kw-badge {
            background: rgba(94, 92, 230, 0.1);
            border: 1px solid rgba(94, 92, 230, 0.2);
            padding: 4px 10px;
            border-radius: 5px;
            font-size: 0.8rem;
            color: #5e5ce6;
            margin-right: 8px;
            margin-bottom: 8px;
            display: inline-block;
        }

        /* Sidebar Branding */
        .sidebar-brand { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 1.5rem; color: #fff; margin-bottom: 2rem; }
        </style>
    """, unsafe_allow_html=True)

def sidebar_nav():
    with st.sidebar:
        st.markdown("<div class='sidebar-brand'>💼 Resume Forge</div>", unsafe_allow_html=True)
        nav = st.radio("Dashboard", ["Optimizer Studio", "Strategic Insights", "Template Library"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#666; font-size:0.7rem;'>PROVIDER GATEWAY</p>", unsafe_allow_html=True)
        st.session_state.provider = st.selectbox("LLM Gateway", list(LLM_MANIFEST.keys()), index=0, label_visibility="collapsed")
        
        st.markdown("<p style='color:#666; font-size:0.7rem; margin-top:1rem;'>NEURAL SELECTION</p>", unsafe_allow_html=True)
        st.session_state.model = st.selectbox("Neural Model", LLM_MANIFEST[st.session_state.provider], index=0, label_visibility="collapsed")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(94,92,230,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(94,92,230,0.1);'>
                <div style='font-size:0.7rem; color:#5e5ce6; font-weight:600;'>INTERNAL STATUS</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'>Active Engine // High Integrity</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def run_optimization(resume, jd, provider, model):
    from agent import ResumeOptimizerAgent
    agent = ResumeOptimizerAgent(provider, model)
    return agent.optimize(resume, jd)

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    if current_nav == "Optimizer Studio":
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.5rem; letter-spacing: -0.05em; font-weight: 800;'>Optimizer Studio.</h1>
                    <p style='color:var(--text-secondary); font-size:1.1rem;'>Professional ATS alignment and resume synchronization.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_in1, col_in2 = st.columns(2)
        with col_in1:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem; letter-spacing:0.1em; font-weight:700;'>SOURCE RESUME</h4>", unsafe_allow_html=True)
            resume_text = st.text_area("source_resume", placeholder="Paste current professional resume text here...", height=350, label_visibility="collapsed")
        with col_in2:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem; letter-spacing:0.1em; font-weight:700;'>TARGET JOB DESCRIPTION</h4>", unsafe_allow_html=True)
            jd_text = st.text_area("jd_text", placeholder="Paste the target job description here...", height=350, label_visibility="collapsed")

        if st.button("SYNCHRONIZE RESUME", use_container_width=True):
            if resume_text and jd_text:
                with st.status("Initializing Neural Forge...", expanded=True) as status:
                    res = run_optimization(resume_text, jd_text, st.session_state.provider, st.session_state.model)
                    st.session_state.optimized_data = res
                    status.update(label="Synchronization Complete", state="complete")
                    st.rerun()

        if st.session_state.optimized_data:
            res = st.session_state.optimized_data
            st.markdown("<br><hr style='border-color:#111'><br>", unsafe_allow_html=True)
            
            # Analytics Row
            a1, a2, a3 = st.columns(3)
            with a1:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">ATS Match Score</div><div class="kpi-value">{res["match_score"]}%</div></div>', unsafe_allow_html=True)
            with a2:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">Keywords Found</div><div class="kpi-value">{len(res["missing_keywords"])} Detected</div></div>', unsafe_allow_html=True)
            with a3:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">Strategic Integrity</div><div class="kpi-value">High</div></div>', unsafe_allow_html=True)

            # Detail Row
            st.markdown("<br>", unsafe_allow_html=True)
            col_left, col_right = st.columns([1, 1.2])

            with col_left:
                st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem; letter-spacing:0.1em; font-weight:700;'>MISSING KEYWORDS</h4>", unsafe_allow_html=True)
                kw_html = "".join([f'<span class="kw-badge">{kw}</span>' for kw in res["missing_keywords"]])
                st.markdown(kw_html if kw_html else "No critical keywords missing.", unsafe_allow_html=True)
                
                st.markdown("<br><h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem; letter-spacing:0.1em; font-weight:700;'>STRATEGIC SUGGESTIONS</h4>", unsafe_allow_html=True)
                for s in res["suggestions"]:
                    st.markdown(f"""
                        <div style='background:rgba(255,255,255,0.02); padding:1rem; border-radius:10px; margin-bottom:10px; border: 1px solid #111;'>
                            <div style='font-size:0.9rem; color:#eee;'>↳ {s}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br><h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem; letter-spacing:0.1em; font-weight:700;'>ADVICE FROM THE FORGE</h4>", unsafe_allow_html=True)
                st.info(res.get("strategic_advice", "No additional advice available."))

            with col_right:
                st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem; letter-spacing:0.1em; font-weight:700;'>OPTIMIZED REBOOT</h4>", unsafe_allow_html=True)
                st.markdown(f'<div class="resume-box">{res["improved_resume"]}</div>', unsafe_allow_html=True)
                if st.button("Download Optimized Resume (.txt)"):
                    st.download_button(label="Download Now", data=res["improved_resume"], file_name="optimized_resume.txt", mime="text/plain")

    elif current_nav == "Strategic Insights":
        st.markdown("<h1>Strategic Insights Dashboard</h1>")
        st.info("Additional analytics on resume performance and career trajectory coming soon.")

if __name__ == "__main__":
    main()
