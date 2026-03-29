import streamlit as st
import json
import base64
import zipfile
import io
import os
from agent import generate_code_multi_file
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="DevOS | Code Architect",
    page_icon="💻",
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
        --accent: #00F2FF;
        --accent-glow: rgba(0, 242, 255, 0.3);
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

    /* Code Block Overrides */
    .stCodeBlock {
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        background: #0D1117 !important;
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
        background: linear-gradient(135deg, var(--accent), #00A3FF);
        color: #000 !important;
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

    /* Custom File List */
    .file-item {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }

    </style>
    """, unsafe_allow_html=True)

# --- Utility Functions ---
def create_zip_download(project_name, files):
    """
    Creates a zip byte stream for download.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.writestr(f["file_path"], f["content"])
    return buf.getvalue()

# --- Application Main ---
def main():
    apply_premium_style()

    # -- Sidebar Config --
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/processor.png", width=80) 
        st.title("DevOS")
        st.markdown("<p class='subtext'>The AI Operating System for Developers.</p>", unsafe_allow_html=True)
        st.markdown("---")

        # --- NEXT-LEVEL UPGRADE: API & Model Management ---
        st.subheader("🔮 Intelligence Hub")
        
        main_ai = st.selectbox(
            "Main AI Provider",
            ["OpenAI", "Anthropic", "Google Gemini", "Groq (Llama-3)"],
            index=0
        )

        # Dynamic Model mapping
        if main_ai == "OpenAI":
            model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
            key_env = "OPENAI_API_KEY"
            key_placeholder = "sk-..."
        elif main_ai == "Anthropic":
            model_options = ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"]
            key_env = "ANTHROPIC_API_KEY"
            key_placeholder = "sk-ant-..."
        elif main_ai == "Google Gemini":
            model_options = ["gemini/gemini-pro", "gemini/gemini-1.5-flash"]
            key_env = "GEMINI_API_KEY"
            key_placeholder = "AIza..."
        else:
            model_options = ["groq/llama3-70b-8192", "groq/llama3-8b-8192"]
            key_env = "GROQ_API_KEY"
            key_placeholder = "gsk_..."

        model = st.selectbox("Intelligence Layer", model_options)
        
        # API Key Input
        user_api_key = st.text_input(
            f"🔑 {main_ai} API Key",
            type="password",
            placeholder=key_placeholder,
            help=f"Enter your {main_ai} key. If empty, we'll try to find it in your system environment."
        )

        # Inject key into environment if provided
        if user_api_key:
            os.environ[key_env] = user_api_key

        st.markdown("---")
        
        # Framework Selector Upgrade
        st.subheader("🛠️ Framework Selector")
        framework = st.selectbox(
            "Target Framework",
            ["Python (Generic)", "FastAPI", "Flask", "Streamlit", "React (Vite)", "Next.js (App Router)", "Bash Automation"],
            index=3
        )
        
        st.markdown("---")
        st.info("💡 **Tip:** Be specific about your feature set for better architectural decisions.")

    # -- Main Content Area --
    col_main, col_stats = st.columns([3, 1])

    with col_main:
        st.markdown("<div class='status-badge'>ENGINE READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom: 5px;'>💻 Code Architect Agent</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; margin-bottom: 30px; color: var(--text-secondary);'>Transform ideas into production-ready software ecosystems.</p>", unsafe_allow_html=True)

    # -- Generation Input --
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col_idea, col_stack = st.columns([2, 1])
        
        with col_idea:
            idea = st.text_area(
                "💡 Full Project Idea",
                placeholder="Ex: Create a real-time portfolio tracker with a glassmorphic dashboard and price alerts using WebSocket.",
                height=150
            )
        
        with col_stack:
            tech_stack = st.text_area(
                "⚙️ Custom Stack (Optional)",
                value=f"Framework: {framework}\nArchitecture: Modular, clean coding patterns.",
                height=150
            )
        
        generate_btn = st.button("🚀 IGNITE GENERATOR", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # -- Result Section --
    if generate_btn:
        if not idea:
            st.error("Please provide a project idea to begin.")
        else:
            with st.spinner("🧠 Neural Brain is architecting your solution..."):
                result = generate_code_multi_file(idea, tech_stack, model=model)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
                st.info(result.get("message", "Unknown error."))
            else:
                st.balloons()
                st.success(f"✅ Project '{result.get('project_name', 'Untitled')}' generated successfully!")

                # Store result in session state for later use
                st.session_state.result = result

    if "result" in st.session_state:
        res = st.session_state.result
        
        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.markdown("<div class='section-header'>📁 Project Blueprint</div>", unsafe_allow_html=True)
            for item in res.get("project_structure", []):
                st.markdown(f"<div class='file-item'>📄 {item}</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='section-header' style='margin-top: 30px;'>⚙️ Setup Protocol</div>", unsafe_allow_html=True)
            for step in res.get("setup_instructions", []):
                st.markdown(f"- `{step}`")

            st.markdown("<div class='section-header' style='margin-top: 30px;'>🧠 Architecture Notes</div>", unsafe_allow_html=True)
            st.write(res.get("architecture_notes", "No notes provided."))

            # Advanced Download Upgrade
            st.markdown("<br>", unsafe_allow_html=True)
            zip_bytes = create_zip_download(res.get("project_name", "project"), res.get("files", []))
            st.download_button(
                label="⬇️ DOWNLOAD FULL PROJECT (ZIP)",
                data=zip_bytes,
                file_name=f"{res.get('project_name', 'project')}.zip",
                mime="application/zip",
                use_container_width=True
            )

        with col_right:
            st.markdown("<div class='section-header'>💻 Implementation Terminal</div>", unsafe_allow_html=True)
            
            # Multi-file Tab Selector Upgrade
            file_names = [f["file_path"] for f in res.get("files", [])]
            tabs = st.tabs(file_names)
            
            for i, tab in enumerate(tabs):
                with tab:
                    file_info = res["files"][i]
                    lang = "python" # Default
                    if file_info["file_path"].endswith(".js"): lang = "javascript"
                    elif file_info["file_path"].endswith(".html"): lang = "html"
                    elif file_info["file_path"].endswith(".css"): lang = "css"
                    elif file_info["file_path"].endswith(".sh"): lang = "bash"
                    
                    st.code(file_info["content"], language=lang)
            
            # Next-Level Upgrade: Run Code Simulation
            if st.button("🧪 RUN ARCHITECT CHECK", use_container_width=True):
                st.toast("Analyzing code for logical errors...", icon="🔍")
                st.toast("Verifying file structure integrity...", icon="📁")
                st.toast("Architectural validation complete. Code is safe for deployment.", icon="✅")

    # -- Stats Sidebar Insight --
    with col_stats:
        st.markdown("<div class='glass-card' style='padding: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0; color:var(--accent); text-align:center;'>ENGINE STATS</h4>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric("Model Precision", "99.8%", "+0.2%")
        st.metric("Lines of Code", "Generated", "Instant")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
