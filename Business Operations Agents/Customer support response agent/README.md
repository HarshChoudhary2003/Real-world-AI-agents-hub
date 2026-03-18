# 🎧 SupportIQ AI — Customer Support Response Agent

<div align="center">
  <img src="https://img.shields.io/badge/AI-SupportIQ-22d3ee?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Premium%20UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Multi--Model-OpenAI%20|%20Anthropic%20|%20Gemini%20|%20Groq-38BDF8?style=flat-square" />
</div>

---

## 🌌 Overview

**SupportIQ AI** is an enterprise-grade Customer Support Response Agent that generates empathetic, professional, policy-compliant draft responses to customer tickets using LLMs. It goes far beyond a basic template — delivering sentiment analysis, frustration scoring, quality self-assessment, escalation detection, channel recommendations, and a premium analytics dashboard.

Built as part of the [Real-world AI Agents Hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub).

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🧠 **Multi-Model AI** | OpenAI, Anthropic, Gemini, Groq — switchable at runtime |
| 😤 **Sentiment Detection** | Frustrated / Angry / Confused / Neutral / Satisfied |
| 📊 **Frustration Score** | 1–10 frustration rating per ticket |
| ⭐ **Quality Scoring** | Empathy, Clarity, Professionalism, Overall (1–10 each) |
| 🚨 **Auto-Escalation** | Keyword + rule-based escalation flagging |
| 📋 **Policy Guard** | Flags responses with promises needing manager approval |
| 📡 **Channel Recommendation** | Email / Live Chat / Phone / Escalate to Manager |
| ⏱️ **ETA Estimation** | Realistic resolution time estimate per ticket |
| 🔄 **Retry Logic** | Exponential backoff with 3 retries on API errors |
| 📦 **Batch Processing** | CSV tickets → JSON + CSV + TXT batch reports |
| 📊 **Analytics Dashboard** | Sentiment trends, quality over time, escalation rates |

---

## 📁 Project Structure

```
Customer support response agent/
├── agent.py                  # Core engine (multi-provider, escalation, quality scoring)
├── app.py                    # Premium Streamlit dashboard
├── input.txt                 # Single ticket input
├── sample_tickets.csv        # Sample batch CSV (6 tickets)
├── requirements.txt          # Python dependencies
├── .env.example              # API key template
├── support_response.json     # Latest single response (auto-generated)
├── support_response.txt      # Latest single report (auto-generated)
├── support_batch_results.json# Batch results (auto-generated)
├── support_batch_results.csv # Batch CSV export (auto-generated)
└── support_history.json      # Dashboard history (auto-generated)
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
cp .env.example .env
# Edit .env with your key

# 3a. Single ticket (CLI)
python agent.py

# 3b. Batch CSV (CLI)
python agent.py --csv sample_tickets.csv

# 3c. Launch dashboard
streamlit run app.py
```

---

## 🖥️ CLI Options

```
python agent.py [options]

  --input       TXT ticket file (default: input.txt)
  --csv         CSV batch file
  --provider    OpenAI | Anthropic | Gemini | Groq
  --model       Model name (provider default if omitted)
  --api-key     API key (uses .env if omitted)
  --version     Show version
```

---

## 📄 Input Format

### Single (`input.txt`)
```
Customer Message:
I was charged twice for my subscription this month and I'm really frustrated.

Issue Category: Billing
Urgency: High
Brand Tone: Professional and empathetic
Customer Name: James Carter
```

### Batch (`sample_tickets.csv`)
```csv
message,customer_name,category,urgency,tone
"I was charged twice!",James Carter,Billing,High,Professional and empathetic
```

---

## 📊 Output Schema

```json
{
  "customer_name": "James Carter",
  "issue_category": "Billing",
  "urgency": "High",
  "detected_sentiment": "Frustrated",
  "frustration_score": 8,
  "greeting": "Dear James,",
  "acknowledgment": "I completely understand your frustration...",
  "response": "We sincerely apologize for the billing error...",
  "next_steps": ["Step 1...", "Step 2...", "Step 3..."],
  "closing": "Thank you for your patience and loyalty...",
  "tone_used": "Empathetic and decisive",
  "response_quality": {
    "empathy_score": 9,
    "clarity_score": 8,
    "professionalism_score": 9,
    "overall_score": 9
  },
  "policy_flags": [],
  "recommended_channel": "Email",
  "escalation_required": false,
  "estimated_resolution_time": "24-48 hours"
}
```

---

## 🛠️ Supported Models

| Provider  | Models |
|---|---|
| OpenAI    | gpt-4.1-mini, gpt-4o, gpt-4o-mini |
| Anthropic | claude-3-5-sonnet, claude-3-opus, claude-3-haiku |
| Gemini    | gemini-2.0-flash, gemini-1.5-flash, gemini-1.5-pro |
| Groq      | llama-3.3-70b, llama-3.1-70b, mixtral-8x7b |

---

## 📄 License

MIT — Part of the [Real-world AI Agents Hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub)

---
*Engineered for Enterprise Customer Excellence • SupportIQ AI v1.0.0*
