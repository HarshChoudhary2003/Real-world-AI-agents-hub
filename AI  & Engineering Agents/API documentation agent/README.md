<div align="center">

# 📖 DocForge AI
### Automated REST API Documentation & Contract Logic Compiler

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Litellm](https://img.shields.io/badge/Powered_by-LiteLLM-10b981.svg?style=for-the-badge&logo=openai)](https://litellm.ai/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

<br>

<img src="https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1000&q=80" alt="DocForge AI Architecture" style="border-radius: 12px; box-shadow: 0 4px 30px rgba(0,0,0,0.5);">

<br>

**Deterministic Documentation Pipelines from Unstructured Intent.**

</div>

---

## ⚡ Overview

**DocForge AI** elegantly transforms messy, unstructured endpoint ideas and requirements into rigid, enterprise-grade generic REST API schemas, complete with data dictionaries, payload examples, and standard HTTP error contracts. It outputs in both cleanly structured `api_docs.json` for CI/CD pipelines and `api_docs.md` for human readability.

## 🚀 Key Features

*   **🧠 Provider Agnostic:** Fully integrated with `LiteLLM`, allowing seamless switching between models like OpenAI (GPT-4o), Anthropic (Claude 3.5), X (Grok), Google (Gemini), and Local (Ollama).
*   **💠 Elite SaaS Dashboard:** A sleek, dark-mode Streamlit UI giving architects a fast execution playground.
*   **📊 Dynamic Table Generation:** Translates parameters into precise schema tables immediately in your browser.
*   **⬇️ Unified Exports:** Push single-click JSON payloads or Markdown outputs straight from the UI.

## ⚙️ Quick Start

### 1. Installation

Ensure you have your environment set up and the core dependencies installed:
```bash
pip install openai litellm streamlit pandas python-dotenv
```

Define your API keys globally inside a `.env` file at the root.

### 2. Launch the Visual Interface

Experience the SaaS Edition GUI:
```bash
cd "API documentation agent"
streamlit run app.py
```

### 3. Command-Line Execution

If you prefer standard bash pipelines:
```bash
python agent.py
```
*Outputs are saved to `api_docs.md` and `api_docs.json` locally.*

---

<div align="center">
<i>Built with 🛡️ by the Post-SaaS Economy Framework. Part of the Real-World AI Agents Hub.</i>
</div>
