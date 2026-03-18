# ✉️ CoverLetter Pro: The Omni-Model Pitch Engine

Welcome to **CoverLetter Pro (Enterprise Edition)**, an AI-powered drafting agent designed to craft perfectly tailored, human-sounding cover letters instantly. It uses cutting-edge LLMs to analyze a job description and draw a direct narrative bridge to your past experience—without ever sounding like a generic AI "bot".

---

## 🔥 Why This Product Stands Out

Generic cover letters get thrown out. Over-the-top AI cover letters get mocked. **CoverLetter Pro** threads the needle:

*   **🎙️ Human-Tone Tuning:** Systemically tuned to avoid "ChatGPT-isms" (e.g., *tapestry, delve, testament*), keeping the language grounded and confident.
*   **🧠 Omni-Model Integration:** Features built-in `litellm` support. Seamlessly switch between Anthropic Claude 3.5 Sonnet (the absolute best at natural writing), OpenAI GPT-4o, Google Gemini, and Groq on the fly.
*   **🎯 Laser-Targeted Drafting:** Automatically isolates the implicit pain points in the Job Description (JD) and addresses them using your precise background.
*   **⏱️ Concise Structure:** Strictly follows a high-conversion 3-to-4 paragraph rule (The Hook, The Proof, The Close).
*   **💎 Premium Streamlit UI:** A gorgeous, red-gradient dark-mode UI with explanatory architecture cards, perfect for selling or showing to users.

---

## 🛠️ Features Included

1.  **Dual Pane Drafting Space:** Intuitive side-by-side pasting of your experience bullets and the target vacancy.
2.  **Smart Field Extraction:** The AI automatically extracts the "Company Name" and "Role Name" from messy JDs.
3.  **Multiple Export Formats:** 
    *   **Formatted Letter:** Beautiful UI display mimicking a clean document.
    *   **Raw JSON Data:** Perfect for developers building automated job-application pipelines.
    *   **Download Options:** One-click download of `.txt` or `.json`.
4.  **Universal API Key Validation:** Secure, local input for whichever AI provider the user decides to choose.

---

## 🚀 How to Run Locally

### Prerequisites
*   Python 3.9+
*   An API Key (Anthropic, OpenAI, Google, or Groq)

### Installation

1. Clone or download this repository.
2. Navigate to the project directory:
   ```bash
   cd "Cover letter writing agent"
   ```
3. Install the required dependencies:
   ```bash
   pip install litellm streamlit openai python-dotenv
   ```

### Starting the Application

Launch the premium Streamlit dashboard using:

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 💸 Monetization Strategy

**CoverLetter Pro** is an excellent companion product to Resume Optimizers, and can be monetized easily:

1.  **AI Bundle SaaS:** Bundle this with the Resume Optimization app and charge a monthly subscription for full career-stack access.
2.  **Automated Application Pipelines:** Use the raw `json` payload to feed an RPA bot that automatically finds jobs, writes the letter, and applies.
3.  **Lead Generation Tool:** Host a free version on a blog to drive traffic to high-ticket interview coaching businesses.

---
*Built with modern Streamlit, Python, and the LiteLLM Universal Gateway.*


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
