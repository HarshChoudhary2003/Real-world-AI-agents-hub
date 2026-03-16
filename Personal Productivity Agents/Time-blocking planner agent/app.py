import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime
import json
import csv
import io
import agent

# ==========================================
# PAGE CONFIGURATION & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="ChronoBlock AI | Pro", page_icon="⏳", layout="wide")

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4 { color: #FFFFFF !important; font-weight: 700 !important; }

    /* Premium Badges */
    .premium-badge {
        background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(14, 165, 233, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Cards Simulation */
    .block-card {
        background: #1E293B;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 0.8rem;
        transition: transform 0.2s;
    }
    .block-card:hover { transform: translateX(5px); box-shadow: -5px 5px 15px -3px rgba(0,0,0,0.5); }
    
    .priority-high { border-left: 4px solid #EF4444; }
    .priority-medium { border-left: 4px solid #F59E0B; }
    .priority-low { border-left: 4px solid #10B981; }

    /* Small labels */
    .time-badge { background: #0B0F19; color: #38BDF8; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 0.9em; display: inline-block; margin-bottom: 5px;}
    .meta-badge { background: #334155; padding: 2px 8px; border-radius: 8px; font-size: 0.8em; margin-left: 10px; color: #E2E8F0;}
    
    /* Input Area styling */
    .stTextInput input, .stFileUploader > div > div { background-color: #1E293B !important; color: white !important;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("⏳ ChronoBlock AI")
    st.markdown('<div class="premium-badge">Algorithmic Time-Boxing Engine</div>', unsafe_allow_html=True)
    st.markdown("Automate your daily calendar. The engine mathematically stacks your priorities into contiguous time blocks, strictly adhering to your operational hours and avoiding fatigue.")

# ==========================================
# SIDEBAR / SETTINGS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=60)
    st.title("Engine Config")
    
    st.markdown("### ⚙️ Provider Selection")
    provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic", "Google Gemini"])
    
    st.markdown("### 🔑 Artificial Intelligence")
    api_key = st.text_input(f"{provider} API Key", type="password", help=f"Enter your {provider} API Key to unlock AI Schedule Optimization.")
    
    if not api_key: st.warning("⚠️ Enter API Key to unlock AI features.")
    else: st.success("🤖 AI Features Active")

    st.markdown("### ⚙️ Engine Level")
    if provider == "OpenAI":
        model_choice = st.selectbox("LLM Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], index=1)
    elif provider == "Anthropic":
        model_choice = st.selectbox("LLM Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"], index=2)
    elif provider == "Google Gemini":
        model_choice = st.selectbox("LLM Model", ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"], index=1)
        
    st.markdown("---")
    
    st.markdown("### ⚙️ Operating Hours")
    start_str = st.time_input("Start Threshold", value=datetime.strptime("09:00", "%H:%M").time())
    end_str = st.time_input("End Threshold", value=datetime.strptime("17:00", "%H:%M").time())
    
    agent.WORKDAY_START = start_str.strftime("%H:%M")
    agent.WORKDAY_END = end_str.strftime("%H:%M")
    
    st.markdown("### 🎛️ Algorithm Tuning")
    agent.BUFFER_MINUTES = st.number_input("Context-Switch Buffer (minutes)", min_value=0, max_value=60, value=agent.BUFFER_MINUTES, step=5)
    
# ==========================================
# MAIN INTERFACE
# ==========================================
tab_dashboard, tab_gantt, tab_export = st.tabs(["⚡ Core Dashboard", "📅 Gantt Optics", "💾 Export Hub"])

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
                "effort": int(row["effort_minutes"]),
                "priority": row["priority"].lower()
            })
    except Exception as e:
        st.error(f"Failed to parse uploaded CSV: {e}")
else:
    try:
        tasks = agent.read_tasks()
    except Exception:
        pass

if not tasks:
    st.info("No tracking sequence active. Upload a tasks CSV on the left panel to begin algorithmic generation.")
    st.stop()
    
# Process Data
schedule, overflow = agent.generate_schedule(tasks)


with tab_dashboard:
    col_input, col_output = st.columns([1, 1.3], gap="large")
    
    with col_input:
        st.subheader("📚 Target Queue")
        
        df_tasks = pd.DataFrame(tasks)
        
        # Color code priority in basic dataframe
        st.dataframe(
            df_tasks, 
            use_container_width=True, hide_index=True
        )
        
        if len(overflow) > 0:
            st.error(f"⚠️ Warning: {len(overflow)} task(s) exceeded available time and spilled onto the floor.")
            for o in overflow:
                st.markdown(f"- **{o.get('task')}** ({o.get('effort')} min | {o.get('priority')})")

    with col_output:
        st.subheader("🧠 Structuring Complete")
        
        for idx, block in enumerate(schedule):
            p_class = f"priority-{block['priority']}"
            st.markdown(f"""
            <div class="block-card {p_class}">
                <div class="time-badge">{block['start']} - {block['end']}</div>
                <h4 style='margin: 8px 0 0 0;'>{block['task']}</h4>
                <div style="margin-top: 5px;">
                    <span class="meta-badge">⏱️ {block['duration']} mins</span>
                    <span class="meta-badge" style="text-transform: capitalize;">{block['priority']} Priority</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Draw buffer block if not the last item
            if idx < len(schedule) - 1 and agent.BUFFER_MINUTES > 0:
                st.markdown(f"""
                <div style="text-align: center; color: #64748B; font-size: 0.8em; margin-bottom: 0.8rem;">
                    ↓ {agent.BUFFER_MINUTES} min Cognitive Buffer
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        st.subheader("💡 AI Schedule Optimizer")
        if st.button("Generate Neural Optimization Review 🚀"):
            if not api_key:
                st.error("Access Denied: Please provide an active API Key in the sidebar.")
            else:
                with st.spinner(f"Neural networks ({provider}) are analyzing your time block density..."):
                    try:
                        import os
                        from litellm import completion
                        
                        if provider == "OpenAI":
                            os.environ["OPENAI_API_KEY"] = api_key
                            model_str = model_choice
                        elif provider == "Anthropic":
                            os.environ["ANTHROPIC_API_KEY"] = api_key
                            model_str = model_choice
                        elif provider == "Google Gemini":
                            os.environ["GEMINI_API_KEY"] = api_key
                            model_str = f"gemini/{model_choice}"

                        payload = {"schedule": schedule, "overflow": overflow}
                        prompt = f"Act as an elite time-management executive assistant. Review the user's daily time-blocking schedule and overflow list:\n{json.dumps(payload)}\n\nProvide a short, 3-4 sentence evaluation. Identify any dangerous context-switching, risk of burnout, or strategic advice for handling the overflow tasks."
                        response = completion(
                            model=model_str,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.7
                        )
                        st.info(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Engine Failure: {str(e)}")

with tab_gantt:
    st.header("📅 Visual Time Stacking")
    
    if len(schedule) > 0:
        gantt_data = []
        today_date = datetime.today().strftime('%Y-%m-%d')
        
        for block in schedule:
            s_time = f"{today_date} {block['start']}:00"
            e_time = f"{today_date} {block['end']}:00"
            gantt_data.append({
                "Task": block['task'],
                "Start": s_time,
                "Finish": e_time,
                "Priority": block['priority'].capitalize()
            })
            
        df_g = pd.DataFrame(gantt_data)
        
        fig = px.timeline(df_g, x_start="Start", x_end="Finish", y="Task", color="Priority",
                          color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"})
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("No logic generated to display.")

with tab_export:
    st.header("💾 Integration Payloads")
    st.markdown("Download the fully assembled logic array to pipe directly into your Google Calendar or output to a readable file.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Webhook / API Payload")
        payload = {"schedule": schedule, "overflow": overflow}
        json_str = json.dumps(payload, indent=2)
        st.download_button("Download Logic Array (JSON)", data=json_str, file_name="time_blocks.json", mime="application/json", use_container_width=True)
            
    with col2:
        st.markdown("### Human Logic List")
        txt_out = "Daily Time-Blocked Schedule\n" + "=" * 40 + "\n\n"
        for b in schedule:
             txt_out += f"{b['start']} - {b['end']}: {b['task']}\n"
             
        if len(overflow) > 0:
            txt_out += "\nUnscheduled Tasks (Overflow):\n"
            for t in overflow:
                txt_out += f"- {t['task']}\n"
            
        st.download_button("Download Blueprint (TXT)", data=txt_out, file_name="time_blocks.txt", mime="text/plain", use_container_width=True)


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
