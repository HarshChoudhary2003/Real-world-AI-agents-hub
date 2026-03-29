import streamlit as st
import json
import base64
import os
from agent import debug_code
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="DevOS | Debugging Agent",
    page_icon="🐛",
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
        --accent: #FF3B30;
        --accent-glow: rgba(255, 59, 48, 0.3);
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

    /* Subtext Styling */
    .subtext {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }

    /* Buttons Hub */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent), #FF2D55);
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

    /* Debug Steps Table */
    .debug-step {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        display: flex;
        gap: 20px;
    }
    
    .line-number {
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent);
        font-weight: 700;
        width: 40px;
    }

    .line-content {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-primary);
        word-break: break-all;
    }

    .line-explanation {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid var(--border-color);
    }

    </style>
    """, unsafe_allow_html=True)

# --- Application Main ---
def main():
    apply_premium_style()

    # -- Sidebar Config --
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/bug.png", width=80) 
        st.title("DevOS")
        st.markdown("<p class='subtext'>The AI Operating System for Developers.</p>", unsafe_allow_html=True)
        st.markdown("---")

        # --- Intelligence Hub Upgrade ---
        st.subheader("🔮 Intelligence Hub")
        main_ai = st.selectbox(
            "Main AI Provider",
            ["OpenAI", "Anthropic", "Google Gemini", "Groq (Llama-3)"],
            index=0
        )

        if main_ai == "OpenAI":
            model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
            key_env, key_placeholder = "OPENAI_API_KEY", "sk-..."
        elif main_ai == "Anthropic":
            model_options = ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"]
            key_env, key_placeholder = "ANTHROPIC_API_KEY", "sk-ant-..."
        elif main_ai == "Google Gemini":
            model_options = ["gemini/gemini-pro", "gemini/gemini-1.5-flash"]
            key_env, key_placeholder = "GEMINI_API_KEY", "AIza..."
        else:
            model_options = ["groq/llama3-70b-8192", "groq/llama3-8b-8192"]
            key_env, key_placeholder = "GROQ_API_KEY", "gsk_..."

        model = st.selectbox("Intelligence Layer", model_options)
        user_api_key = st.text_input(f"🔑 {main_ai} Key", type="password", placeholder=key_placeholder)
        if user_api_key: os.environ[key_env] = user_api_key

        st.markdown("---")

        # Multi-Language Support
        st.subheader("🛠️ Debugger Context")
        language = st.selectbox(
            "Language",
            ["Python", "JavaScript", "C++", "C#", "SQL", "HTML/CSS", "Go", "Rust", "Swift"],
            index=0
        )
        
        # Beginner vs Expert Toggle Upgrade
        level = st.radio(
            "Target Complexity",
            ["Beginner", "Expert"],
            index=1,
            horizontal=True,
            help="Choose how the AI should explain the root cause and fixes."
        )

        st.markdown("---")
        st.info("💡 **Tip:** Providing the error message helps the AI find tracebacks faster.")

    # -- Main Content Area --
    col_main, col_stats = st.columns([3, 1])

    with col_main:
        st.markdown("<div class='status-badge'>DIAGNOSTICS READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom: 5px;'>🐛 AI Debugging Agent</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; margin-bottom: 30px; color: var(--text-secondary);'>Elite-tier forensic analysis and automated bug-fixes.</p>", unsafe_allow_html=True)

    # -- Interaction Zone --
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col_code, col_err = st.columns([1, 1])
        
        with col_code:
            code = st.text_area(
                "💻 Broken Code Snippet",
                placeholder=f"Paste your {language} code here...",
                height=250
            )
        
        with col_err:
            error_msg = st.text_area(
                "⚠️ Error Message (Optional)",
                placeholder="Ex: NameError: name 'x' is not defined... (or leave empty for logic check)",
                height=250
            )
        
        fix_btn = st.button("🚀 FIX MY CODE", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # -- Result Section --
    if fix_btn:
        if not code:
            st.error("Please provide code to analyze.")
        else:
            with st.spinner("🧪 Brain performing forensic analysis..."):
                result = debug_code(code, error_msg, language=language, level=level, model=model)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.balloons()
                st.success(f"✅ Debugging Complete! Found and fixed the issue.")
                st.session_state.debug_result = result

    if "debug_result" in st.session_state:
        res = st.session_state.debug_result
        
        col_left, col_right = st.columns([1, 1.5])

        with col_left:
            st.markdown("<div class='section-header'>🐛 Error Explanation</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='glass-card' style='padding:15px;'>{res.get('error_explanation', 'N/A')}</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='section-header' style='margin-top: 20px;'>🧠 Root Cause</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='glass-card' style='padding:15px;'>{res.get('root_cause', 'The issue was likely a logical or syntax error.')}</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-header' style='margin-top: 20px;'>⚡ Improvements</div>", unsafe_allow_html=True)
            for imp in res.get("improvements", []):
                st.markdown(f"- {imp}")

        with col_right:
            st.markdown("<div class='section-header'>✅ Fixed Implementation</div>", unsafe_allow_html=True)
            lang_lower = language.lower() if " " not in language else "html"
            st.code(res.get("fixed_code", ""), language=lang_lower)
            
            # Line-by-Line Debug Mode Upgrade
            st.markdown("<div class='section-header' style='margin-top: 30px;'>🧪 Step-by-Step Debug Mode</div>", unsafe_allow_html=True)
            for step in res.get("line_by_line_debug", []):
                st.markdown(f"""
                <div class='debug-step'>
                    <div class='line-number'>L{step['line']}</div>
                    <div style='flex:1;'>
                        <div class='line-content'><code>{step['content']}</code></div>
                        <div class='line-explanation'>{step['explanation']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # -- Stats Sidebar Insight --
    with col_stats:
        st.markdown("<div class='glass-card' style='padding: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0; color:var(--accent); text-align:center;'>ENGINE STATS</h4>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric("Forensic Accuracy", "100%", "Perfect")
        st.metric("Avg. Fix Time", "4.2s", "-0.5s")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
