import streamlit as st
import json
import os
import litellm
import pandas as pd
import plotly.express as px
from datetime import date
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. SETUP & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ToolForge AI | Autonomous Tool-Calling Console",
    page_icon="⚡",
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
        background: linear-gradient(90deg, #f59e0b, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -2px;
    }
    .sub-header { color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }

    .glass-card {
        background: rgba(22, 25, 35, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        margin-bottom: 1.5rem;
        transition: border-color 0.2s ease;
    }
    .glass-card:hover { border-color: rgba(245, 158, 11, 0.4); }

    .kpi-card { background: #1a1e2e; border: 1px solid #2e3244; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }
    .kpi-label { font-size: 0.8rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; }
    .kpi-value { font-size: 1.5rem; font-weight: 700; color: #fff; margin-top: 0.5rem; }

    .result-banner {
        background: linear-gradient(135deg, rgba(245,158,11,0.15) 0%, rgba(239,68,68,0.15) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    .stButton>button {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%;
        box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.4);
    }

    .stTextArea textarea { background: #1a1e2e !important; border: 1px solid #2e3244 !important; color: #e2e8f0 !important; border-radius: 12px !important; font-family: 'JetBrains Mono', monospace !important; }
    .stTextInput>div>div>input { background: #1a1e2e !important; border: 1px solid #2e3244 !important; color: #e2e8f0 !important; border-radius: 8px !important; }

    .tool-badge { display: inline-block; padding: 0.4rem 1rem; border-radius: 9999px; font-size: 0.85rem; font-weight: 700; margin: 0.2rem; }
    .tool-calc   { background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
    .tool-unit   { background: rgba(14,165,233,0.2); color: #38bdf8; border: 1px solid rgba(14,165,233,0.3); }
    .tool-pct    { background: rgba(34,197,94,0.2);  color: #4ade80;  border: 1px solid rgba(34,197,94,0.3); }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. TOOL REGISTRY
# -----------------------------------------------------------------------------
def calculator(quantity: float, price: float, tax_rate: float) -> float:
    return round(quantity * price * (1 + tax_rate), 2)

def unit_converter(value: float, from_unit: str, to_unit: str) -> float:
    conversions = {
        ("km", "miles"): lambda v: round(v * 0.621371, 4),
        ("miles", "km"): lambda v: round(v * 1.60934, 4),
        ("kg", "lbs"): lambda v: round(v * 2.20462, 4),
        ("lbs", "kg"): lambda v: round(v / 2.20462, 4),
        ("celsius", "fahrenheit"): lambda v: round((v * 9/5) + 32, 2),
        ("fahrenheit", "celsius"): lambda v: round((v - 32) * 5/9, 2),
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        return conversions[key](value)
    raise ValueError(f"Unsupported: {from_unit} → {to_unit}")

def percentage_calculator(base: float, rate: float) -> float:
    return round(base * (rate / 100), 2)

TOOL_MAP = {
    "calculator": calculator,
    "unit_converter": unit_converter,
    "percentage_calculator": percentage_calculator,
}

TOOL_COLORS = {
    "calculator": "tool-calc",
    "unit_converter": "tool-unit",
    "percentage_calculator": "tool-pct",
}

# -----------------------------------------------------------------------------
# 4. AGENT LOGIC
# -----------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an advanced Tool-Calling Agent with access to the following tools:

1. calculator(quantity, price, tax_rate) — Computes purchase totals with tax. tax_rate is a decimal (e.g., 8% = 0.08).
2. unit_converter(value, from_unit, to_unit) — Converts between units (km, miles, kg, lbs, celsius, fahrenheit).
3. percentage_calculator(base, rate) — Computes a percentage of a value.

Rules:
- Analyze the task to select the correct tool
- Extract exact parameters with correct data types (all numbers must be floats)
- Do NOT change task intent

Return ONLY valid JSON:
{
  "reasoning": "Why this tool was selected",
  "tool_used": "tool_name",
  "inputs": { ...float parameters... },
  "result": null,
  "final_answer": ""
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

def run_agent(task: str, model: str = "gpt-4o", api_key: str = None) -> dict:
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task}
        ],
        "temperature": 0.2
    }
    if api_key:
        kwargs["api_key"] = api_key

    response = litellm.completion(**kwargs)
    decision = extract_json(response.choices[0].message.content)

    tool_name = decision.get("tool_used", "")
    if tool_name in TOOL_MAP:
        result = TOOL_MAP[tool_name](**decision["inputs"])
        decision["result"] = result
        decision["final_answer"] = f"Tool `{tool_name}` executed successfully. Result: {result}"
    else:
        decision["result"] = "N/A"
        decision["final_answer"] = "No matching tool was invoked for this task."

    return decision

# -----------------------------------------------------------------------------
# 5. MAIN INTERFACE
# -----------------------------------------------------------------------------
def main():
    local_css()

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;color:white;'>ToolForge <span style='color:#f59e0b;'>AI</span></h2>", unsafe_allow_html=True)

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
        selected_label = st.selectbox("Inference Engine", list(provider_map.keys()))
        target_model   = provider_map[selected_label]

        st.markdown("---")
        st.markdown("### 🔑 API Management")
        user_api_key = st.text_input("Custom API Key (Optional)", type="password")

        st.markdown("---")
        st.markdown("### 🛠️ Registered Tools")
        st.markdown("<span class='tool-badge tool-calc'>🧮 calculator</span>", unsafe_allow_html=True)
        st.markdown("<span class='tool-badge tool-unit'>📐 unit_converter</span>", unsafe_allow_html=True)
        st.markdown("<span class='tool-badge tool-pct'>📊 percentage_calculator</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.info(f"Dispatching to: **{selected_label.split('—')[-1].strip() if '—' in selected_label else selected_label.split(' ')[-1]}**")

    # ── Main Content ──────────────────────────────────────────
    st.markdown("<h1 class='main-header'>Autonomous Tool-Calling Console</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Define a task — the agent autonomously selects the right tool, extracts parameters, and executes with zero friction.</p>", unsafe_allow_html=True)

    # Input
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📝 Task Definition")
    task_input = st.text_area(
        "Natural Language Task",
        height=120,
        value="Calculate the total cost if 3 items cost $49 each, including 8% tax.",
        help="Write any task that requires calculation, unit conversion, or percentage math."
    )
    if st.button("⚡ Execute Agent"):
        if task_input:
            with st.spinner(f"Orchestrating inference via {selected_label.split('—')[-1].strip() if '—' in selected_label else selected_label}..."):
                try:
                    result = run_agent(task_input, model=target_model, api_key=user_api_key)
                    st.session_state['result'] = result
                except Exception as e:
                    st.session_state['result'] = {"error": str(e)}
        else:
            st.warning("Please define a task first.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Results
    if st.session_state.get('result'):
        res = st.session_state['result']

        if "error" in res:
            st.error(f"🔴 Execution Error: {res['error']}")
        else:
            badge_cls = TOOL_COLORS.get(res.get('tool_used', ''), 'tool-calc')
            st.markdown(f"""
            <div class='result-banner'>
                <span class='tool-badge {badge_cls}'>🛠️ {res.get('tool_used','—')}</span>
                <h2 style='color:#fbbf24; margin:0.75rem 0 0;'>{res.get('result', '—')}</h2>
                <p style='color:#94a3b8;font-size:1rem;margin-top:0.5rem;'>{res.get('final_answer','')}</p>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 🧠 Agent Reasoning")
                st.write(res.get("reasoning", "—"))
                st.markdown("#### 📥 Extracted Inputs")
                st.json(res.get("inputs", {}))
                st.markdown("</div>", unsafe_allow_html=True)

            with col_b:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 📊 Execution Trace")
                # Show a simple bar with the result value if numeric
                try:
                    val = float(res.get('result', 0))
                    df = pd.DataFrame({"Phase": ["Raw Input", "After Processing"], "Value": [val / (1 + list(res.get("inputs", {}).values())[-1]) if "tax_rate" in res.get("inputs", {}) else val * 0.9, val]})
                    fig = px.bar(df, x="Phase", y="Value", color="Phase", color_discrete_sequence=["#f59e0b", "#ef4444"])
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'), showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.write(f"**Result:** `{res.get('result', '—')}`")
                st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;'>ToolForge AI © 2026 | Autonomous Tool Orchestration | Powered by LiteLLM</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    if 'result' not in st.session_state:
        st.session_state['result'] = None
    main()
