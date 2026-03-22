import re
import json

readme_path = r"h:\100 AI Agents\README.md"
output_path = r"h:\100 AI Agents\master_hub.py"

with open(readme_path, "r", encoding="utf-8") as f:
    text = f.read()

categories_data = {}
current_category = None

lines = text.split("\n")
for line in lines:
    if line.startswith("### "):
        cat_match = re.search(r"###\s*(.*)", line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            categories_data[current_category] = []
    elif line.startswith("- ["):
        if current_category:
            agent_match = re.search(r"\[([^\]]+)\]\(([^)]+)\)\s*–\s*(.*)", line)
            if agent_match:
                name_raw = agent_match.group(1).replace("**", "").strip()
                path_raw = agent_match.group(2).strip()
                desc_raw = agent_match.group(3).strip()
                
                if path_raw.startswith("./"):
                    path_raw = path_raw[2:]
                github_url = f"https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/{path_raw}"
                
                categories_data[current_category].append({
                    "name": name_raw,
                    "url": github_url,
                    "desc": desc_raw
                })

# Build the main template
template = r"""import streamlit as st
import json
import re

st.set_page_config(
    page_title="Agent OS | Dynamic Hub",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CATEGORIES_RAW = __CATEGORIES_DATA__

# Sanitize data for surrogate-sensitive environments
def sanitize(text):
    if not isinstance(text, str): return text
    return text.encode('utf-8', 'ignore').decode('utf-8').replace('"', '\\"').replace("'", "\\'")

CATEGORIES = {sanitize(k): [{sanitize(key): sanitize(val) if isinstance(val, str) else val for key, val in a.items()} for a in v] for k, v in CATEGORIES_RAW.items()}

def apply_styles():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-color: #0b0c10;
        --sidebar-bg: #14161f;
        --card-bg: #1f2833;
        --card-hover: #161b22;
        --accent: #45a29e;
        --glow: #66fcf1;
        --text-p: #c5c6c7;
        --text-bright: #66fcf1;
        --border: #45a29e;
        --font-main: 'Outfit', -apple-system, sans-serif;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--text-p);
        font-family: var(--font-main);
    }

    header, footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    /* Sidebar Navigation Rail */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid rgba(102, 252, 241, 0.1);
    }

    .nav-category {
        padding: 10px 20px;
        color: var(--text-p);
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        display: block;
        margin: 4px 12px;
        border-radius: 8px;
    }

    .nav-category:hover {
        background: rgba(102, 252, 241, 0.05);
        color: var(--glow);
        transform: translateX(5px);
    }

    /* Hero Section with Animated Gradient */
    .hero-container {
        text-align: center;
        padding: 60px 0 100px;
        position: relative;
        overflow: hidden;
    }

    .hero-title {
        font-size: 72px;
        font-weight: 800;
        background: linear-gradient(90deg, #66fcf1, #45a29e, #1f2833, #66fcf1);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: flowing-gradient 8s linear infinite;
        margin-bottom: 20px;
        letter-spacing: -2px;
    }

    @keyframes flowing-gradient {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 0%; }
    }

    .hero-sub {
        font-size: 24px;
        color: var(--text-p);
        opacity: 0.8;
        max-width: 800px;
        margin: 0 auto 40px;
        line-height: 1.4;
    }

    /* Colorful Card Styling with Hover Pop */
    @keyframes card-fade-in {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .agent-card {
        background: #14161f;
        border: 1px solid rgba(102, 252, 241, 0.1);
        border-radius: 12px;
        padding: 30px;
        height: 100%;
        position: relative;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: card-fade-in 0.6s ease-out backwards;
    }

    .agent-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: var(--glow);
        box-shadow: 0 15px 35px rgba(102, 252, 241, 0.1);
        background: #1c212b;
    }

    .agent-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #66fcf1, #45a29e);
        opacity: 0;
        transition: opacity 0.3s;
    }

    .agent-card:hover::before {
        opacity: 1;
    }

    .agent-name {
        color: #fff;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .agent-desc {
        color: var(--text-p);
        font-size: 14px;
        line-height: 1.6;
        opacity: 0.7;
    }

    .card-meta {
        margin-top: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .badge {
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        background: rgba(102, 252, 241, 0.1);
        color: var(--glow);
        border: 1px solid rgba(102, 252, 241, 0.2);
    }

    /* Category Headers */
    .cat-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 40px;
        border-left: 5px solid var(--glow);
        padding-left: 20px;
        color: #fff;
        scroll-margin-top: 50px;
    }

    .stTextInput input {
        background: rgba(20, 22, 31, 0.8) !important;
        border: 1px solid rgba(102, 252, 241, 0.1) !important;
        color: #fff !important;
        border-radius: 50px !important;
        padding: 15px 25px !important;
        font-size: 18px !important;
        transition: all 0.3s !important;
    }

    .stTextInput input:focus {
        border-color: var(--glow) !important;
        box-shadow: 0 0 20px rgba(102, 252, 241, 0.1) !important;
    }

    </style>
    ''', unsafe_allow_html=True)

def main():
    apply_styles()

    with st.sidebar:
        st.markdown('''
        <div style="padding: 40px 20px; text-align: center;">
            <h1 style="color: #66fcf1; font-weight: 900; letter-spacing: -2px; font-size: 36px;">A.O.S</h1>
            <p style="color: #45a29e; font-size: 12px; text-transform: uppercase; font-weight: 700; letter-spacing: 2px;">Neural Registry</p>
        </div>
        ''', unsafe_allow_html=True)
        
        for cat in CATEGORIES.keys():
            cat_id = cat.lower().replace(" ", "-").replace("&", "and")
            clean_name = re.sub(r'[^\w\s]', '', cat).strip()
            # If re.sub fails to clean everything for nav anchors, we use simple labels
            if not clean_name: clean_name = "Category"
            st.markdown(f'<a href="#{cat_id}" class="nav-category">{clean_name}</a>', unsafe_allow_html=True)

    st.markdown('''
    <div class="hero-container">
        <h1 class="hero-title">Beyond Software.</h1>
        <p class="hero-sub">The global registry for 78 autonomous agents architected to drive the post-SaaS economy infrastructure.</p>
    </div>
    ''', unsafe_allow_html=True)

    search_q = st.text_input("", placeholder="Search the decentralized agent intelligence registry...").lower()

    if search_q:
        cols = st.columns(3)
        found = 0
        for cat_name, agents in CATEGORIES.items():
            for agent in agents:
                if search_q in agent['name'].lower() or search_q in agent['desc'].lower() or search_q in cat_name.lower():
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card">
                            <div class="agent-name">{name}</div>
                            <div class="agent-desc">{desc}</div>
                            <div class="card-meta">
                                <span class="badge">Operational</span>
                                <span style="color: #66fcf1; font-size: 12px;">Explore →</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[found % 3]:
                        st.markdown(card_html, unsafe_allow_html=True)
                    found += 1
    else:
        for idx, (cat_name, agents) in enumerate(CATEGORIES.items()):
            cat_id = cat_name.lower().replace(" ", "-").replace("&", "and")
            st.markdown(f'<div id="{cat_id}" class="cat-title">{cat_name}</div>', unsafe_allow_html=True)
            
            chunk_size = 3
            for i in range(0, len(agents), chunk_size):
                chunk = agents[i:i+chunk_size]
                cols = st.columns(3)
                for j, agent in enumerate(chunk):
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    # Add delay for staggered animation
                    delay = (i + j) * 0.05
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card" style="animation-delay: {delay}s;">
                            <div class="agent-name">{name}</div>
                            <div class="agent-desc">{desc}</div>
                            <div class="card-meta">
                                <span class="badge">v1.8</span>
                                <span style="color: #66fcf1; font-size: 12px; font-weight: 600;">System Access →</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[j]:
                        st.markdown(card_html, unsafe_allow_html=True)
                st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
"""

# Replace the marker with actual JSON data
final_code = template.replace("__CATEGORIES_DATA__", json.dumps(categories_data, indent=4))

with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_code)

print("Dynamic Animated Hub Streamlit application generated.")
