# 📄 ResumeAI Pro: The Ultimate Resume Optimization Engine

Welcome to **ResumeAI Pro (Enterprise Edition)**, a premium AI-powered tool designed to instantly restructure and rewrite resumes to perfectly match any target job description. Built for career coaches, recruiters, and ambitious job seekers, this agent ensures maximum Applicant Tracking System (ATS) compatibility while highlighting measurable impact.

---

## 🔥 Why This Product is a Game-Changer

Forget standard resume builders that just offer templates. **ResumeAI Pro** actually *does the heavy lifting* of rewriting content:

*   **⚡ AI-Driven Rewriting:** Automatically rewrites experience bullets to focus on impact, metrics, and outcomes.
*   **🎯 Laser-Targeted Alignment:** Analyzes the target Job Description (JD) and flawlessly maps your existing experience to the employer's needs.
*   **🤖 ATS Mastery:** Extracts the highly specific keywords and skills required by modern ATS filters, ensuring your resume gets read by a human.
*   **🛡️ Factually Accurate:** Strict systemic prompting ensures the AI *never* invents experience—it only enhances the presentation of what you already have.
*   **💎 Premium Streamlit UI:** A sleek, dark-mode, enterprise-ready web interface perfect for white-labeling or selling as a SaaS product.

---

## 🛠️ Features Included

1.  **Dual Pane Interface:** Intuitive side-by-side pasting of your raw resume and the target JD.
2.  **Instant Content Generation:** Returns an Executive Summary, ATS-Optimized Skills, and Impact-Driven Experience bullets.
3.  **Multiple Export Formats:** 
    *   **Formatted Preview:** Beautiful UI display mimicking a real document.
    *   **Raw JSON Data:** Perfect for developers wanting to integrate this agent into a larger pipeline or SaaS application.
    *   **Download Options:** One-click download of `.txt` or `.json` assets.
4.  **Custom Key Management:** Allows users to input their own OpenAI API keys securely within the session.

---

## 🚀 How to Run Locally

### Prerequisites
*   Python 3.9+
*   An OpenAI API Key

### Installation

1. Clone or download this repository.
2. Navigate to the project directory:
   ```bash
   cd "Resume optimization agent"
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Or just run: `pip install streamlit openai python-dotenv`)*

### Starting the Application

Run the following command to launch the premium dashboard:

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 💸 Monetization Strategy

Because of its polished UI and highly valuable output, **ResumeAI Pro** is primed for monetization:

1.  **B2C SaaS:** Charge users a monthly subscription (e.g., $9/month) for unlimited resume tailoring.
2.  **B2B Tool:** Sell the script and UI to career counseling agencies or university career centers.
3.  **Lead Magnet:** Offer 1 free optimization run to capture high-intent emails for high-ticket coaching services.
4.  **API Integration:** Use the core logic (`agent.py` or the JSON output of `app.py`) as a backend microservice for a larger HR tech platform.

---
*Built with modern Streamlit, Python, and OpenAI's GPT models.*


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
