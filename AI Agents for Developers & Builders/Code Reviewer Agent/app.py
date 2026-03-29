import streamlit as st
import json
import base64
import os
from agent import review_code_advanced
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="DevOS | Code Reviewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Theme Injection ---
def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-color: #0A0A0B;
        --secondary-bg: #141416;
        --accent: #EAB308; /* Luxury Gold */
        --accent-glow: rgba(234, 179, 8, 0.2);
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
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
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
        gap: 12px;
    }

    /* AI Status Badge */
    .status-badge {
        background: var(--accent-glow);
        border: 1px solid var(--accent);
        color: var(--accent);
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 10px;
        letter-spacing: 0.05em;
    }

    /* Subtext Styling */
    .subtext {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }

    /* Metric Overrides */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        color: var(--accent);
    }

    /* High Risk Badge */
    .risk-high { background: rgba(255, 59, 48, 0.1); border: 1px solid #FF3B30; color: #FF3B30; padding: 2px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; }
    .risk-med { background: rgba(255, 159, 10, 0.1); border: 1px solid #FF9F0A; color: #FF9F0A; padding: 2px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; }
    .risk-low { background: rgba(52, 199, 89, 0.1); border: 1px solid #34C759; color: #34C759; padding: 2px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; }

    /* Issue List */
    .issue-item {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid var(--accent);
        padding: 15px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 12px;
    }

    /* Buttons Hub */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent), #CA8A04);
        color: #000 !important;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 800;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 10px 20px var(--accent-glow);
    }

    </style>
    """, unsafe_allow_html=True)

# --- Application Main ---
def main():
    apply_premium_style()

    # -- Sidebar Config --
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/fine-print.png", width=80) 
        st.title("DevOS")
        st.markdown("<p class='subtext'>The AI Operating System for Developers.</p>", unsafe_allow_html=True)
        st.markdown("---")

        # --- NEXT-LEVEL UPGRADE: Intelligence Hub ---
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
        user_api_key = st.text_input(f"🔑 {main_ai} API Key", type="password", placeholder=key_placeholder)
        if user_api_key: os.environ[key_env] = user_api_key

        st.markdown("---")

        # Review Configuration Upgrade
        st.subheader("🏗️ Review Context")
        language = st.selectbox("Code Language", ["Python", "JavaScript", "TypeScript", "React/Node", "C#", "Rust", "Swift", "Go", "Java"], index=0)
        style_guide = st.selectbox("Style Guide", ["Standard (Industry)", "Clean Code Core", "PEP8 (Python)", "AirBnB (JS)", "Google Style"], index=0)

        st.markdown("---")
        st.info("💡 **Tip:** Mention specific patterns (like TDD or SOLID) for deeper structural critiques.")

    # -- Main Content Area --
    col_main, col_stats = st.columns([3, 1])

    with col_main:
        st.markdown("<div class='status-badge'>AUDIT READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom: 5px;'>👨‍💻 AI Code Reviewer</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; margin-bottom: 30px; color: var(--text-secondary);'>Simulate a Senior Engineer review in milliseconds.</p>", unsafe_allow_html=True)

    # -- Input Section --
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        code = st.text_area(
            "💻 Implementation to Audit",
            placeholder="Paste your source code for a high-intensity review...",
            height=300
        )
        
        review_btn = st.button("🚀 INITIATE CODE AUDIT", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # -- Result Section --
    if review_btn:
        if not code:
            st.warning("Please provide code to audit.")
        else:
            with st.spinner("🧠 Senior Engineer analyzing architecture..."):
                result = review_code_advanced(code, language=language, style_guide=style_guide, model=model)
            
            if "error" in result:
                st.error(f"Audit Error: {result['error']}")
            else:
                st.balloons()
                st.success("✅ Code Audit Complete! Strategic insights generated.")
                st.session_state.review_result = result
                st.session_state.original_code = code

    if "review_result" in st.session_state:
        res = st.session_state.review_result
        orig = st.session_state.original_code
        
        col_metrics, col_pr = st.columns([1, 2.5])
        
        with col_metrics:
            st.markdown("<div class='section-header'>📊 Metrics</div>", unsafe_allow_html=True)
            st.metric("Quality Score", f"{res.get('quality_score', 0)}/10", delta_color="normal")
            
            st.markdown("<div class='section-header' style='margin-top: 30px;'>🛡 Security Risks</div>", unsafe_allow_html=True)
            if not res.get("security_risks"):
                st.markdown("<span class='risk-low'>SECURE</span> Neutral findings.", unsafe_allow_html=True)
            else:
                for risk in res.get("security_risks", []):
                    st.markdown(f"<span class='risk-high'>VULNERABILITY</span> {risk}", unsafe_allow_html=True)
            
            st.markdown("<div class='section-header' style='margin-top: 30px;'>⚡ Improvements</div>", unsafe_allow_html=True)
            for imp in res.get("improvements", []):
                st.markdown(f"- {imp}")

        with col_pr:
            st.markdown("<div class='section-header'>💬 GitHub PR Mode (Core Summary)</div>", unsafe_allow_html=True)
            st.info(res.get("pr_summary", "Strategic implementation audit finished."))
            
            st.markdown("<div class='section-header' style='margin-top: 25px;'>⚠️ Technical Issues</div>", unsafe_allow_html=True)
            for issue in res.get("issues", []):
                severity_class = f"risk-{issue['severity'].lower()}" if issue.get('severity') else "risk-low"
                st.markdown(f"""
                <div class='issue-item'>
                    <span class='{severity_class}'>{issue.get('severity', 'LOW')}</span> 
                    <strong>Line {issue.get('line', 'N/A')}</strong>: {issue['description']}
                    <p style='color: var(--text-secondary); margin-top:10px; font-size: 0.9rem;'>{issue.get('rationale', '')}</p>
                </div>
                """, unsafe_allow_html=True)

        # NEXT-LEVEL UPGRADE: Diff View Side-by-Side
        st.markdown("<div class='section-header' style='margin-top: 40px;'>⚔️ Implementation Audit (Before vs After)</div>", unsafe_allow_html=True)
        col_old, col_new = st.columns(2)
        
        lang_key = language.lower() if " " not in language else "python"
        with col_old:
            st.markdown("<p style='text-align:center; color: var(--text-secondary);'>ORIGINAL</p>", unsafe_allow_html=True)
            st.code(orig, language=lang_key)
        
        with col_new:
            st.markdown("<p style='text-align:center; color: var(--accent);'>REFACTORED (DevOS)</p>", unsafe_allow_html=True)
            st.code(res.get("refactored_code", ""), language=lang_key)

    # -- Stats Sidebar Insight --
    with col_stats:
        st.markdown("<div class='glass-card' style='padding: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0; color:var(--accent); text-align:center;'>AUDIT STATS</h4>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric("Review Depth", "Senior Arch.", "+15%")
        st.metric("Response Latency", "1.8s", "-0.2s")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
