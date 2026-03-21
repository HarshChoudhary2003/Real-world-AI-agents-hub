# 📊 Sheet-Logic AI (Spreadsheet Formula Generator)

Architect high-performance, complex formulas across multiple platforms (Excel, Google Sheets, Airtable, Notion) with neural logic synthesis.

## 🚀 Overview
**Sheet-Logic AI v2.0** is a professional data architect designed for spreadsheet power users and automation specialists. It converts complex natural language requests into mathematically optimized formulas, ensuring strict syntax adherence and providing a **technical logic breakdown** for every output.

## ⚡ Key Features
- **Multi-Platform Native Syntax**: Generates precise formulas for Excel, Google Sheets, Airtable, and Notion with correct delimiter and function mapping.
- **Neural Logic Synthesis**: Breaks down the calculation path into human-readable technical steps.
- **Error Guardrails**: Identifies potential boundary errors like #N/A, #REF!, or zero-division points before you even paste the formula.
- **Alternative Optimizations**: Suggests Pivot Table approaches or advanced scripting hacks when standard formulas might be inefficient.
- **Multi-Provider Architecture**: Choose your intelligence brain from OpenAI, Gemini, Claude, DeepSeek, or Groq.

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Premium Creative UI with Syntax Highlighting)
- **Intelligence**: LiteLLM (Multi-model support)
- **Data Protocols**: JSON for logical object export, TXT for formula draft summaries.

## 📂 Structure
- `agent.py`: Core formula engine and multi-provider CLI wrapper.
- `app.py`: Premium animated Streamlit dashboard with component logic breakdown.
- `input.txt`: Default formula request for testing.
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
- **Primary Formula**: The mathematically optimized result.
- **Component Decomposition**: Step-by-step explanation of what each function name and range filter achieves.
- **Validation Guardrails**: Assumptions and data structure requirements for the formula to succeed.

---
*Part of the [Real-world-AI-agents-hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub)*
