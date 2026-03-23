import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import json
import pandas as pd
import plotly.express as px
from agent import analyze_sentiment, save_outputs
import os
import time

# Page Configuration: Minimalist & Apple-level
st.set_page_config(
    page_title="SentimentCore | Neural Brain Interface",
    page_icon="🔆",
    layout="wide",
)

# Initialize Session State
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'last_result' not in st.session_state:
    st.session_state['last_result'] = None
if 'graph_active' not in st.session_state:
    st.session_state['graph_active'] = False

# --- APPLE-LEVEL PREMIUM BRAIN INTERFACE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600&family=Space+Grotesk:wght@300;500;700&display=swap');

    :root {
        --bg-pure: #0A0A0A;
        --accent-gold: #F59E0B;
        --border-soft: rgba(255, 255, 255, 0.05);
        --text-pure: #FFFFFF;
        --text-dim: #71717A;
    }

    .stApp {
        background-color: var(--bg-pure);
        color: var(--text-pure);
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit Noise */
    #MainMenu, footer, header {visibility: hidden;}

    /* Premium Floating Indicators */
    .system-status {
        position: fixed;
        top: 40px;
        left: 40px;
        z-index: 1000;
        pointer-events: none;
    }
    
    .status-text {
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        font-size: 0.65rem;
        letter-spacing: 5px;
        color: var(--text-dim);
    }
    
    .status-active {
        color: var(--accent-gold);
        text-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
    }

    .brain-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -2px;
        margin-top: 10px;
        color: white;
    }

    /* Floating Command Interface (Apple-style) */
    .command-box {
        position: fixed;
        bottom: 50px;
        right: 50px;
        width: 380px;
        background: rgba(20, 20, 20, 0.7);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid var(--border-soft);
        border-radius: 24px;
        padding: 24px;
        z-index: 1000;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    }

    /* Minimal Metric Panel */
    .metric-card {
        padding: 15px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-dim);
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 500;
        color: white;
    }

    /* Animation Styles */
    @keyframes subtlePulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
</style>
""", unsafe_allow_html=True)

# --- GRAPH VISUALIZATION (THE BRAIN) ---
def render_brain():
    nodes = [
        Node(id="SENTIMENT_CORE", label="SentimentCore AI", size=30, color="#F59E0B" if st.session_state['graph_active'] else "#FFFFFF", image="https://cdn-icons-png.flaticon.com/512/3663/3663365.png", shape="circularImage"),
        Node(id="SOCIAL_FEED", label="Social Grid", size=20, color="#71717A"),
        Node(id="NEWS_FEED", label="News Grid", size=20, color="#71717A"),
        Node(id="ANALYTIC_HUB", label="Analytic Hub", size=20, color="#71717A"),
        Node(id="DIVERGENCE", label="Divergence Audit", size=25, color="#F59E0B" if st.session_state['graph_active'] else "#71717A"),
        Node(id="REPORT", label="Heuristic Report", size=20, color="#FFFFFF", shape="diamond")
    ]
    
    edges = [
        Edge(source="SOCIAL_FEED", target="SENTIMENT_CORE", label="INGEST", animated=st.session_state['graph_active'], color="#F59E0B" if st.session_state['graph_active'] else "#333333"),
        Edge(source="NEWS_FEED", target="SENTIMENT_CORE", label="INGEST", animated=st.session_state['graph_active'], color="#F59E0B" if st.session_state['graph_active'] else "#333333"),
        Edge(source="ANALYTIC_HUB", target="SENTIMENT_CORE", label="QUERY", animated=st.session_state['graph_active']),
        Edge(source="SENTIMENT_CORE", target="DIVERGENCE", label="REASON", animated=st.session_state['graph_active']),
        Edge(source="DIVERGENCE", target="REPORT", label="OUTPUT", animated=st.session_state['graph_active'])
    ]

    config = Config(
        width=1500,
        height=750,
        directed=True,
        physics=True,
        hierarchical=False,
        node={"labelProperty": "label", "font": {"color": "#71717A", "size": 13, "face": "Inter"}},
        link={"labelProperty": "label", "renderLabel": False},
        collapsible=False
    )
    
    return agraph(nodes=nodes, edges=edges, config=config)

# Foreground Info
st.markdown("""
<div class="system-status">
    <div class="status-text">NEURAL LINK: <span class="status-active">""" + ("ACTIVE" if st.session_state['graph_active'] else "STABLE") + """</span></div>
    <div class="brain-title">SentimentCore Pro</div>
</div>
""", unsafe_allow_html=True)

# Full-Screen Graph Background
render_brain()

# --- FLOATING COMMAND INTERFACE (APPLE STYLE) ---
st.markdown('<div class="command-box">', unsafe_allow_html=True)

st.markdown("<p style='font-family:Inter; font-size:0.85rem; color:#A1A1AA; margin-bottom:20px;'>Intelligence Configuration</p>", unsafe_allow_html=True)

hub_provider = st.selectbox("Provider", ["OpenAI", "Google", "Anthropic", "xAI"], key="prov")
model_map = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini"], "Google": ["gemini-1.5-pro"],
    "Anthropic": ["claude-3-5-sonnet-20240620"], "xAI": ["grok-beta"]
}
selected_model = st.selectbox("Model", model_map[hub_provider], key="mod")

st.markdown("---")

if st.session_state['last_result']:
    res = st.session_state['last_result']
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Sentiment Profile</div>
            <div class="metric-value">{res['overall_sentiment']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Neural Confidence</div>
            <div class="metric-value">{res['confidence_level']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Divergence Scan", expanded=False):
        st.markdown(f"<p style='font-size:0.85rem; color:#A1A1AA;'>{res.get('divergence_notes', 'N/A')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.85rem; color:white; font-weight:500;'>{res.get('executive_summary', 'N/A')}</p>", unsafe_allow_html=True)

user_command = st.text_input("Execute Neural Command...", placeholder="/audit or 'analyze Bitcoin'")

if user_command:
    if "/audit" in user_command or "analyze" in user_command.lower() or "sentiment" in user_command.lower():
        st.session_state['graph_active'] = True
        with st.spinner(" "):
            try:
                with open("sentiment_input.txt", "r") as f: context = f.read()
                data = analyze_sentiment(context, model_name=selected_model)
                save_outputs(data)
                st.session_state['last_result'] = data
                st.success("Analysis Sequential.")
            except Exception as e:
                st.error(f"Neural Error: {e}")
        st.session_state['graph_active'] = False
        st.rerun()
    else:
        st.info("Direct protocol not found. Use /audit to trigger a multi-source neural scan.")

st.markdown('</div>', unsafe_allow_html=True)

# Global Graph Formatting
st.markdown("""<style>.stAgraph { width: 100vw !important; height: 100vh !important; }</style>""", unsafe_allow_html=True)
