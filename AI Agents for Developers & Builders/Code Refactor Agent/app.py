import streamlit as st
import os
from agent import refactor_code

st.set_page_config(
    page_title="DevOS | Code Refactor",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-color: #0A0A0B;
        --accent: #10B981;
        --accent-alt: #059669;
        --accent-glow: rgba(16, 185, 129, 0.25);
        --red: #EF4444;
        --yellow: #F59E0B;
        --text-primary: #FFFFFF;
        --text-secondary: #94A3B8;
        --border-color: #334155;
        --card-bg: rgba(30, 41, 59, 0.5);
        --code-bg: #0D1117;
    }

    .stApp { background: var(--bg-color); color: var(--text-primary); font-family: 'Outfit', sans-serif; }
    header, footer { visibility: hidden !important; }

    .glass-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 26px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    .status-badge {
        background: var(--accent-glow);
        border: 1px solid var(--accent);
        color: var(--accent);
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 10px;
        letter-spacing: 0.08em;
    }

    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border-color);
    }

    .list-item {
        background: rgba(255,255,255,0.04);
        border-left: 3px solid var(--accent);
        padding: 10px 16px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 9px;
        font-size: 0.92rem;
        color: var(--text-primary);
        line-height: 1.55;
    }
    .list-item-red  { border-left-color: var(--red); }
    .list-item-yellow { border-left-color: var(--yellow); }

    .complexity-box {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 14px;
        padding: 14px 20px;
        text-align: center;
        margin-bottom: 14px;
    }
    .complexity-label { font-size: 0.75rem; color: var(--text-secondary); letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 4px; }
    .complexity-value { font-size: 1.4rem; font-weight: 700; color: var(--accent); font-family: 'JetBrains Mono', monospace; }
    .complexity-value-red { color: var(--red); }

    .diff-block {
        background: var(--code-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 14px;
    }
    .diff-header {
        background: rgba(255,255,255,0.05);
        padding: 8px 16px;
        font-size: 0.8rem;
        color: var(--text-secondary);
        font-family: 'JetBrains Mono', monospace;
        border-bottom: 1px solid var(--border-color);
    }
    .diff-old {
        background: rgba(239, 68, 68, 0.1);
        border-left: 3px solid var(--red);
        padding: 10px 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.83rem;
        color: #FCA5A5;
        white-space: pre-wrap;
        word-break: break-all;
    }
    .diff-new {
        background: rgba(16, 185, 129, 0.1);
        border-left: 3px solid var(--accent);
        padding: 10px 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.83rem;
        color: #6EE7B7;
        white-space: pre-wrap;
        word-break: break-all;
    }
    .diff-reason {
        padding: 8px 16px;
        font-size: 0.85rem;
        color: var(--text-secondary);
        border-top: 1px solid var(--border-color);
        font-style: italic;
    }

    .stButton>button {
        background: linear-gradient(135deg, var(--accent), var(--accent-alt));
        color: #000 !important;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 22px var(--accent-glow);
    }

    .subtext { font-size: 0.93rem; color: var(--text-secondary); }
    </style>
    """, unsafe_allow_html=True)

def main():
    apply_premium_style()

    # --- Sidebar ---
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/lightning-bolt.png", width=75)
        st.title("DevOS")
        st.markdown("<p class='subtext'>AI Code Refactor & Optimization Agent.</p>", unsafe_allow_html=True)
        st.markdown("---")

        st.subheader("🔮 Intelligence Hub")
        main_ai = st.selectbox("Main AI Provider", ["OpenAI", "Anthropic", "Google Gemini", "Groq (Llama-3)"])
        models = {
            "OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"],
            "Google Gemini": ["gemini/gemini-pro", "gemini/gemini-1.5-flash"],
            "Groq (Llama-3)": ["groq/llama3-70b-8192", "groq/llama3-8b-8192"]
        }
        model = st.selectbox("Intelligence Layer", models[main_ai])
        user_api_key = st.text_input(f"🔑 {main_ai} API Key", type="password")
        if user_api_key:
            env_map = {"OpenAI": "OPENAI_API_KEY", "Anthropic": "ANTHROPIC_API_KEY",
                       "Google Gemini": "GEMINI_API_KEY", "Groq (Llama-3)": "GROQ_API_KEY"}
            os.environ[env_map[main_ai]] = user_api_key

        st.markdown("---")
        st.subheader("🛠️ Refactor Settings")
        style_guide = st.selectbox("Style Guide", [
            "PEP8 (Python)", "Clean Architecture", "Google Style Guide",
            "Airbnb (JavaScript)", "SOLID Principles", "Functional Style"
        ])

        st.markdown("---")
        st.info("💡 **Power Tip:** Clean code is not about clever tricks — it's about clarity, intention, and simplicity.")

    # --- Header ---
    col_hdr, col_stats = st.columns([3, 1])
    with col_hdr:
        st.markdown("<div class='status-badge'>REFACTOR ENGINE READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom:6px;'>✨ Code Refactor & Optimization Agent</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:1.15rem; color:var(--text-secondary); margin-bottom:28px;'>Transform messy code into clean, performant, production-grade software.</p>", unsafe_allow_html=True)

    # --- Input ---
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        code_input = st.text_area(
            "💻 Paste Code to Refactor",
            value="def calc(l):\n    s=0\n    for i in range(len(l)):\n        s=s+l[i]\n    return s/len(l)",
            height=200,
            placeholder="Paste any messy, inefficient, or unclean code..."
        )
        refactor_btn = st.button("🚀 REFACTOR & OPTIMIZE", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Stats widget ---
    with col_stats:
        st.markdown("<div class='glass-card' style='padding:20px; margin-top:80px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0; color:var(--accent); text-align:center;'>REFACTOR STATS</h4>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric("Code Quality", "A+", "Instant")
        st.metric("Tech Debt Cleared", "High", "↑ ROI")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Logic ---
    if refactor_btn:
        if not code_input.strip():
            st.error("Please paste some code to refactor.")
        else:
            with st.spinner("🧠 Principal Engineer is refactoring your code..."):
                result = refactor_code(code_input, style_guide=style_guide, model=model)

            if "error" in result:
                st.error(f"Engine Failure: {result['error']}")
                st.info(result.get("message", ""))
            else:
                st.success(f"✅ Refactoring Complete: **{result.get('title', 'Code')}**")
                st.session_state.refactor_result = result

    # --- Dashboard ---
    if "refactor_result" in st.session_state:
        res = st.session_state.refactor_result

        # Complexity row
        complexity = res.get("complexity", {})
        if complexity:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class='complexity-box' style='border-color:rgba(239,68,68,0.4); background:rgba(239,68,68,0.08);'>
                    <div class='complexity-label'>Before (Original)</div>
                    <div class='complexity-value complexity-value-red'>{complexity.get('before', 'O(?)')}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class='complexity-box'>
                    <div class='complexity-label'>After (Refactored)</div>
                    <div class='complexity-value'>{complexity.get('after', 'O(?)')}</div>
                </div>""", unsafe_allow_html=True)

        # Summary
        if res.get("summary"):
            st.markdown(f"""
            <div class='glass-card' style='border-color:rgba(16,185,129,0.3);'>
                <div class='section-header'>📋 Refactor Summary</div>
                <p style='color:var(--text-secondary); font-size:0.97rem; line-height:1.65; margin:0;'>{res['summary']}</p>
            </div>""", unsafe_allow_html=True)

        # Code columns
        col_left, col_right = st.columns([1, 1])

        with col_left:
            # Refactored Code
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>✨ Refactored Code</div>", unsafe_allow_html=True)
            st.code(res.get("refactored_code", ""), language="python")
            st.download_button(
                "⬇️ Download Refactored Code",
                data=res.get("refactored_code", ""),
                file_name=f"refactored_{res.get('title','code').lower().replace(' ','_')}.py",
                mime="text/plain",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            # Improvements
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>⚡ Improvements Made</div>", unsafe_allow_html=True)
            for item in res.get("improvements", []):
                st.markdown(f"<div class='list-item'>{item}</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-header' style='margin-top:18px;'>📈 Performance Gains</div>", unsafe_allow_html=True)
            for item in res.get("performance_gains", []):
                st.markdown(f"<div class='list-item'>{item}</div>", unsafe_allow_html=True)

            st.markdown("<div class='section-header' style='margin-top:18px;'>🧠 Readability Enhancements</div>", unsafe_allow_html=True)
            for item in res.get("readability_enhancements", []):
                st.markdown(f"<div class='list-item list-item-yellow'>{item}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Style violations
        violations = res.get("style_violations_fixed", [])
        if violations:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='section-header'>🚨 Style Violations Fixed ({len(violations)})</div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, v in enumerate(violations):
                with cols[i % 2]:
                    st.markdown(f"<div class='list-item list-item-red'>{v}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Diff highlights
        diffs = res.get("diff_highlights", [])
        if diffs:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🔀 Before vs After Diff</div>", unsafe_allow_html=True)
            for diff in diffs:
                st.markdown(f"""
                <div class='diff-block'>
                    <div class='diff-header'>CHANGE DETECTED</div>
                    <div class='diff-old'>- {diff.get('original','')}</div>
                    <div class='diff-new'>+ {diff.get('refactored','')}</div>
                    <div class='diff-reason'>💡 {diff.get('reason','')}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
