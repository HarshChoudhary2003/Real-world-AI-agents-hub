# 🧬 NeuralData AI v2.0: Advanced CSV Batch Integrity Matrix

A powerhouse for CSV data cleaning and integrity auditing that leverages **Pandas** and **LLMs (OpenAI, Anthropic, Groq)** for deep semantic refinement.

---

## ⚡ Features (V2.0 Matrix)
- **📂 Neural Batch Matrix**: Upload multiple CSV files at once. Generate individual and aggregate health scores across entire datasets.
- **🛠️ Custom Neural Rules**: Inject logic directives directly from the UI or code.
    - **Range**: Ensure numerical values (e.g., age) fall within specific bounds.
    - **Regex**: Enforce pattern matching for emails, phone numbers, or IDs.
    - **Not Null**: Zero-tolerance policy for missing values in critical columns.
- **🦾 Semantic Repair**: Beyond simple regex. Uses LLMs to fix typos, standardize inconsistent categories, and resolve logical gaps.
- **🚨 Intelligent Anomaly Detection**: Identifies out-of-range numerical values and flags them for review.
- **💎 Premium Dashboard v2.0**: Enhanced Glassmorphism UI with Aggregate Health Gauges, Logic Injection panels, and interactive Batch Audit matrices.

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   cd csv-data-cleaning-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Keys**:
   Create a `.env` file or provide keys directly in the Streamlit Sidebar:
   ```env
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

---

## 🚀 Usage

### Option 1: Premium Dashboard (Recommended)
Run the Streamlit app to access the neural interface:
```bash
streamlit run app.py
```

### Option 2: CLI Batch Mode
Run the core engine locally on current directory CSVs:
```bash
python agent.py
```

---

## 🧪 Validation Matrix
Check the following in your audit:
- **Duplicates**: Perfect de-duplication of similar rows across files.
- **Rule Violations**: See exact rows and columns failing your custom logic.
- **Aggregate Score**: Monitor the health of your entire data warehouse from one gauge.

---
*Built with ❤️ by the NeuralData AI Team*
