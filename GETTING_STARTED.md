# 🚀 Getting Started with Agent OS

Welcome to the future of autonomous intelligence. This guide will walk you through setting up the **Real-world AI Agents Hub** and launching your first premium agent.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.10 or higher**
- **Git**
- **Virtual Environment Tool** (e.g., `venv` or `conda`)

---

## 🛠️ Installation

### 1. Clone the Massive Core
```bash
git clone https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub.git
cd Real-world-AI-agents-hub
```

### 2. Setup Virtual Environment
**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Global Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Most agents require API keys to function. Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your credentials:
```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
# Optional:
GROQ_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
```

---

## 💠 Launching the System

### Option A: The Centralized Hub (Recommended)
Launch the **Master Dashboard** to explore and run all 128 agents from a single interface.
```bash
streamlit run master_hub.py
```

### Option B: Individual Agent Launch
Navigate to any agent folder and launch its specific dashboard.
```bash
cd "Personal Productivity Agents/daily-priority-agent"
streamlit run app.py
```

---

## 🏗️ Building Your Own Agent

Want to contribute? Follow these steps:
1. **Choose a Category:** e.g., `Business Operations Agents`.
2. **Create a Folder:** `my-new-awesome-agent`.
3. **Draft the Logic:** Create `core.py` for the agent logic.
4. **Design the UI:** Create `app.py` using our custom Glassmorphism styles.
5. **Document:** Add a local `README.md`.

Refer to [CONTRIBUTING.md](./CONTRIBUTING.md) for our "Elite UI/UX" standards.

---

## 🆘 Troubleshooting

- **Dependency Conflicts:** If you encounter errors, try installing requirements within the specific agent folder.
- **API Errors:** Ensure your `.env` keys are correct and you have sufficient credits.
- **UI Issues:** Make sure you are using a modern browser (Chrome, Edge, or Safari).

---

> [!NOTE]
> For deep technical details, check out [ARCHITECTURE.md](./ARCHITECTURE.md).
