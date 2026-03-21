# 🛡️ Data-Guard AI (Data Validation Agent)

Perform deep forensic and mechanical audits on dataset integrity to identify breaches, explain root causes, and architect surgical code fixes.

## 🚀 Overview
**Data-Guard AI v2.0** is an enterprise-grade Data Quality & Governance OS. It combines strict **mechanical validation** (schema, types, ranges) with **AI-driven forensics** to translate isolated data errors into strategic remediation plans and pipeline hardening blueprints.

## ⚡ Key Features
- **Hybrid Validation Engine**: Pairs ultra-fast mechanical checks (Pandas) with high-fidelity linguistic insights (LiteLLM).
- **Forensic Deep Dives**: Explains the "Mechanical Reason" for every breach and provides a "Surgical Fix" for its resolution.
- **Health-Coded Dashboard**: Visualizes data integrity with animated status badges and severity color-coding (Red/Yellow/Green).
- **Rule Performance Mapping**: Tracks which validation rules are being breached most frequently to identify systemic data leakage.
- **Multi-Provider Architecture**: Choose your intelligence brain from OpenAI, Gemini, Claude, DeepSeek, or Groq.

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Premium Creative UI with Animated Status Signals)
- **Intelligence**: LiteLLM (Multi-model support)
- **Data Protocols**: JSON for forensic report export, TXT for diagnostic summaries.

## 📂 Structure
- `agent.py`: Core hybrid engine and multi-provider CLI wrapper.
- `app.py`: Premium animated Streamlit dashboard with component forensics.
- `input_data.csv`: Sample dataset for testing.
- `requirements.txt`: Project dependencies.

## 🚀 Quick Launch

### 1. CLI Usage
```bash
python agent.py
```

### 2. Dashboard Usage
```bash
streamlit run app.py
```

## 📊 Strategic Output
The agent outputs a structured JSON analysis including:
- **Integrity Audit**: A numerical health index, a status verdict, and a strategic summary.
- **Rule Performance**: Metrics on which rules passed or failed.
- **Violation Forensics**: Row-by-row analysis of breaches with surgical remediation steps.

---
*Part of the [Real-world-AI-agents-hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub)*
