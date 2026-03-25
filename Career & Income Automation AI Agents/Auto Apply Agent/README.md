# 🤖 Auto Apply Agent

The **Auto Apply Agent** is a sophisticated multi-agent orchestrator that connects all previous agents in the **CareerOS** suite into a single, high-impact application workflow.

## 🧬 Career Intelligence Swarm: Workflow
1.  **Resume Optimizer Agent**: Dynamically reshapes your resume text to match the core keywords and requirements of the target Job Description.
2.  **Cover Letter Agent**: Crafts an impact-driven, personalized cover letter based on the *optimized* resume.
3.  **Analyst Agent**: Calculates a final match score and provides a summary of the alignment.
4.  **Assisted Apply Mode**: Opens the application page directly and prepares all documents for instant submission.

## 🛠️ Multi-Agent Architecture
This agent utilizes a **Pipeline Pattern** to ensure each step builds on the previous agent's intelligence:
- Imports logic from `Resume Optimizer Agent` and `Cover Letter Generator Agent`.
- Synchronizes output through the `workflow.py` brain.
- Supports any AI model via common LiteLLM routing.

## 🚀 Quick Launch
```bash
pip install -r requirements.txt
streamlit run app.py
```
