# 🔔 PingCraft AI | Smart Notification Engine

**PingCraft AI** is a hyper-efficient algorithmic scheduling and notification engine designed to automate your personal reminder spacing. 

Instead of manually setting alarms for every task, you supply a manifest of deadlines and priority levels. PingCraft mathematically clusters and calculates *exactly* when you need to be warned to ensure you never miss a deadline without overwhelming you with notification spam.

---

## ✨ Enterprise Features

### 1. ⚡ Algorithmic Warning Calculation
A premium **Streamlit** Web Interface (`app.py`) built to visualize your impending task load.
- **Dynamic Tuning:** Adjust the underlying priority math on-the-fly via the sidebar. Need 14-day warnings instead of 7-day warnings for high-priority items? Type it in and watch the engine recalculate every task instantly.
- **Visual Notification Density:** The built-in **Plotly** engine generates an interactive timeline graph. This allows you to visually spot "Notification Fatigue" clusters days before they happen.

### 2. 🔌 Automation-Ready Architecture
Outputs structured data that can easily map to enterprise API workflows.
- **Twilio & Zapier Ready:** The backend automatically compiles a strictly typed `reminders.json` payload containing the exact ISO string dates, contexts, and string payloads. You can pipe this directly into SMS architectures or Email dispatchers.
- **Executive Readouts:** Generates clean, human-readable schedule text files that you can dump directly into your daily note system (Obsidian, Notion, Logseq).

---

## ⚙️ How It Works (The Core Logic)

Unlike LLM-based agents, PingCraft relies on a deterministic mathematical algorithm to space out its alerts. Here is the step-by-step breakdown of the `agent.py` logic:

### Step 1: Ingestion & Normalization
The engine loads the raw `.csv` task manifest and standardizes it. It converts deadline strings (e.g., `2026-03-25`) into strict underlying Python `datetime` objects for mathematical comparison.

### Step 2: The Spacing Matrix (PRIORITY_RULES)
The core logic relies on a dictionary mapping called the Spacing Matrix. By default, it looks like this:
```python
PRIORITY_RULES = {
    "high": [7, 3, 1, 0],  # Warn 7 days prior, 3 days prior, 1 day prior, and day of
    "medium": [3, 1],      # Warn 3 days prior, 1 day prior
    "low": [1]             # Warn only 1 day prior
}
```

### Step 3: Trigger Calculation
The agent iterates linearly over your parsed tasks:
1. It cross-references the task's text priority (`high`, `medium`, `low`) with the Spacing Matrix.
2. For each integer in the matrix array, it calculates a `timedelta(days=X)`.
3. It subtracts that `timedelta` from the task's strict deadline.
4. **The Safety Valve:** Before it logs the alert, it verifies `reminder_date >= date.today()`. This prevents the engine from generating a massive backlog of ghost notifications for tasks that were assigned months ago.

### Step 4: Output Synthesis
All valid calculated reminders are grouped into a single array, sorted chronologically, and written strictly to `reminders.json` and a human-readable `reminders.txt`.

---

## 🚀 Installation & Setup

### Requirements
- Python 3.9+
- *(Note: PingCraft AI relies purely on CPU calculation logic. It does **not** require an OpenAI API Key to generate schedules!)*

### 1. Install Dependencies
Run the following command to download the plotting and frontend engines:
```bash
pip install streamlit pandas plotly
```

### 2. Prepare Your Manifest
The system expects a `tasks.csv` file inside the root folder (or you can upload one dynamically via the UI).
Ensure it matches exactly this schema:

| task | deadline | priority | context |
| :--- | :--- | :--- | :--- |
| Submit tax documents | 2026-04-15 | high | personal |
| Follow up with vendor | 2026-03-22 | medium | work |

### 3. Run the Application
Start the powerful Streamlit engine from your terminal:
```bash
python -m streamlit run app.py
```
*Note: The system will automatically open a local server at `http://localhost:8501` to view your dashboard.*

---

## 💻 Tech Stack
- **Frontend / UI:** Streamlit (Custom Premium CSS injection)
- **Data Parsing:** Native Python `csv`, `json`, `datetime`
- **Analytics:** Pandas DataFrames, Plotly Express Bar Clustering


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
