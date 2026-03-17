# 🧾 Invoice Intel Pro (Advanced Invoice Agent)

An elite, multi-model automated invoice processing system designed for enterprise-grade financial data extraction, mathematical verification, and audit logging.

## ✨ Advanced Features
- **🧠 Multi-Model Neural Core**: Choose between OpenAI (GPT-4), Anthropic (Claude 3.5), Google (Gemini 1.5), or Groq (Llama 3) for the engine.
- **🛡️ 3-Tier Validation System**:
    - **Extraction Precision**: High-fidelity field mapping (Vendor, Date, Currency, etc.).
    - **Mathematical Reconciliation**: Automatic cross-check of line items + tax vs. total amount.
    - **Heuristic Flags**: Detection of future dates, missing invoice numbers, and significant discrepancies.
- **📊 Premium Analytics Hub**: 
    - **Glassmorphism UI**: High-end Streamlit dashboard with custom CSS.
    - **Visual Audit**: Real-time cost distribution pie charts and validation logs.
    - **Detailed Audit Table**: Tabular view of all extracted line items.
- **📥 Enterprise Export**: Download multi-format artifacts including JSON audits and human-readable text summaries.

## 📁 Project Architecture
- `agent.py`: Multi-provider orchestration and validation logic.
- `app.py`: Premium Streamlit interface.
- `input.txt`: Data buffer for CLI operations.
- `invoice.json`: Validated structured output.
- `invoice.txt`: Comprehensive human-readable audit report.

## 🚀 Deployment Guide

### 1. Environment Setup
Install the advanced neural dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configuration
Configure your provider keys in a `.env` file:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
GROQ_API_KEY=gsk_...
```

### 3. Execution

#### CLI Extraction
```bash
python agent.py
```

#### Neural Dashboard (Recommended)
```bash
streamlit run app.py
```

## 🛠️ Tech Stack
- **Engine**: OpenAI, Anthropic, Google, Groq
- **Frontend**: Streamlit + Custom Glassmorphism CSS
- **Visualization**: Plotly Express
- **Analysis**: Pandas
- **Logic**: Neural JSON-enforcement with mathematical cross-validation
