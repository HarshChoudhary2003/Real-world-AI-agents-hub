import streamlit as st
import json
import os
import pandas as pd
from datetime import date
from agent import read_workflow, architect_execution_path, save_outputs

# Set Page Config
st.set_page_config(
    page_title="Orchestra-Core AI | Systems Orchestration OS",
    page_icon="🎼",
    layout="wide",
)

# Premium Creative Styling
st.markdown("""
    <style>
    @keyframes lineGlow {
        0% { border-left-color: rgba(56, 189, 248, 0.3); }
        50% { border-left-color: rgba(56, 189, 248, 1); }
        100% { border-left-color: rgba(56, 189, 248, 0.3); }
    }
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .main { background-color: #0c0a09; }
    .stApp { background: radial-gradient(circle at bottom center, #111827 0%, #0c0a09 100%); }
    
    .node-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 5px solid #38bdf8;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        animation: fadeInSlide 0.7s ease-out;
    }
    .node-card:nth-child(even) { animation-delay: 0.1s; }
    .node-card:nth-child(odd) { animation-delay: 0.2s; }

    .efficiency-meter {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        border: 4px solid #38bdf8;
        background: rgba(56, 189, 248, 0.05);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
    }
    .section-header {
        color: #f8fafc;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 15px;
        border-right: 4px solid #38bdf8;
        padding-right: 15px;
        width: fit-content;
    }
    .sidebar-section {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .priority-badge {
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        background: #38bdf8;
        color: #0c0a09;
        text-transform: uppercase;
    }
    .recovery-blueprint {
        background: rgba(16, 185, 129, 0.05);
        border: 1px dashed #10b981;
        padding: 15px;
        border-radius: 8px;
        color: #10b981;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Logo & Title
st.title("🎼 Orchestra-Core AI")
st.markdown("### Strategic Systems Pipeline & Workflow Orchestrator")
st.caption("Architect high-performance execution paths with multi-step dependency resolution and surgical recovery logic.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Orchestra Config")
    
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

        api_key = st.text_input("Provider API Key (Optional)", type="password")
        temperature = st.slider("Logical Creative Scope", 0.0, 1.0, 0.2)
        st.markdown('</div>', unsafe_allow_html=True)

    st.header("📂 Data Import")
    if st.button("Load User Onboarding Workflow"):
        st.session_state.raw_workflow_json = """{
  "workflow_name": "User Onboarding Automation",
  "steps": [
    {"id": "create_user", "depends_on": [], "action": "Database Entry"},
    {"id": "send_welcome_email", "depends_on": ["create_user"], "action": "Email SMTP"},
    {"id": "provision_access", "depends_on": ["create_user"], "action": "Cloud IAM Provisioning"},
    {"id": "notify_slack_channel", "depends_on": ["provision_access"], "action": "Webhook Call"}
  ]
}"""

# Layout Split
col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.markdown('<div class="section-header">🛠️ Request Architecture</div>', unsafe_allow_html=True)
    workflow_json = st.text_area(
        "Paste the raw workflow JSON to architect:",
        value=st.session_state.get("raw_workflow_json", ""),
        height=450,
        placeholder='{"workflow_name": "My Flow", "steps": [...] }'
    )
    
    if st.button("🚀 Architect Execution Path"):
        if workflow_json:
            with st.spinner("Synthesizing dependency paths and resolving parallelization groups..."):
                try:
                    # Save for agent read
                    with open("workflow.json", "w", encoding="utf-8") as f:
                        f.write(workflow_json)
                    
                    workflow_data = json.loads(workflow_json)
                    blueprint_data = architect_execution_path(workflow_data, model_name, api_key)
                    st.session_state.orch_audit = (blueprint_data, workflow_data)
                    save_outputs(blueprint_data)
                    st.success("Execution Blueprint Synced!")
                except Exception as e:
                    st.error(f"Logic failure: {e}")
        else:
            st.warning("Please provide a workflow JSON first.")

with col_output:
    if "orch_audit" in st.session_state:
        blueprint_data, workflow_data = st.session_state.orch_audit
        oa = blueprint_data.get('orchestra_assessment', {})
        score = int(oa.get('efficiency_score', '0'))
        
        # Summary Area
        st.markdown(f"""
            <div class="efficiency-meter">
                <span style="font-size: 2rem; font-weight: 900; color: #38bdf8;">{score}%</span>
                <span style="font-size: 0.7rem; color: #94a3b8; font-weight: 600;">EFFICIENCY</span>
            </div>
            <div align="center" style="margin-top: 15px; margin-bottom: 25px; color: #94a3b8; font-style: italic;">
                Verdict: <strong style="color: #38bdf8;">{oa.get('verdict')}</strong><br>
                {oa.get('diagnostic_overview')}
            </div>
        """, unsafe_allow_html=True)

        tab_blueprint, tab_recovery, tab_diag = st.tabs(["🚀 Execution Path", "🛡️ Recovery Blueprint", "🧬 Diagnostics & Tips"])
        
        with tab_blueprint:
            st.markdown('<div class="section-header">🚀 Path Architecture</div>', unsafe_allow_html=True)
            for step in blueprint_data.get('execution_blueprint', []):
                st.markdown(f"""
                    <div class="node-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="font-weight: 800; color: #f8fafc;">{step.get('step_id')}</span>
                            <span class="priority-badge">PRIORITY {step.get('priority_level')}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.9rem;"><strong>Action:</strong> {step.get('action_intent')}</p>
                        <span style="color: #38bdf8; font-size: 0.75rem;">Group: {step.get('parallel_group')}</span>
                    </div>
                """, unsafe_allow_html=True)

        with tab_recovery:
            st.markdown('<div class="section-header">🛡️ Surgical Remediation Blueprints</div>', unsafe_allow_html=True)
            for rec in blueprint_data.get('recovery_blueprints', []):
                st.markdown(f"**Step ID**: `{rec.get('step_id')}` | **Scenario**: *{rec.get('incident_type')}*")
                st.markdown(f"""
                    <div class="recovery-blueprint">
                        <strong>SURGICAL REMEDIATION:</strong><br>{rec.get('surgical_remediation')}
                    </div>
                """, unsafe_allow_html=True)
                st.divider()

        with tab_diag:
            st.markdown('<div class="section-header">🧬 Component Diagnostics</div>', unsafe_allow_html=True)
            dd = blueprint_data.get('dependency_diagnostics', {})
            
            if dd.get('circular_nodes'):
                st.error(f"❌ **CIRCULAR LOOPS FOUND**: {dd.get('circular_nodes')}")
            else:
                st.success("✅ No circular dependencies detected in the manifold.")
                
            st.markdown("#### Potential Bottlenecks")
            for node in dd.get("bottleneck_nodes", []):
                st.warning(f"⚠️ **{node}**: This step is a critical path anchor.")

            st.divider()
            st.markdown("#### ⚡ Pro Architect Tips")
            for tip in blueprint_data.get("pro_architect_tips", []):
                st.info(f"💡 {tip}")
            
            st.download_button("📥 Export Logic JSON", json.dumps(blueprint_data, indent=2), "workflow_arch.json", "application/json")
    else:
        st.info("Paste a workflow JSON and click 'Architect' to reveal the execution path and recovery blueprints.")

# Footer
st.markdown("---")
st.markdown("<div align='center'>Architected with Orchestra-Core AI | Mastering Systems Complexity</div>", unsafe_allow_html=True)
