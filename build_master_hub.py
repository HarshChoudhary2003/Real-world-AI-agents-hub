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
    page_title="Agent OS | Elite Edition",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed",
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
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg: #000000;
        --nav-bg: rgba(0, 0, 0, 0.75);
        --accent: #00F5FF;
        --accent-alt: #7000FF;
        --card-bg: #111111;
        --text: #F5F5F7;
        --text-dim: #86868B;
        --border: #1D1D1F;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
        font-family: 'Outfit', sans-serif;
    }

    header, footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    /* Elite Top Navigation Bar */
    .elite-nav {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 60px;
        background: var(--nav-bg);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 60px;
        z-index: 999999;
    }

    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 22px;
        letter-spacing: -1px;
        background: linear-gradient(135deg, var(--accent), var(--accent-alt));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-decoration: none;
    }

    .nav-links {
        display: flex;
        gap: 40px;
        align-items: center;
    }

    .nav-item {
        color: var(--text-dim);
        font-size: 13px;
        font-weight: 500;
        text-decoration: none;
        letter-spacing: 0.02em;
        transition: all 0.3s;
        position: relative;
    }

    .nav-item:hover {
        color: var(--text);
    }

    .nav-item::after {
        content: "";
        position: absolute;
        bottom: -4px; left: 0; width: 0%; height: 1.5px;
        background: var(--accent);
        transition: width 0.3s cubic-bezier(0.19, 1, 0.22, 1);
    }

    .nav-item:hover::after {
        width: 100%;
    }

    .nav-cta {
        background: #fff;
        color: #000;
        padding: 8px 18px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: 600;
        text-decoration: none;
        transition: transform 0.2s;
    }

    .nav-cta:hover {
        transform: scale(1.05);
    }

    /* Layout & Hero */
    .block-container {
        padding-top: 140px !important;
        padding-bottom: 100px !important;
        max-width: 1300px !important;
    }

    .hero {
        text-align: center;
        margin-bottom: 100px;
    }

    .hero h1 {
        font-size: 84px !important;
        font-weight: 800;
        line-height: 1.05;
        letter-spacing: -3px;
        margin-bottom: 30px;
    }

    .hero p {
        font-size: 24px;
        color: var(--text-dim);
        max-width: 800px;
        margin: 0 auto;
    }

    /* Registry Display */
    .category-title {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin: 80px 0 40px;
        color: var(--text);
        scroll-margin-top: 100px;
    }

    .agent-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 32px;
        height: 100%;
        transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        cursor: pointer;
        display: flex;
        flex-direction: column;
    }

    .agent-card:hover {
        background: #161618;
        border-color: #323235;
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .agent-name {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 12px;
        color: #fff;
    }

    .agent-desc {
        color: var(--text-dim);
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 24px;
    }

    .card-footer {
        margin-top: auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .tag {
        font-size: 11px;
        font-weight: 700;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .arrow {
        color: var(--accent);
        font-size: 18px;
        transition: transform 0.3s;
    }

    .agent-card:hover .arrow {
        transform: translateX(5px);
    }

    .search-input input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        color: white !important;
        font-size: 16px !important;
    }

    </style>
    
    <div class="elite-nav">
        <a href="#" class="nav-logo">AGENT OS</a>
        <div class="nav-links">
            <a href="#registry" class="nav-item">Registry</a>
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub" class="nav-item">Core Repo</a>
            <a href="#" class="nav-cta">Deploy Nodes</a>
        </div>
    </div>
    ''', unsafe_allow_html=True)

def main():
    apply_styles()

    st.markdown('''
    <div class="hero">
        <h1>Autonomous Operations.</h1>
        <p>A unified orchestration layer for 78 deterministic AI agents architected for the next-generation economic engine.</p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div id="registry" class="search-input">', unsafe_allow_html=True)
    search_q = st.text_input("", placeholder="Search the decentralized node registry...").lower()
    st.markdown('</div>', unsafe_allow_html=True)

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
                            <div class="card-footer">
                                <span class="tag">Active</span>
                                <span class="arrow">→</span>
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
            st.markdown(f'<div id="{cat_id}" class="category-title">{cat_name}</div>', unsafe_allow_html=True)
            
            chunk_size = 3
            for i in range(0, len(agents), chunk_size):
                chunk = agents[i:i+chunk_size]
                cols = st.columns(3)
                for j, agent in enumerate(chunk):
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card">
                            <div class="agent-name">{name}</div>
                            <div class="agent-desc">{desc}</div>
                            <div class="card-footer">
                                <span class="tag">Operational</span>
                                <span class="arrow">→</span>
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

print("Elite Edition Hub with Top Nav generated.")
