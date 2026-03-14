import streamlit as st
import pandas as pd
import plotly.express as px
import json
import csv
from datetime import date, datetime
import io
import agent

# ==========================================
# PAGE CONFIGURATION & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="PingCraft AI | Pro", page_icon="🔔", layout="wide")

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #0E1117;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4 { color: #FFFFFF !important; font-weight: 700 !important; }

    /* Premium Badges */
    .premium-badge {
        background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(225, 29, 72, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Cards Simulation */
    .reminder-card {
        background: #1E293B;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 0.8rem;
        transition: transform 0.2s;
    }
    .reminder-card:hover { transform: translateX(5px); box-shadow: -5px 5px 15px -3px rgba(0,0,0,0.5); }
    
    /* Priority Colors */
    .priority-high { border-left: 4px solid #EF4444; }
    .priority-medium { border-left: 4px solid #F59E0B; }
    .priority-low { border-left: 4px solid #3B82F6; }

    /* Small labels */
    .date-label { color: #94A3B8; font-size: 0.9em; font-weight: 600;}
    .context-label { background: #334155; padding: 2px 8px; border-radius: 8px; font-size: 0.8em; margin-left: 10px;}
    
    /* Input Area styling */
    .stFileUploader > div > div { background-color: #1E293B !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🔔 PingCraft AI")
    st.markdown('<div class="premium-badge">Smart Notification Engine</div>', unsafe_allow_html=True)
    st.markdown("Automate your reminders algorithmically. Upload your master task sheet, and the engine calculates exactly *when* you need to be warned based entirely on urgency profiles.")

# ==========================================
# SIDEBAR / SETTINGS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=60)
    st.title("Engine Config")
    
    st.markdown("### 🎛️ Algorithm Tuning")
    st.markdown("Override the default mathematical spacing for reminders.")
    
    # Let user override the PRIORITY_RULES dynamically
    val_high = st.text_input("High Priority Map (Days)", value="7, 3, 1, 0", help="Spaced repetition of notifications before the deadline.")
    val_med = st.text_input("Medium Priority Map (Days)", value="3, 1")
    val_low = st.text_input("Low Priority Map (Days)", value="1")
    
    try:
        agent.PRIORITY_RULES["high"] = [int(x.strip()) for x in val_high.split(",")]
        agent.PRIORITY_RULES["medium"] = [int(x.strip()) for x in val_med.split(",")]
        agent.PRIORITY_RULES["low"] = [int(x.strip()) for x in val_low.split(",")]
        st.success("Runtime map updated successfully.")
    except Exception:
        st.error("Invalid map syntax. Use comma separated integers (e.g. 7, 3, 1).")

    
# ==========================================
# MAIN INTERFACE
# ==========================================
tab_dashboard, tab_timeline, tab_data = st.tabs(["⚡ Core Dashboard", "📅 Notification Timeline", "💾 Export Hub"])

# ----------------- DATA LOADING -----------------
tasks = []
uploaded_file = st.sidebar.file_uploader("📂 Upload tasks.csv", type=["csv"], help="Or leave empty to read local `tasks.csv`.")

if uploaded_file is not None:
    try:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        reader = csv.DictReader(stringio)
        for row in reader:
            tasks.append({
                "task": row["task"],
                "deadline": agent.parse_date(row["deadline"]),
                "priority": row["priority"].lower(),
                "context": row.get("context", "")
            })
    except Exception as e:
        st.error(f"Failed to parse uploaded CSV: {e}")
else:
    try:
        tasks = agent.read_tasks()
    except Exception as e:
        pass

if not tasks:
    st.info("No tracking sequence active. Upload a tasks CSV on the left panel to begin algorithmic mapping.")
    st.stop()
    
# Process Data
reminders = agent.build_reminders(tasks)


with tab_dashboard:
    col_input, col_output = st.columns([1, 2], gap="large")
    
    with col_input:
        st.subheader("📚 Raw Task Ingestion")
        st.markdown(f"**Loaded:** `{len(tasks)}` Active Missions")
        
        df_tasks = pd.DataFrame(tasks)
        
        # Color code priority in basic dataframe
        st.dataframe(
            df_tasks.assign(
               deadline=df_tasks['deadline'].astype(str)
            ), 
            use_container_width=True, hide_index=True
        )

    with col_output:
        st.subheader(f"🧠 Calculated Warning Pings ({len(reminders)})")
        st.markdown("The neural algorithm has processed your task list and generated the following required alert instances.")
        
        # Display upcoming first
        for idx, r in enumerate(reminders):
            p_class = f"priority-{r['priority']}"
            context_badge = f"<span class='context-label'>{str(r['context']).upper()}</span>" if r['context'] else ""
            st.markdown(f"""
            <div class="reminder-card {p_class}">
                <div class="date-label">🔔 Scheduled Execution: {r['remind_on']} | Target Deadline: {r['deadline']}</div>
                <h4 style='margin: 8px 0 0 0;'>{r['task']} {context_badge}</h4>
            </div>
            """, unsafe_allow_html=True)


with tab_timeline:
    st.header("📅 Warning Sequence Map")
    st.markdown("Visualizing the density of algorithmic warnings clustering around your immediate future.")
    
    if len(reminders) > 0:
        df_reminders = pd.DataFrame(reminders)
        
        # We want to see how many reminders happen on each day
        df_counts = df_reminders.groupby(['remind_on', 'priority']).size().reset_index(name='count')
        
        fig_bar = px.bar(df_counts, x="remind_on", y="count", color="priority", 
                         title="Notification Density Waveform",
                         color_discrete_map={"high": "#EF4444", "medium": "#F59E0B", "low": "#3B82F6"},
                         labels={"remind_on": "Chronological Date", "count": "Pings per day"})
        
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.info("💡 **Optics:** Large spikes indicate days where your notification architecture will be heavily loaded with high-priority warnings.")
    else:
        st.warning("No future reminders spawned. Either tasks have passed, or the algorithm priority maps are zeroed.")


with tab_data:
    st.header("💾 Integration Payloads")
    st.markdown("Download the fully assembled logic array to pipe directly into your Zapier, Twilio, or Google Calendar engines.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Webhook / API Payload")
        json_str = json.dumps(reminders, indent=2)
        st.download_button("Download Array (JSON)", data=json_str, file_name="calculated_reminders.json", mime="application/json")
        with st.expander("Preview JSON Payload"):
            st.code(json_str, language='json')
            
    with col2:
        st.markdown("### Human Logic List")
        txt_out = "Smart Reminder Schedule\n" + "=" * 40 + "\n\n"
        for r in reminders:
            txt_out += f"{r['remind_on']} -> {r['message']}\n"
            
        st.download_button("Download Briefing (TXT)", data=txt_out, file_name="calculated_reminders.txt", mime="text/plain")
        with st.expander("Preview Plain Text"):
            st.code(txt_out, language='text')

