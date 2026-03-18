# 📋 AgendaCraft AI | Intelligent Meeting Architect

**AgendaCraft AI** automates the most tedious part of meeting management: translating loose ideas, rough duration limits, and scattered participant lists into a perfectly structured, time-boxed, outcome-driven agenda.

Instead of staring at a blank document trying to divide 60 minutes between 3 departments, simply input your constraints. The neural engine creates the timeline, allocates the correct duration chunks, and automatically assigns ownership of each talking point.

---

## ✨ Enterprise Features

### 1. 🚀 Real-Time Architecture Engine
A beautiful **Streamlit** Web Interface that feels like an enterprise software solution.
- **Dynamic Content Ingestion:** Paste blocks of raw constraints ("Needs to be 60 mins, Mark is doing the intro, we need to decide on Q3 budget") or upload unformatted `.txt` files directly.
- **Automated Time-Boxing:** The AI enforces strict mathematics. It generates individual sub-topics that sum up precisely to your target meeting duration. It even includes a UI warning if it detects a math overflow error.
- **Auto-Assignment Logic:** The agent reads your participant list and intuitively assigns "Owners" to specific discussion blocks based on the required expertise of the topic.

### 2. 🔌 Flexible AI Backend
Powered by OpenAI Models to ensure deep contextual reasoning.
- **Model Toggling:** Easily swap between `GPT-4o` (for highly complex, multi-team alignment meetings) and `GPT-4o-Mini` (for standard weekly syncs) right from the frontend sidebar.
- **Failsafe JSON Strictness:** The backend employs OpenAI's dedicated `response_format={"type": "json_object"}` wrapper and manual markdown-stripping, ensuring the payload never breaks when plugged into API endpoints.

### 3. 💾 Zero-Friction Exports
Push the generated logic out into the real world immediately.
- **Machine-Readable JSON:** Get the strict object representation to push directly into internal corporate tools or a Calendar API payload.
- **Executive-Ready TXT:** Download a perfectly formatted, printable Daily Briefing. Copy-paste this right into the Google Calendar / Outlook invite block.

---

## 🛠️ How it Works (Under the Hood)

The core `agent.py` logic relies heavily on "System Prompting" to enforce rules. Here is roughly what the backend demands from the AI:

1. **Duration Law:** "Agenda must fit within the provided duration."
2. **Objective Alignment:** "Focus strictly on the provided objective."
3. **Data Schema Enforcement:** The LLM is isolated within this return map:
```json
{
  "meeting_title": "",
  "objective": "",
  "total_duration_minutes": 0,
  "agenda": [
    {
      "topic": "",
      "time_minutes": 0,
      "owner": "",
      "outcome": ""
    }
  ]
}
```

---

## 🚀 Installation & Setup

### Requirements
- Python 3.9+
- An Active OpenAI API Key (inputted directly through the frontend GUI)

### 1. Install Dependencies
```bash
pip install streamlit openai
```

### 2. Fire up the Interface
Navigate to the project directory and invoke the local web engine:
```bash
cd "Meeting agenda generator agent"
streamlit run app.py
```
*Note: This instantly opens your UI at `http://localhost:8501`. Paste your OpenAI key into the sidebar to activate the extraction engine.*

---

**Meetings cost time and money. AgendaCraft AI ensures you never waste either.**


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
