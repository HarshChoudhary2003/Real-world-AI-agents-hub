import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from agent import analyze_funnel, save_outputs, SYSTEM_PROMPT

# Set Page Config
st.set_page_config(
    page_title="Funnel-Force AI | Performance Diagnostic Engine",
    page_icon="⚡",
    layout="wide",
)

# Dark Glassmorphism Styling
st.markdown("""
    <style>
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .main { background-color: #0b0e14; }
    .stApp { background: radial-gradient(circle at bottom right, #1a1e26 0%, #0b0e14 100%); }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        animation: slideInLeft 0.8s ease-out;
    }
    .metric-card:hover {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid #00d4ff;
        transform: translateY(-5px);
    }
    .metric-label { color: #8892b0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; }
    .metric-value { color: #00d4ff; font-size: 2rem; font-weight: 900; }
    .section-header {
        color: #ccd6f6;
        border-left: 4px solid #00d4ff;
        padding-left: 15px;
        margin-top: 30px;
        margin-bottom: 20px;
        font-size: 1.5rem;
        font-weight: 700;
        animation: slideInLeft 0.6s ease-out;
    }
    .sidebar-section {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: rgba(255, 255, 255, 0.02);
        border-radius: 10px 10px 0 0;
        padding: 0 20px;
        color: #8892b0;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 212, 255, 0.1) !important;
        border-bottom: 2px solid #00d4ff !important;
        color: #00d4ff !important;
    }
    .roadmap-card {
        background: rgba(0, 212, 255, 0.03);
        border-left: 5px solid #00d4ff;
        padding: 20px;
        border-radius: 4px 15px 15px 4px;
        margin-bottom: 20px;
        transition: 0.3s all ease;
    }
    .roadmap-card:hover {
        background: rgba(0, 212, 255, 0.07);
        transform: translateX(5px);
    }
    </style>
""", unsafe_allow_html=True)

