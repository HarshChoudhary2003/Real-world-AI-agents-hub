import streamlit as st
import json
import numpy as np
from datetime import date
import io
import agent

# ==========================================
# PAGE CONFIGURATION & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="BrainVault AI | RAG System", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 700 !important; }

    /* Premium Badges */
    .premium-badge {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Cards Simulation */
    .query-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        border-left: 4px solid #8B5CF6;
        transition: transform 0.2s;
    }
    
    .db-card {
        background: #0F172A;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-bottom: 10px;
        font-size: 0.9em;
        color: #94A3B8;
    }

    /* Standard inputs */
    .stTextInput input, .stTextArea textarea, .stNumberInput input { 
        background-color: #1E293B !important; 
        color: white !important; 
        border: 1px solid #475569 !important;
    }
    
    .source-pill {
        background-color: #475569;
        color: #E2E8F0;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🧠 BrainVault AI")
    st.markdown('<div class="premium-badge">Semantic RAG Engine</div>', unsafe_allow_html=True)
    st.markdown("A private local knowledge base powered by Vector Embeddings. Upload your notes, research, or docs, and query them with absolute retrieval accuracy.")

# ==========================================
# SIDEBAR / SETTINGS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3565/3565983.png", width=60)
    st.title("Neural Core")
    
    st.markdown("### 🔑 Authentication")
    api_key = st.text_input("OpenAI API Key (sk-...)", type="password", help="Required to run embedding models and LLM queries.")
    
    if not api_key: st.warning("⚠️ Waiting for API Key...")
    else: 
        st.success("🤖 Core Activated")
        import openai
        # Safely instantiate a localized client
        agent.client = openai.OpenAI(api_key=api_key)

    st.markdown("---")
    st.markdown("### ⚙️ Engine Level")
    embed_choice = st.selectbox("Embedding Engine", ["text-embedding-3-small", "text-embedding-ada-002"])
    agent.EMBED_MODEL = embed_choice
    
    chat_choice = st.selectbox("Synthesizer Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], index=1)
    agent.CHAT_MODEL = chat_choice
    
    top_k_slider = st.slider("Top-K Retrieval", min_value=1, max_value=10, value=3)

# ==========================================
# MAIN INTERFACE
# ==========================================
tab_search, tab_upload, tab_db = st.tabs(["🔍 Semantic Search", "📥 Ingest Knowledge", "💾 Vector Datastore"])

# ---------------------------------------------
# TAB: UPLOAD / INGESTION
# ---------------------------------------------
with tab_upload:
    st.header("Upload Brain Matter")
    st.markdown("Add unstructured text to your vector datastore. The engine will chunk it, embed it algebraically, and store it locally.")
    
    ingest_method = st.radio("Input format:", ["Upload TXT File", "Manual Text Entry"], horizontal=True)
    
    chunks = []
    
    if ingest_method == "Manual Text Entry":
        raw_text = st.text_area("Paste Notes / Docs here:", height=250, placeholder="AI agents are autonomous systems that can plan...\nVector databases allow semantic search...")
        if raw_text:
            # Simple line-based chunking for now
            chunks = [line.strip() for line in raw_text.split('\n') if line.strip()]
    else:
        uploaded_notes = st.file_uploader("Upload Notes (.txt)", type=["txt"])
        if uploaded_notes:
            stringio = io.StringIO(uploaded_notes.getvalue().decode("utf-8"))
            raw_text = stringio.read()
            chunks = [line.strip() for line in raw_text.split('\n') if line.strip()]

    st.markdown(f"**Detected Sequence Chunks:** `{len(chunks)}`")
    
    if st.button("🔌 Vectorize & Store", type="primary"):
        if not api_key:
            st.error("Error: Please provide an OpenAI API key to access vector models.")
        elif not chunks:
            st.warning("No text sequence detected to ingest.")
        else:
            with st.spinner("Calculating n-dimensional vectors..."):
                try:
                    embeddings = agent.embed_texts(chunks)
                    records = agent.store_knowledge(chunks, embeddings)
                    st.success(f"Successfully processed {len(records)} knowledge chunks into the datastore!")
                except Exception as e:
                    st.error(f"Ingestion Failure: {e}")

# ---------------------------------------------
# TAB: SEARCH / RAG ENGINE
# ---------------------------------------------
with tab_search:
    st.header("Query the Void")
    st.markdown("Ask anything. The engine will mathematically retrieve the closest contextual notes and synthesize a precise answer.")
    
    # Try to load existing datastore
    records = []
    try:
        records = agent.load_knowledge()
    except Exception:
        pass
        
    query = st.text_input("What do you want to know?", placeholder="e.g. What is RAG and why is it useful?", help="Powered by cosine similarity.")
    
    if st.button("Execute Query ⚡", type="primary"):
        if not api_key:
             st.error("Error: OpenAI API key required.")
        elif not query.strip():
            st.warning("Please enter a valid query string.")
        else:
            if not records:
                st.info("💡 Note: No local datastore found. Operating on Pure Base Intelligence Mode.")
            with st.spinner("Executing semantic search and generation..."):
                try:
                    top_contexts = agent.retrieve(query, records, top_k=top_k_slider)
                    answer = agent.answer_query(query, top_contexts)
                    
                    st.markdown("### 🤖 Synthesized Output")
                    st.markdown(f"""
                    <div class="query-card">
                        <p style="font-size:1.1em; line-height: 1.6;">{answer}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("🔍 View Retrieved Sources Context"):
                        st.markdown(f"*(The mathematical top {len(top_contexts)} closest text vectors to your query)*")
                        for idx, ctx in enumerate(top_contexts, 1):
                            st.markdown(f"<div class='db-card'><strong>[Source {idx}]</strong> {ctx}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Search Execution Failed: {e}")
                    
# ---------------------------------------------
# TAB: DATASTORE INSPECTOR
# ---------------------------------------------
with tab_db:
    st.header("Datastore Inspector")
    st.markdown("Raw view of your embedded `.json` RAG records.")
    
    try:
        current_db = agent.load_knowledge()
        st.metric("Total Embeddings Cached", len(current_db))
        
        for i, row in enumerate(current_db):
            with st.expander(f"Chunk ID: {i} | Length: {len(row.get('text', ''))} chars"):
                st.markdown(f"**Raw Text:** {row.get('text')}")
                st.markdown(f"**Timestamp:** {row.get('created')}")
                st.caption(f"*Vector Dimensions Sample (First 5 floats):* {str(row.get('embedding', [])[:5])}...")
    except FileNotFoundError:
        st.info("No compiled knowledge.json file found. The datastore is pristine.")
    except Exception as e:
        st.error(f"Failed to load datastore: {e}")
