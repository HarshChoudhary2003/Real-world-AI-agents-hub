# 🔥 StreakForge AI | Algorithmic Habit Tracker

**StreakForge AI** is an incredibly fast, pure-math algorithmic tracking engine. It mathematically calculates the consistency vector, exact current streak, and fail-rate of your targeted daily habits based simply on a raw CSV log file.

Instead of managing manual calendars or clicking UI elements, dump your raw log payloads into this engine and let it parse the operational velocity of your lifestyle.

---

## ✨ Enterprise Features

### 1. Mathematical Diagnostics
The engine processes rows of chronological `yes/no` logs and runs them through a deterministic loop:
- **Baseline Rule:** If a habit's density/consistency over its tracked lifetime drops below `75%`, the engine flags it as "Requiring Reinforcement" and generates a system recommendation to reduce difficulty mapping or change environment triggers.
- Automatically isolates the missed days into an array for easy debugging of personal "failure patterns".

### 2. Streamlit Analytics Visualizer
The Enterprise UI (`app.py`) parses the logic directly into visual arrays.
- **Progression Optics:** Built natively on `plotly.express`, it renders a scatter plot mapping the precise days you completed or failed tasks, acting like a GitHub-commit heatmap for your life.

### 3. Zapier / Workflow Output
Produces direct JSON arrays that can be easily wired into automation platforms. (E.g. IF a habit drops below 75%, trigger a webhook to email you a warning).

---

## 🚀 Installation & Setup

### Requirements
- Python 3.9+
- *(Note: StreakForge AI is an LLM-Agnostic, deterministic mathematical codebase that works safely without API keys.)*

### 1. Install Dependencies
Run the following array of installations to spin up the local graphical dashboard:
```bash
pip install streamlit pandas plotly
```

### 2. Run Headless
Provide your baseline `habits.csv` and execute natively from the CLI:
```bash
python agent.py
```
This drops the tracking telemetry straight into `habits.json` and human-readable `habits.txt`.

### 3. Launch the Premium Dashboard (`app.py`)
To view the Heatmap/Scatter timelines:
```bash
python -m streamlit run app.py
```

---

## 💻 Tech Stack
- **Frontend / UI:** Streamlit (Custom Premium CSS injection)
- **Mathematical Processing:** Native Python `collections.defaultdict` mapping
- **Data Rendering:** Pandas DataFrames
- **Charting Engine:** Plotly Express (Bar and Scatter Plot)


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
