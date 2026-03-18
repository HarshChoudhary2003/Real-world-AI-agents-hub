# 🎯 SWOT Analysis Agent (Advanced)

An AI-powered Strategic Planning Agent that transforms organizational context into a comprehensive SWOT-to-TOWS matrix. Built with Python and OpenAI GPT-4o-mini.

## 🚀 Features

- **Deep Contextual Analysis**: Goes beyond simple bullet points to provide impact assessment.
- **TOWS Matrix Generation**: Automatically derives strategic actions (SO, WO, ST, WT strategies) based on SWOT findings.
- **Premium Streamlit UI**: A professional-grade dashboard for interactive analysis.
- **Structured Outputs**: Generates both machine-readable `swot_analysis.json` and human-readable `swot_analysis.txt`.
- **Impact Scoring**: Categorizes factors by Impact (High/Medium/Low) for better prioritization.

## 📁 Project Structure

```text
swot-analysis-agent/
├── agent.py         # Core logic and OpenAI integration
├── app.py           # Streamlit Dashboard UI
├── input.txt        # Sample context for the agent
├── requirements.txt # Project dependencies
├── swot_analysis.json # Latest generated JSON result
└── swot_analysis.txt  # Latest generated TXT report
```

## 🛠️ Setup & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file or set your environment variable:
```bash
OPENAI_API_KEY=your_key_here
```

### 3. Run the CLI Version
```bash
python agent.py
```

### 4. Run the Streamlit UI
```bash
streamlit run app.py
```

## 🧠 Strategic Framework
This agent doesn't just list factors; it uses the **TOWS Matrix** framework to help organizations:
- **SO (Strengths + Opportunities)**: Use internal strengths to capitalize on external opportunities.
- **WO (Weaknesses + Opportunities)**: Mitigate internal weaknesses by using external opportunities.
- **ST (Strengths + Threats)**: Leverage internal strengths to buffer against external threats.
- **WT (Weaknesses + Threats)**: Defensive strategies to prevent weaknesses from being exploited by external threats.
