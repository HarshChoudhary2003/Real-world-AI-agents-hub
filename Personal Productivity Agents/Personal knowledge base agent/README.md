# 🧠 BrainVault AI | Local Knowledge RAG Engine

**BrainVault AI** is a fully functional, locally contained Retrieval-Augmented Generation (RAG) knowledge engine. 

Instead of relying on broad LLM internet scraping, BrainVault ingests *your* specific text notes, fragments them, deeply embeds them using OpenAI's dense vector neural networks, and performs hyper-accurate semantic similarity searches to answer questions based strictly on your private localized data.

---

## ✨ Enterprise Features

### 1. Local Vector Architecture
Unlike generic SaaS tools that upload your personal notes to third-party datastores, BrainVault computes everything locally. 
- Using OpenAI's `text-embedding-3-small` model, it converts your text blocks into multi-dimensional float arrays. 
- Calculates contextual similarity using an advanced mathematical `Cosine Similarity` matrix under the hood, all without spinning up slow SQL or external databases.

### 2. Pure Base Intelligence Fallback
BrainVault intelligently tracks references. If it finds text in your datastore that answers your question, it leverages that explicitly.
If your datastore is empty, or the local context lacks the specific answer, the agent seamlessly pivots to "General Knowledge Mode" and leverages the foundational power of GPT-4o-mini to answer your queries dynamically.

### 3. Streamlit Datastore Inspector
The robust Enterprise UI features three powerful navigation tabs:
- **Semantic Search:** Execute queries against your vector store with natural language. 
- **Knowledge Ingestion:** Dump walls of unstructured text or research notes and allow the LLM to process and embed it locally.
- **Datastore Optics:** Visually inspect your underlying `.json` database file arrays to debug embedded text blocks.

---

## 🚀 Installation & Setup

### Requirements
- Python 3.9+
- A valid OpenAI API Key (Required for Embedding Vectors + RAG completion)

*Note: For absolute data-consistency, the mathematical semantic embeddings in BrainVault rely exclusively on OpenAI. Modifying the underlying `litellm` gateway might cause embedding mismatches. It is optimized explicitly for OpenAI architecture.*

### 1. Install Dependencies
Run the following command to download the parsing and frontend engines:
```bash
pip install streamlit openai numpy pandas
```

### 2. Run the Command-Line Agent (Base)
You can interact with the engine using native CLI hooks by passing unstructured texts.
```bash
python agent.py
```

### 3. Launch the Premium Dashboard (`app.py`)
Start the visual Streamlit engine to get direct GUI access to ingest your unstructured notes payload.
```bash
python -m streamlit run app.py
```

---

## 💻 Tech Stack
- **Frontend / UI:** Streamlit (Custom Premium CSS injection)
- **Vector Embedding:** `text-embedding-3-small`
- **Core Intelligence:** `gpt-4o-mini`
- **Datastore Logic:** Native `.json`, `numpy` Cosine Similarity calculations
