# 💸 ExpenseIQ AI

An enterprise-grade AI agent that intelligently categorizes expenses, detects anomalies and duplicate charges, flags policy violations, and generates spending intelligence reports — powered by multi-provider LLM support.

## 🌟 Features
* **Smart Categorization**: AI-powered expense classification into standard accounting categories with confidence scores.
* **Anomaly Detection**: Automatic flagging of duplicates, unusual amounts, and potential policy violations.
* **Budget Intelligence**: Real-time budget utilization tracking with visual breakdown charts.
* **Spending Insights**: AI-generated recommendations and trend analysis for better financial decisions.
* **Premium Dark Dashboard**: Emerald-themed glassmorphism Streamlit UI with gradient accents and interactive expense cards.
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
