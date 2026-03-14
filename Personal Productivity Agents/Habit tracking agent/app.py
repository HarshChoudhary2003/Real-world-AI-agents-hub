import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import csv
import io
import agent

# ==========================================
# PAGE CONFIGURATION & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="StreakForge AI | Pro", page_icon="🔥", layout="wide")

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4 { color: #FFFFFF !important; font-weight: 700 !important; }

    /* Premium Badges */
    .premium-badge {
        background: linear-gradient(135deg, #F97316 0%, #C2410C 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Cards Simulation */
    .habit-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        transition: transform 0.2s;
        border-top: 4px solid #F97316;
    }
    .habit-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }
    
    .streak-badge { background: rgba(249, 115, 22, 0.2); color: #F97316; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 1.1em; display: inline-block; margin-bottom: 5px;}
    .meta-badge { background: #334155; padding: 4px 10px; border-radius: 8px; font-size: 0.8em; margin-left: 10px; color: #E2E8F0; font-weight:600;}
    
    /* Success / Fail text */
    .txt-success { color: #10B981; font-weight: bold; }
    .txt-fail { color: #EF4444; font-weight: bold; }
    
    /* Input Area styling */
    .stTextInput input, .stFileUploader > div > div { background-color: #1E293B !important; color: white !important;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🔥 StreakForge AI")
    st.markdown('<div class="premium-badge">Algorithmic Habit Tracking</div>', unsafe_allow_html=True)
    st.markdown("Track streaks, visualize consistency waveforms, and let the algorithm mathematically identify your operational blind spots.")

# ==========================================
# SIDEBAR / SETTINGS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3257/3257258.png", width=60)
    st.title("Engine Config")
    
    st.markdown("### ⚙️ Provider Selection")
    provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic", "Google Gemini"])
    
    st.markdown("### 🔑 Artificial Intelligence")
    api_key = st.text_input(f"{provider} API Key", type="password", help=f"Enter your {provider} API Key to unlock the AI Habit Coach.")
    
    if not api_key:
        st.warning("⚠️ Enter API Key to unlock AI features.")
    else:
        st.success("🤖 AI Features Active")

    st.markdown("### ⚙️ Engine Level")
    if provider == "OpenAI":
        model_choice = st.selectbox("LLM Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], index=1)
    elif provider == "Anthropic":
        model_choice = st.selectbox("LLM Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"], index=2)
    elif provider == "Google Gemini":
        model_choice = st.selectbox("LLM Model", ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"], index=1)
    
    st.markdown("---")
    st.markdown("### 📊 Metrics")
    st.info("The algorithm actively tracks your persistence density and flags routines dropping below 75% consistency for immediate recalibration.")
    
# ==========================================
# MAIN INTERFACE
# ==========================================
tab_dashboard, tab_visuals, tab_export = st.tabs(["⚡ Core Dashboard", "📈 Progression Optics", "💾 Export Hub"])

# ----------------- DATA LOADING -----------------
records = []
uploaded_file = st.sidebar.file_uploader("📂 Upload habits.csv", type=["csv"], help="Or leave empty to read local `habits.csv`.")

if uploaded_file is not None:
    try:
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        reader = csv.DictReader(stringio)
        for row in reader:
            records.append({
                "habit": row["habit"],
                "date": agent.parse_date(row["date"]),
                "completed": row["completed"].lower() == "yes",
                "notes": row.get("notes", "")
            })
    except Exception as e:
        st.error(f"Failed to parse uploaded CSV: {e}")
else:
    try:
        records = agent.read_habits()
    except Exception:
        pass

if not records:
    st.info("No habit payload detected. Upload your sequence logs on the left panel to initialize.")
    st.stop()
    
# Process Data
analysis_results = agent.analyze_habits(records)

with tab_dashboard:
    st.subheader("🧠 Algorithmic Consistency Engine")
    
    # Render Cards into a flex layout simulation using columns if few, or a loop
    col1, col2 = st.columns(2)
    
    cards = list(analysis_results.items())
    
    for i, (habit_name, r) in enumerate(cards):
        with (col1 if i % 2 == 0 else col2):
             st.markdown(f"""
             <div class="habit-card">
                <h3>{habit_name}</h3>
                <div class="streak-badge">🔥 {r['current_streak']} Day Streak</div>
                <div class="meta-badge">Target Rate: <span class="{'txt-success' if r['consistency_percent'] >= 75 else 'txt-fail'}">{r['consistency_percent']}%</span></div>
                
                <hr style="border:1px solid #334155;">
                <p><strong>System Insight:</strong> {r['insight']}</p>
                <p style="color:#94A3B8;"><strong>Algorithm Directive:</strong> {r['recommendation']}</p>
                
             </div>
             """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("💡 AI Habit Coach")
    if st.button("Generate Personalized Neural Coaching 🚀"):
        if not api_key:
            st.error("Access Denied: Please provide an active API Key in the sidebar.")
        else:
            with st.spinner(f"Neural networks ({provider}) are analyzing your consistency density..."):
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

                    prompt = f"Act as an elite personal coach. Review the user's habit tracking consistency data:\n{json.dumps(analysis_results)}\n\nProvide a harsh but highly motivational 3-4 sentence evaluation of their performance and what they need to fix tomorrow."
                    response = completion(
                        model=model_str,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    st.info(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Engine Failure: {str(e)}")


with tab_visuals:
    st.header("📈 Data Velocity")
    
    if len(analysis_results) > 0:
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("#### Consistency Vectors")
            df_bar = pd.DataFrame([
                {"Habit": k, "Consistency %": v["consistency_percent"]} for k,v in analysis_results.items()
            ])
            fig_bar = px.bar(df_bar, x="Habit", y="Consistency %", color="Consistency %",
                             color_continuous_scale=px.colors.diverging.RdYlGn,
                             title="Overall Habit Precision")
            # add a threshold line
            fig_bar.add_hline(y=75, line_dash="dash", line_color="orange", annotation_text="Baseline (75%)")
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with c2:
            st.markdown("#### Streak Mass")
            df_streak = pd.DataFrame([
                {"Habit": k, "Streak": v["current_streak"]} for k,v in analysis_results.items()
            ])
            fig_str = px.bar(df_streak, x="Habit", y="Streak", color="Streak",
                             color_continuous_scale="Oranges",
                             title="Active Consecutive Days")
            fig_str.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
            st.plotly_chart(fig_str, use_container_width=True)
            
        # Draw a literal timeline for habits using scatter dots
        st.markdown("---")
        st.markdown("#### Hit/Miss Sequence Tracking")
        
        flat_logs = []
        for h, v in analysis_results.items():
            for entry in v.get('entries_log', []):
                flat_logs.append({
                    "Habit": h,
                    "Date": entry['date'],
                    "Status": "Hit" if entry['completed'] else "Missed"
                })
        
        if len(flat_logs) > 0:
            df_logs = pd.DataFrame(flat_logs)
            fig_scatter = px.scatter(df_logs, x="Date", y="Habit", color="Status", 
                                     color_discrete_map={"Hit": "#10B981", "Missed": "#EF4444"},
                                     symbol="Status", size_max=15)
            fig_scatter.update_traces(marker=dict(size=12))
            fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
            st.plotly_chart(fig_scatter, use_container_width=True)
            

with tab_export:
    st.header("💾 Integration Payloads")
    st.markdown("Download the compiled analytics arrays.")
    
    co1, co2 = st.columns(2)
    
    with co1:
        st.markdown("### Webhook / API Payload")
        json_str = json.dumps(analysis_results, indent=2)
        st.download_button("Download Logic Array (JSON)", data=json_str, file_name="habits_analysis.json", mime="application/json", use_container_width=True)
            
    with co2:
        st.markdown("### Human Logic List")
        txt_out = "Habit Tracking Summary\n" + "=" * 40 + "\n\n"
        for habit, r in analysis_results.items():
             txt_out += f"Habit: {habit}\n"
             txt_out += f"Consistency: {r['consistency_percent']}%\n"
             txt_out += f"Current Streak: {r['current_streak']} days\n"
             txt_out += f"Missed Days: {', '.join(r['missed_days']) or 'None'}\n"
             txt_out += f"Insight: {r['insight']}\n"
             txt_out += f"Recommendation: {r['recommendation']}\n\n"
             
        st.download_button("Download Blueprint (TXT)", data=txt_out, file_name="habits_summary.txt", mime="text/plain", use_container_width=True)
