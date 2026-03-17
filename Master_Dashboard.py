import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Agents Hub | Master Control Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');

    /* Global Background */
    .stApp {
        background-color: #020617;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 2rem;
        margin-bottom: 0px;
    }
    
    .subtitle {
        color: #94A3B8;
        font-size: 1.4rem;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        color: #94A3B8;
        font-size: 1rem;
        font-weight: 600;
        padding: 0px 24px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(56, 189, 248, 0.1);
        color: #38BDF8;
    }

    .stTabs [aria-selected="true"] {
        background-color: #38BDF8 !important;
        color: #020617 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }

    /* Card Styling */
    .app-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.75rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 280px;
        display: flex;
        flex-direction: column;
        margin-bottom: 1.5rem;
    }
    
    .app-card:hover {
        transform: translateY(-8px);
        background: rgba(15, 23, 42, 0.8);
        border-color: #38BDF8;
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
    }
    
    .app-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .app-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 0.75rem;
    }
    
    .app-desc {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.5;
        flex-grow: 1;
        margin-bottom: 1.5rem;
    }
    
    .launch-link {
        text-decoration: none;
        background: linear-gradient(90deg, #38BDF8 0%, #2563EB 100%);
        color: #FFFFFF !important;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.9rem;
        text-align: center;
        transition: all 0.2s;
        display: block;
    }
    
    .launch-link:hover {
        filter: brightness(1.2);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }

    /* Category Badges */
    .cat-badge {
        font-size: 0.7rem;
        text-transform: uppercase;
        font-weight: 900;
        padding: 3px 8px;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        display: inline-block;
        letter-spacing: 0.05em;
    }
    .badge-blue { background: rgba(56, 189, 248, 0.1); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.2); }
    .badge-purple { background: rgba(167, 139, 250, 0.1); color: #A78BFA; border: 1px solid rgba(167, 139, 250, 0.2); }
    .badge-green { background: rgba(52, 211, 153, 0.1); color: #34D399; border: 1px solid rgba(52, 211, 153, 0.2); }
</style>
""", unsafe_allow_html=True)

# Main Branding
st.markdown('<div class="main-title">AI Agents Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Global Control Center for 100+ Neural Architectures</div>', unsafe_allow_html=True)

# Define Tabs
tab_productivity, tab_writing, tab_research = st.tabs([
    "🚀 Personal Productivity",
    "✍️ Writing & Content",
    "🔍 Research & Analysis"
])

def render_agent_grid(agents):
    for i in range(0, len(agents), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(agents):
                agent = agents[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="app-card">
                        <div class="cat-badge {agent['badge_class']}">{agent['category']}</div>
                        <div class="app-icon">{agent['icon']}</div>
                        <div class="app-title">{agent['name']}</div>
                        <div class="app-desc">{agent['desc']}</div>
                        <a href="{agent['url']}" target="_blank" class="launch-link">Launch {agent['name']} →</a>
                    </div>
                    """, unsafe_allow_html=True)

# 1. Productivity Suite Agents
productivity_agents = [
    {"name": "TaskBrain AI", "icon": "🧠", "desc": "NLP task ingestion, sub-task breakdowns, and urgency sorting.", "category": "Planning", "badge_class": "badge-blue", "url": "http://localhost:8501"},
    {"name": "MailMind AI", "icon": "📧", "desc": "Summarize long email threads and generate action items intelligently.", "category": "Comms", "badge_class": "badge-purple", "url": "http://localhost:8502"},
    {"name": "SyncGuard AI", "icon": "📅", "desc": "Calendar Conflict Resolver. Detect logic overlaps and resolve double-bookings.", "category": "Planning", "badge_class": "badge-blue", "url": "http://localhost:8503"},
    {"name": "AgendaCraft AI", "icon": "📋", "desc": "Engineered meeting timelines. Transform loose ideas into structured blocks.", "category": "Comms", "badge_class": "badge-purple", "url": "http://localhost:8504"},
    {"name": "BrainVault AI", "icon": "🗄️", "desc": "Local Knowledge RAG vector space. Ask questions against your private text arrays.", "category": "Knowledge", "badge_class": "badge-green", "url": "http://localhost:8505"},
    {"name": "Reflect AI", "icon": "🧘", "desc": "Daily Goal Reflection. Algorithmically parse daily success and failure metrics.", "category": "Tracking", "badge_class": "badge-blue", "url": "http://localhost:8506"},
    {"name": "PingCraft AI", "icon": "🔔", "desc": "Smart Notification Engine. Mathematically space out alerts to prevent fatigue.", "category": "Planning", "badge_class": "badge-blue", "url": "http://localhost:8507"},
    {"name": "ActionForge AI", "icon": "⚡", "desc": "Neural Task Extractor. Rip actionable deliverables out of chaotic text.", "category": "Knowledge", "badge_class": "badge-green", "url": "http://localhost:8508"},
    {"name": "ChronoBlock AI", "icon": "⏳", "desc": "Mathematical continuous task packing to eliminate empty operational space.", "category": "Planning", "badge_class": "badge-blue", "url": "http://localhost:8509"},
    {"name": "StreakForge AI", "icon": "🔥", "desc": "Algorithmic Habit Tracking with Plotly heatmaps and density metrics.", "category": "Tracking", "badge_class": "badge-blue", "url": "http://localhost:8510"}
]

# 2. Writing & Content Studio Agents
writing_agents = [
    {"name": "BlogCraft AI", "icon": "📝", "desc": "Research, outline, and write SEO-optimized blog posts automatically.", "category": "Creation", "badge_class": "badge-purple", "url": "http://localhost:8511"},
    {"name": "LetterForge", "icon": "💼", "desc": "Tailor high-impact cover letters to your background and job descriptions.", "category": "Career", "badge_class": "badge-blue", "url": "http://localhost:8512"},
    {"name": "FAQGen Pro", "icon": "💬", "desc": "Extract friction points to synthesize highly credible, trust-building FAQs.", "category": "Marketing", "badge_class": "badge-green", "url": "http://localhost:8513"},
    {"name": "GrammarGuard", "icon": "✨", "desc": "Deep semantic editing and tone correction beyond standard checks.", "category": "Polishing", "badge_class": "badge-purple", "url": "http://localhost:8514"},
    {"name": "HookPoint AI", "icon": "🔗", "desc": "Formulate high-engagement, viral-ready LinkedIn hooks and posts.", "category": "Social", "badge_class": "badge-blue", "url": "http://localhost:8515"},
    {"name": "CopyAlchemy", "icon": "🛍️", "desc": "Map technical features to real-world outcomes for narrative conversions.", "category": "Marketing", "badge_class": "badge-green", "url": "http://localhost:8516"},
    {"name": "ResumeRocket", "icon": "📄", "desc": "Algorithmic parsing and enhancement based on job roles and ATS metrics.", "category": "Career", "badge_class": "badge-blue", "url": "http://localhost:8517"},
    {"name": "SEOptimize", "icon": "🔎", "desc": "Transform seed queries into high-intent predictive SEO keyword clusters.", "category": "Marketing", "badge_class": "badge-green", "url": "http://localhost:8518"},
    {"name": "SlideStream", "icon": "📽️", "desc": "Convert chaotic scripts into beautifully paced, visually striking slide decks.", "category": "Presentation", "badge_class": "badge-purple", "url": "http://localhost:8519"},
    {"name": "ToneTuner", "icon": "🎭", "desc": "Recalibrate text into any persona while guaranteeing semantic fidelity.", "category": "Polishing", "badge_class": "badge-purple", "url": "http://localhost:8520"}
]

# 3. Research & Analysis Studio Agents
research_agents = [
    {"name": "ScholarAI", "icon": "🎓", "desc": "Deconstruct complex scientific literature into plain-language summaries.", "category": "Academic", "badge_class": "badge-blue", "url": "http://localhost:8521"},
    {"name": "CompeteIntel AI", "icon": "⚔️", "desc": "Map competitive landscapes and identify market white spaces with DNA audits.", "category": "Strategy", "badge_class": "badge-purple", "url": "http://localhost:8522"},
    {"name": "TrendSynthetix AI", "icon": "💹", "desc": "Synthesize market signals into structured actionable insights and trends.", "category": "Market", "badge_class": "badge-green", "url": "http://localhost:8523"},
    {"name": "NewsFlow", "icon": "📰", "desc": "Distill global news cycles into thematic, structured intelligence digests.", "category": "News", "badge_class": "badge-blue", "url": "http://localhost:8524"},
    {"name": "WebScout AI", "icon": "🌐", "desc": "Autonomous intelligence engine designed to synthesize complex web topics.", "category": "Deep Web", "badge_class": "badge-purple", "url": "http://localhost:8525"},
    {"name": "StreamBrief", "icon": "🎬", "desc": "Transform dense video transcripts into structured intelligence and insights.", "category": "Media", "badge_class": "badge-green", "url": "http://localhost:8526"},
    {"name": "SWOT Horizon AI", "icon": "🎯", "desc": "Advanced SWOT-to-TOWS matrix generator with multi-model strategic analysis.", "category": "Strategy", "badge_class": "badge-purple", "url": "http://localhost:8527"},
    {"name": "PolicyGuard AI", "icon": "⚖️", "desc": "Precise thematic synthesis for enterprise policies and regulatory frameworks.", "category": "Compliance", "badge_class": "badge-green", "url": "http://localhost:8528"},
    {"name": "CapitalMind AI", "icon": "💰", "desc": "Architect rigorous, evidence-driven investment theses with neural intelligence.", "category": "Finance", "badge_class": "badge-purple", "url": "http://localhost:8529"}
]

with tab_productivity:
    st.markdown("<br>", unsafe_allow_html=True)
    render_agent_grid(productivity_agents)

with tab_writing:
    st.markdown("<br>", unsafe_allow_html=True)
    render_agent_grid(writing_agents)

with tab_research:
    st.markdown("<br>", unsafe_allow_html=True)
    render_agent_grid(research_agents)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding: 2rem;'>
    <p style='color:#94A3B8; font-size: 1rem;'>
        Developed with ❤️ by <a href='https://github.com/HarshChoudhary2003' style='color:#38BDF8; text-decoration:none;'>Harsh Choudhary</a>
    </p>
    <p style='color:#475569; font-size: 0.8rem;'>
        System Operational • 29 Neural Agents Online • Engineered for Enterprise Automation
    </p>
</div>
""", unsafe_allow_html=True)
