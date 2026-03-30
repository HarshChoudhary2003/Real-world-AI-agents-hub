import streamlit as st
import os
from agent import deploy_project

st.set_page_config(
    page_title="DevOS | Deployment Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_premium_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-color: #0A0A0B;
        --accent: #3B82F6;
        --accent-alt: #1D4ED8;
        --accent-glow: rgba(59, 130, 246, 0.25);
        --green: #10B981;
        --yellow: #F59E0B;
        --red: #EF4444;
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
    .list-item-green { border-left-color: var(--green); }
    .list-item-yellow { border-left-color: var(--yellow); }
    .list-item-red { border-left-color: var(--red); }

    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        background: rgba(59, 130, 246, 0.06);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .step-num {
        background: var(--accent);
        color: #000;
        font-weight: 800;
        font-size: 0.8rem;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .step-text { font-size: 0.92rem; color: var(--text-primary); line-height: 1.5; padding-top: 2px; }

    .env-chip {
        display: inline-block;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #6EE7B7;
        padding: 5px 13px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 4px 4px 4px 0;
        font-family: 'JetBrains Mono', monospace;
    }

    .platform-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent), var(--accent-alt));
        color: #fff;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .cost-box {
        background: linear-gradient(135deg, rgba(59,130,246,0.12), rgba(16,185,129,0.08));
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        margin-bottom: 16px;
    }
    .cost-label { font-size: 0.75rem; color: var(--text-secondary); letter-spacing: 0.07em; text-transform: uppercase; }
    .cost-value { font-size: 2rem; font-weight: 800; color: var(--accent); margin: 6px 0; }
    .cost-note { font-size: 0.85rem; color: var(--text-secondary); }

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


PLATFORM_ICONS = {
    "Render (Free Tier)": "🟣",
    "AWS ECS (Fargate)": "🟠",
    "AWS Lambda (Serverless)": "🟠",
    "Google Cloud Run": "🔵",
    "Vercel": "⚫",
    "Railway": "🟤",
    "Fly.io": "🟡",
    "DigitalOcean App Platform": "🔵",
    "Azure Container Apps": "🔷",
    "Kubernetes (Self-managed)": "⚙️",
}


