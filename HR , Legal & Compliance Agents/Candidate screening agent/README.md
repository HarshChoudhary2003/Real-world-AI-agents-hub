<div align="center">

# 🔎 ScreenGenius AI
### Unbiased Algorithmic Candidate Profiling System

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Litellm](https://img.shields.io/badge/Powered_by-LiteLLM-10b981.svg?style=for-the-badge&logo=openai)](https://litellm.ai/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

<br>

<img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1000&q=80" alt="ScreenGenius AI" style="border-radius: 12px; box-shadow: 0 4px 30px rgba(0,0,0,0.5);">

<br>

**Strips away conscious and unconscious bias, focusing strictly on hard metric matches.**

</div>

---

## ⚡ Overview

**ScreenGenius AI (Candidate Screening Agent)** performs highly structured, objective analysis mapping raw candidate resumes directly against formal job requisitions. It evaluates candidates explicitly on what they provide, outputting clear lists of *Matched* vs *Missing* variables along with a synthesized diagnostic score.

Crucially: this application acts purely as an assistant. It does not output "Hired / Rejected", but rather surfaces actionable talent intelligence for human hiring partners.

## 🚀 Key Features

*   **🛡️ Bias Neutralization:** Instructed at the neural level to completely ignore protected attributes and formatting tricks.
*   **📊 Metric Scoring:** Generates a 0-100 `qualification_score` quantifying the intersection overlap between requirements and experience.
*   **💠 Executive HR Dashboard:** Dual-pane comparison layout mapped directly into an Emerald/Titanium UI scheme optimized for Human Resource workflows.
*   **🧠 Provider Agnostic:** Progressive input structures allow scaling to enterprise local boundaries via Ollama/Grok/Antrhopic integrations.

## ⚙️ Quick Start

### 1. Execute Headless Screen
Feed `job.txt` and `resume.txt` inside the folder to the core parser:
```bash
cd "HR , Legal & Compliance Agents/Candidate screening agent"
python agent.py
```

### 2. Enter Visual Auditing
```bash
streamlit run app.py
```
*(Starts on local Streamlit defaults, likely 8501-8510 depending on availability).*

---

<div align="center">
<i>Built with 🛡️ by the Post-SaaS Economy Framework. Part of the Real-World AI Agents Hub.</i>
</div>
