import streamlit as st
import json
import os
import time
import psutil
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# --- Page Config ---
st.set_page_config(
    page_title="Sentinel | Live Monitoring",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SaaS Premium UI (Vercel/Linear Style) ---
def inject_premium_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        :root {
            --bg-main: #000000;
            --bg-card: #0a0a0a;
            --accent: #50e3c2; /* Sentinel Cyan */
            --border: #1f1f1f;
            --text-primary: #ffffff;
            --text-secondary: #888888;
        }

        .main { background: var(--bg-main); color: var(--text-primary); }
        [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid var(--border); }
        [data-testid="stHeader"] { background: transparent; }
        footer { visibility: hidden; }
        .stDeployButton { display: none; }

        h1, h2, h3, p, span, div { font-family: 'Inter', sans-serif !important; }
        
        /* KPI Cards */
        .kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s ease;
        }
        .kpi-card:hover { border-color: #444; }
        .kpi-label { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
        .kpi-value { font-size: 1.5rem; font-weight: 600; color: var(--text-primary); }

        /* Live Status Indicator */
        .live-dot {
            width: 8px;
            height: 8px;
            background: #50e3c2;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            box-shadow: 0 0 10px #50e3c2;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(80, 227, 194, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(80, 227, 194, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(80, 227, 194, 0); }
        }

        /* Chart Styling Overrides */
        .stPlotlyChart { background-color: var(--bg-card) !important; border: 1px solid var(--border); border-radius: 12px; }

        /* Table Premium Styling */
        div[data-testid="stTable"] { 
            background: var(--bg-card); 
            border: 1px solid var(--border); 
            border-radius: 12px; 
            overflow: hidden; 
        }

        </style>
    """, unsafe_allow_html=True)

def sidebar_nav():
    with st.sidebar:
        st.markdown("<h2 style='color:white; margin-bottom:2rem;'>📡 Sentinel.AI</h2>", unsafe_allow_html=True)
        nav = st.radio("Primary Modules", ["Live Watch", "Audit Logs", "System Config"], label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#111'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888; font-size:0.7rem;'>NODE CONFIGURATION</p>", unsafe_allow_html=True)
        
        threshold = st.slider("CPU Threshold (%)", 0, 100, 80)
        st.session_state.threshold = threshold
        
        interval = st.select_slider("Polling Interval (s)", options=[1, 2, 5, 10, 30], value=5)
        st.session_state.interval = interval
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:rgba(80,227,194,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(80,227,194,0.1);'>
                <div style='font-size:0.7rem; color:#50e3c2; font-weight:600;'>INTERNAL TELEMETRY</div>
                <div style='font-size:0.85rem; color:white; margin-top:0.2rem;'><span class='live-dot'></span>Active Node</div>
            </div>
        """, unsafe_allow_html=True)
        return nav

def main():
    inject_premium_css()
    current_nav = sidebar_nav()

    if current_nav == "Live Watch":
        # --- Header Section ---
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:2.5rem;'>
                <div>
                    <h1 style='font-size: 2.2rem; letter-spacing: -0.05em; font-weight: 700;'>Live Watch</h1>
                    <p style='color:#888; font-size:0.95rem;'>High-frequency telemetry monitoring with persistence-aware alerting.</p>
                </div>
                <div style='text-align:right'>
                    <div style='color:#888; font-size:0.75rem; margin-bottom:4px;'>SYSTEM UPTIME</div>
                    <div style='color:white; font-size:1.1rem; font-weight:700;'>99.98%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- Metrics Dashboard ---
        col_main, col_spacer, col_side = st.columns([1.5, 0.05, 0.8])

        with col_main:
            # Live Chart Container
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>CPU UTILIZATION REAL-TIME</h4>", unsafe_allow_html=True)
            
            # Temporary state for real-time chart data
            if 'chart_data' not in st.session_state:
                st.session_state.chart_data = pd.DataFrame(columns=["timestamp", "cpu"])
            
            # Simulated real-time fetch (replace with actual logic)
            curr_cpu = psutil.cpu_percent()
            new_entry = pd.DataFrame({"timestamp": [datetime.now()], "cpu": [curr_cpu]})
            st.session_state.chart_data = pd.concat([st.session_state.chart_data, new_entry], ignore_index=True).tail(30)
            
            st.line_chart(st.session_state.chart_data.set_index("timestamp"), color="#50e3c2")
            
            if curr_cpu > st.session_state.threshold:
                st.warning(f"THRESHOLD EXCEEDED: {curr_cpu}% (Limit: {st.session_state.threshold}%)")
            
            # Sleep slightly to control refresh in the loop
            time.sleep(1) # Slow refresh for UI stability
            st.rerun()

        with col_side:
            st.markdown("<h4 style='font-size:0.85rem; color:#888; margin-bottom:1rem;'>RESOURCE KPI</h4>", unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-card"><div class="kpi-label">Node CPU</div><div class="kpi-value">{curr_cpu}%</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-card"><div class="kpi-label">Persistence Queue</div><div class="kpi-value">0 / 3</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-card"><div class="kpi-label">Alerts Triggered</div><div class="kpi-value">0</div></div>', unsafe_allow_html=True)

    elif current_nav == "Audit Logs":
        st.markdown("<h1>System Audit Logs</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;'>Persistent record of all operational deviations.</p>", unsafe_allow_html=True)
        
        # Mock logs
        logs = pd.DataFrame([
            {"Timestamp": "2026-03-24 09:40:02", "Metric": "CPU", "Value": "82%", "Action": "Alert Queued"},
            {"Timestamp": "2026-03-24 09:35:14", "Metric": "CPU", "Value": "45%", "Action": "Logged"},
            {"Timestamp": "2026-03-24 09:30:00", "Metric": "CPU", "Value": "12%", "Action": "Logged"},
        ])
        st.table(logs)

    elif current_nav == "System Config":
        st.markdown("<h1>Internal Configuration</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;'>Fine-tune the sentinel intelligence swarm.</p>", unsafe_allow_html=True)
        st.checkbox("Enable persistence-aware alerting", value=True)
        st.checkbox("Log local anomalies", value=True)
        st.button("Reset Node State")

if __name__ == "__main__":
    main()
