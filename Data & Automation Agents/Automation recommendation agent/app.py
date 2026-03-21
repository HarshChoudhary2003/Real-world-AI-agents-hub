import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from datetime import date
from agent import read_workflow_data, generate_automation_strategy, save_outputs

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Auto-Strategist AI | SaaS Edition",
    page_icon="🏗️",
    layout="wide",
)

# --- SaaS ELITE CSS v2.0 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: radial-gradient(circle at top right, #111827 0%, #020617 100%);
        color: #f1f5f9;
        overflow-x: hidden;
    }

    /* Top Nav */
    .nav-container {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 64px;
        background: rgba(2, 6, 23, 0.7);
        backdrop-filter: blur(15px);
        z-index: 1000;
        display: flex;
        align-items: center;
        padding: 0 40px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        justify-content: space-between;
    }
    .nav-logo { font-size: 1.1rem; font-weight: 800; color: #facc15; letter-spacing: 0.1rem; }
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
        padding-top: 20px;
    }
    
    /* KPI Area */
    .kpi-row {
        display: flex;
        gap: 24px;
        margin-bottom: 30px;
    }
    .kpi-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 24px;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeUp 0.8s ease-out;
    }
    .kpi-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.04); border-color: #facc15; }
    
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Opportunity Cards */
    .opp-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        animation: slideIn 0.8s ease-out;
    }
    .opp-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 6px; height: 100%;
        background: #facc15;
    }

    /* Badges */
    .priority-badge {
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .priority-critical { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid #ef4444; }
    .priority-high { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid #f59e0b; }
    
    /* Buttons */
    .stButton button {
        background: #facc15 !important;
        color: #0c0a09 !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        border: none !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(250, 204, 21, 0.4);
    }
    .stButton button:active { transform: scale(0.95); }

    /* Empty States */
    .empty-state {
        text-align: center;
        padding: 50px;
        color: #64748b;
        background: rgba(255, 255, 255, 0.01);
        border: 2px dashed rgba(255, 255, 255, 0.05);
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TOP NAV ---
st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">AUTO-STRATEGIST AI</div>
        <div style="display: flex; align-items: center; gap: 20px; color: #64748b; font-size: 0.85rem;">
            <span>Architecture Hub v2.0</span>
            <div style="width: 38px; height: 38px; border-radius: 50%; background: #facc15; display: flex; align-items: center; justify-content: center; color: #000; font-weight: 800; font-size: 0.7rem;">AS</div>
        </div>
    </div>
    <div style="height: 80px;"></div>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'Overview'

def switch_page(name):
    st.session_state.page = name

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🗺️ Strategy Map")
    if st.button("🏗️ Strategic Overview", use_container_width=True): switch_page('Overview')
    if st.button("📓 Workflow Mining", use_container_width=True): switch_page('Mining')
    if st.button("🛡️ Transformation", use_container_width=True): switch_page('Transformation')
    if st.button("⚙️ Core Settings", use_container_width=True): switch_page('Settings')
    
    st.divider()
    st.markdown("### 🎛️ Provider Selection")
    provider = st.selectbox("Intelligence Core", ["OpenAI", "Google Gemini", "Claude", "Groq"])
    model = st.selectbox("Target Model", ["gpt-4o-mini", "gemini-1.5-flash", "claude-3-5-sonnet", "llama-3.1-70b"])
    api_key_input = st.text_input("Ingest API Key (Optional)", type="password")
    
    st.divider()
    st.caption("Strategy synthesized via Auto-Strategist AI Platform.")

# --- ROUTES ---
if st.session_state.page == 'Overview':
    st.markdown('<h2 style="font-weight: 800; letter-spacing: -1.5px;">Business Transformation Dashboard</h2>', unsafe_allow_html=True)
    
    if "strategy_audit" in st.session_state:
        data = st.session_state.strategy_audit
        sa = data.get('strategic_assessment', {})
        score = int(sa.get('readiness_score', 0))
        
        # KPI ROW
        st.markdown(f"""
            <div class="kpi-row">
                <div class="kpi-card">
                    <div style="font-size: 0.75rem; color: #64748b; font-weight: 800;">READINESS SCORE</div>
                    <div style="font-size: 2.2rem; font-weight: 900; color: #facc15;">{score}%</div>
                </div>
                <div class="kpi-card">
                    <div style="font-size: 0.75rem; color: #64748b; font-weight: 800;">OPPORTUNITIES Identifed</div>
                    <div style="font-size: 2.2rem; font-weight: 900;">{sa.get('total_potential_identified')}</div>
                </div>
                <div class="kpi-card">
                    <div style="font-size: 0.75rem; color: #64748b; font-weight: 800;">EST. ROI CYCLE</div>
                    <div style="font-size: 2.2rem; font-weight: 900; color: #3b82f6;">Q3 <span style="font-size: 0.8rem; color: #64748b;">'26</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # PROMPT BRIEF
        st.markdown(f'<div class="opp-card"><h3>🚀 Strategic Executive Summary</h3><p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6;">{sa.get("executive_summary")}</p></div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("### 🏆 High-ROI Candidates")
            for item in data.get('automation_roadmap', []):
                pri = item.get('priority', 'standard').lower()
                st.markdown(f"""
                    <div class="opp-card" style="border-left-color: {'#ef4444' if pri == 'critical' else '#facc15'};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; color: #f8fafc;">{item.get('candidate')}</h4>
                            <span class="priority-badge priority-{pri}">{item.get('priority')}</span>
                        </div>
                        <p style="color: #64748b; font-size: 0.9rem; margin: 15px 0;">{item.get('strategic_rationale')}</p>
                        <div style="display: flex; gap: 10px;">
                            <span style="background: rgba(255,255,255,0.04); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem;">Impact: {item.get('impact_rating')}/10</span>
                            <span style="background: rgba(59, 130, 246, 0.1); color: #3b82f6; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem;">Tech: {item.get('tech_stack_suggestion')[0] if item.get('tech_stack_suggestion') else 'Custom'}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with col_right:
            st.markdown("### 📊 Distribution")
            # Simulated ROI Chart
            chart_data = pd.DataFrame({
                "Target": ["Admin", "Sales", "Ops", "Finance"],
                "Saved Hours": [45, 20, 15, 60]
            })
            fig = px.pie(chart_data, values="Saved Hours", names="Target", template="plotly_dark", hole=0.7, color_discrete_sequence=px.colors.sequential.YlOrBr)
            fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('<div class="opp-card"><h4>🛡️ Structural Risks</h4>', unsafe_allow_html=True)
            for risk in data.get('structural_risks', []):
                st.markdown(f"• {risk}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="opp-card" style="border-left-color: #3b82f6;"><h4>⚡ Architect Pro-Tips</h4>', unsafe_allow_html=True)
            for tip in data.get('transformation_pro_tips', []):
                st.success(f"▶ {tip}")
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        st.markdown("""<div class="empty-state"><h3>No active strategy map found</h3><p>Upload a workflow description in the 'Workflow Mining' section to resolve your automation potential.</p></div>""", unsafe_allow_html=True)

elif st.session_state.page == 'Mining':
    st.markdown('<h2 style="font-weight: 800; letter-spacing: -1.5px;">Neural Process Mining</h2>', unsafe_allow_html=True)
    st.markdown('<div class="opp-card"><h3>📥 Workflow Feed Ingestion</h3>', unsafe_allow_html=True)
    flows_input = st.text_area("Paste manual workflow steps, frequencies, and pain points here:", height=300, value=st.session_state.get("flows_raw", ""))
    
    if st.button("🚀 Execute Strategic Scoping"):
        if flows_input:
            with st.spinner("Analyzing process patterns and calculating ROI heuristics..."):
                try:
                    # Save for agent read
                    with open("workflows.txt", "w", encoding="utf-8") as f:
                        f.write(flows_input)
                    
                    strategy = generate_automation_strategy(flows_input, "gpt-4o-mini", api_key_input)
                    st.session_state.strategy_audit = strategy
                    st.session_state.flows_raw = flows_input
                    save_outputs(strategy)
                    st.toast("✅ Strategic Roadmap Synthesized!", icon="🚀")
                    switch_page('Overview')
                    st.rerun()
                except Exception as e:
                    st.error(f"Scoping failed: {e}")
        else:
            st.warning("Please provide workflow data.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'Transformation':
    st.markdown('<h2 style="font-weight: 800; letter-spacing: -1.5px;">Transformation Readiness</h2>', unsafe_allow_html=True)
    if "strategy_audit" in st.session_state:
        data = st.session_state.strategy_audit
        for item in data.get('automation_roadmap', []):
            st.markdown(f"""
                <div class="opp-card">
                    <h4 style="color: #facc15;">{item.get('candidate')}</h4>
                    <p style="color: #94a3b8;"><strong>Expected Outcomes:</strong></p>
                    <ul>
                        {''.join([f'<li>{o}</li>' for o in item.get('expected_outcomes', [])])}
                    </ul>
                    <hr style="border-color: rgba(255,255,255,0.05);">
                    <p style="color: #facc15; font-size: 0.8rem;">IMPLEMENTATION PREREQUISITES:</p>
                    <p style="color: #64748b; font-size: 0.85rem;">{', '.join(item.get('pre_requisites', []))}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Strategize your hub first.")

elif st.session_state.page == 'Settings':
    st.markdown('<h2 style="font-weight: 800; letter-spacing: -1.5px;">Global Control</h2>', unsafe_allow_html=True)
    st.markdown('<div class="opp-card">', unsafe_allow_html=True)
    st.checkbox("Enable Real-time ROI Pulse", value=True)
    st.checkbox("Enable Neural Process Mapping", value=True)
    st.slider("Strategic Conservatism", 0.1, 1.0, 0.4)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""<div style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(5px); padding: 8px 40px; text-align: center; font-size: 0.65rem; color: #475569; border-top: 1px solid rgba(255,255,255,0.05); z-index: 1000;">Architected by AUTO-STRATEGIST AI | Unified Process Transformation OS</div>""", unsafe_allow_html=True)
