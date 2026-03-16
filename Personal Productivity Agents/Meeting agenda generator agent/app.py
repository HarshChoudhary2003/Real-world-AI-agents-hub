import streamlit as st
import pandas as pd
import plotly.express as px
import json
import base64
from datetime import datetime, date, timedelta
from io import StringIO
import agent

# ==========================================
# PAGE CONFIGURATION & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="AgendaCraft AI | Pro", page_icon="📋", layout="wide")

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 700 !important; }

    /* Premium Badges */
    .premium-badge {
        background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(236, 72, 153, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Cards Simulation */
    .agenda-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        border-left: 4px solid #EC4899;
        transition: transform 0.2s;
    }
    .agenda-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }
    
    /* Small info pills */
    .time-badge { background-color: #0F172A; padding: 4px 10px; border-radius: 6px; font-weight: 600; color: #38BDF8; font-size: 14px;}
    .owner-badge { background-color: #475569; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 14px;}
    
    /* Standard inputs */
    .stTextInput input, .stTextArea textarea, .stNumberInput input { 
        background-color: #1E293B !important; 
        color: white !important; 
        border: 1px solid #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CALENDAR ICS GENERATOR
# ==========================================
def generate_ics(title, description, duration_mins):
    now = datetime.utcnow()
    # Mocking a meeting time to start in exactly 1 hour for the ICS file
    start_time = now + timedelta(hours=1)
    end_time = start_time + timedelta(minutes=duration_mins)
    
    dtstamp = now.strftime("%Y%m%dT%H%M%SZ")
    dtstart = start_time.strftime("%Y%m%dT%H%M%SZ")
    dtend = end_time.strftime("%Y%m%dT%H%M%SZ")
    
    safe_desc = description.replace("\n", "\\n")
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AgendaCraft AI//Meeting Generator//EN
BEGIN:VEVENT
UID:{dtstamp}-agendacraft@ai
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{title}
DESCRIPTION:{safe_desc}
END:VEVENT
END:VCALENDAR"""
    return ics_content

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("📋 AgendaCraft AI")
    st.markdown('<div class="premium-badge">Enterprise Meeting Architect</div>', unsafe_allow_html=True)
    st.markdown("Automate meeting structure, assign speakers, and export directly to Google Calendar/Outlook.")

# ==========================================
# SIDEBAR / SETTINGS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=60)
    st.title("Engine Config")
    
    st.markdown("### ⚙️ Provider Selection")
    provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic", "Google Gemini"])
    
    st.markdown("### 🔑 Authentication")
    api_key = st.text_input(f"{provider} API Key", type="password", help=f"Enter your {provider} API Key to unlock generation.")
    
    if not api_key: st.warning("⚠️ Enter API Key to unlock features.")
    else: st.success("🤖 Neural Engine Active")

    st.markdown("---")
    st.markdown("### ⚙️ Engine Level")
    if provider == "OpenAI":
        model_choice = st.selectbox("LLM Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], index=1)
    elif provider == "Anthropic":
        model_choice = st.selectbox("LLM Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"], index=2)
    elif provider == "Google Gemini":
        model_choice = st.selectbox("LLM Model", ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"], index=1)

# ==========================================
# MAIN INTERFACE
# ==========================================
tab_builder, tab_analytics = st.tabs(["🏗️ Builder Canvas", "📈 Meeting Analytics"])

with tab_builder:
    col_input, col_output = st.columns([1, 1.3], gap="large")
    
    with col_input:
        st.subheader("📥 Meeting Parameters")
        
        entry_mode = st.radio("Input Method:", ["Form Builder", "Raw Text Block"], horizontal=True)
        
        if entry_mode == "Form Builder":
            m_title = st.text_input("Event Title", value="Q1 Product Planning")
            m_obj = st.text_input("Core Objective", value="Decide priorities for Q1 roadmap and align teams")
            
            c1, c2 = st.columns(2)
            m_dur = c1.number_input("Duration (mins)", min_value=10, max_value=240, value=60, step=10)
            m_type = c2.selectbox("Meeting Type", ["Decision / Alignment", "Brainstorming", "Status Update", "Retrospective"])
            
            m_part = st.text_area("Participants / Departments", value="Product, Engineering, Marketing", height=68)
            m_constr = st.text_area("Specific Constraints/Focus", value="Must decide top 3 features by the end.", height=68)
            
            # Synthesize into raw text for the agent
            meeting_text = f"Meeting Title: {m_title}\nObjective: {m_obj}\nDuration: {m_dur} minutes\nMeeting Type: {m_type}\nParticipants: {m_part}\nConstraints: {m_constr}"
        else:
            default_text = "Meeting Title: Q1 Product Planning\nObjective: Decide priorities for Q1 roadmap and align teams\nDuration: 60 minutes\nMeeting Type: decision\nParticipants: Product, Engineering, Marketing\nConstraints: Must decide top 3 features"
            meeting_text = st.text_area("Paste Meeting Requirements:", value=default_text, height=400)
                
        process_btn = st.button("Generate Architecture 🚀", type="primary", use_container_width=True)
    
    with col_output:
        st.subheader("🧠 Synthesized Itinerary")
        
        if process_btn:
            if not api_key:
                st.error("Authentication Error: Active OpenAI API Key required.")
            elif not meeting_text.strip():
                st.warning("Please provide meeting context to analyze.")
            else:
                with st.spinner("Neural networks are mapping timelines..."):
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

                        response = completion(
                            model=model_str,
                            messages=[
                                {"role": "system", "content": agent.SYSTEM_PROMPT},
                                {"role": "user", "content": meeting_text}
                            ],
                            temperature=0.3
                        )
                        
                        content = response.choices[0].message.content.strip()
                        if content.startswith("```json"): content = content[7:-3].strip()
                        elif content.startswith("```"): content = content[3:-3].strip()
                            
                        result = json.loads(content)
                        st.session_state['latest_agenda'] = result # Save to session state for Analytics tab
                        
                        # --- DISPLAY RESULTS ---
                        st.success("Successfully engineered agenda.")
                        
                        # High-level Metrics
                        h1, h2, h3 = st.columns(3)
                        h1.metric("Scheduled Time", f"{result.get('total_duration_minutes', 0)} mins")
                        h2.metric("Total Agenda Items", len(result.get('agenda', [])))
                        
                        total_time = sum([item.get('time_minutes', 0) for item in result.get('agenda', [])])
                        usage_perc = min(int((total_time / result.get('total_duration_minutes', 1)) * 100), 100)
                        h3.metric("Bandwidth Usage", f"{usage_perc}%", delta=f"{total_time} mins allocated", delta_color="off")
                        
                        st.progress(usage_perc / 100.0)
                        if total_time > result.get('total_duration_minutes', 0):
                            st.error(f"⚠️ Warning: Scheduled topics sum to {total_time} mins, exceeding the {result.get('total_duration_minutes')} minute limit!")
                            
                        st.markdown("---")
                        
                        # Sequential Timeline
                        st.markdown(f"### 🎯 Mandate: *{result.get('objective', 'None provided')}*")
                        
                        txt_out = f"Meeting Agenda ({date.today()})\n"
                        txt_out += "=" * 45 + "\n\n"
                        txt_out += f"Title: {result.get('meeting_title', 'Untitled')}\n"
                        txt_out += f"Objective: {result.get('objective', '')}\n"
                        txt_out += f"Duration: {result.get('total_duration_minutes', 0)} minutes\n\n"
                        
                        for idx, item in enumerate(result.get('agenda', []), 1):
                            st.markdown(f"""
                            <div class="agenda-card">
                                <h4 style="margin-top:0;">{idx}. {item.get('topic', 'Untitled')}</h4>
                                <span class="time-badge">⏱️ {item.get('time_minutes', 0)} mins block</span>
                                <span class="owner-badge">👤 Leader: {item.get('owner', 'Unassigned')}</span>
                                <div style="margin-top: 15px; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 6px; border-left: 2px solid #38BDF8;">
                                    <strong>🎯 Required Outcome:</strong> {item.get('outcome', 'None')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            txt_out += f"{idx}. {item.get('topic', '')} ({item.get('time_minutes', 0)} min)\n"
                            txt_out += f"   Owner: {item.get('owner', '')}\n"
                            txt_out += f"   Outcome: {item.get('outcome', '')}\n\n"
                            
                        # Exports Box
                        st.markdown("---")
                        st.markdown("### 💾 Payload Export & Calendar Sync")
                        c1, c2, c3 = st.columns(3)
                        c1.download_button("Download Raw JSON", data=json.dumps(result, indent=2), file_name="agenda.json", mime="application/json")
                        c2.download_button("Copy text (TXT)", data=txt_out, file_name="agenda.txt", mime="text/plain")
                        
                        ics_data = generate_ics(result.get('meeting_title', 'Untitled'), txt_out, result.get('total_duration_minutes', 60))
                        c3.download_button("📅 Add to Google/Outlook (.ics)", data=ics_data, file_name="meeting.ics", mime="text/calendar")
                        
                    except Exception as e:
                        st.error(f"Engine Failure: {str(e)}")
        else:
            # Welcome splash when loading tab if not processed yet
            if 'latest_agenda' not in st.session_state:
                st.markdown("""
                <div style="text-align: center; padding: 60px; color: #64748B; border: 2px dashed #334155; border-radius: 12px; margin-top: 30px;">
                    <h3>Awaiting Parameters</h3>
                    <p>Configure the meeting constraints on the left and initialize the Neural Engine.</p>
                </div>
                """, unsafe_allow_html=True)


with tab_analytics:
    st.header("Meeting Flow & Analytics")
    if 'latest_agenda' in st.session_state:
        agenda_data = st.session_state['latest_agenda']
        agenda_list = agenda_data.get('agenda', [])
        
        if len(agenda_list) > 0:
            st.markdown(f"Visualizing data for: **{agenda_data.get('meeting_title', 'Meeting')}**")
            
            # --- 1. Gantt Chart Simulation ---
            r1c1, r1c2 = st.columns(2)
            
            with r1c1:
                st.markdown("#### Time Allocation by Owner")
                # Group time by owner
                owner_time = {}
                for item in agenda_list:
                    owner = item.get('owner', 'Unassigned')
                    owner_time[owner] = owner_time.get(owner, 0) + item.get('time_minutes', 0)
                
                df_pie = pd.DataFrame(list(owner_time.items()), columns=["Owner", "Minutes"])
                fig_pie = px.pie(df_pie, values='Minutes', names='Owner', hole=0.4,
                                 color_discrete_sequence=px.colors.sequential.RdBu)
                fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
                st.plotly_chart(fig_pie, use_container_width=True)

            with r1c2:
                # Generate pseudo-timeline for Gantt chart
                timeline_data = []
                # Use today + 09:00 AM as a dummy start baseline
                current_time = datetime.combine(date.today(), datetime.min.time()).replace(hour=9, minute=0)
                
                for item in agenda_list:
                    dur = item.get('time_minutes', 0)
                    end_time = current_time + timedelta(minutes=dur)
                    timeline_data.append({
                        "Topic": item.get('topic', 'Untitled'),
                        "Start": current_time,
                        "Finish": end_time,
                        "Owner": item.get('owner', 'Unassigned')
                    })
                    current_time = end_time
                    
                df_gantt = pd.DataFrame(timeline_data)
                
                st.markdown("#### Sequential Flow Timeline")
                fig_gantt = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Topic", color="Owner",
                                        title="")
                fig_gantt.update_yaxes(autorange="reversed")
                fig_gantt.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0', xaxis_title="Timeline Progression")
                # Hide actual x-axis time labels since they are dummy
                fig_gantt.update_xaxes(showticklabels=False)
                st.plotly_chart(fig_gantt, use_container_width=True)
                
            st.info("💡 **Insight:** Use these optics to verify if you are giving your critical departments enough 'air-time' during the meeting block.")
                
        else:
            st.warning("No agenda topics generated to analyze.")
    else:
        st.info("Execute a meeting generation in the 'Builder Canvas' first to view structural analytics.")


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
