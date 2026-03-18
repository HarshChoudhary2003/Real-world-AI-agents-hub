# 💳 ExpenseIQ AI — Expense Categorization Agent

<div align="center">
  <img src="https://img.shields.io/badge/AI-Expense%20Categorization-818cf8?style=for-the-badge&logo=openai&logoColor=white" alt="ExpenseIQ AI" />
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Premium%20UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Multi--Model-OpenAI%20|%20Anthropic%20|%20Gemini%20|%20Groq-38BDF8?style=flat-square" />
</div>

---

## 🌌 Overview

**ExpenseIQ AI** is an enterprise-grade Expense Categorization Agent that intelligently assigns business expense categories to transactions using Large Language Models. It produces structured, confidence-rated categorizations with justifications and flags for ambiguous or policy-sensitive expenses.

Built as part of the **Real-world AI Agents Hub**, it features both a **Python CLI** and a **premium Streamlit dashboard**.

---

## ✨ Key Features

- 🧠 **Multi-Model Intelligence** — OpenAI, Anthropic, Gemini, and Groq support
- 🏷️ **Smart Categorization** — Vendor + description context-aware category assignment
- 📊 **Confidence Rating** — High / Medium / Low with explainable justifications
- 🚩 **Flag System** — Surfaces ambiguous, dual-purpose, or policy-sensitive expenses
- 📈 **Spend Analytics** — Historical category frequency and confidence distribution charts
- 📦 **Batch Mode** — Categorize multiple transactions from a CSV in one run
- 📄 **Dual Export** — Outputs `expense_categorization.json` and `expense_categorization.txt`

---

## 📁 Project Structure

```
Expense categorization agent/
├── agent.py              # Core CLI agent (multi-provider)
├── app.py                # Premium Streamlit UI
├── input.txt             # Sample transaction input
├── requirements.txt      # Python dependencies
├── .env.example          # API key template
└── README.md             # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your provider API key
```

### 3a. Run CLI Agent

```bash
python agent.py
```

**Output:**
```
🔍 Analyzing expense transaction...
✅ Expense categorized successfully.
   Category   : Software
   Confidence : High
```

### 3b. Launch Streamlit Dashboard

```bash
streamlit run app.py
```

---

## 📄 Input Format (`input.txt`)

```
Transaction Description: Zoom Video Communications Monthly Subscription
Vendor: Zoom
Amount: $149.99
Date: 2025-06-05
Available Categories:
- Software
- Travel
- Marketing
- Office Supplies
- Professional Services
```

---

## 📊 Output Format

### `expense_categorization.json`
```json
{
  "vendor": "Zoom",
  "description": "Zoom Video Communications Monthly Subscription",
  "amount": "$149.99",
  "date": "2025-06-05",
  "category": "Software",
  "confidence": "High",
  "justification": "Zoom is a well-known video conferencing SaaS product billed monthly, clearly falling under software subscriptions.",
  "flags": []
}
```

### `expense_categorization.txt`
```
Expense Categorization Report (2025-06-05)
=======================================================

Vendor       : Zoom
Description  : Zoom Video Communications Monthly Subscription
Amount       : $149.99
Date         : 2025-06-05
Category     : Software
Confidence   : High
Justification: Zoom is a well-known video conferencing SaaS product...

Flags: None
```

---

## 🛠️ Supported Models

| Provider  | Model                         |
|-----------|-------------------------------|
| OpenAI    | gpt-4.1-mini, gpt-4o          |
| Anthropic | claude-3-5-sonnet, claude-3-opus |
| Gemini    | gemini-1.5-flash, gemini-1.5-pro |
| Groq      | llama-3.1-70b, mixtral-8x7b   |

---

## 📄 License

MIT License — Part of the [Real-world AI Agents Hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub)

---

*Engineered for Enterprise Automation • ExpenseIQ AI*
