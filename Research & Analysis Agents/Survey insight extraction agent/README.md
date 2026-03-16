# 📊 Survey Insight Extraction Agent (Pro Edition)

An enterprise-grade, multi-model intelligence engine designed to transform chaotic survey responses into structured, actionable insights.

## 🚀 Pro Features

- **🌐 Multi-Model Engine**: Native support for OpenAI (GPT-4o), Anthropic (Claude 3.5), Google (Gemini 1.5), and Groq (Llama 3.1).
- **🧠 Latent Theme Extraction**: Automatically groups responses into meaningful categories using neural embedding patterns.
- **🎭 Sentiment Mapping**: Pinpoints the emotional tone across diverse datasets.
- **🛸 Minority Signal Detection**: Surfaces "voice of the customer" outliers often missed by traditional tools.
- **❓ Strategic Follow-ups**: Suggests high-impact optimization questions based on findings.
- **💎 Premium Dashboard**: Glassmorphism UI with real-time analytics and multi-provider routing.

## 📁 Project Structure

- `agent.py`: Core CLI engine and AI logic.
- `ui.py`: Premium Streamlit dashboard interface.
- `input.txt`: Data source for the CLI engine.
- `requirements.txt`: Project dependencies.
- `survey_insights.json`: Structured output (generated after run).
- `survey_insights.txt`: Human-readable summary (generated after run).

## 🛠️ Setup & Usage

### 1. Requirements
Install dependencies using pip:
```bash
pip install -r requirements.txt
```

### 2. API Key
Ensure your `OPENAI_API_KEY` is set in your environment variables.

### 3. Run via CLI
Update `input.txt` with your survey data and run:
```bash
python agent.py
```

### 4. Run via Streamlit UI
For a premium interactive experience, launch the dashboard:
```bash
streamlit run ui.py
```

## 📄 License
This agent is part of the [Real-world AI Agents Hub](https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub). MIT Licensed.
