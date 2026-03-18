# ⚖️ PolicyGuard: Policy Document Summarizer Agent

[![Intelligence](https://img.shields.io/badge/Focus-Regulatory_Intelligence-059669?style=for-the-badge&logo=googlesheets)](https://openai.com/)
[![Expert AI](https://img.shields.io/badge/AI-Compliance_Expert-blueviolet?style=for-the-badge&logo=openai)](https://openai.com/)
[![Market-Ready](https://img.shields.io/badge/Status-Market_Ready-success?style=for-the-badge)](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub)

**PolicyGuard** is a sophisticated AI agent designed to translate complex regulatory documents and enterprise policies into clear, actionable, and neutral summaries. It preserves legal intent while highlighting obligations, implications, and hidden ambiguities.

---

## 🌟 Premium Features

- **⚖️ Legal Intent Preservation**: Specifically engineered to summarize without introducing subjective interpretation.
- **📋 Key Requirement Mapping**: Extracts specific obligations into structured lists.
- **🚩 Ambiguity Detection**: Flags sections that are unclear or open to multiple interpretations.
- **✨ Universal Provider Support**: Seamlessly integrates with OpenAI, Groq, OpenRouter, DeepSeek, and local LLMs (Ollama).
- **📥 Professional Export**: Generate and download reports in both `.json` (structured data) and `.txt` (human-readable) formats.
- **🎨 Premium UI**: A sleek, emerald-themed Dashboard designed for compliance officers and legal professionals.

---

## 🛠 Tech Stack

- **Backend**: Python 3.9+
- **AI Engine**: GPT-4o-mini (Default) / Multi-Provider Support
- **UI Framework**: Streamlit (Premium Emerald/Slate Aesthetic)
- **Environment**: Dotenv for secure API management

---

## 🚀 Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY='your-api-key-here'
```

### 3. Usage

#### **PolicyGuard Dashboard (Recommended)**
Experience the full graphical interface with thematic cards and export tools.
```bash
streamlit run app.py
```

#### **CLI Batch Mode**
Quickly process documents via terminal:
```bash
python agent.py
```

---

## 📂 Project Structure

```text
policy-summarizer-agent/
├── app.py              # Premium Streamlit Dashboard
├── agent.py            # CLI Logic & Batch Processor
├── input.txt           # Policy text input source
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (User created)
└── README.md           # Documentation
```

---

## 🤝 Part of the AI Agents Hub
Developed by [Harsh Choudhary](https://github.com/HarshChoudhary2003). 
*Translating complexity into clarity.*

---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
