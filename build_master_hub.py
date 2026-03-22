import re
import urllib.parse

readme_path = r"h:\100 AI Agents\README.md"
output_path = r"h:\100 AI Agents\master_hub.py"

with open(readme_path, "r", encoding="utf-8") as f:
    text = f.read()

categories = {}
current_category = None

lines = text.split("\n")
for line in lines:
    if line.startswith("### "):
        # e.g., "### 💼 Business Operations Systems"
        cat_match = re.search(r"###\s*(.*)", line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            categories[current_category] = []
    elif line.startswith("- ["):
        if current_category:
            # e.g., "- [💼 **TalentForge AI**](./HR%20,%20Legal%20&%20Compliance%20Agents/Job%20description%20generator%20agent) – Inclusive requisition..."
            agent_match = re.search(r"\[([^\]]+)\]\(([^)]+)\)\s*–\s*(.*)", line)
            if agent_match:
                name_raw = agent_match.group(1).replace("**", "").strip()
                path_raw = agent_match.group(2).strip()
                desc_raw = agent_match.group(3).strip()
                
                if path_raw.startswith("./"):
                    path_raw = path_raw[2:]
                github_url = f"https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/{path_raw}"
                
                categories[current_category].append({
                    "name": name_raw,
                    "url": github_url,
                    "desc": desc_raw
                })

# Build navigation items for the menu bar
nav_items_html = ""
for cat in categories.keys():
    cat_id = cat.lower().replace(" ", "-").replace("&", "and")
    # Clean emoji for nav labels
    clean_label = re.sub(r'[^\w\s]', '', cat).strip()
    if clean_label:
        nav_items_html += f'<a href="#{cat_id}" class="nav-link">{clean_label}</a>'

# Build the Streamlit application code
streamlit_code = f"""import streamlit as st

st.set_page_config(
    page_title="Agent OS | Master Hub",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def apply_styles():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Variables & Base */
    :root {{
        --bg-color: #000000;
        --card-bg: #0A0A0A;
        --card-hover: #121212;
        --accent: #2997FF;
        --text-primary: #F5F5F7;
        --text-secondary: #86868B;
        --border: #1D1D1F;
        --glass-bg: rgba(0, 0, 0, 0.75);
    }}

    .stApp {{
        background-color: var(--bg-color);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, sans-serif;
    }}

    header {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    [data-testid="stToolbar"] {{visibility: hidden !important;}}

    /* Sticky Menu Bar */
    .menu-bar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 52px;
        background: var(--glass-bg);
        backdrop-filter: saturate(180%) blur(20px);
        -webkit-backdrop-filter: saturate(180%) blur(20px);
        border-bottom: 0.5px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        z-index: 999999;
    }}

    .brand {{
        font-weight: 600;
        font-size: 19px;
        letter-spacing: -0.01em;
        color: var(--text-primary);
        text-decoration: none;
    }}

    .nav-links {{
        display: flex;
        gap: 32px;
    }}

    .nav-link {{
        color: var(--text-secondary);
        text-decoration: none;
        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.01em;
        transition: color 0.2s ease;
    }}

    .nav-link:hover {{
        color: var(--text-primary);
    }}

    /* Content Layout */
    .block-container {{
        padding-top: 100px !important;
        padding-bottom: 100px !important;
        max-width: 1060px !important;
    }}

    .hero-section {{
        text-align: center;
        margin-bottom: 80px;
    }}

    h1 {{
        font-weight: 700;
        font-size: 56px !important;
        letter-spacing: -0.015em;
        line-height: 1.07;
        margin-bottom: 16px;
    }}

    .sub-header {{
        color: var(--text-secondary);
        font-size: 24px;
        font-weight: 500;
        line-height: 1.16;
        letter-spacing: 0.009em;
        max-width: 700px;
        margin: 0 auto;
    }}

    /* Category Blocks */
    .category-block {{
        margin-top: 48px;
        scroll-margin-top: 80px;
    }}

    .category-title {{
        font-size: 28px;
        font-weight: 600;
        letter-spacing: 0.007em;
        margin-bottom: 24px;
        color: var(--text-primary);
    }}

    /* Agent Cards */
    .agent-link {{
        text-decoration: none !important;
        display: block;
        height: 100%;
    }}

    .agent-card {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 28px;
        height: 100%;
        transition: all 0.5s cubic-bezier(0.15, 0, 0.15, 1);
        display: flex;
        flex-direction: column;
    }}

    .agent-card:hover {{
        background: var(--card-hover);
        transform: scale(1.02);
        border-color: #333333;
    }}

    .agent-name {{
        color: var(--text-primary);
        font-size: 19px;
        font-weight: 600;
        margin-bottom: 8px;
    }}

    .agent-desc {{
        color: var(--text-secondary);
        font-size: 14px;
        line-height: 1.42;
        font-weight: 400;
    }}

    /* Accent Line */
    .accent-line {{
        width: 60px;
        height: 2px;
        background: var(--accent);
        margin: 24px auto 0;
        border-radius: 2px;
    }}
    </style>
    
    <div class="menu-bar">
        <a href="#" class="brand">Agent OS</a>
        <div class="nav-links">
            {nav_items_html}
        </div>
    </div>
    ''', unsafe_allow_html=True)

def main():
    apply_styles()

    st.markdown('''
    <div class="hero-section">
        <h1>Intelligence Unbound.</h1>
        <p class="sub-header">78 high-fidelity autonomous agents architected for the next-generation enterprise.</p>
        <div class="accent-line"></div>
    </div>
    ''', unsafe_allow_html=True)

"""

# Append categories and agents
for cat_name, agents in categories.items():
    if not agents:
        continue
    
    cat_id = cat_name.lower().replace(" ", "-").replace("&", "and")
    streamlit_code += f'    st.markdown("<div id=\'{cat_id}\' class=\'category-block\'><div class=\'category-title\'>{cat_name.replace(chr(39), chr(92)+chr(39))}</div></div>", unsafe_allow_html=True)\n'
    
    # Split agents into rows of 3
    chunk_size = 3
    for i in range(0, len(agents), chunk_size):
        chunk = agents[i:i+chunk_size]
        streamlit_code += "    cols = st.columns(3)\n"
        for j, agent in enumerate(chunk):
            name = agent['name'].replace(chr(39), chr(92)+chr(39))
            desc = agent['desc'].replace(chr(39), chr(92)+chr(39))
            url = agent['url']
            
            card_html = f'''
            <a href="{url}" target="_blank" class="agent-link">
                <div class="agent-card">
                    <div class="agent-name">{name}</div>
                    <div class="agent-desc">{desc}</div>
                </div>
            </a>
            '''
            streamlit_code += f"    with cols[{j}]:\n"
            streamlit_code += f"        st.markdown('''{card_html}''', unsafe_allow_html=True)\n"

streamlit_code += """
if __name__ == "__main__":
    main()
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(streamlit_code)

print("Master Hub Streamlit application generated successfully.")
