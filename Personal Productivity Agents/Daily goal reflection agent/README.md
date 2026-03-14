# 🧘 Reflect AI | Cognitive Mirror Engine

**Reflect AI** is a powerful daily journaling and reflection analyzer. Stop just tracking what you do, and start identifying **why** friction is occurring. 

By comparing what you *planned* against what you *actually accomplished*, the internal LLM mathematically quantifies your "Daily Velocity", extracts critical operational insights, and algorithmically builds actionable suggestions to improve your protocols tomorrow.

---

## ✨ Enterprise Features

### 1. Multi-Provider Intelligence
Powered by `litellm`, the Web Application (`app.py`) natively supports dynamically swapping between LLM providers:
- **OpenAI:** `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`
- **Anthropic:** `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- **Google:** `gemini-1.5-pro`, `gemini-1.5-flash`

### 2. Deep Diagnostic Extraction
The agent does more than summarize. It is strictly prompted by a robust JSON schema to systematically analyze "Friction Notes" and explicitly rip out:
- High-level executive summaries of the day's performance.
- Concrete blocks of completed and missed targets.
- Nuanced reasons / lessons learned on why specific objectives structurally failed.
- A hyper-actionable checklist of protocols for the user's next day.

### 3. Visual "Daily Velocity" Analytics
The Streamlit frontend utilizes **Plotly Express** to render an automated pie chart mapping your objective success rate. Watching your "Daily Velocity" (Completed / Total Goals) visually improves positive reinforcement loops and exposes operational blindspots.

---

## 🚀 Installation & Setup

### Requirements
- Python 3.9+
- A valid API Key (OpenAI, Anthropic, or Google)

### 1. Install Dependencies
Run the following command to download the parsing and frontend engines:
```bash
pip install streamlit openai litellm pandas plotly
```

### 2. Run the Command-Line Agent (Base)
You can optionally run the engine headlessly without the dashboard. Provide a `day.txt` file structured with your objectives and run:
```bash
python agent.py
```
This drops the calculations into `reflection.json` and `reflection.txt`.

### 3. Launch the Premium Dashboard (`app.py`)
Start the visual Streamlit engine to leverage intuitive copy/pasting, live tabular visualizers, and the multi-provider neural toggle!
```bash
python -m streamlit run app.py
```

---

## 💻 Tech Stack
- **Frontend / UI:** Streamlit (Custom Premium CSS injection)
- **Neural Routing:** `litellm` (LLM-Agnostic Processing)
- **Core Intelligence:** Base GPT Prompting Schema
- **Data Rendering:** Pandas DataFrames, Plotly Express
