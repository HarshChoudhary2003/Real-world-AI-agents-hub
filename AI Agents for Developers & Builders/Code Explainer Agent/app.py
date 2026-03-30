import streamlit as st
import os
from agent import explain_code

st.set_page_config(
    page_title="DevOS | Code Explainer",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-color: #0A0A0B;
        --accent: #F59E0B;
        --accent-alt: #EF4444;
        --accent-glow: rgba(245, 158, 11, 0.25);
        --text-primary: #FFFFFF;
        --text-secondary: #94A3B8;
        --border-color: #334155;
        --card-bg: rgba(30, 41, 59, 0.5);
    }

    .stApp { background: var(--bg-color); color: var(--text-primary); font-family: 'Outfit', sans-serif; }
    header, footer { visibility: hidden !important; }

    .glass-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 28px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 22px;
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
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border-color);
    }

    .concept-chip {
        display: inline-block;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #FCD34D;
        padding: 5px 14px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px 4px 4px 0;
    }

    .list-item {
        background: rgba(255,255,255,0.04);
        border-left: 3px solid var(--accent);
        padding: 10px 16px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 9px;
        font-size: 0.93rem;
        color: var(--text-primary);
        line-height: 1.55;
    }

    .list-item-red { border-left-color: #EF4444; }
    .list-item-green { border-left-color: #10B981; }

    .line-block {
        background: #0D1117;
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }

    .line-code {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #93C5FD;
        margin-bottom: 6px;
    }

    .line-explain {
        font-size: 0.9rem;
        color: var(--text-secondary);
    }

    .complexity-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 14px 20px;
        text-align: center;
        margin-bottom: 14px;
    }

    .complexity-label { font-size: 0.78rem; color: var(--text-secondary); letter-spacing: 0.06em; text-transform: uppercase; }
    .complexity-value { font-size: 1.4rem; font-weight: 700; color: var(--accent); font-family: 'JetBrains Mono', monospace; }

    .interview-box {
        background: linear-gradient(135deg, rgba(245,158,11,0.1), rgba(239,68,68,0.1));
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 14px;
        padding: 18px 22px;
        font-size: 0.95rem;
        line-height: 1.65;
        color: var(--text-primary);
    }

    .interview-mode-badge {
        background: linear-gradient(135deg, #F59E0B, #EF4444);
        color: #000;
        font-weight: 800;
        padding: 3px 12px;
        border-radius: 50px;
        font-size: 0.78rem;
        letter-spacing: 0.05em;
        display: inline-block;
        margin-bottom: 10px;
    }

    .stButton>button {
        background: linear-gradient(135deg, var(--accent), #D97706);
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
        st.image("https://img.icons8.com/parakeet/512/000000/book.png", width=75)
        st.title("DevOS")
        st.markdown("<p class='subtext'>AI Code Explainer & Learning Agent.</p>", unsafe_allow_html=True)
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

        user_api_key = st.text_input(f"🔑 {main_ai} API Key", type="password",
            help="Enter your API key. Falls back to environment variables if empty.")
        if user_api_key:
            env_map = {"OpenAI": "OPENAI_API_KEY", "Anthropic": "ANTHROPIC_API_KEY",
                       "Google Gemini": "GEMINI_API_KEY", "Groq (Llama-3)": "GROQ_API_KEY"}
            os.environ[env_map[main_ai]] = user_api_key

        st.markdown("---")
        st.subheader("🎛️ Explainer Settings")

        difficulty = st.selectbox("Difficulty Mode", ["Beginner", "Intermediate", "Advanced"], index=1)
        interview_mode = st.toggle("🎙️ Interview Mode", value=False,
            help="Rephrase explanation as a structured interview answer.")

        st.markdown("---")
        st.info("💡 **Tip:** Use Interview Mode to prepare confident, structured answers for technical rounds.")

    # --- Header ---
    col_hdr, col_stats = st.columns([3, 1])
    with col_hdr:
        st.markdown("<div class='status-badge'>EXPLAINER ENGINE READY</div>", unsafe_allow_html=True)
        if interview_mode:
            st.markdown("<span class='interview-mode-badge'>🎙️ INTERVIEW MODE ON</span>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom:6px;'>📘 Code Explainer Agent</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:1.15rem; color:var(--text-secondary); margin-bottom:28px;'>Understand any code instantly — from logic to interview answers.</p>", unsafe_allow_html=True)

    # --- Input ---
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        code_input = st.text_area(
            "💻 Paste Your Code",
            value="for i in range(5):\n    print(i)",
            height=200,
            placeholder="Paste any function, class, script, or snippet..."
        )
        explain_btn = st.button("🚀 EXPLAIN THIS CODE", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Stats widget ---
    with col_stats:
        st.markdown("<div class='glass-card' style='padding:20px; margin-top:80px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0; color:var(--accent); text-align:center;'>LEARNING STATS</h4>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric("Clarity Score", "99.5%", "+0.5%")
        st.metric("Concepts Mapped", "Auto", "Deep")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Generation ---
    if explain_btn:
        if not code_input.strip():
            st.error("Please paste some code to explain.")
        else:
            with st.spinner("🧠 Neural tutor is analyzing your code..."):
                result = explain_code(code_input, difficulty=difficulty,
                                      interview_mode=interview_mode, model=model)

            if "error" in result:
                st.error(f"Engine Failure: {result['error']}")
                st.info(result.get("message", ""))
            else:
                st.success(f"✅ Explanation Ready: **{result.get('title', 'Code Analysis')}**")
                st.session_state.explain_result = result

    # --- Dashboard ---
    if "explain_result" in st.session_state:
        res = st.session_state.explain_result

        # Complexity row
        complexity = res.get("complexity", {})
        if complexity:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class='complexity-box'>
                    <div class='complexity-label'>Time Complexity</div>
                    <div class='complexity-value'>{complexity.get('time', 'N/A')}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class='complexity-box'>
                    <div class='complexity-label'>Space Complexity</div>
                    <div class='complexity-value'>{complexity.get('space', 'N/A')}</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                difficulty_color = {"Beginner": "#10B981", "Intermediate": "#F59E0B", "Advanced": "#EF4444"}.get(difficulty, "#F59E0B")
                st.markdown(f"""
                <div class='complexity-box' style='border-color:{difficulty_color}40; background:rgba(0,0,0,0.2);'>
                    <div class='complexity-label'>Difficulty Mode</div>
                    <div class='complexity-value' style='color:{difficulty_color}; font-size:1.1rem;'>{difficulty}</div>
                </div>""", unsafe_allow_html=True)

        # Main columns
        col_left, col_right = st.columns([1, 1])

        with col_left:
            # Simple Explanation
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🧠 Simple Explanation</div>", unsafe_allow_html=True)
            st.write(res.get("simple_explanation", ""))

            # Concepts
            st.markdown("<div class='section-header' style='margin-top:20px;'>📘 Concepts Used</div>", unsafe_allow_html=True)
            concepts_html = "".join([f"<span class='concept-chip'>{c}</span>" for c in res.get("concepts", [])])
            st.markdown(f"<div>{concepts_html}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Improvements
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>⚡ Optimization Suggestions</div>", unsafe_allow_html=True)
            for imp in res.get("improvements", []):
                st.markdown(f"<div class='list-item list-item-green'>{imp}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            # Line-by-Line
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🔍 Line-by-Line Breakdown</div>", unsafe_allow_html=True)
            for item in res.get("line_by_line", []):
                if isinstance(item, dict):
                    line = item.get("line", "")
                    explanation = item.get("explanation", "")
                else:
                    line = ""
                    explanation = str(item)
                st.markdown(f"""
                <div class='line-block'>
                    <div class='line-code'><code>{line}</code></div>
                    <div class='line-explain'>{explanation}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Interview Mode Panel
        if interview_mode and res.get("interview_answer"):
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🎙️ Interview Answer</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='interview-box'>{res['interview_answer']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Study Notes expander
        if res.get("study_notes"):
            with st.expander("📓 Download Study Notes"):
                st.text_area("Study Notes", value=res["study_notes"], height=180)
                st.download_button(
                    "⬇️ Download Notes (.txt)",
                    data=res["study_notes"],
                    file_name=f"notes_{res.get('title','code').lower().replace(' ','_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()
