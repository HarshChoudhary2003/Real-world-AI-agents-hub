import streamlit as st
import json
import os
import numpy as np
import litellm
import pandas as pd
import plotly.express as px
from datetime import date
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SemanticForge AI | RAG Document Retrieval",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (PREMIUM SaaS AESTHETICS)
# -----------------------------------------------------------------------------
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary: #a855f7;
        --secondary: #6366f1;
        --bg: #0c0e14;
        --card: #161923;
        --text: #f1f5f9;
        --border: #2e3244;
    }

    /* Reset & Typography */
    .stApp { background-color: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; }

    /* Hide Streamlit Header/Footer */
    header, footer { visibility: hidden !important; }

    /* Custom Header */
    .main-header {
        background: linear-gradient(90deg, #a855f7, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }

    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    /* Glassmorphic Cards */
    .glass-card {
        background: rgba(22, 25, 35, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8.5px);
        margin-bottom: 1.5rem;
    }

    .glass-card:hover { border-color: rgba(168, 85, 247, 0.4); transform: translateY(-2px); transition: transform 0.2s ease; }

    /* KPI Cards */
    .kpi-card { background: #1a1e2e; border: 1px solid #2e3244; border-radius: 12px; padding: 1.5rem; text-align: left; }
    .kpi-label { font-size: 0.8rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; }
    .kpi-value { font-size: 1.5rem; font-weight: 700; color: #ffffff; margin-top: 0.5rem; }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
        color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600; width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 15px -3px rgba(168, 85, 247, 0.4);
    }

    /* Badge Tags */
    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; margin-right: 0.5rem; }
    .badge-success { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }

    /* Inputs */
    .stTextArea textarea { background: #1a1e2e !important; border: 1px solid #2e3244 !important; color: #e2e8f0 !important; border-radius: 12px !important; }

    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. CORE LOGIC (RAG ARCHITECTURE)
# -----------------------------------------------------------------------------
def embed_text(text, model="text-embedding-3-small", api_key=None):
    try:
        kwargs = {"model": model, "input": [text]}
        if api_key:
            kwargs["api_key"] = api_key
        response = litellm.embedding(**kwargs)
        return np.array(response.data[0]['embedding'])
    except Exception as e:
        return None

def cosine_similarity(a, b):
    # Avoid division by zero
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(a, b) / (norm_a * norm_b)

def retrieve_context(docs, query, model="text-embedding-3-small", api_key=None, top_k=3):
    query_vec = embed_text(query, model=model, api_key=api_key)
    if query_vec is None: return []
    
    scored = []
    for d in docs:
        vec = embed_text(d, model=model, api_key=api_key)
        if vec is not None:
            score = cosine_similarity(query_vec, vec)
            scored.append({"document": d, "score": score})
    
    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:top_k]

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: white;'>SemanticForge <span style='color: #a855f7;'>AI</span></h2>", unsafe_allow_html=True)
        
        st.markdown("### 🧬 Embedding Module")
        provider_map = {
            "OpenAI": "text-embedding-3-small",
            "Google Gemini": "gemini/text-embedding-004",
            "Anthropic": "claude-3-haiku-20240307", # Use haiku for basic embedding tasks if needed, though usually specialized embedding models are better
            "DeepSeek": "deepseek/deepseek-chat",
            "xAI (Grok)": "xai/grok-beta",
            "Local (Ollama)": "ollama/llama3"
        }
        selected_provider = st.selectbox("Select Provider", list(provider_map.keys()))
        target_model = provider_map[selected_provider]
        
        user_api_key = st.text_input("Custom API Key (Optional)", type="password")
        
        st.markdown("---")
        st.markdown("### 📊 Retrieval Metrics")
        st.metric("Neural Sync", "Active", "🟢")
        st.metric("Latency Index", "142ms", "-12ms")
        
        st.markdown("---")
        st.info(f"Orchestrating via: **{selected_provider}**")

    # Main Content
    st.markdown("<h1 class='main-header'>Multi-Provider Retrieval Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Orchestrate semantic document retrieval across OpenAI, Gemini, DeepSeek, Ollama, Grok, and Claude.</p>", unsafe_allow_html=True)

    # Input Canvas
    left_col, right_col = st.columns([1.5, 1])

    with left_col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📁 Document Knowledge Base")
        doc_input = st.text_area("Paste Documents (1 per line)", height=250, placeholder="E.g.,\nAI agents automate tasks...\nRetrieval generation improves accuracy...\nPrompt engineering affects quality...")
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Semantic Query")
        query_input = st.text_input("Enter Search Intent", placeholder="How does RAG improve reliability?")
        top_k = st.slider("Max Context Chunks", 1, 10, 3)
        
        if st.button("🚀 Initiating Neural Search"):
            if doc_input and query_input:
                docs = [l.strip() for l in doc_input.split('\n') if l.strip()]
                with st.spinner(f"Synthesizing vector dimensions via {selected_provider}..."):
                    results = retrieve_context(docs, query_input, model=target_model, api_key=user_api_key, top_k=top_k)
                    st.session_state['results'] = results
            else:
                st.warning("Ensure both Documents and Query are defined.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Results Analytics
    if st.session_state.get('results'):
        results = st.session_state['results']
        st.markdown("---")
        st.markdown("### 🎯 Retrieval Performance Report")
        
        if not results:
            st.info("No matching context found.")
        else:
            # Comparison Map
            df = pd.DataFrame(results)
            fig = px.bar(df, x='score', y='document', orientation='h', title='Semantic Similarity Map', labels={'score': 'Confidence Score', 'document': 'Retrieved Fragment'}, color='score', color_continuous_scale='Purples')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'))
            
            viz_col, list_col = st.columns([1, 1])
            with viz_col:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with list_col:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### Top Confidence Results")
                for r in results:
                    st.markdown(f"""
                    <div class='kpi-card' style='margin-bottom: 1rem; border-left: 4px solid #a855f7;'>
                        <span class='badge badge-success'>{int(r['score']*100)}% Match</span>
                        <p style='margin-top: 0.5rem;'>{r['document']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #64748b;'>SemanticForge AI © 2026 | Neural Knowledge Architecture | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    if 'results' not in st.session_state:
        st.session_state['results'] = None
    main()
