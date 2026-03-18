# 🎭 AI Tone Alchemist Pro

An enterprise-grade, multi-model AI agent designed to flawlessly rewrite text into any specific tone without hallucinating or losing semantic meaning. 

Built with an advanced Chain-of-Thought architecture, it guarantees perfect feature-to-tone reproduction while suppressing typical robotic AI fluffy cliches.

## 🌟 Features
* **Multi-Provider Hub**: Supports OpenAI (`gpt-4o`, `gpt-4o-mini`), Google Gemini (`gemini-1.5-pro`), and Anthropic Claude (`claude-3-5-sonnet`).
* **Semantic Fidelity Engine**: Strict prompting pipeline ensures no original facts are dropped and no false claims are added.
* **Thought Process Exposer**: See exactly *why* the AI chose the words it did.
* **Universal Export**: One-click download of the JSON payload or a formatted markdown Text Draft.

## 🚀 Getting Started

### Prerequisites
Make sure you have your desired API keys:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`

### Installation
```bash
pip install openai anthropic google-generativeai streamlit
```

### Running the App
Run the premium Streamlit Dashboard:
```bash
streamlit run app.py
```

Alternatively, run the headless CLI Pipeline:
```bash
python agent.py
```


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
