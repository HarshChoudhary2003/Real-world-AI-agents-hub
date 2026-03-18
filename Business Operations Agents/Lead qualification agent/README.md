# 🎯 LeadScore AI

An enterprise-grade AI agent that qualifies sales leads using the BANT (Budget, Authority, Need, Timeline) framework, providing precise scoring, classification, green/red flag analysis, and tailored next-action recommendations for the sales team.

## 🌟 Features
* **BANT Qualification Engine**: Deep 4-dimensional lead analysis with individual dimension scoring and detailed assessments.
* **Precision Lead Scoring**: 1-100 score with automatic Hot/Warm/Cool/Cold classification.
* **Flag Analysis**: Identifies green flags (positive indicators) and red flags (warning signals) with disqualification risk assessment.
* **Sales Strategy**: Generates recommended next actions and tailored talking points for follow-up calls.
* **Premium Dark Dashboard**: Amber & Indigo-themed Streamlit UI with score ring visualization, BANT cards, and interactive flag displays.
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
