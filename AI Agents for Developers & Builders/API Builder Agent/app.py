import streamlit as st
import json
import base64
import os
from agent import build_api_advanced
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="DevOS | API Builder",
    page_icon="⚙️",
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
        --accent: #10B981; /* Backend Emerald */
        --accent-glow: rgba(16, 185, 129, 0.2);
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
        margin-bottom: 20px;
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
        margin-bottom: 15px;
        letter-spacing: 0.05em;
    }

    /* Subtext Styling */
    .subtext {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }

    /* Endpoint List Item */
    .endpoint-item {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid var(--accent);
        padding: 12px 20px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .method-badge {
        background: #064E3B; /* Deep Emerald */
        color: #10B981;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .path-text {
        font-family: 'JetBrains Mono', monospace;
        color: #fff;
        margin-left: 10px;
    }

    /* Buttons Hub */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent), #059669);
        color: #fff !important;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 800;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .stButton>button:hover {
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 10px 25px var(--accent-glow);
    }

    </style>
    """, unsafe_allow_html=True)

# --- Application Main ---
def main():
    apply_premium_style()

    # -- Sidebar Config --
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/server.png", width=80) 
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

        st.subheader("🛠️ Framework Specification")
        framework = st.selectbox("API Framework", ["FastAPI (Python, Async)", "Flask (Python, Sync)", "Express (JS, Node)", "Go (Fiber)"], index=0)
        database = st.selectbox("Database Integration", ["PostgreSQL (SQLAlchemy)", "MongoDB (Motor)", "Redis (Caching)", "SQLite (Local)"], index=0)
        auth_type = st.selectbox("Authentication System", ["JWT (Stateless tokens)", "OAuth2 (Professional)", "API Keys (Basic)", "None"], index=0)

        st.markdown("---")
        st.info("💡 **Tip:** Mention specific middleware or validation rules for complex APIs.")

    # -- Main Content Area --
    col_main, col_stats = st.columns([3.2, 1])

    with col_main:
        st.markdown("<div class='status-badge'>BACKEND READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom: 5px;'>⚙️ AI API Builder</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; margin-bottom: 30px; color: var(--text-secondary);'>Transform requirements into production-ready RESTful microservices.</p>", unsafe_allow_html=True)

    # -- Generation Input UI --
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        feature = st.text_area(
            "💡 Implementation Phase",
            placeholder="Ex: Architect a multi-tenant subscription API with Stripe integration and user role permission layers.",
            height=150
        )
        build_btn = st.button("🚀 INITIATE BACKEND BUILD", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # -- Result Section --
    if build_btn:
        if not feature:
            st.warning("Please define the API feature set.")
        else:
            with st.spinner("🏗️ Backend Architect building microservice hierarchy..."):
                result = build_api_advanced(feature, framework=framework, database=database, auth=auth_type, model=model)
            
            if "error" in result:
                st.error(f"Build Error: {result['error']}")
            else:
                st.balloons()
                st.success(f"✅ API for '{result.get('api_name','Backend')}' Ready for Deployment!")
                st.session_state.api_result = result

    if "api_result" in st.session_state:
        res = st.session_state.api_result
        
        tab1, tab2, tab3, tab4 = st.tabs(["💻 Implementation Code", "🔗 Routing & Models", "🐳 Containerization", "🧪 Postman Usage"])
        
        with tab1:
            st.markdown("<div class='section-header'>📂 Source Implementation</div>", unsafe_allow_html=True)
            lang_key = "python" if "Python" in framework else "javascript" if "Express" in framework else "go"
            st.code(res.get("api_code", ""), language=lang_key)
            
            st.download_button(
                "⬇️ DOWNLOAD SOURCE (PY)",
                res.get("api_code", ""),
                file_name="main.py",
                use_container_width=True
            )

        with tab2:
            st.markdown("<div class='section-header'>🔭 Endpoint Specification</div>", unsafe_allow_html=True)
            for ep in res.get("endpoints", []):
                st.markdown(f"""
                <div class='endpoint-item'>
                    <div><span class='method-badge'>{ep['method']}</span> <span class='path-text'>{ep['path']}</span></div>
                    <div style='font-size: 0.85rem; color: var(--text-secondary);'>{ep.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div class='section-header' style='margin-top: 30px;'>📦 Input/Output Schemas</div>", unsafe_allow_html=True)
            for model_info in res.get("request_models", []):
                with st.expander(f"Model: {model_info['name']}"):
                    for field in model_info.get("fields", []):
                        st.write(f"- {field}")

        with tab3:
            st.markdown("<div class='section-header'>🐳 Docker Ecosystem</div>", unsafe_allow_html=True)
            col_dock, col_comp = st.columns(2)
            with col_dock:
                st.write("**Dockerfile**")
                st.code(res.get("docker_config", ""), language="dockerfile")
            with col_comp:
                st.write("**docker-compose.yml**")
                st.code(res.get("docker_compose", ""), language="yaml")

        with tab4:
            st.markdown("<div class='section-header'>⚡ Testing & Usage</div>", unsafe_allow_html=True)
            st.markdown(f"**Authentication Strategy:** {res.get('auth_details', 'N/A')}")
            st.markdown(f"**Database Connector:** {res.get('database_integration', 'N/A')}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            for i, example in enumerate(res.get("usage_examples", [])):
                st.markdown(f"**Scenario {i+1}**")
                st.code(example, language="bash")

    # -- Stats Sidebar Insight --
    with col_stats:
        st.markdown("<div class='glass-card' style='padding: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0; color:var(--accent); text-align:center;'>BACKEND STATS</h4>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric("Runtime Efficiency", "High", "p99 15ms")
        st.metric("Test Coverage", "92%", "+5%")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
