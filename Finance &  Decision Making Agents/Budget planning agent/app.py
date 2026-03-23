import streamlit as st
import json
import pandas as pd
import plotly.express as px
from agent import generate_budget, save_outputs
import os

# Page Configuration
st.set_page_config(
    page_title="Budget Planning Agent | Financial Intelligence",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for SaaS-Elite Glassmorphism
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    .stApp {
        background: transparent;
    }
    [data-testid="stHeader"] {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #0ea5e9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(56, 189, 248, 0.3);
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# App Content
st.title("💼 Budget Planning Agent")
st.markdown("### Generative Financial Intelligence & Strategic Allocation")

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/money-bag.png", width=80)
    st.header("Configuration")
    st.info("This agent uses GPT-4o-mini to analyze your income, expenses, and goals to create a strategic budget plan.")
    
    if st.button("Reset Input"):
        st.rerun()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📝 Financial Data Input")
    
    # Default input values if file exists
    default_input = ""
    if os.path.exists("budget_input.txt"):
        with open("budget_input.txt", "r") as f:
            default_input = f.read()
    
    user_input = st.text_area(
        "Enter your income, fixed expenses, and financial goals:",
        value=default_input,
        height=300,
        placeholder="Income: $10,000\nExpenses:\n- Rent: $2,000\nGoals:\n- Save for house..."
    )
    
    if st.button("🚀 Generate Budget Plan"):
        if user_input:
            with st.spinner("🧠 Agent is calculating allocations..."):
                try:
                    # Save current input
                    with open("budget_input.txt", "w") as f:
                        f.write(user_input)
                    
                    # Generate budget
                    budget_data = generate_budget(user_input)
                    st.session_state['budget_data'] = budget_data
                    save_outputs(budget_data)
                    st.success("✅ Analysis Complete!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please provide some financial data.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if 'budget_data' in st.session_state:
        data = st.session_state['budget_data']
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Executive Summary")
        st.write(data.get("budget_summary", ""))
        
        # Remaining Balance Metric
        balance = data.get("remaining_balance", "$0")
        st.markdown(f'<div class="metric-label">Remaining Balance</div><div class="metric-value">{balance}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart Data
        allocations = data.get("allocations", [])
        if allocations:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🎯 Allocation Breakdown")
            
            # Prepare data for Plotly
            df = pd.DataFrame(allocations)
            # Cleanup percentages for sorting/plotting
            df['percentage_val'] = df['percentage'].str.replace('%', '').astype(float)
            
            fig = px.pie(
                df, 
                values='percentage_val', 
                names='category',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Darkmint
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#f8fafc',
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # List table
            st.table(df[['category', 'amount', 'percentage']])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Goal Alignment
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🚀 Strategic Alignment")
        for goal in data.get("goal_alignment_notes", []):
            st.info(goal)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Waiting for input to generate visualization...")
        st.image("https://img.icons8.com/fluency/144/calculator.png")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>Budget Planning Agent v1.0 | Built for the Autonomous Enterprise</p>", 
    unsafe_allow_html=True
)
