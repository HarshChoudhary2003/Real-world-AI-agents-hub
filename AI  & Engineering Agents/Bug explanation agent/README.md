<div align="center">

# 🐛 BugSentinel AI
### Neural Traceback Analysis & Root Cause Diagnostic Forensics

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Litellm](https://img.shields.io/badge/Powered_by-LiteLLM-f43f5e.svg?style=for-the-badge&logo=openai)](https://litellm.ai/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

<br>

<img src="https://images.unsplash.com/photo-1555099962-4199c345e5dd?auto=format&fit=crop&w=1000&q=80" alt="Bug Sentinel Metrics" style="border-radius: 12px; box-shadow: 0 4px 30px rgba(0,0,0,0.5);">

<br>

**Decipher Complex Stack Traces without Hallucinating Fixes.**

</div>

---

## ⚡ Overview

**BugSentinel AI** specializes purely in interpreting and diagnosing software execution anomalies. It takes error constraints alongside code snippets and evaluates the core breakdown point—providing plain english traceback evaluations and root causes without simply throwing random untested code fixes at you.

## 🚀 Key Features

*   **🔎 Root Cause Triaging:** Strips away boilerplate crash logs to target exact line-number context crashes.
*   **🛑 Non-Destructive Explanations:** Complies with rules to NOT write fix-code, but logically deduce *why* an exception triggered based on Python paradigms.
*   **📊 Export Workflows:** Rapidly outputs explanations as txt files for internal tracking tickets via the console.
*   **🌐 Sentinel UI Edition:** A rich dual-input Streamlit Dashboard for parallel code & trace visualization.

## ⚙️ Quick Start

### 1. Terminal Execution
Drop the breaking code inside `code_snippet.py` and the exception trace in `error.txt`, then run:
```bash
python agent.py
```

### 2. Streamlit Dashboard
```bash
streamlit run app.py
```

---

<div align="center">
<i>Built with 🛡️ by the Post-SaaS Economy Framework. Part of the Real-World AI Agents Hub.</i>
</div>
