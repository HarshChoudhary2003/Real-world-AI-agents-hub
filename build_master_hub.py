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
# Using raw strings or multi-line strings without f-string for the heavy parts

template = r"""import streamlit as st
import json
import re

st.set_page_config(
    page_title="Agent OS | Professional Hub",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

CATEGORIES = __CATEGORIES_DATA__

def apply_styles():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-color: #0d1117;
        --sidebar-bg: #161b22;
        --card-bg: #0d1117;
        --card-border: #30363d;
        --card-hover: #1c212b;
        --accent: #2f81f7;
        --accent-glow: rgba(47, 129, 247, 0.15);
        --text-p: #f0f6fc;
        --text-s: #8b949e;
        --font-main: 'Inter', -apple-system, system-ui;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--text-p);
        font-family: var(--font-main);
    }

    header, footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--card-border);
    }

    .sidebar-header {
        padding: 32px 24px;
        margin-bottom: 24px;
        border-bottom: 1px solid var(--card-border);
        text-align: center;
    }

    .nav-category {
        padding: 8px 16px;
        border-radius: 6px;
        color: var(--text-s);
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
        display: block;
        margin: 2px 12px;
    }

    .nav-category:hover {
        background: rgba(177, 186, 196, 0.12);
        color: var(--text-p);
    }

    .block-container {
        padding-top: 48px !important;
        padding-left: 64px !important;
        padding-right: 64px !important;
        max-width: 1440px !important;
    }

    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 48px;
    }

    .stats-badge {
        background: var(--accent-glow);
        color: var(--accent);
        padding: 6px 16px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid rgba(47, 129, 247, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .category-section {
        margin-bottom: 48px;
        scroll-margin-top: 48px;
    }

    .cat-head {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--card-border);
    }

    .cat-name {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-p);
    }

    .agent-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 6px;
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: border-color 0.2s, background-color 0.2s;
        cursor: pointer;
    }

    .agent-card:hover {
        border-color: #8b949e;
        background: #161b22;
    }

    .agent-name {
        color: var(--accent);
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .agent-desc {
        color: var(--text-s);
        font-size: 13.5px;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .card-footer {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: auto;
    }

    .tag {
        font-size: 11px;
        color: var(--text-s);
        padding: 2px 8px;
        background: #161b22;
        border: 1px solid var(--card-border);
        border-radius: 100px;
    }

    .stTextInput input {
        background-color: #0d1117 !important;
        border: 1px solid var(--card-border) !important;
        color: var(--text-p) !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
    }

    </style>
    ''', unsafe_allow_html=True)

def main():
    apply_styles()

    with st.sidebar:
        st.markdown('''
        <div class="sidebar-header">
            <h1 style="font-size: 24px; font-weight: 800; margin: 0; color: #f0f6fc;">Agent<span style="color:#2f81f7;">Registry</span></h1>
            <code style="font-size: 10px; color:#8b949e; background:none;">v2.4.0 OPERATIONAL</code>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<p style='padding: 0 24px; font-size: 11px; font-weight: 600; color:#484f58; text-transform: uppercase;'>Navigation</p>", unsafe_allow_html=True)
        
        for cat in CATEGORIES.keys():
            cat_id = cat.lower().replace(" ", "-").replace("&", "and")
            clean_name = re.sub(r'[^\w\s]', '', cat).strip()
            st.markdown(f'<a href="#{cat_id}" class="nav-category">{clean_name}</a>', unsafe_allow_html=True)

    st.markdown('''
        <div class="top-bar">
            <div>
                <h2 style="font-size: 32px; font-weight: 600; margin: 0; color: #f0f6fc;">Systems Intelligence Hub</h2>
                <p style="color:#8b949e; font-size: 16px; margin-top: 8px;">Deterministic multi-agent orchestration registry for enterprise automation.</p>
            </div>
            <div class="stats-badge">78 Nodes Online</div>
        </div>
    ''', unsafe_allow_html=True)

    search_q = st.text_input("", placeholder="Search 78 specialized agents by name, capability, or department...").lower()

    if search_q:
        cols = st.columns(4)
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
                            <div>
                                <div class="agent-name">{name}</div>
                                <div class="agent-desc">{desc}</div>
                            </div>
                            <div class="card-footer">
                                <span class="tag">Production</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[found % 4]:
                        st.markdown(card_html, unsafe_allow_html=True)
                    found += 1
        if found == 0:
            st.warning("Query returned zero agents.")
    else:
        for cat_name, agents in CATEGORIES.items():
            cat_id = cat_name.lower().replace(" ", "-").replace("&", "and")
            st.markdown(f'''
                <div id="{cat_id}" class="category-section">
                    <div class="cat-head">
                        <div class="cat-name">{cat_name}</div>
                        <span style="color:#484f58; font-size: 12px; margin-left: auto;">{len(agents)} instances</span>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            chunk_size = 4
            for i in range(0, len(agents), chunk_size):
                chunk = agents[i:i+chunk_size]
                cols = st.columns(chunk_size)
                for j, agent in enumerate(chunk):
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card">
                            <div>
                                <div class="agent-name">{name}</div>
                                <div class="agent-desc">{desc}</div>
                            </div>
                            <div class="card-footer">
                                <span class="tag">Active</span>
                                <span style="font-size: 12px; color: #2f81f7;">Open Hub →</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[j]:
                        st.markdown(card_html, unsafe_allow_html=True)
                st.markdown('<div style="margin-bottom: 24px;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
"""

# Replace the marker with actual JSON data
final_code = template.replace("__CATEGORIES_DATA__", json.dumps(categories_data, indent=4))

with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_code)

print("Professional Hub Streamlit application generated successfully.")