# App Title & Header
st.title("⚡ Funnel-Force AI")
st.markdown("### Performance Diagnostic & Conversion Strategy Engine")
st.caption("Identify leakages, diagnose friction, and architect growth strategies with multi-model intelligence.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        # Global Provider-first Standard
        provider = st.selectbox(
            "Select Intelligence Provider",
            ["OpenAI", "Google Gemini", "Anthropic Claude", "DeepSeek", "Groq (Llama 3)", "Custom"]
        )

        if provider == "OpenAI":
            model_name = st.selectbox("Select Model", ["gpt-4o-mini", "gpt-4o", "o1-mini"])
        elif provider == "Google Gemini":
            model_name = st.selectbox("Select Model", ["gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash"])
        elif provider == "Anthropic Claude":
            model_name = st.selectbox("Select Model", ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"])
        elif provider == "DeepSeek":
            model_name = st.selectbox("Select Model", ["deepseek/deepseek-chat"])
        elif provider == "Groq (Llama 3)":
            model_name = st.selectbox("Select Model", ["groq/llama-3.1-70b-versatile", "groq/llama-3.1-8b-instant"])
        else:
            model_name = st.text_input("Enter LiteLLM Model ID", "")

        api_key = st.text_input("Provider API Key (Optional)", type="password", help="Overrides environment variables.")
        temperature = st.slider("Diagnostic Creativity", 0.0, 1.0, 0.4)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Data Import")
    uploaded_file = st.file_uploader("Upload Funnel Metrics (TXT)", type=["txt"])
    
    if st.button("Load Example Case Study"):
        st.session_state.funnel_input = """Funnel Stages:
- Visits: 50,000
- Signup Start: 12,500
- Signup Success: 7,500
- Active User: 3,200

Segment: Organic Search
Goal: Maximize High-Intent Activations"""

# Layout Split
col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.markdown('<div class="section-header">🛠️ Funnel Raw Metrics</div>', unsafe_allow_html=True)
    
    funnel_text = st.text_area(
        "Paste funnel metrics, segments, and goals below:",
        value=st.session_state.get("funnel_input", ""),
        height=300,
        placeholder="e.g., Visits: 1000\nAdd to Cart: 100\nCheckout: 20..."
    )
    
    if uploaded_file:
        funnel_text = str(uploaded_file.read(), "utf-8")
        st.text_area("Uploaded File Content", value=funnel_text, height=150)

    if st.button("⚡ Run Performance Audit"):
        if funnel_text:
            with st.spinner("Analyzing funnel behavior & calculating conversion efficiency..."):
                try:
                    insights = analyze_funnel(funnel_text, model_name, api_key)
                    st.session_state.funnel_insights = insights
                    save_outputs(insights)
                    st.success("Audit Complete!")
                except Exception as e:
                    st.error(f"Diagnostic Error: {e}")
        else:
            st.warning("Please provide funnel data first.")

with col_output:
    st.markdown('<div class="section-header">🔍 Strategic Audit Results</div>', unsafe_allow_html=True)
    
    if "funnel_insights" in st.session_state:
        data = st.session_state.funnel_insights
        
        # Stats summary row
        metrics = data.get("conversion_metrics", {})
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Overall CR</div><div class="metric-value">{metrics.get("overall", "N/A")}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Efficiency</div><div class="metric-value">Optimized</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Leakage</div><div class="metric-value">Detected</div></div>', unsafe_allow_html=True)

        # Tabbed Analysis
        tab_viz, tab_diag, tab_roadmap = st.tabs(["📊 Funnel Viz", "🧠 Diagnostics", "🛣️ Growth Roadmap"])
        
        with tab_viz:
            # Simple parsing for visualization (extract numbers from input)
            st.markdown("#### Behavioral Continuity")
            # Try to build a list for the funnel chart
            stages = []
            counts = []
            
            # Simple heuristic to extract numbers from the raw input for the chart
            raw_lines = funnel_text.split("\n")
            for line in raw_lines:
                if ":" in line:
                    parts = line.split(":")
                    label = parts[0].strip("- ")
                    val_str = "".join(filter(str.isdigit, parts[1]))
                    if val_str:
                        stages.append(label)
                        counts.append(int(val_str))
            
            if stages and counts:
                fig = go.Figure(go.Funnel(
                    y=stages,
                    x=counts,
                    textinfo="value+percent initial",
                    marker={"color": ["#00d4ff", "#00b4ff", "#0094ff", "#0074ff"]}
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#8892b0")
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Provide structured 'Stage: Value' input to generate the funnel chart.")

        with tab_diag:
            st.markdown("#### Executive Summary")
            st.write(data.get("summary"))
            
            st.markdown("#### Critical Drop-off Points")
            for drop in data.get("drop_off_stages", []):
                st.markdown(f"**{drop.get('stage')}** (Lost {drop.get('drop_off_pct')})")
                st.info(drop.get("psychological_reason"))
            
            st.markdown("#### Conversion Stages")
            at_each = metrics.get("at_each_stage", {})
            for pair, pct in at_each.items():
                st.markdown(f"- **{pair}**: {pct}")

        with tab_roadmap:
            st.markdown("#### Observed Patterns")
            for pattern in data.get("observed_patterns", []):
                st.write(f"👁️ {pattern}")
                
            st.markdown("#### Prioritized Focus Areas")
            for action in data.get("prioritized_actions", []):
                with st.container():
                    st.markdown(f"""
                        <div class="roadmap-card">
                            <span style="color: #00d4ff; font-weight: bold;">[{action.get('priority')}]</span> 
                            <span style="font-weight: 700; color: #ccd6f6;">{action.get('focus_area')}</span><br>
                            <span style="font-size: 0.85rem; color: #8892b0;">Potential Lift: {action.get('potential_impact')}</span><br>
                            <span style="font-size: 0.85rem; color: #ff9d00;">Counter-Bias: {action.get('suggested_counter_bias')}</span>
                        </div>
                    """, unsafe_allow_html=True)

        # Export Options
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "📥 Export JSON Audit",
                data=json.dumps(data, indent=2),
                file_name=f"funnel_audit_{date.today()}.json",
                mime="application/json"
            )
        with c2:
            st.download_button(
                "📝 Download Strategy Brief",
                data=data.get("summary", ""),
                file_name=f"funnel_summary_{date.today()}.txt",
                mime="text/plain"
            )
    else:
        st.info("Input funnel metrics and click 'Run Audit' to reveal strategic insights.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Developed by Antigravity | Advanced Funnel Intelligence Engine</div>", unsafe_allow_html=True)
