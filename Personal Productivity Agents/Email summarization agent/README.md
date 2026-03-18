# 📧 MailMind AI | Smart Summarization Engine

**MailMind AI** is a cutting-edge Enterprise Email Intelligence application. Turn pages of stressful, long-winded email threads into concise, actionable data points in milliseconds.

Say goodbye to manual reading and highlighting. Paste an email string or upload an `.eml` file, and the neural engine handles the precise extraction of priorities, deadlines, and action items.

---

## ✨ Enterprise Features

### 1. ⚡ Live Processing Engine
An intuitive, beautiful web interface built with **Streamlit** that makes digesting information effortless.
- **Deep Synthesization:** Input raw text and immediately extract a 2-3 sentence *Executive Summary*.
- **Action Mapping:** Extracts specific To-Do list items formatted as checkboxes so you know exactly who needs to do what.
- **Urgency Engine:** Dynamically assigns a heatmpped *(Red/Orange/Blue)* urgency level to the email subject.
- **Timeline Parser:** Extracts any mentioned dates and maps them out in an isolated "Deadlines" view.

### 2. 🔌 Flexible AI Backend
Powered naturally by OpenAI Models, dynamically configurable per user.
- **Model Toggling:** Switch dynamically between `GPT-4o`, `GPT-4o-Mini`, or `GPT-3.5-Turbo` within the UI depending on the logical rigor required.
- **Structured JSON Adherence:** The backend script forces exactly typed JSON schemas, stripping out markdown hallucinations automatically so developer API integrations never break.

### 3. 💾 Zero-Friction Exports
Want to pull this into Notion, Jira, or a Google Doc?
- **Download JSON:** Grabs the perfectly formatted raw JSON string output. 
- **Download TXT:** Grabs an automated "Daily Briefing" style list, ready to copy-paste.

---

## 🛠️ How it Works (Under the Hood)

The core `agent.py` script instructs the LLM via strict `SYSTEM_PROMPTS` to act exclusively as an extraction engine:

```json
// The exact output schema enforced on the AI Engine:
{
  "summary": "String",
  "key_points": ["List of strings"],
  "action_items": ["List of strings"],
  "deadlines": ["List of strings"],
  "urgency": "Low | Medium | High"
}
```

The script protects against markdown artifacts by manually peeling ````json` code blocks and utilizes OpenAI's `response_format={"type": "json_object"}` safety wrapper to guarantee parsing stability.

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
Navigate to the project directory and invoke the Streamlit server:
```bash
cd "Email summarization agent"
streamlit run app.py
```
*Note: This will instantly open a local web server at `http://localhost:8501`. If it's your first time, simply paste your Open AI API key into the sidebar when it loads.*

---

## 🧠 Why we built this
Modern professionals spend over 28% of their day reading and processing email. **MailMind AI** is designed to slice that workload precisely in half. Instead of hunting through long chains for that single date or to-do list, this tool acts as your personal Chief of Staff—serving only what matters.


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
