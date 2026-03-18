# 🧬 CRMPulse AI — CRM Data Enrichment Agent

<div align="center">
  <img src="https://img.shields.io/badge/AI-CRMPulse-34d399?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Premium%20UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Multi--Model-OpenAI%20|%20Anthropic%20|%20Gemini%20|%20Groq-38BDF8?style=flat-square" />
</div>

---

## 🌌 Overview

**CRMPulse AI** is an enterprise-grade CRM Data Enrichment Agent that intelligently fills in missing B2B contact and company fields using AI inference from available context (email domain, company name, role, location). It delivers per-field confidence scoring, lead scoring, dedup detection, and a rich analytics dashboard.

Built as part of the [Real-world AI Agents Hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub).

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🧠 **Multi-Model AI** | OpenAI, Anthropic, Gemini, Groq — switchable at runtime |
| 🏢 **Company Profiling** | Industry, size, revenue, funding stage, HQ, founded year |
| 🎯 **Lead Scoring** | 1–100 AI-powered lead potential score with reasoning |
| 📊 **Confidence Scoring** | High / Medium / Low per enriched field |
| ⚙️ **Tech Stack Inference** | Likely technologies used, based on industry + company type |
| 🔗 **LinkedIn URL** | Pattern-based LinkedIn URL suggestion |
| 🔎 **Dedup Detection** | MD5-hash duplicate detection across all enrichment runs |
| 📋 **Data Quality %** | Overall CRM record completeness score |
| 🔄 **Retry Logic** | Exponential backoff with 3 retries |
| 📦 **Batch Processing** | CSV → JSON + CSV + TXT batch enrichment reports |
| ⚠️ **Flag System** | Transparent flags for uncertain inferences |

---

## 📁 Project Structure

```
CRM data enrichment agent/
├── agent.py                  # Core enrichment engine
├── app.py                    # Premium Streamlit dashboard
├── input.txt                 # Single record input
├── sample_records.csv        # Sample batch CSV (6 records)
├── requirements.txt
├── .env.example
├── crm_enriched.json         # Latest enrichment output (auto-generated)
├── crm_enriched.txt          # Latest text report (auto-generated)
└── crm_history.json          # Dashboard history (auto-generated)
```

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env   # Add your API key

# Single record (CLI)
python agent.py

# Batch enrichment
python agent.py --csv sample_records.csv

# Dashboard
streamlit run app.py
```

---

## 📄 Input Format

```
Name: Jane Doe
Email: jane.doe@techstartup.com
Company: TechStartup Inc.
Known Fields:
- Role: Product Manager
- Location: San Francisco, CA
Missing Fields:
- Industry
- Company Size
- Account Segment
- Funding Stage
```

---

## 📊 Output Schema

```json
{
  "name": "Jane Doe",
  "email": "jane.doe@techstartup.com",
  "company": "TechStartup Inc.",
  "enriched_fields": {
    "industry": "Software / SaaS",
    "company_size": "10-50 employees",
    "annual_revenue": "$1M-$10M",
    "account_segment": "Startup",
    "funding_stage": "Series A",
    "linkedin_url": "linkedin.com/in/jane-doe",
    "technologies_used": ["Slack", "Notion", "AWS", "React"],
    "headquarters": "San Francisco, CA",
    "founded_year": "2019"
  },
  "confidence": { "industry": "High", "company_size": "Medium", ... },
  "data_quality_score": 78,
  "lead_score": 82,
  "lead_score_reason": "Senior PM at a funded SaaS startup — high purchase authority.",
  "enrichment_summary": "Enriched 8 fields with high overall confidence...",
  "recommended_actions": ["Schedule discovery call", "Send product demo link", "Add to Enterprise nurture sequence"],
  "flags": []
}
```

---

## 🛠️ Supported Models

| Provider | Models |
|---|---|
| OpenAI | gpt-4.1-mini, gpt-4o, gpt-4o-mini |
| Anthropic | claude-3-5-sonnet, claude-3-opus, claude-3-haiku |
| Gemini | gemini-2.0-flash, gemini-1.5-flash, gemini-1.5-pro |
| Groq | llama-3.3-70b, llama-3.1-70b, mixtral-8x7b |

---

*Engineered for Enterprise CRM Excellence • CRMPulse AI v1.0.0*
