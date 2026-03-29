import streamlit as st
import json
import base64
import os
from agent import design_system_advanced
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="DevOS | System Architect",
    page_icon="🧠",
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
        --accent: #FF5E0E; /* Tech Orange */
        --accent-glow: rgba(255, 94, 14, 0.2);
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
        margin-bottom: 10px;
        letter-spacing: 0.05em;
    }

    /* Subtext Styling */
    .subtext {
        font-size: 0.95rem;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }

    /* Mermaid Visual Container */
    .mermaid-container {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    /* Data Flow List */
    .flow-item {
        background: rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid var(--border-color);
        padding: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .flow-number {
        color: var(--accent);
        font-weight: 800;
        font-size: 1.2rem;
        min-width: 30px;
    }

    /* Buttons Hub */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent), #FF8533);
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

# --- Mermaid Support Function ---
def render_mermaid(mermaid_code):
    """
    Renders Mermaid code in Streamlit using a simple HTML wrapper.
    """
    html_code = f"""
    <div class="mermaid">
    {mermaid_code}
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
    """
    return st.components.v1.html(html_code, height=600, scrolling=True)

# --- Application Main ---
def main():
    apply_premium_style()

    # -- Sidebar Config --
    with st.sidebar:
        st.image("https://img.icons8.com/parakeet/512/000000/tree-structure.png", width=80) 
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

        st.subheader("📊 System Constraints")
        scale = st.selectbox(
            "User Scale Intensity",
            ["Small (1K users)", "Medium (100K users)", "Large (1M+ users)", "Ultra (Global Swarm)"],
            index=2
        )
        
        st.markdown("---")
        st.info("💡 **Tip:** Mention specific latency (e.g., <100ms) or consistency (e.g., Eventual vs Strong) requirements.")

    # -- Main Content Area --
    col_main, col_stats = st.columns([3.2, 1])

    with col_main:
        st.markdown("<div class='status-badge'>BLUEPRINT READY</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin-bottom: 5px;'>🏗️ AI System Architect</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; margin-bottom: 30px; color: var(--text-secondary);'>Architecting billion-scale platforms in real-time.</p>", unsafe_allow_html=True)

    # -- Input Component --
    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        idea = st.text_area(
            "🎯 System Objective",
            placeholder="Ex: Architect a distributed, real-time betting platform for global cricket matches with ultra-low latency requirements and live balance updates.",
            height=150
        )
        arch_btn = st.button("🚀 GENERATE BLUEPRINT", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # -- Result Engine --
    if arch_btn:
        if not idea:
            st.warning("Please define a system objective.")
        else:
            with st.spinner("🧠 Staff Engineer architecting distributed clusters..."):
                result = design_system_advanced(idea, scale, model=model)
            
            if "error" in result:
                st.error(f"Design Error: {result['error']}")
            else:
                st.balloons()
                st.success(f"✅ Architecture for '{result.get('system_name','System')}' Ready!")
                st.session_state.arch_result = result

    # -- Display Architecture --
    if "arch_result" in st.session_state:
        res = st.session_state.arch_result
        
        tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Architecture Visual", "📦 Core Components", "💾 Database & APIs", "💰 Cost & Scale"])
        
        with tab1:
            st.markdown("<div class='section-header'>📐 Topographical Blueprint</div>", unsafe_allow_html=True)
            if res.get("mermaid_diagram"):
                render_mermaid(res["mermaid_diagram"])
            else:
                st.warning("High-level diagram not available for this scale.")
            
            st.markdown("<div class='section-header' style='margin-top: 30px;'>🔄 System Execution Flow</div>", unsafe_allow_html=True)
            for i, step in enumerate(res.get("data_flow", [])):
                st.markdown(f"<div class='flow-item'><div class='flow-number'>{i+1}</div>{step}</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div class='section-header'>🧱 Distributed Components</div>", unsafe_allow_html=True)
            cols = st.columns(min(len(res.get("components", [])), 3))
            for i, comp in enumerate(res.get("components", [])):
                with cols[i % 3]:
                    st.markdown(f"**{comp['name']}**")
                    st.caption(comp.get("tech_choice", "Tech Agnostic"))
                    st.write(comp["responsibility"])
            
            st.markdown("<div class='section-header' style='margin-top: 30px;'>⚙️ Tech Stack Hub</div>", unsafe_allow_html=True)
            stack_cols = st.columns(4)
            ts = res.get("tech_stack", {})
            with stack_cols[0]: st.write("**Frontend**\n" + "\n".join([f"- {i}" for i in ts.get("frontend", [])]))
            with stack_cols[1]: st.write("**Backend**\n" + "\n".join([f"- {i}" for i in ts.get("backend", [])]))
            with stack_cols[2]: st.write("**Data**\n" + "\n".join([f"- {i}" for i in ts.get("database", [])]))
            with stack_cols[3]: st.write("**Infrastructure**\n" + "\n".join([f"- {i}" for i in ts.get("devops", [])]))

        with tab3:
            st.markdown("<div class='section-header'>💾 Tactical Database Schema</div>", unsafe_allow_html=True)
            for db in res.get("database_schema", []):
                st.markdown(f"**Table: {db['table']}**")
                st.code("\n".join(db.get("columns", [])), language="sql")
            
            st.markdown("<div class='section-header' style='margin-top: 30px;'>🔌 API Endpoint Specification</div>", unsafe_allow_html=True)
            st.table(res.get("api_endpoints", []))

        with tab4:
            st.markdown("<div class='section-header'>📈 Multi-Phase Scaling Protocol</div>", unsafe_allow_html=True)
            for s in res.get("scaling_strategy", []):
                st.markdown(f"🎯 **{s['aspect']}**: {s['solution']}")
            
            st.markdown("<div class='section-header' style='margin-top: 30px;'>💰 Estimated Monthly Expenditure</div>", unsafe_allow_html=True)
            for cost in res.get("cost_estimation", []):
                st.metric(cost["service"], cost["estimated_monthly_cost"], cost.get("rationale", "Standard Infra"))

    # -- Stats Sidebar Insight --
    with col_stats:
        st.markdown("<div class='glass-card' style='padding: 20px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0; color:var(--accent); text-align:center;'>BLUEPRINT STATS</h4>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric("Scalability Factor", "10M+", "Tier-1")
        st.metric("Fault Tolerance", "99.99%", "High")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
