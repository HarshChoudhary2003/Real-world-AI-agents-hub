# 🤝 SalesFollowAI Pro

An enterprise-grade AI agent designed to craft perfectly toned, highly consultative sales follow-up messages based on previous interactions, buyer personas, and targeted next-step objectives.

## 🌟 Features
* **Context-Driven Drafting**: Intelligently parses your meeting notes to prove you listened and understood prospect challenges.
* **Value Reinforcement**: Automatically weaves your product's value proposition directly into the conversation naturally.
* **Call to Action**: Generates clear, low-pressure next steps aligned precisely with your follow-up objective.
* **Premium Dark Dashboard**: Executive-styled sapphire and slate glassmorphism UI with segmented message previews.
* **Multi-Provider Hub**: Supports OpenAI, Anthropic Claude, Google Gemini, and Groq via LiteLLM.
* **Universal Export**: 1-click download of ready-to-send TXT drafts or structured JSON schemas.

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
