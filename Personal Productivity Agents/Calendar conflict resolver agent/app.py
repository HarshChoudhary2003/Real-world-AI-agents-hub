import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import agent
import io
import json

# ==========================================
# PAGE CONFIGURATION & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="SyncGuard AI | Calendar Resolution", page_icon="📅", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 700 !important; }

    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        background-color: #1E293B;
        border-radius: 8px;
        color: #E2E8F0;
        border: 1px solid #334155;
    }
    .streamlit-expanderContent {
        background-color: #0B0F19;
        border: 1px solid #334155;
        border-top: none;
    }

    /* Premium Badges */
    .premium-badge {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .severity-high { background-color: #EF4444; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }
    .severity-medium { background-color: #F59E0B; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }
    .severity-low { background-color: #3B82F6; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }

    /* Cards */
    .conflict-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        border-left: 4px solid #EF4444;
    }
    
    .conflict-card.type-no_buffer {
        border-left: 4px solid #F59E0B;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("📅 SyncGuard AI")
    st.markdown('<div class="premium-badge">Calendar Intelligence Engine</div>', unsafe_allow_html=True)
    st.markdown("Automatically audit your weekly schedules, detect overlapping commitments, enforce meeting buffers, and algorithmically resolve conflicts based on priority logic.")

# ==========================================
# SIDEBAR / SETTINGS 
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2693/2693507.png", width=60)
    st.title("Engine Config")
    
    st.markdown("### ⚙️ Buffer Constraints")
    # Bind directly to the agent's buffer
    agent.BUFFER_MINUTES = st.slider(
        "Required Buffer (mins)", 
        min_value=0, max_value=60, value=agent.BUFFER_MINUTES, step=5,
        help="How much time must exist between two back-to-back meetings before it's flagged as a warning?"
    )

    st.markdown("### 📥 Schedule Ingestion")
    uploaded_file = st.file_uploader("Upload Calendar CSV", type=["csv"], help="Must contain: title, start_time, end_time, priority, type, flexible")
    
    st.markdown("---")
    st.info("SyncGuard automatically evaluates scheduling priority matrices to suggest logical human-in-the-loop resolutions.")

# ==========================================
# DATA LOADING LOGIC
# ==========================================
events = []
if uploaded_file is not None:
    try:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        import csv
        reader = csv.DictReader(stringio)
        for row in reader:
            events.append(agent.Event(
                title=row.get("title", "Untitled"),
                start=agent.parse_datetime(row["start_time"]),
                end=agent.parse_datetime(row["end_time"]),
                priority=agent.PRIORITY_MAP.get(row.get("priority", "medium").lower(), 2),
                event_type=row.get("type", "event"),
                flexible=str(row.get("flexible", "yes")).lower() in ["yes", "true", "1"]
            ))
        events = sorted(events, key=lambda e: e.start)
    except Exception as e:
        st.error(f"Error parsing uploaded logic: {e}")
else:
    try:
        events = agent.read_calendar("calendar.csv")
    except Exception as e:
        st.warning(f"No valid local calendar.csv found. Please upload one. Error: {e}")

# Proceed only if we have events
if not events:
    st.stop()

# Run Engine
conflicts = agent.detect_conflicts(events)

# ==========================================
# MAIN TABS
# ==========================================
tab_dashboard, tab_timeline, tab_export = st.tabs([
    "🚨 Conflict Resolver Dashboard", 
    "📈 Visual Timeline",
    "💾 Data Exports"
])

# ----------------- TAB 1: DASHBOARD -----------------
with tab_dashboard:
    # Top Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Events Audited", len(events))
    c2.metric("Total Conflicts Found", len(conflicts), delta=f"{len(conflicts)} Warnings", delta_color="inverse")
    
    high_sev = len([c for c in conflicts if c['severity'] == "high"])
    c3.metric("High Severity Blocks", high_sev)
    
    c4.metric("Strict Priority Entities", len([e for e in events if e.priority == 3]))

    st.markdown("---")
    st.header("Actionable Resolutions")
    
    if not conflicts:
        st.success("✅ No scheduling conflicts detected! Your calendar is perfectly optimized.")
    else:
        for idx, c in enumerate(conflicts, 1):
            c_type_display = "Direct Overlap" if c['type'] == 'overlap' else f"Buffer Violation (<{agent.BUFFER_MINUTES}m)"
            css_class = "type-overlap" if c['type'] == 'overlap' else "type-no_buffer"
            sev_class = f"severity-{c['severity'].lower()}"
            
            st.markdown(f"""
            <div class="conflict-card {css_class}">
                <h3>{idx}. {c['event_a']} ⚡ {c['event_b']}</h3>
                <p>
                    <span class='{sev_class}'>{c['severity'].upper()} SEVERITY</span> &nbsp;|&nbsp; 
                    <strong>Issue:</strong> {c_type_display}
                </p>
                <div style="background: rgba(59, 130, 246, 0.1); padding: 10px; border-radius: 8px; margin-top: 15px; border-left: 3px solid #3B82F6;">
                    <strong>🤖 AI Recommendation:</strong> {c['suggestion']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 2: TIMELINE / GANTT -----------------
with tab_timeline:
    st.header("Schedule Topography")
    st.markdown("Visual representation of exactly where log-jams are occurring.")
    
    if events:
        # Prepare DataFrame for Plotly Timeline
        df_events = pd.DataFrame([
            {
                "Task": e.title,
                "Start": e.start,
                "Finish": e.end,
                "Priority": "High" if e.priority == 3 else ("Medium" if e.priority == 2 else "Low"),
                "Type": e.event_type
            } for e in events
        ])
        
        # Plotly timeline
        fig = px.timeline(
            df_events, 
            x_start="Start", 
            x_end="Finish", 
            y="Task", 
            color="Priority",
            color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#3B82F6"},
            title="Daily Agenda Trace"
        )
        
        fig.update_yaxes(autorange="reversed") # Standard Gantt flow
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font_color='#E2E8F0',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table view snippet
        with st.expander("View Raw Datastore"):
            st.dataframe(df_events, use_container_width=True)

# ----------------- TAB 3: EXPORT -----------------
with tab_export:
    st.header("Intelligence Exports")
    st.markdown("Push structured data out for automations or Executive Assistants.")
    
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        st.markdown("#### JSON Datastore")
        st.markdown("*(Machine-readable strict schema)*")
        json_output = json.dumps(conflicts, indent=2)
        st.download_button("Download conflicts.json", data=json_output, file_name="conflicts.json", mime="application/json")
        
    with col_ex2:
        st.markdown("#### Human-Readable TXT")
        st.markdown("*(Best for sharing in Slack/Email)*")
        txt_out = "Calendar Conflict Report\n"
        txt_out += "=" * 40 + "\n\n"
        for c in conflicts:
            txt_out += f"- Conflict between {c['event_a']} and {c['event_b']}\n"
            txt_out += f"  Type: {c['type']}, Severity: {c['severity']}\n"
            txt_out += f"  Suggested Action: {c['suggestion']}\n\n"
            
        st.download_button("Download conflicts.txt", data=txt_out, file_name="conflicts.txt", mime="text/plain")


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
