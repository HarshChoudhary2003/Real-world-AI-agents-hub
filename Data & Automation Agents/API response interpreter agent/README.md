# 🔌 API-Insight AI (API Response Interpreter)

Perform deep forensic analysis on raw API payloads to identify root causes, map data nodes, and architect surgical code fixes.

## 🚀 Overview
**API-Insight AI v2.0** is an advanced diagnostic engine for backend developers and systems architects. It translates cryptic JSON responses and non-standard HTTP status codes into **human-readable intelligence**, identifying linguistic failures, structural anomalies, and potential security vulnerabilities.

## ⚡ Key Features
- **Forensic Error Analysis**: Pinpoints the "Mechanical Reason" for failures beyond the standard error message.
- **Payload Node Mapping**: Automatically identifies critical data nodes, their intent, and validity status.
- **Surgical Code Fixes**: Provides a "Blueprint Fix" for every identified error (e.g., specific retry logic or payload corrections).
- **Security & PII Auditing**: Flags exposed PII, verbose stack traces, or sensitive headers in the API response.
- **Multi-Provider Architecture**: Native selection of your intelligence brain (OpenAI, Gemini, Claude, DeepSeek, or Groq).

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Premium Creative UI with Severity Color-Coding)
- **Intelligence**: LiteLLM (Multi-model support)
- **Data Protocols**: JSON for forensic object export, TXT for diagnostic brief summaries.

## 📂 Structure
- `agent.py`: Core diagnostic engine and multi-provider CLI wrapper.
- `app.py`: Premium animated Streamlit dashboard with component logic breakdown.
- `response.json`: Sample API payload for testing.
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
- **Audit Report**: Summary of the response, intent of the status code, and severity level.
- **Payload Nodes**: Detailed mapping of JSON fields and their data types.
- **Root Cause Forensics**: Technical reasoning for errors and the corresponding code remediation.

---
*Part of the [Real-world-AI-agents-hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub)*
