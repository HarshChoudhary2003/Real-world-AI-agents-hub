import streamlit as st
import json
import base64
import os
from agent import generate_quality_tests
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="DevOS | Test Case Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Theme Injection ---
def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-color: #0A0A0B;
        --secondary-bg: #141416;
        --accent: #D946EF;
        --accent-glow: rgba(217, 70, 239, 0.3);
        --text-primary: #FFFFFF;
        --text-secondary: #94A3B8;
        --border-color: #334155;
        --card-bg: rgba(30, 41, 59, 0.5);
    }

    .stApp {
        background: var(--bg-color);
        color: var(--text-primary);
        font-family: 'Outfit', sans-serif;
    }

    header, footer {visibility: hidden !important;}

    /* Glassmorphic Cards */
    .glass-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
        color: var(--accent);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* AI Status Badge */
    .status-badge {
        background: var(--accent-glow);
        border: 1px solid var(--accent);
        color: var(--accent);
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* List Item Hub */
    .list-item {
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid var(--accent);
        padding: 12px 18px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 10px;
        font-size: 0.95rem;
        color: var(--text-primary);
    }

    /* Subtext Styling */
    .subtext {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }

    /* Buttons Hub */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent), #A21CAF);
        color: #fff !important;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px var(--accent-glow);
    }

    </style>
    """, unsafe_allow_html=True)

# --- Application Main ---
def main():
    apply_premium_style()

    # -- Sidebar Config --
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/lab-items.png", width=80) 
        st.title("DevOS")
        st.markdown("<p class='subtext'>Elite QA + Testing Intelligence Agent.</p>", unsafe_allow_html=True)
        st.markdown("---")

        st.subheader("🔮 Intelligence Hub")
        
        main_ai = st.selectbox(
            "Main AI Provider",
            ["OpenAI", "Anthropic", "Google Gemini", "Groq (Llama-3)"],
            index=0
        )

        models = {
            "OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"],
            "Google Gemini": ["gemini/gemini-pro", "gemini/gemini-1.5-flash"],
            "Groq (Llama-3)": ["groq/llama3-70b-8192", "groq/llama3-8b-8192"]
        }

        model = st.selectbox("Intelligence Layer", models[main_ai])
        
        user_api_key = st.text_input(
            f"🔑 {main_ai} API Key",
            type="password",
            help=f"Enter your {main_ai} key. If left empty, system environment keys will be used."
        )

        if user_api_key:
            env_map = {"OpenAI": "OPENAI_API_KEY", "Anthropic": "ANTHROPIC_API_KEY", "Google Gemini": "GEMINI_API_KEY", "Groq (Llama-3)": "GROQ_API_KEY"}
            os.environ[env_map[main_ai]] = user_api_key

        st.markdown("---")
        
        st.subheader("🧪 Framework Preferences")
        framework = st.selectbox(
            "Target Framework",
            ["pytest (Recommended)", "unittest", "Jest", "Go Test", "JUnit"],
            index=0
        )
        
        st.markdown("---")
        st.info("💡 **Quality First:** Real engineering practice: **Code → Test → Validate.**")

    # -- Header Section --
    col_main, col_stats = st.columns([3, 1])
    with col_main:
        st.markdown("<div class='status-badge'>QUALITY AGENT READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom: 5px;'>🧪 Test Case Generator Agent</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; margin-bottom: 30px; color: var(--text-secondary);'>Elite automated testing suites and edge case diagnostics for mission-critical code.</p>", unsafe_allow_html=True)

    # -- Input Area --
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        code_input = st.text_area(
            "💻 Paste Your Code / Function",
            placeholder="def calculate_roi(investment, return_val):\n    return (return_val - investment) / investment",
            height=200
        )
        
        col_gen, _ = st.columns([1, 1])
        with col_gen:
            generate_btn = st.button("🚀 GENERATE TEST SUITE", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # -- Generation Logic --
    if generate_btn:
        if not code_input:
            st.error("Please provide code to analyze.")
        else:
            with st.spinner("🧠 Neural SDET is architecting your test suite..."):
                result = generate_quality_tests(code_input, framework=framework, model=model)
            
            if "error" in result:
                st.error(f"Generation Hub Failure: {result['error']}")
                st.info(result.get("message", "Error in AI processing."))
            else:
                st.success(f"✅ Success: {result.get('project_name', 'Test Suite')} built following {framework} standards!")
                st.session_state.test_result = result

    # -- Dashboard Display --
    if "test_result" in st.session_state:
        res = st.session_state.test_result
        
        col_tests, col_intel = st.columns([2, 1])

        with col_tests:
            st.markdown("<div class='section-header'>📂 Generated Test Suite</div>", unsafe_allow_html=True)
            st.code(res.get("unit_tests", "No tests generated."), language="python")
            
            st.download_button(
                label="⬇️ DOWNLOAD TEST FILE",
                data=res.get("unit_tests", ""),
                file_name=f"test_{res.get('project_name', 'suite').lower().replace(' ', '_')}.py",
                mime="text/plain",
                use_container_width=True
            )

        with col_intel:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header' style='font-size: 1.2rem;'>⚠️ Edge Cases</div>", unsafe_allow_html=True)
            for case in res.get("edge_cases", []):
                st.markdown(f"<div class='list-item'>{case}</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='section-header' style='font-size: 1.2rem; margin-top: 20px;'>🐛 Bugs to Watch</div>", unsafe_allow_html=True)
            for bug in res.get("bugs_to_watch", []):
                st.markdown(f"<div class='list-item' style='border-left-color: #EF4444;'>{bug}</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='section-header' style='font-size: 1.2rem; margin-top: 20px;'>📊 Test Strategy</div>", unsafe_allow_html=True)
            for strategy in res.get("test_strategy", []):
                st.markdown(f"<div class='list-item' style='border-left-color: #10B981;'>{strategy}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        with st.expander("🎓 Engineering Logic & Coverage Analysis"):
            col_notes, col_cov = st.columns(2)
            with col_notes:
                st.subheader("Architectural Notes")
                st.info(res.get("engineering_notes", "No notes available."))
            with col_cov:
                st.subheader("Coverage Intelligence")
                st.warning(res.get("coverage_analysis", "Coverage estimation unavailable."))

    # -- Stats Sidebar Insight --
    with col_stats:
        st.markdown("<div class='glass-card' style='padding: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0; color:var(--accent); text-align:center;'>QA STATS</h4>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric("Test Stability", "99.9%", "+0.01%")
        st.metric("Risk Reduction", "High", "95%")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
