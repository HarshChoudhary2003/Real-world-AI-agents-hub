<div align="center">
  <img src="https://img.shields.io/badge/AI_Agent-Elite-blue?style=for-the-badge&logo=openai" alt="Premium AI Agent">
  <img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit UI">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" alt="Python">
</div>

# ✍️ Elite Auto-SEO Blog Post Generator Agent

A premium, enterprise-grade AI content creation pipeline that instantly turns raw ideas into perfectly structured, SEO-optimized blog posts designed to rank and convert. 

Forget generic "ChatGPT outputs." This Elite Agent utilizes an advanced systematic schema to engineer high-retention content, complete with optimized metadata, engaging hooks, and platform-specific social media collateral—all through a beautiful, cross-model UI.

---

## 🔥 Why This Agent? (The Value Proposition)

* **Multi-LLM Engine:** Instantly toggle between the world's best models including **OpenAI (GPT-4o, o1-preview, o3-mini)**, **Anthropic (Claude 3.5 Sonnet)**, and **Google (Gemini 2.0 Flash/Pro)**—all seamlessly integrated into one command center.
* **Native SEO Optimization:** Stop paying for separate SEO tools. The agent automatically drafts your `slug`, `seoTitle`, `metaDescription`, and embeds your exact target `keywords` directly into the JSON/markdown backbone.
* **Psychological Hooks & Formatting:** Programmed to eliminate fluff and jargon, the agent constructs content using proven copywriting best practices including bullet-points, high-contrast listicles, and strong conclusions with clear Calls-To-Action.
* **Social Media Collateral:** Automatically generates a companion Twitter/LinkedIn promotional post complete with emojis and hashtags so you can distribute immediately.
* **Dual-Action Interface:** Run it blazing fast from your CLI via `agent.py`, or use the stunning, dark-mode `app.py` Streamlit dashboard for a beautiful visual workflow.

---

## 🛠 Features

1. **Rich Streamlit UI:** A gorgeous `app.py` interface featuring dynamic metadata expanders and rich markdown rendering.
2. **Advanced Creativity Controls:** A built-in tuning slider gives you total control over the AI's "Creativity" vs "Factual" (temperature) bounds.
3. **Structured Outputs:** Automatically dual-writes a `blog.json` for precise database extraction and a highly readable `blog.txt` for immediate publishing.
4. **Context Injection:** Dedicated inputs allowing you to paste in custom reference data or documentation to ground the AI in absolute truth.

---

## 🚀 Getting Started

### 1. Requirements

Ensure you have Python installed, then install the required AI SDKs and the UI framework:

```bash
pip install openai anthropic google-generativeai streamlit
```

### 2. Configuration & Launch (UI Mode - Recommended)

The premium web interface allows you to input your API keys dynamically. It requires zero hardcoded environment variables to start!

```bash
cd "Blog post generator agent"
python -m streamlit run app.py
```

The application will launch on `http://localhost:8501`. 

### 3. CLI Mode (Headless Execution)

To run the agent directly from the terminal (perfect for cron-jobs or automation integrations):

1. Define your parameters inside `blog.txt`.
2. Export your chosen API Key in your terminal:
   ```bash
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-key"
   $env:ANTHROPIC_API_KEY="your-key"
   $env:GEMINI_API_KEY="your-key"
   ```
3. Execute the engine:
   ```bash
   python agent.py
   ```

Outputs will instantly compile into `blog.json` and `blog.txt`.

---

## 💼 Commercial & Agency Use

The **Elite Auto-SEO Blog Post Generator Agent** is highly optimized for scale. The raw JSON structuring returned by the generative engine makes it incredibly easy to pipe these generated posts directly into a Headless CMS, WordPress REST API, or any automated newsletter distribution pipeline. 

> *Build complete content marketing empires autonomously.*


---

Developed with ❤️ by [Harsh Choudhary](https://github.com/HarshChoudhary2003) | *Building the future of Agentic Intelligence.*
