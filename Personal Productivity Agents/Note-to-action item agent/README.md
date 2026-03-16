# ⚡ ActionForge AI | Neural Task Extractor

**ActionForge AI** is a powerful Natural Language Processing agent designed to parse through chaotic meeting notes, brainstorming sessions, and loose brainstorming text, extracting *only* strictly defined and actionable tasks.

Instead of hunting for what you need to do amidst walls of text, provide the raw notes and let the LLM automatically structure your payload.

---

## ✨ Enterprise Features

### 1. Multi-Provider Intelligence
Powered by `litellm`, the Web Application (`app.py`) natively supports dynamically swapping between LLM providers:
- **OpenAI:** `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`
- **Anthropic:** `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- **Google:** `gemini-1.5-pro`, `gemini-1.5-flash`

### 2. High-Fidelity Extraction
The system is strictly prompted to return a rigid JSON schema, discarding ideas, opinions, and decisions that do not map to concrete actions. It intelligently categorizes:
- The Action Title
- Implied Deadlines
- The Owner/Assignee
- Urgency / Priority (Low, Medium, High)
- The raw source sentence that spawned the extraction.

### 3. Database-Ready Outputs
The parsed intelligence array can be downloaded seamlessly as a `JSON` payload (ready for API ingestion into Jira, Asana, or Trello), or as a Human-Readable text schedule (`.txt`) for immediate copy-pasting into your daily logs.

---

## 🚀 Installation & Setup

### Requirements
- Python 3.9+
- A valid API Key (OpenAI, Anthropic, or Google)

### 1. Install Dependencies
Run the following command to download the parsing and frontend engines:
```bash
pip install streamlit openai litellm pandas
```

### 2. Run the Command-Line Agent (Base)
You can execute the core logic directly in terminal. Create a `notes.txt` file and run:
```bash
python agent.py
```
This will strip the actions and dump them silently into `actions.json` and `actions.txt`.

### 3. Launch the Premium Dashboard (`app.py`)
Start the visual Streamlit engine to leverage intuitive copy/pasting, live tabular visualizers, and the multi-provider neural toggle!
```bash
python -m streamlit run app.py
```

---

## 💻 Tech Stack
- **Frontend / UI:** Streamlit (Custom Premium CSS injection)
- **Neural Routing:** `litellm` (LLM-Agnostic Processing)
- **Core Intelligence:** OpenAI Base Module (GPT Prompting)
- **Data Structuring:** Pandas DataFrames, Native JSON parsing


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
