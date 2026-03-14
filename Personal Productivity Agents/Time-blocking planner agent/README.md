# ⏳ ChronoBlock AI | Time-Boxing Engine

**ChronoBlock AI** is an algorithmic daily scheduling engine. It ingests your raw task list, calculates explicit priorities against task durations, and programmatically packs them into contiguous blocks of time that fit perfectly within your working hours.

If you have assigned yourself too much work for a single day, ChronoBlock will slice off the lowest priority targets and push them to the **Overflow Buffer**, ensuring your core daily timeline remains completely realistic.

---

## ✨ Enterprise Features

### 1. Mathematical Task Stacking
The Web Application (`app.py`) algorithmically sorts the target queue. 
- High priority, massive tasks are slotted directly into the start of your day for maximum focus.
- A built-in "Context-Switch Buffer" automatically injects padding (default 10 mins) between heavy tasks so your schedule doesn't collapse if a meeting runs over. 
- **Dynamic Tuning:** Adjust your absolute Operating Hours and Buffer Padding live through the UI sidebar, and watch the entire timeline rewrite itself to match.

### 2. Plotly Gantt Scheduling
Built-in data visualization using Plotly strips the raw JSON array and converts it into a visual **Gantt Chart timeline**. This allows you to visually audit your entire day at a glance, color-coded by task urgency.

### 3. API-Ready Output Structuring
Download the resulting architecture via the `💾 Export Hub`.
- **JSON Payload:** Ready to be consumed by automation hooks (Zapier/Make) to natively pipe the blocks into Google Calendar API.
- **Human Markdown:** A clean, markdown-ready block for copy-pasting directly into Slack updates, Notion, or Obsidian daily logs.

---

## 🚀 Installation & Setup

### Requirements
- Python 3.9+
- *(Note: ChronoBlock AI strictly relies on deterministic CPU algorithms. It does **not** mandate an OpenAI API key or LLM connection!)*

### 1. Install Dependencies
Run the following terminal command to provision the frontend UI:
```bash
pip install streamlit pandas plotly
```

### 2. Run the Headless Engine (CLI)
You can calculate schedule permutations directly in the terminal without a UI layer. The system reads from `tasks.csv` out of the box.
```bash
python agent.py
```
Outputs are written to `schedule.json` and `schedule.txt`.

### 3. Launch the Premium Dashboard (`app.py`)
To use the live Gantt visualizers and realtime algorithm adjustments, initialize the powerful Streamlit GUI:
```bash
python -m streamlit run app.py
```

---

## 💻 Tech Stack
- **Frontend / UI:** Streamlit (Custom Premium CSS injection)
- **Mathematical Processing:** Native Python dictionaries, lists, and `datetime` manipulation.
- **Data Rendering:** Pandas DataFrames
- **Charting Engine:** Plotly Express Timeline / Gantt
