# 📅 SyncGuard AI | Enterprise Calendar Resolution

**SyncGuard AI** is a state-of-the-art intelligent scheduling tool designed for high-performance teams, Executive Assistants, and professionals. 
Instead of visually scanning endless blocks of messy calendar times, SyncGuard mathematically audits your week to detect direct overlaps, enforce critical padding logic (meeting buffers), and output AI-assisted resolutions based entirely on priority and flexibility.

Say goodbye to manual double-booking panics or burnt-out back-to-back meeting strings without biological breaks. 

---

## ✨ Enterprise Features

### 1. 🚨 Conflict Resolver Dashboard
An ultra-premium web interface built with **Streamlit** that visualizes your entire calendar health at a single glance.
- **Topographical Detection:** Not just direct overlaps—SyncGuard alerts you if two meetings are booked closer to each other than your allowed threshold (e.g., 10 minutes).
- **Intelligent Resolvers:** An embedded heuristic engine automatically decides *how* to fix the calendar using flexibility rules:
    - *"Reschedule 'Code Review' (Low Priority) out of 'Client Call' (High Priority)."*
    - *"Requires human decision (Two high priority strict boundaries)."*
- **Severity Indexing:** Conflicts are automatically classified as `High` (involving protected events) or `Medium` severity.

### 2. 📈 Visual Plotly Timeline
*See logjams before they happen.*
- **Topographical Gantt Charts:** Built strictly via **Plotly Express**, this chart turns your boring calendar CSV into a clean left-to-right visualization to easily spot clustering behavior.
- **Color-Coded Priority:** Red chunks for strictly protected High-priority execution blocks, Blue chunks for lower priority, malleable time.

### 3. 💾 Automated Data Exports
Designed to plug right back into corporate infrastructures. 
- **JSON Structured Data:** Generate strict JSON arrays mapping overlapping conflicts and exact suggestions via the integrated GUI.
- **Human C-Suite TXT:** Generates an automated readable ".txt" briefing perfectly formatted to send via Slack, Teams, or Email.

### 4. 🎛️ Dynamic Parameter Sandbox
Test multiple workflow constraints in real-time.
- **Adjustable Buffer Constraints:** Need 15 minutes between sales calls but only 5 minutes between internal syncs? Adjust the buffer slider in the sidebar and instantly watch the dashboard recalculate and re-classify buffer violations.
- **Hot-swappable Datasets:** Native drag-and-drop CSV handler lets you analyze different team members' schedules in seconds without rewriting source code.

---

## ⚙️ How It Works (The Core Logic)

The underlying cognitive engine (`agent.py`) systematically parses and grades every meeting mathematically. Here is the step-by-step breakdown of the agent's logic:

### Step 1: Ingestion & Normalization
The system ingests the raw `.csv` calendar schedule and standardizes it into deeply typed `dataclass` objects. It processes text deadlines into `datetime` values and maps human text (`High`/`Medium`/`Low`) into computational integers (`3`/`2`/`1`). Critically, it sorts all events sequentially by their starting timestamps.

### Step 2: Anomaly Detection (The Sandbox)
The engine iterates linearly through the sorted calendar. For every two consecutive events (`event_a` and `event_b`), it checks two boolean triggers:
* **The Overlap Trigger:** If `event_a.end > event_b.start` evaluates to `True`, it flags an immediate, hard Double-Booking conflict.
* **The Buffer Trigger:** It calculates the delta (`event_b.start - event_a.end`). If this delta is less than the user's `BUFFER_MINUTES` threshold (e.g., `< 10 minutes`), it flags a Buffer Violation.

### Step 3: Heuristic Resolution
Once a conflict is flagged, the agent compares the metadata of the two clashing events to generate an automated recommendation:
1. **Priority Trumping:** If `event_a` has higher priority and `event_b` is marked `flexible=True`, the agent states: `"Reschedule event_b"`.
2. **Mutual Malleability:** If both events are `flexible=True`, it suggests: `"Shorten or reschedule one event"`.
3. **The Deadlock Clause:** If neither event is flexible (or they hold equally high priority), the engine refuses to guess and triggers a strict Escalation response: `"Requires human decision"`.

### Step 4: Output Synthesis
The calculated logjams are compiled into an array, assigned Severity Ratings based on the involved priorities, and mapped precisely into both a beautiful UI dashboard and exportable programmatic JSON payloads.

---

## 🚀 Installation & Setup

### Requirements
- Python 3.9+

### 1. Install Dependencies
Run the following command to download the plotting and frontend engines:
```bash
pip install streamlit pandas plotly
```

### 2. Prepare Your Calendar (Optional)
The system reads a local `calendar.csv` file by default (or you can drag-and-drop upload a new one through the Web UI). 
Ensure it matches exactly this schema:

| title | start_time | end_time | priority | type | flexible |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Team Sync | 2025-12-23 09:00 | 2025-12-23 10:00 | high | meeting | no |
| Lunch Break | 2025-12-23 12:30 | 2025-12-23 13:00 | low | personal | yes |

### 3. Run the Application
Start the powerful Streamlit engine from your terminal:
```bash
python -m streamlit run app.py
```
*Note: The system will automatically open a local server at `http://localhost:8501`.*

---

## 💻 Tech Stack
- **Frontend / UI:** Streamlit (Custom Premium CSS injection)
- **Data Parsing:** Native Python `csv`, `dataclasses`, `datetime`
- **Analytics:** Pandas DataFrames, Plotly Express Gantt Charts

Take control of your time proactively. With **SyncGuard AI**, your calendar is computationally protected.


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
