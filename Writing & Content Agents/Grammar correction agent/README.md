# ✍️ GrammarPro | Advanced AI Editing Engine

Welcome to **GrammarPro**, an elite-tier AI text editor that doesn't just catch typos, but completely restructures your prose while preserving your unique voice. Built with an incredibly powerful visual architecture, this application acts as your personal "Grammarly on steroids."

---

## 🔥 Why This Product is Unrivaled

Most grammar correction tools are rigid and over-corrective. GrammarPro utilizes state-of-the-art LLM capabilities to understand *context*, intent, and tone:

*   **🔍 The Diff Visualizer:** Perhaps the most powerful feature. Don't just trust the AI blindly. The app generates a beautifully styled inline Diff (red for deletions, green for insertions) showing you exactly *what* changed and *why*.
*   **🎛️ Granular Control:**
    *   **Audience Targeting:** Tell the AI if you are writing for an Academic journal, a Professional business client, or a Casual internet audience.
    *   **Editing Aggressiveness:** Select whether you just want basic typos fixed ("Light Verification") or deeply awkward sentences aggressively rewritten for punchiness ("Heavy Edit").
*   **📝 Editor Diagnostics:** The AI provides a dynamically generated list of "Correction Notes," explaining its stylistic choices directly to the user so they can improve their writing over time.
*   **🧠 Omni-Model Integration:** Uses `litellm` to seamlessly route prompts to Anthropic Claude 3.5 Sonnet (the absolute gold-standard for human editing), OpenAI GPT-4o, Google Gemini, or Groq.

---

## 🚀 How to Run Locally

### Prerequisites
*   Python 3.9+
*   An API Key (Anthropic, OpenAI, Google, or Groq)

### Installation

1. Enter the project directory:
   ```bash
   cd "Grammar correction agent"
   ```
2. Install dependencies:
   ```bash
   pip install litellm streamlit openai python-dotenv
   ```

### Application Launch

Launch the premium editing dashboard using:

```bash
streamlit run app.py
```

It will elegantly open across your localhost terminal.

---

## 💸 Monetization Strategy

The editing space is massive. GrammarPro is positioned to compete directly with premium subscriptions like Grammarly Business:

1.  **Usage-Based SaaS:** Offer users an interface where they pay per 1,000 words analyzed, heavily abstracting the LLM costs.
2.  **Specialized Editing Desks:** Sell instances of this specialized for specific niches, such as *Legal Document Grammar Verification* or *Medical Journal Grammar Checking*, using heavily targeted system prompts.
3.  **Content Agency Asset:** Integrate this into large-scale content marketing teams to enforce a uniform style guide across freelance writers before publication. 

---
*Built with modern Streamlit, Inline Diff Logic, and the LiteLLM Gateway.*


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
