import re

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
                
                # Format name (remove emoji maybe or keep it clean)
                # Let's keep the emoji for now.
                
                # Format path to github URL
                # Path looks like ./HR%20,%20Legal...
                if path_raw.startswith("./"):
                    path_raw = path_raw[2:]
                github_url = f"https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/{path_raw}"
                
                categories[current_category].append({
                    "name": name_raw,
                    "url": github_url,
                    "desc": desc_raw
                })

# Build the Streamlit application code
streamlit_code = """import streamlit as st

st.set_page_config(
    page_title="AI Agent Hub",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def apply_apple_design():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Reset and Base typography */
    body, .stApp {
        background-color: #000000;
        color: #F5F5F7;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide heavy Streamlit UI elements */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .css-1rs6os {visibility: hidden;}
    .css-17ziqus {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    /* Top Layout Spacing */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 5rem !important;
        max-width: 1100px !important;
    }

    /* Master Headings */
    h1 {
        font-weight: 500;
        font-size: 3rem !important;
        letter-spacing: -0.015em;
        text-align: center;
        color: #F5F5F7;
        margin-bottom: 0.5rem;
    }
    
    .stMarkdown p.sub-header {
        text-align: center;
        color: #86868B;
        font-size: 1.15rem;
        font-weight: 400;
        letter-spacing: 0.005em;
        margin-bottom: 4rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }

    /* Category Headers */
    .category-title {
        color: #F5F5F7;
        font-size: 1.4rem;
        font-weight: 500;
        letter-spacing: 0.01em;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #333336;
        padding-bottom: 0.8rem;
    }

    /* Agent Cards (Grid simulated via Streamlit columns, styled via HTML) */
    .agent-link-wrapper {
        text-decoration: none;
    }
    
    .agent-card {
        background-color: #111111;
        border: 1px solid #222222;
        border-radius: 14px;
        padding: 24px;
        height: 100%;
        min-height: 140px;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        cursor: pointer;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .agent-card:hover {
        background-color: #1A1A1A;
        border-color: #333333;
        transform: translateY(-2px);
    }

    .agent-name {
        color: #F5F5F7;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-decoration: none;
    }

    .agent-desc {
        color: #86868B;
        font-size: 0.85rem;
        line-height: 1.4;
        font-weight: 400;
    }
    
    </style>
    ''', unsafe_allow_html=True)

def main():
    apply_apple_design()

    st.markdown("<h1>Agent OS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>A curated ecosystem of autonomous enterprise intelligence. Click any agent to inspect its operational architecture.</p>", unsafe_allow_html=True)

"""

# Append categories and agents
for cat_name, agents in categories.items():
    if not agents:
        continue
        
    streamlit_code += f'    st.markdown("<div class=\'category-title\'>{cat_name.replace(chr(39), chr(92)+chr(39))}</div>", unsafe_allow_html=True)\n'
    
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
            <a href="{url}" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">{name}</div>
                    <div class="agent-desc">{desc}</div>
                </div>
            </a>
            '''
            streamlit_code += f"    with cols[{j}]:\n"
            streamlit_code += f"        st.markdown('''{card_html}''', unsafe_allow_html=True)\n"
            
        streamlit_code += "    st.markdown('<br>', unsafe_allow_html=True)\n"

streamlit_code += """
if __name__ == "__main__":
    main()
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(streamlit_code)

print("Master Hub Streamlit application generated successfully.")
