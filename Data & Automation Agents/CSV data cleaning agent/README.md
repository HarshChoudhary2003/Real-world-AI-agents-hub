# 🧬 NeuralData AI v3.0: Omni-Model Batch Integrity Matrix

A high-performance engine for CSV data cleaning and integrity auditing that leverages **LiteLLM** to support 100+ AI models including OpenAI, Anthropic, Gemini, Groq, and more.

---

## ⚡ Features (v3.0 Omni-Engine)
- **🦾 Omni-Model Hub**: Support for any AI model via LiteLLM. Toggle between GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, and Llama 3 with ease.
- **📂 Neural Batch Matrix**: High-velocity batch cleaning for multiple CSVs. Generate individual diagnostic logs and aggregate health metrics.
- **🛠️ Custom Logic Injection**:
    - **Range**: Numerical bounds enforcement.
    - **Regex**: Pattern-based validation (email, phone, IDs).
    - **Not Null**: Critical identity protection.
    - **AI Directives**: Use the LLM's world knowledge to fix semantic typos and inconsistent labels.
- **🚨 Intelligent Anomaly Detection**: Automatic detection and logging of out-of-range data.
- **💎 Premium v3.0 UI**: Modern Glassmorphism interface with **Token Matrix** management for all major AI providers.

---

## 🛠️ Installation & Tech Stack

1. **Clone the repository**:
   ```bash
   cd csv-data-cleaning-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Core Stack**:
    - **Orchestration**: LiteLLM + Instructor
    - **Analysis**: Pandas + Plotly
    - **UI**: Streamlit (Glassmorphism CSS)

---

## 🚀 Usage

### Option 1: Premium Dashboard (Recommended)
Run the Streamlit app to access the Omni-Model interface:
```bash
streamlit run app.py
```

### Option 2: CLI Mode
Run the core engine locally on current directory CSVs:
```bash
python agent.py
```

---

## 🧬 Neural Token Matrix
Configure these in the Streamlit Sidebar or your `.env` file:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `GROQ_API_KEY`

---
*Architected for Enterprise • Engineered for Immediate Impact*
