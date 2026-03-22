import streamlit as st
import json
import os
import litellm
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ThinkForge AI | Multi-Step Reasoning Engine",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS
# -----------------------------------------------------------------------------
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp { background-color: #0c0e14; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden !important; }
    section[data-testid="stSidebar"] { background-color: #111420 !important; border-right: 1px solid #2e3244; width: 320px !important; }

    .main-header {
        background: linear-gradient(90deg, #22c55e, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; letter-spacing: -2px; margin-bottom: 0.5rem;
    }
    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(22, 25, 35, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(34, 197, 94, 0.35); }

    /* Step cards - timeline feel */
    .step-card {
        background: #1a1e2e;
        border-left: 4px solid #22c55e;
        border-radius: 0 12px 12px 0;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        position: relative;
    }
    .step-number {
        display: inline-block;
        background: linear-gradient(135deg, #22c55e, #0ea5e9);
        color: white; font-weight: 800; font-size: 0.75rem;
        padding: 0.2rem 0.6rem; border-radius: 9999px; margin-bottom: 0.5rem;
    }
    .step-title  { font-weight: 700; font-size: 1rem; color: #f1f5f9; }
    .step-detail { color: #94a3b8; font-size: 0.9rem; margin-top: 0.4rem; }
    .step-result { color: #4ade80; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; margin-top: 0.5rem; }

    /* Final answer banner */
    .answer-banner {
        background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(14,165,233,0.15));
        border: 1px solid rgba(34,197,94,0.35);
        border-radius: 14px; padding: 2rem; text-align: center; margin-bottom: 2rem;
    }

    /* Badges */
    .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; margin: 0.2rem; }
    .badge-math    { background: rgba(34,197,94,0.2);  color: #4ade80;  border: 1px solid rgba(34,197,94,0.3); }
    .badge-logic   { background: rgba(14,165,233,0.2); color: #38bdf8;  border: 1px solid rgba(14,165,233,0.3); }
    .badge-strategy{ background: rgba(168,85,247,0.2); color: #c084fc;  border: 1px solid rgba(168,85,247,0.3); }
    .badge-analysis{ background: rgba(245,158,11,0.2); color: #fbbf24;  border: 1px solid rgba(245,158,11,0.3); }
    .badge-mixed   { background: rgba(239,68,68,0.2);  color: #f87171;  border: 1px solid rgba(239,68,68,0.3); }

    .stButton>button {
        background: linear-gradient(135deg, #22c55e 0%, #0ea5e9 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.35);
    }
    .stTextArea textarea { background: #1a1e2e !important; border: 1px solid #2e3244 !important; color: #e2e8f0 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. AGENT CORE LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an advanced Multi-Step Reasoning Agent (ThinkForge AI).

Rules:
- Decompose the problem into clear, numbered logical steps
- Show intermediate calculations and conclusions per step
- Validate constraints at each step
- Explicitly state all assumptions made

Return ONLY valid JSON with this schema:
{
  "problem_type": "math | logic | strategy | analysis | mixed",
  "steps": [
    {
      "step_number": 1,
      "title": "Short step title",
      "reasoning": "Detailed explanation of this step",
      "interim_result": "Intermediate value or conclusion from this step"
    }
  ],
  "final_answer": "Clear, complete final answer",
  "confidence": 0.0 to 1.0,
  "assumptions": ["Assumption 1", "Assumption 2"]
}
"""

def extract_json(content: str) -> dict:
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    if "{" in content:
        content = content[content.find("{"):content.rfind("}")+1]
    return json.loads(content)

def solve_problem(problem: str, model: str, api_key: str = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": problem}
        ],
        "temperature": 0.2
    }
    if api_key:
        kwargs["api_key"] = api_key
    response = litellm.completion(**kwargs)
    return extract_json(response.choices[0].message.content)

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>ThinkForge <span style='color:#22c55e;'>AI</span></h2>", unsafe_allow_html=True)

        st.markdown("### 🧬 Provider Console")
        provider_map = {
            "🌐 OpenAI — GPT-4o":          "gpt-4o",
            "🌐 OpenAI — GPT-4o Mini":     "gpt-4o-mini",
            "🎭 Claude 3.5 Sonnet":        "claude-3-5-sonnet-20240620",
            "🎭 Claude 3 Haiku":           "claude-3-haiku-20240307",
            "🔶 Gemini 1.5 Pro":           "gemini/gemini-1.5-pro",
            "🔶 Gemini 1.5 Flash":         "gemini/gemini-1.5-flash",
            "🐋 DeepSeek Chat":            "deepseek/deepseek-chat",
            "🚀 Grok-Beta":                "xai/grok-beta",
            "🏠 Llama 3 (Ollama)":         "ollama/llama3",
            "🏠 Mistral (Ollama)":         "ollama/mistral",
            "🔓 Llama 3 70B (Groq)":       "groq/llama3-70b-8192",
            "🔓 Mixtral 8x7B (Groq)":      "groq/mixtral-8x7b-32768",
        }
        selected_label = st.selectbox("Reasoning Engine", list(provider_map.keys()))
        target_model   = provider_map[selected_label]

        st.markdown("---")
        st.markdown("### 🔑 API Management")
        user_api_key = st.text_input("Custom API Key (Optional)", type="password")

        st.markdown("---")
        st.markdown("### 📊 Session Stats")
        problems_solved = len([k for k in st.session_state if k.startswith("result_")])
        st.metric("Problems Solved", problems_solved, "this session")
        st.info(f"Engine: **{selected_label.split('—')[-1].strip() if '—' in selected_label else selected_label.split(' ')[-1]}**")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Multi-Step Reasoning Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Decompose complex problems into structured reasoning chains using any AI provider.</p>", unsafe_allow_html=True)

    # Input
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🧩 Problem Statement")
    problem_input = st.text_area(
        "Describe your problem",
        height=160,
        value=(
            "A company has a budget of $120,000.\n"
            "Marketing costs $2,500 per campaign.\n"
            "Engineering costs $8,000 per feature.\n"
            "If the company runs 20 marketing campaigns, how many features can it build?"
        ),
    )
    if st.button("🧠 Reason Through Problem"):
        if problem_input.strip():
            with st.spinner(f"Orchestrating {selected_label.split('—')[-1].strip() if '—' in selected_label else selected_label}..."):
                try:
                    result = solve_problem(problem_input, model=target_model, api_key=user_api_key if user_api_key else None)
                    st.session_state['result'] = result
                    # count session solves
                    st.session_state[f"result_{len([k for k in st.session_state if k.startswith('result_')])}"] = True
                except Exception as e:
                    st.session_state['result'] = {"error": str(e)}
        else:
            st.warning("Please enter a problem to analyze.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Results
    if st.session_state.get('result'):
        res = st.session_state['result']

        if "error" in res:
            st.error(f"🔴 Reasoning Error: {res['error']}")
        else:
            # Type + confidence badges
            ptype = res.get('problem_type', 'mixed')
            badge_cls = f"badge-{ptype}" if ptype in ["math","logic","strategy","analysis","mixed"] else "badge-mixed"
            confidence = res.get('confidence', 0.9)

            # Final answer banner
            st.markdown(f"""
            <div class='answer-banner'>
                <span class='badge {badge_cls}'>{ptype.upper()}</span>
                <h2 style='color:#4ade80; margin:0.75rem 0 0.25rem; font-size:1.4rem;'>{res.get('final_answer','')}</h2>
                <p style='color:#94a3b8; margin:0;'>Confidence: {int(confidence*100)}%</p>
            </div>
            """, unsafe_allow_html=True)

            # Two-column layout: steps + chart
            left_col, right_col = st.columns([1.3, 0.7])

            with left_col:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 🔗 Reasoning Chain")
                for step in res.get("steps", []):
                    st.markdown(f"""
                    <div class='step-card'>
                        <span class='step-number'>STEP {step['step_number']}</span>
                        <div class='step-title'>{step['title']}</div>
                        <div class='step-detail'>{step['reasoning']}</div>
                        <div class='step-result'>→ {step['interim_result']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with right_col:
                # Confidence gauge
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 📈 Confidence Gauge")
                fig_conf = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=round(confidence * 100, 1),
                    suffix="%",
                    gauge={
                        "axis":  {"range": [0, 100], "tickcolor": "#94a3b8"},
                        "bar":   {"color": "#22c55e"},
                        "steps": [
                            {"range": [0,  50],  "color": "#1a1e2e"},
                            {"range": [50, 80],  "color": "#1e2a1e"},
                            {"range": [80, 100], "color": "#1a2e1a"},
                        ],
                        "bgcolor": "#1a1e2e",
                        "bordercolor": "#2e3244",
                    },
                    number={"font": {"color": "#f1f5f9"}},
                ))
                fig_conf.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#94a3b8'),
                    height=230, margin=dict(t=20, b=10, l=20, r=20)
                )
                st.plotly_chart(fig_conf, use_container_width=True)

                # Step complexity chart
                st.markdown("#### ⚙️ Step Breakdown")
                step_df = pd.DataFrame([
                    {"Step": f"S{s['step_number']}", "Length": len(s['reasoning'])}
                    for s in res.get("steps", [])
                ])
                fig_steps = px.bar(step_df, x="Step", y="Length",
                                   color_discrete_sequence=["#22c55e"],
                                   labels={"Length": "Detail Depth"})
                fig_steps.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#f1f5f9'),
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=190,
                )
                st.plotly_chart(fig_steps, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Assumptions
                if res.get("assumptions"):
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown("#### 📋 Assumptions")
                    for a in res["assumptions"]:
                        st.markdown(f"- {a}")
                    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>ThinkForge AI © 2026 | Structured Reasoning Architecture | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    if 'result' not in st.session_state:
        st.session_state['result'] = None
    main()