def main():
    apply_premium_style()

    # --- Sidebar ---
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/rocket.png", width=75)
        st.title("DevOS")
        st.markdown("<p class='subtext'>AI Deployment & DevOps Agent.</p>", unsafe_allow_html=True)
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
        st.subheader("☁️ Deployment Settings")
        platform = st.selectbox("Target Platform", list(PLATFORM_ICONS.keys()))
        enable_k8s = st.toggle("⚙️ Include Kubernetes Manifest", value=False,
            help="Generate a K8s Deployment + Service YAML for container orchestration.")

        st.markdown("---")
        st.info("💡 **DevOps Tip:** Never hardcode secrets. Always use environment variables and secret managers.")

    # --- Header ---
    col_hdr, col_stats = st.columns([3, 1])
    with col_hdr:
        st.markdown("<div class='status-badge'>DEVOPS ENGINE READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom:6px;'>🚀 Deployment & DevOps Agent</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:1.15rem; color:var(--text-secondary); margin-bottom:28px;'>From project idea to cloud-deployed production system — automated.</p>", unsafe_allow_html=True)

    # --- Input ---
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col_proj, col_stack = st.columns([2, 1])
        with col_proj:
            project = st.text_area(
                "💡 Project Description",
                value="A Streamlit AI chatbot powered by OpenAI with conversation history and user authentication.",
                height=130,
                placeholder="Describe your project in detail..."
            )
        with col_stack:
            stack = st.text_area(
                "⚙️ Tech Stack",
                value="Python, Streamlit, OpenAI API, SQLite",
                height=130,
                placeholder="e.g. FastAPI, PostgreSQL, Redis, Docker"
            )
        deploy_btn = st.button("🚀 GENERATE DEPLOYMENT PLAN", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Stats ---
    with col_stats:
        icon = PLATFORM_ICONS.get(platform, "☁️")
        st.markdown(f"""
        <div class='glass-card' style='padding:20px; margin-top:80px; text-align:center;'>
            <h4 style='margin:0; color:var(--accent);'>TARGET PLATFORM</h4>
            <div style='font-size:2.5rem; margin:10px 0;'>{icon}</div>
            <div style='font-size:0.85rem; color:var(--text-secondary);'>{platform}</div>
        </div>""", unsafe_allow_html=True)

    # --- Logic ---
    if deploy_btn:
        if not project.strip():
            st.error("Please describe your project.")
        else:
            with st.spinner(f"🧠 Principal DevOps Engineer architecting your deployment on {platform}..."):
                result = deploy_project(project, stack, platform=platform, enable_k8s=enable_k8s, model=model)

            if "error" in result:
                st.error(f"Engine Failure: {result['error']}")
                st.info(result.get("message", ""))
            else:
                st.success(f"✅ Deployment Plan Ready: **{result.get('title', 'Project')}**")
                st.session_state.deploy_result = result

    # --- Dashboard ---
    if "deploy_result" in st.session_state:
        res = st.session_state.deploy_result

        # Cost box
        cost = res.get("cost_estimate", {})
        if cost:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class='cost-box'>
                    <div class='cost-label'>Est. Monthly Cost</div>
                    <div class='cost-value'>{cost.get('monthly','N/A')}</div>
                    <div class='cost-note'>{cost.get('notes','')[:80]}</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class='cost-box' style='border-color:rgba(16,185,129,0.3);'>
                    <div class='cost-label'>Platform</div>
                    <div class='cost-value' style='font-size:1.1rem; padding:8px 0;'>{PLATFORM_ICONS.get(platform,'☁️')} {platform.split('(')[0].strip()}</div>
                    <div class='cost-note'>Target deployment environment</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                k8s_status = "✅ Included" if enable_k8s else "⏭️ Skipped"
                st.markdown(f"""
                <div class='cost-box' style='border-color:rgba(245,158,11,0.3);'>
                    <div class='cost-label'>Kubernetes</div>
                    <div class='cost-value' style='font-size:1rem; padding:12px 0; color:var(--yellow);'>{k8s_status}</div>
                    <div class='cost-note'>Container orchestration manifest</div>
                </div>""", unsafe_allow_html=True)

        # Tab layout for different artifact types
        tab_docker, tab_compose, tab_cicd, tab_k8s = st.tabs([
            "🐳 Dockerfile", "🔧 Docker Compose", "⚡ GitHub Actions CI/CD", "☸️ Kubernetes"
        ])

        with tab_docker:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🐳 Dockerfile</div>", unsafe_allow_html=True)
            st.code(res.get("docker_setup", "# Dockerfile not generated"), language="docker")
            if res.get("docker_setup"):
                st.download_button("⬇️ Download Dockerfile", data=res["docker_setup"],
                    file_name="Dockerfile", mime="text/plain", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_compose:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🔧 docker-compose.yml</div>", unsafe_allow_html=True)
            st.code(res.get("docker_compose", "# docker-compose not generated"), language="yaml")
            if res.get("docker_compose"):
                st.download_button("⬇️ Download docker-compose.yml", data=res["docker_compose"],
                    file_name="docker-compose.yml", mime="text/plain", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_cicd:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>⚡ GitHub Actions Workflow</div>", unsafe_allow_html=True)
            st.code(res.get("ci_cd_yaml", "# CI/CD YAML not generated"), language="yaml")
            if res.get("ci_cd_yaml"):
                st.download_button("⬇️ Download .github/workflows/deploy.yml",
                    data=res["ci_cd_yaml"], file_name="deploy.yml", mime="text/plain", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_k8s:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>☸️ Kubernetes Manifest</div>", unsafe_allow_html=True)
            k8s = res.get("kubernetes_manifest", "N/A")
            if k8s and k8s != "N/A":
                st.code(k8s, language="yaml")
                st.download_button("⬇️ Download k8s-manifest.yml", data=k8s,
                    file_name="k8s-manifest.yml", mime="text/plain", use_container_width=True)
            else:
                st.info("☸️ Kubernetes manifest was not requested. Enable the toggle in the sidebar and regenerate.")
            st.markdown("</div>", unsafe_allow_html=True)

        # Bottom row: deployment steps, env vars, security
        col_left, col_right = st.columns([1, 1])

        with col_left:
            # Deployment Steps
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>☁️ Deployment Steps</div>", unsafe_allow_html=True)
            for i, step in enumerate(res.get("deployment_steps", []), 1):
                st.markdown(f"""
                <div class='step-item'>
                    <div class='step-num'>{i}</div>
                    <div class='step-text'>{step}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # CI/CD Suggestions
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>🔁 CI/CD Suggestions</div>", unsafe_allow_html=True)
            for item in res.get("ci_cd_suggestions", []):
                st.markdown(f"<div class='list-item list-item-green'>{item}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            # Environment Variables
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'>⚙️ Environment Variables</div>", unsafe_allow_html=True)
            env_vars = res.get("env_variables", [])
            env_html = "".join([f"<span class='env-chip'>{v.split('=')[0]}</span>" for v in env_vars])
            st.markdown(f"<div style='margin-bottom:14px;'>{env_html}</div>", unsafe_allow_html=True)
            env_content = "\n".join(env_vars)
            st.code(env_content, language="bash")
            st.download_button("⬇️ Download .env.example", data=env_content,
                file_name=".env.example", mime="text/plain", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Security Checklist
            security = res.get("security_checklist", [])
            if security:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("<div class='section-header'>🔐 Security Checklist</div>", unsafe_allow_html=True)
                for item in security:
                    st.markdown(f"<div class='list-item list-item-yellow'>🔒 {item}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
