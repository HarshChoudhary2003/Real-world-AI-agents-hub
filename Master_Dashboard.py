import streamlit as st

st.set_page_config(page_title="Productivity Suite AI | Central Hub", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #020617;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .subtitle {
        color: #94A3B8;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }

    .app-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        border-color: #38BDF8;
    }
    
    .app-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .app-desc {
        color: #94A3B8;
        font-size: 0.95rem;
        flex-grow: 1;
        margin-bottom: 1.5rem;
    }
    
    .launch-btn {
        display: inline-block;
        background: #38BDF8;
        color: #020617 !important;
        text-decoration: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        text-align: center;
        transition: background 0.2s;
    }
    
    .launch-btn:hover {
        background: #7DD3FC;
    }
    
    /* Category styles */
    .cat-badge {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 20px;
        margin-bottom: 1rem;
        display: inline-block;
    }
    .cat-planning { background: rgba(56, 189, 248, 0.1); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.2); }
    .cat-comms { background: rgba(167, 139, 250, 0.1); color: #A78BFA; border: 1px solid rgba(167, 139, 250, 0.2); }
    .cat-knowledge { background: rgba(52, 211, 153, 0.1); color: #34D399; border: 1px solid rgba(52, 211, 153, 0.2); }
    .cat-tracking { background: rgba(244, 114, 182, 0.1); color: #F472B6; border: 1px solid rgba(244, 114, 182, 0.2); }

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Personal Productivity OS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your 10-Agent Neural Architecture. Automate your entire operational day.</div>', unsafe_allow_html=True)

# Define the apps
apps = [
    {
        "name": "TaskBrain AI",
        "icon": "🧠",
        "desc": "Daily Priority App. NLP task ingestion, sub-task breakdowns, and urgency sorting.",
        "port": 8501,
        "cat": "planning",
        "cat_name": "Planning & Focus"
    },
    {
        "name": "MailMind AI",
        "icon": "📧",
        "desc": "Intelligently summarize long email threads, extract logic maps, and generate action items.",
        "port": 8502,
        "cat": "comms",
        "cat_name": "Comms & Outreach"
    },
    {
        "name": "SyncGuard AI",
        "icon": "📅",
        "desc": "Calendar Conflict Resolver. Detect logic overlaps and gracefully resolve double-bookings.",
        "port": 8503,
        "cat": "planning",
        "cat_name": "Planning & Focus"
    },
    {
        "name": "AgendaCraft AI",
        "icon": "📋",
        "desc": "Engineered meeting timelines. Drop in loose ideas; get structured ics calendar blocks out.",
        "port": 8504,
        "cat": "comms",
        "cat_name": "Comms & Outreach"
    },
    {
        "name": "BrainVault AI",
        "icon": "🗄️",
        "desc": "Local Knowledge RAG vector space. Ask questions against your private text arrays.",
        "port": 8505,
        "cat": "knowledge",
        "cat_name": "Intel & Knowledge"
    },
    {
        "name": "Reflect AI",
        "icon": "🧘",
        "desc": "Daily Goal Reflection. Algorithmically parse why you succeeded or failed your targets today.",
        "port": 8506,
        "cat": "tracking",
        "cat_name": "Habits & Tracking"
    },
    {
        "name": "PingCraft AI",
        "icon": "🔔",
        "desc": "Smart Notification Engine. Mathematically space out deadline alerts to prevent fatigue.",
        "port": 8507,
        "cat": "planning",
        "cat_name": "Planning & Focus"
    },
    {
        "name": "ActionForge AI",
        "icon": "⚡",
        "desc": "Neural Task Extractor. Rip strict actionable deliverables out of chaotic unstructured text.",
        "port": 8508,
        "cat": "knowledge",
        "cat_name": "Intel & Knowledge"
    },
    {
        "name": "ChronoBlock AI",
        "icon": "⏳",
        "desc": "Mathematical continuous task packing. Eliminate empty space in your operational blocks.",
        "port": 8509,
        "cat": "planning",
        "cat_name": "Planning & Focus"
    },
    {
        "name": "StreakForge AI",
        "icon": "🔥",
        "desc": "Algorithmic Habit Tracking. Plotly heatmaps and persistence density metrics.",
        "port": 8510,
        "cat": "tracking",
        "cat_name": "Habits & Tracking"
    }
]

# Layout rows
for i in range(0, len(apps), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(apps):
            app = apps[i + j]
            with cols[j]:
                st.markdown(f"""
                <div class="app-card">
                    <div class="cat-badge cat-{app['cat']}">{app['cat_name']}</div>
                    <div class="app-title">{app['icon']} {app['name']}</div>
                    <div class="app-desc">{app['desc']}</div>
                    <a href="http://localhost:{app['port']}" target="_blank" class="launch-btn">Launch Application →</a>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center; color:#64748B;'>System Operational • 10 Neural Agents Online • Engineered for Enterprise </div>", unsafe_allow_html=True)
