# 🎤 AI Interview Simulator Agent

The **AI Interview Simulator** provides a high-fidelity, interactive environment for technical and behavioral interview preparation, part of the **CareerOS** suite.

## 🧠 Core Intelligence: The Feedback Loop
Unlike static generation, this agent uses a **closed-loop simulation**:
1.  **Question Generator Agent**: Synthesizes a realistic technical question based on your target **role**, desired **difficulty**, and provided **resume context**.
2.  **Evaluator Agent**: Acts as a Lead Hiring Manager, analyzing your response for accuracy, clarity, and depth.
3.  **Benchmarking**: Provides an "Ideal Answer" to compare your performance against the elite 1% of candidates.

## 🛠️ Features
- **Stateful Iteration**: Generate questions, answer them, and receive feedback per-round.
- **Multi-Model Support**: Powered by LiteLLM—switch between OpenAI, Gemini, or Groq for different interviewing "personalities".
- **Quantitative Metrics**: Real-time hiring score (0-10) and PASS/REJECT status tracking.
- **Actionable Advice**: Direct feedback on strengths and weaknesses with specific improvement steps.

## 🚀 Quick Launch
```bash
pip install -r requirements.txt
streamlit run app.py
```
