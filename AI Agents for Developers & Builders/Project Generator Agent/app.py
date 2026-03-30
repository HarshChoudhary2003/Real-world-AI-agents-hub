import streamlit as st
import os
from agent import generate_project

st.set_page_config(
    page_title="DevOS | Project Generator",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

DOMAINS = [
    "AI / Machine Learning", "Web Development", "Data Science & Analytics",
    "Mobile Apps", "DevOps & Cloud", "Cybersecurity", "Blockchain & Web3",
    "Game Development", "IoT & Embedded Systems", "Open Source Tools"
]

DIFFICULTY_META = {
    "Beginner":     {"color": "#10B981", "icon": "🟢", "time": "1–3 days"},
    "Intermediate": {"color": "#F59E0B", "icon": "🟡", "time": "1–2 weeks"},
    "Advanced":     {"color": "#EF4444", "icon": "🔴", "time": "3–6 weeks"},
}

def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-color: #0A0A0B;
        --accent: #A855F7;
        --accent-alt: #7C3AED;
        --accent-glow: rgba(168, 85, 247, 0.25);
        --green: #10B981;
        --yellow: #F59E0B;
        --red: #EF4444;
        --blue: #3B82F6;
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

    .project-hero {
        background: linear-gradient(135deg, rgba(168,85,247,0.15), rgba(124,58,237,0.08));
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 20px;
    }
    .project-name {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #A855F7, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin:0 0 6px 0;
    }
    .project-tagline {
        font-size: 1.05rem;
        color: var(--text-secondary);
        font-style: italic;
        margin-bottom: 14px;
    }
    .project-idea { font-size: 0.97rem; color: var(--text-primary); line-height: 1.7; }

    .section-header {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border-color);
    }

    .feature-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 8px;
        background: rgba(168, 85, 247, 0.07);
        border: 1px solid rgba(168, 85, 247, 0.15);
        font-size: 0.92rem;
        color: var(--text-primary);
        line-height: 1.5;
    }
    .feature-dot {
        width: 8px; height: 8px;
        background: var(--accent);
        border-radius: 50%;
        flex-shrink: 0;
        margin-top: 6px;
    }

    .tech-chip {
        display: inline-block;
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #93C5FD;
        padding: 5px 13px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 4px 4px 4px 0;
        font-family: 'JetBrains Mono', monospace;
    }

    .roadmap-week {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 12px;
        position: relative;
    }
    .roadmap-week-label {
        font-size: 0.75rem;
        color: var(--accent);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .roadmap-milestone {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 10px;
    }
    .roadmap-task {
        font-size: 0.87rem;
        color: var(--text-secondary);
        padding: 3px 0 3px 16px;
        position: relative;
    }
    .roadmap-task::before {
        content: "›";
        position: absolute;
        left: 4px;
        color: var(--accent);
        font-weight: 700;
    }

    .hook-box {
        background: rgba(168, 85, 247, 0.08);
        border: 1px solid rgba(168, 85, 247, 0.25);
        border-radius: 14px;
        padding: 16px 20px;
        font-size: 0.95rem;
        line-height: 1.65;
        color: var(--text-primary);
        font-style: italic;
        margin-bottom: 12px;
    }
    .hook-label {
        font-size: 0.72rem;
        color: var(--accent);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .bonus-item {
        background: rgba(16, 185, 129, 0.07);
        border-left: 3px solid var(--green);
        padding: 10px 16px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 9px;
        font-size: 0.92rem;
        color: var(--text-primary);
    }

    .stButton>button {
        background: linear-gradient(135deg, var(--accent), var(--accent-alt));
        color: #fff !important;
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


def render_roadmap(roadmap):
    for item in roadmap:
        if isinstance(item, dict):
            week = item.get("week", "")
            milestone = item.get("milestone", "")
            tasks = item.get("tasks", [])
            tasks_html = "".join([f"<div class='roadmap-task'>{t}</div>" for t in tasks])
            st.markdown(f"""
            <div class='roadmap-week'>
                <div class='roadmap-week-label'>{week}</div>
                <div class='roadmap-milestone'>{milestone}</div>
                {tasks_html}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='roadmap-week'>
                <div class='roadmap-task'>{item}</div>
            </div>""", unsafe_allow_html=True)


def main():
    apply_premium_style()

    # --- Sidebar ---
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/idea.png", width=75)
        st.title("DevOS")
        st.markdown("<p class='subtext'>AI Project Generator & Idea Engine.</p>", unsafe_allow_html=True)
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
        st.subheader("🎛️ Project Settings")
        domain = st.selectbox("🌐 Domain", DOMAINS)
        level = st.selectbox("🎯 Difficulty", ["Beginner", "Intermediate", "Advanced"], index=1)
        meta = DIFFICULTY_META[level]
        st.markdown(f"<div style='font-size:0.85rem; color:{meta['color']}; margin-top:-8px;'>{meta['icon']} Est. build time: {meta['time']}</div>", unsafe_allow_html=True)
        keywords = st.text_input("✨ Keywords / Interests (optional)", placeholder="e.g. finance, NLP, real-time")

        st.markdown("---")
        st.info("💡 **Tip:** Add keywords to get highly personalized project ideas for your interests.")

    # --- Header ---
    col_hdr, col_stats = st.columns([3, 1])
    with col_hdr:
        st.markdown("<div class='status-badge'>IDEA ENGINE READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom:6px;'>💡 AI Project Generator Agent</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:1.15rem; color:var(--text-secondary); margin-bottom:28px;'>From domain and difficulty to a complete, portfolio-worthy project blueprint — instantly.</p>", unsafe_allow_html=True)

    # --- Input trigger ---
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.markdown(f"**Selected:** `{domain}` · `{level}` · {meta['icon']} {meta['time']}")
        gen_btn = st.button("🚀 GENERATE PROJECT BLUEPRINT", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Stats ---
    with col_stats:
        st.markdown(f"""
        <div class='glass-card' style='padding:20px; margin-top:80px; text-align:center;'>
            <h4 style='margin:0; color:var(--accent);'>IDEA STATS</h4>
            <hr style='border-color:#334155; margin:10px 0;'>
            <div style='font-size:0.75rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.07em;'>Domains</div>
            <div style='font-size:1.5rem; font-weight:800; color:var(--accent);'>{len(DOMAINS)}</div>
            <div style='font-size:0.75rem; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.07em; margin-top:10px;'>Difficulties</div>
            <div style='font-size:1.5rem; font-weight:800; color:var(--accent);'>3</div>
        </div>""", unsafe_allow_html=True)

    # --- Logic ---
    if gen_btn:
        with st.spinner("🧠 Architecting your project blueprint..."):
            result = generate_project(domain, level, keywords=keywords, model=model)

        if "error" in result:
            st.error(f"Engine Failure: {result['error']}")
            st.info(result.get("message", ""))
        else:
            st.balloons()
            st.session_state.project_result = result

    # --- Dashboard ---
    if "project_result" in st.session_state:
        res = st.session_state.project_result

        # Hero card
        st.markdown(f"""
        <div class='project-hero'>
            <div class='project-name'>💡 {res.get('project_name', 'Untitled Project')}</div>
            <div class='project-tagline'>"{res.get('tagline', '')}"</div>
            <div class='project-idea'>{res.get('idea', '')}</div>
        </div>""", unsafe_allow_html=True)

        # Main columns
        col_left, col_right = st.columns([1, 1])

        with col_left:
            # Features
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>✨ Core Features</div>", unsafe_allow_html=True)
            for feat in res.get("features", []):
                st.markdown(f"<div class='feature-item'><div class='feature-dot'></div><div>{feat}</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Tech Stack
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>⚙️ Tech Stack</div>", unsafe_allow_html=True)
            chips_html = "".join([f"<span class='tech-chip'>{t.split(' - ')[0].strip()}</span>" for t in res.get("tech_stack", [])])
            st.markdown(f"<div style='margin-bottom:14px;'>{chips_html}</div>", unsafe_allow_html=True)
            for t in res.get("tech_stack", []):
                parts = t.split(" - ", 1)
                if len(parts) == 2:
                    st.markdown(f"<div style='font-size:0.88rem; color:var(--text-secondary); margin-bottom:5px;'>**{parts[0]}** — {parts[1]}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Architecture
            if res.get("architecture"):
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-header'>🧱 Architecture</div>", unsafe_allow_html=True)
                st.write(res["architecture"])
                st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            # Roadmap
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🗺️ Build Roadmap</div>", unsafe_allow_html=True)
            render_roadmap(res.get("roadmap", []))
            st.markdown("</div>", unsafe_allow_html=True)

            # Bonus ideas
            if res.get("bonus_ideas"):
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-header'>🚀 Bonus / Extension Ideas</div>", unsafe_allow_html=True)
                for idea in res["bonus_ideas"]:
                    st.markdown(f"<div class='bonus-item'>{idea}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # Viral hooks
        gh_hook = res.get("github_readme_hook", "")
        li_hook = res.get("linkedin_hook", "")
        if gh_hook or li_hook:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>📢 Share This Project</div>", unsafe_allow_html=True)
            hc1, hc2 = st.columns(2)
            with hc1:
                st.markdown(f"<div class='hook-label'>🐙 GitHub README Hook</div><div class='hook-box'>{gh_hook}</div>", unsafe_allow_html=True)
                st.button("📋 Copy GitHub Hook", key="gh_copy", help=gh_hook)
            with hc2:
                st.markdown(f"<div class='hook-label'>💼 LinkedIn Hook</div><div class='hook-box'>{li_hook}</div>", unsafe_allow_html=True)
                st.button("📋 Copy LinkedIn Hook", key="li_copy", help=li_hook)
            st.markdown("</div>", unsafe_allow_html=True)

        # Export full plan
        export_text = f"""# {res.get('project_name', '')}
> {res.get('tagline', '')}

## Idea
{res.get('idea', '')}

## Features
{chr(10).join(['- ' + f for f in res.get('features', [])])}

## Tech Stack
{chr(10).join(['- ' + t for t in res.get('tech_stack', [])])}

## Architecture
{res.get('architecture', '')}

## Roadmap
{chr(10).join(['- ' + (item.get('week','') + ': ' + item.get('milestone','') if isinstance(item, dict) else str(item)) for item in res.get('roadmap', [])])}

## GitHub README Hook
{res.get('github_readme_hook', '')}

## LinkedIn Hook
{res.get('linkedin_hook', '')}
"""
        st.download_button(
            "⬇️ Download Full Project Blueprint (.md)",
            data=export_text,
            file_name=f"{res.get('project_name','project').replace(' ','_').lower()}_blueprint.md",
            mime="text/markdown",
            use_container_width=True
        )


if __name__ == "__main__":
    main()
