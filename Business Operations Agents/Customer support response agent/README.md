# 🛡️ SupportCraft AI

An enterprise-grade AI agent that analyzes customer support tickets, assesses sentiment and urgency, and generates highly professional, empathetic responses complete with next steps, escalation recommendations, and internal team notes.

## 🌟 Features
* **Ticket Intelligence Engine**: Automatic analysis of customer sentiment, urgency level, issue category, and core problem identification.
* **Adaptive Tone Control**: Select from empathetic, friendly, formal, solution-focused, or apologetic response tones.
* **Email-Ready Responses**: Generates complete, polished email responses with subject lines, personalized greetings, structured bodies, and professional closings.
* **Internal Notes System**: Auto-generates escalation recommendations, follow-up dates, and knowledge base tags for the support team.
* **Premium Dark Dashboard**: Deep purple glassmorphism-styled Streamlit UI with gradient accents and interactive cards.
* **Multi-Provider Hub**: Supports OpenAI, Anthropic Claude, Google Gemini, Groq, Mistral, DeepSeek, and OpenRouter via LiteLLM.
* **Universal Export**: 1-click download of email TXT or raw JSON payloads.

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
