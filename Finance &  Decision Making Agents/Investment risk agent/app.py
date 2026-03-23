import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import json
import pandas as pd
import plotly.express as px
from agent import assess_risk, save_outputs
import os
import time

# Page Configuration
st.set_page_config(
    page_title="RiskVault | Neural Brain Interface",
    page_icon="🧠",
    layout="wide",
)

# Initialize Session State
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'last_result' not in st.session_state:
    st.session_state['last_result'] = None
if 'graph_active' not in st.session_state:
    st.session_state['graph_active'] = False

# --- AI BRAIN INTERFACE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-editor: #020202;
        --accent: #E11D48; /* Crimson/Rose for Risk */
        --text-head: #FFFFFF;
        --border-glass: rgba(225, 29, 72, 0.2);
    }

    .stApp {
        background-color: var(--bg-editor);
        color: #A1A1AA;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Hide Streamlit Artifacts */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

    .floating-panel {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 400px;
        background: rgba(15, 15, 20, 0.85);
        backdrop-filter: blur(15px);
        border: 1px solid var(--border-glass);
        border-radius: 20px;
        padding: 24px;
        z-index: 1000;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    }
    
    .graph-info {
        position: fixed;
        top: 30px;
        left: 30px;
        z-index: 1000;
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)

# --- GRAPH VISUALIZATION (THE BRAIN) ---
def render_brain():
    nodes = [
        Node(id="RiskVault", label="RiskVault Pro", size=35, shape="circularImage", image="https://cdn-icons-png.flaticon.com/512/2091/2091665.png", color="#E11D48"),
        Node(id="Input", label="Input Matrix", size=25, color="#71717A"),
        Node(id="MarketHub", label="Market Hub", size=25, color="#3B82F6"),
        Node(id="Heuristic", label="Heuristic Core", size=25, color="#10B981"),
        Node(id="Outcome", label="Risk Report", size=25, shape="square", color="#FFFFFF")
    ]
    
    edges = [
        Edge(source="Input", target="RiskVault", label="INGEST", animated=st.session_state['graph_active']),
        Edge(source="RiskVault", target="MarketHub", label="QUERY", animated=st.session_state['graph_active']),
        Edge(source="MarketHub", target="RiskVault", label="CONTEXT", animated=st.session_state['graph_active']),
        Edge(source="RiskVault", target="Heuristic", label="REASON", animated=st.session_state['graph_active']),
        Edge(source="Heuristic", target="Outcome", label="OUTPUT", animated=st.session_state['graph_active'])
    ]
    
    # Active State Coloring
    if st.session_state['graph_active']:
        for n in nodes:
            if n.id != "Input": n.color = "#E11D48"

    config = Config(
        width=1400,
        height=700,
        directed=True,
        physics=True,
        hierarchical=False,
        node={"labelProperty": "label", "font": {"color": "white", "size": 14, "face": "Space Grotesk"}},
        link={"labelProperty": "label", "renderLabel": True, "font": {"color": "#71717A", "size": 12}},
        collapsible=False
    )
    
    return agraph(nodes=nodes, edges=edges, config=config)

st.markdown("""
<div class="graph-info">
    <h1 style='font-weight:900; letter-spacing:-2px; color:white; margin:0; size:3rem;'>RISKVAULT BRAIN</h1>
    <p style='color:#E11D48; font-weight:600; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem;'>System State: <span style='color:white;'>""" + ("PROCESSING" if st.session_state['graph_active'] else "IDLE") + """</span></p>
</div>
""", unsafe_allow_html=True)

# Full-Screen Graph Background
graph_col, extra_col = st.columns([1, 0.01])
with graph_col:
    render_brain()

# --- FLOATING COMMAND INTERFACE ---
st.markdown('<div class="floating-panel">', unsafe_allow_html=True)

st.markdown("<h3 style='margin:0; size:1.2rem; color:white;'>Protocol Management</h3>", unsafe_allow_html=True)
hub_provider = st.selectbox("Market Hub Provider", ["OpenAI", "Google", "Anthropic", "xAI"])
model_map = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini"],
    "Google": ["gemini-1.5-pro"],
    "Anthropic": ["claude-3-5-sonnet-20240620"],
    "xAI": ["grok-beta"]
}
selected_model = st.selectbox("Intelligence Axis", model_map[hub_provider])

st.markdown("---")

if st.session_state['last_result']:
    res = st.session_state['last_result']
    st.markdown(f"**Risk Profile**: <span style='color:#E11D48;'>{res['risk_profile']}</span>", unsafe_allow_html=True)
    st.markdown(f"**Resilience Score**: {res['risk_score']}/100")
    
    with st.expander("Detailed Risk Heuristics", expanded=False):
        for r in res['risks']:
            st.markdown(f"**{r['risk']}** ({r['category']})")
            st.markdown(f"Impact: {r['impact']} | {r['notes']}")
            st.markdown("---")

user_command = st.text_input("Message RiskVault... (e.g., /evaluate or 'market audit')")

if user_command:
    if "/evaluate" in user_command or "risk" in user_command.lower() or "audit" in user_command.lower():
        st.session_state['graph_active'] = True
        with st.spinner(" "):
            try:
                with open("investment_input.txt", "r") as f: context = f.read()
                data = assess_risk(context, model_name=selected_model)
                save_outputs(data)
                st.session_state['last_result'] = data
                st.success("Neural Audit Complete.")
            except Exception as e:
                st.error(f"Heuristic Loop Interrupted: {e}")
        st.session_state['graph_active'] = False
        st.rerun()
    else:
        st.info("System awaiting protocol command. Initiate /evaluate for a multi-axis neural audit.")

st.markdown('</div>', unsafe_allow_html=True)

# Layout Refinement for Graph center
st.markdown("""<style>.stAgraph { width: 100vw !important; }</style>""", unsafe_allow_html=True)
