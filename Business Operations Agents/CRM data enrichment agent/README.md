# 🧬 CRM DataForge AI

An enterprise-grade AI agent that transforms raw CRM contact and company records into rich, actionable intelligence — complete with industry classification, tech stack detection, buying signal analysis, decision-maker mapping, and lead scoring.

## 🌟 Features
* **Deep Lead Enrichment**: AI-powered profile analysis with industry classification, estimated size, tech stack signals, and inferred pain points.
* **Decision Maker Mapping**: Identifies key stakeholders and provides tailored engagement strategies for each persona.
* **Lead Scoring Engine**: Automatic 1-10 lead readiness scoring based on enriched context.
* **Premium Dark Dashboard**: Glassmorphism-styled Streamlit UI with gradient accents, metric badges, and interactive cards.
* **Multi-Provider Hub**: Supports OpenAI, Anthropic Claude, Google Gemini, Groq, Mistral, DeepSeek, and OpenRouter via LiteLLM.
* **Universal Export**: 1-click download of structured TXT reports or raw JSON payloads.

## 🚀 Getting Started

### Prerequisites
API keys from your preferred provider:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `GROQ_API_KEY`

### Installation
```bash
pip install -r requirements.txt
```

### Running the App
Run the interactive Streamlit Dashboard:
```bash
streamlit run app.py
```

Run the headless CLI Pipeline:
```bash
python agent.py
```
