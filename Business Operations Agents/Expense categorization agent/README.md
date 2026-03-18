# 💳 ExpenseIQ AI — Enterprise Expense Categorization Agent

<div align="center">
  <img src="https://img.shields.io/badge/AI-ExpenseIQ-818cf8?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Premium%20UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Multi--Model-OpenAI%20|%20Anthropic%20|%20Gemini%20|%20Groq-38BDF8?style=flat-square" />
</div>

---

## 🌌 Overview

**ExpenseIQ AI** is an enterprise-grade Expense Categorization Agent that intelligently classifies business transactions using Large Language Models. It goes far beyond basic categorization — delivering GL code suggestions, tax deductibility estimates, policy compliance checks, duplicate detection, risk scoring, and a premium Streamlit analytics dashboard.

Built as part of the [Real-world AI Agents Hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub).

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🧠 **Multi-Model AI** | OpenAI, Anthropic, Gemini, Groq — switchable at runtime |
| 🏷️ **Rich Categorization** | Category + Subcategory + GL Code suggestion |
| 📊 **Confidence Scoring** | High/Medium/Low + numeric 0–1 score |
| 💰 **Tax Deductibility** | % deductible + deductible amount + tax notes |
| ⚖️ **Policy Engine** | Approved / Review Required / Flagged statuses |
| 🔁 **Duplicate Detection** | MD5-hash based dedup across all processed transactions |
| 🚩 **Smart Flags** | Over-limit amounts, dual-purpose expenses, policy breaches |
| ⚡ **Risk Scoring** | 0–10 risk score per transaction |
| 🔄 **Recurring Detection** | One-time / Likely Recurring / Definitely Recurring |
| 📦 **Batch Processing** | CSV batch input → JSON + CSV + TXT batch reports |
| 🔃 **Retry Logic** | Exponential backoff with 3 retries on API errors |
| 📈 **Analytics Dashboard** | Spend treemap, risk scatter, timeline, policy breakdown |
| 📋 **Audit Log** | Filterable full transaction history with exports |

---

## 📁 Project Structure

```
Expense categorization agent/
├── agent.py                    # Core engine (multi-provider, retry, dedup, batch)
├── app.py                      # Premium Streamlit dashboard
├── input.txt                   # Single transaction input
├── sample_batch.csv            # Sample batch CSV (10 transactions)
├── requirements.txt            # Python dependencies
├── .env.example                # API key template
├── expense_categorization.json # Latest single result (auto-generated)
├── expense_categorization.txt  # Latest single report (auto-generated)
├── expense_batch_results.json  # Batch results (auto-generated)
├── expense_batch_results.csv   # Batch CSV export (auto-generated)
├── expense_dedup_db.json       # Duplicate detection store (auto-generated)
└── expense_history.json        # Dashboard history (auto-generated)
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
cp .env.example .env
# Edit .env — add your provider key(s)
```

### 3a. Single Transaction (CLI)
```bash
python agent.py
```

### 3b. Batch CSV (CLI)
```bash
python agent.py --csv sample_batch.csv --provider OpenAI
```

### 3c. Launch Dashboard
```bash
streamlit run app.py
```

---

## 🖥️ CLI Options

```
python agent.py [options]

Options:
  --input      TXT input file (default: input.txt)
  --csv        CSV batch file path
  --provider   OpenAI | Anthropic | Gemini | Groq
  --model      Model name (uses provider default if omitted)
  --api-key    API key (uses .env if omitted)
  --categories Comma-separated list (for CSV mode)
```

---

## 📄 Input Format

### Single (`input.txt`)
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

### Batch (`sample_batch.csv`)
```csv
description,vendor,amount,date
Monthly Zoom subscription,Zoom,$149.99,2025-06-05
AWS cloud services,Amazon Web Services,$1240.00,2025-06-01
```

---

## 📊 Output Schema

```json
{
  "vendor": "Zoom",
  "description": "Zoom Video Communications Monthly Subscription",
  "amount": "$149.99",
  "amount_numeric": 149.99,
  "currency": "USD",
  "date": "2025-06-05",
  "category": "Software",
  "subcategory": "Video Conferencing",
  "confidence": "High",
  "confidence_score": 0.97,
  "justification": "Zoom is a well-known SaaS video conferencing platform...",
  "tax_deductible": true,
  "tax_deductibility_pct": 100,
  "tax_notes": "Fully deductible as ordinary business software expense (IRC §162).",
  "policy_status": "Approved",
  "flags": [],
  "suggested_gl_code": "6100-Software-SaaS",
  "recurring_likelihood": "Definitely Recurring",
  "risk_score": 1
}
```

---

## 🛠️ Supported Models

| Provider  | Models |
|-----------|--------|
| OpenAI    | gpt-4.1-mini, gpt-4o, gpt-4o-mini, gpt-4-turbo |
| Anthropic | claude-3-5-sonnet, claude-3-opus, claude-3-haiku |
| Gemini    | gemini-1.5-flash, gemini-1.5-pro, gemini-2.0-flash |
| Groq      | llama-3.1-70b, mixtral-8x7b, llama3-70b |

---

## 📄 License

MIT — Part of the [Real-world AI Agents Hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub)

---
*Engineered for Enterprise Automation • ExpenseIQ AI*
