# 📈 Market Trend Summarization Agent

A powerful, AI-driven intelligence agent designed to synthesize complex market data into structured, actionable insights. Whether you are tracking Enterprise AI, Fintech shifts, or Global Logistics, this agent identifies meaningful trends, distinguishes them from noise, and highlights critical implications.

## 🚀 Features

- **Multi-Model Intelligence**: Supported by **LiteLLM**, allowing you to switch between **OpenAI, Anthropic (Claude), Google (Gemini), and Groq** seamlessly.
- **Trend Synthesis**: Automatically identifies and categorizes market signals.
- **Deep Implications**: Moves beyond surface-level summaries to explain *why* it matters.
- **Risk Identification**: Surfaces uncertainties and potential headwinds.
- **Dual Interface**: Use the Python CLI for automated workflows or the Premium Streamlit UI for an interactive experience.
- **Structured Export**: Outputs in both `JSON` (for data pipelines) and `TXT` (for human review).

## 🛠️ Setup & Installation

1. **Clone the repository** (or navigate to the folder).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key**:
   Create a `.env` file or set your environment variable:
   ```env
   OPENAI_API_KEY=your_key_here
   ```

## 📖 Usage

### Premium Streamlit Interface (Recommended)
Launch the interactive dashboard:
```bash
streamlit run app.py
```

### Python CLI
Run the agent directly from the command line using `input.txt`:
```bash
python agent.py
```

## 📂 Project Structure

- `agent.py`: Core logic for the AI agent.
- `app.py`: Premium Streamlit dashboard.
- `input.txt`: Configuration for the market scope.
- `requirements.txt`: Project dependencies.
- `market_trends.json/txt`: Generated output files.

---
*Built with ❤️ by Antigravity AI Agent*


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
