import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import agent
import io
import csv
import json
from datetime import datetime
import time

try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

# ==========================================
# PAGE CONF & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="TaskBrain AI | Pro Edition", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 1.1em !important;
        background-color: #1E293B;
        border-radius: 8px;
        color: #E2E8F0;
        border: 1px solid #334155;
    }
    
    .streamlit-expanderContent {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-top: none;
    }

    /* Metric box styling */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        color: #3B82F6;
        font-weight: 800;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1.0rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Premium Badge */
    .premium-badge {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(217, 119, 6, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .ai-badge {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.70rem;
        font-weight: 700;
        margin-left: 8px;
        vertical-align: middle;
    }

    /* Cards Simulation */
    .task-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .task-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    
    /* Progress bar styling override */
    .stProgress .st-bo {
        background-color: #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🧠 TaskBrain AI")
    st.markdown('<div class="premium-badge">Enterprise Edition</div>', unsafe_allow_html=True)
    st.markdown("Harness cutting-edge AI to dynamically manage your workload, automatically break down complex tasks, and optimize your schedule.")

# ==========================================
# SIDEBAR / SETTINGS / INTELLIGENCE
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2111/2111432.png", width=60)
    st.title("Brain Settings")
    
    st.markdown("### ⚙️ Provider Selection")
    provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic", "Google Gemini"])

    st.markdown("### 🔑 Artificial Intelligence")
    api_key = st.text_input(f"{provider} API Key", type="password", help=f"Enter your {provider} API Key to unlock advanced NLP parsing, AI Briefings, and subtask generation.")
    
    if not api_key:
        st.warning("⚠️ Enter API Key to unlock AI features.")
    else:
        st.success("🤖 AI Features Active")

    st.markdown("### ⚙️ Engine Level")
    if provider == "OpenAI":
        model_choice = st.selectbox("LLM Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], index=2)
    elif provider == "Anthropic":
        model_choice = st.selectbox("LLM Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"], index=2)
    elif provider == "Google Gemini":
        model_choice = st.selectbox("LLM Model", ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"], index=1)

    ai_personality = st.selectbox(
        "AI Assistant Personality", 
        ["Executive Coach (Professional)", "Drill Sergeant (Strict)", "Zen Master (Calm)"]
    )

    st.markdown("---")
    st.markdown("### ⏱️ Agent Constraints")
    agent.AVAILABLE_MIN = st.number_input(
        "Available bandwidth today (min)", 
        min_value=15, max_value=1440, value=agent.AVAILABLE_MIN, step=15
    )

    st.markdown("### ⚖️ Algorithmic Weights")
    agent.WEIGHTS["urgency"] = st.slider("Urgency Weight", 0.0, 10.0, agent.WEIGHTS["urgency"], 0.5)
    agent.WEIGHTS["importance"] = st.slider("Importance Weight", 0.0, 10.0, agent.WEIGHTS["importance"], 0.5)
    agent.WEIGHTS["quickwin_bonus"] = st.slider("Quickwin Bonus", 0.0, 10.0, agent.WEIGHTS["quickwin_bonus"], 0.5)

# ==========================================
# AI HELPER FUNCTIONS
# ==========================================
from litellm import completion
import os

def get_ai_briefing(plan_summary, personality_str, key, provider, model_choice):
    if not LITELLM_AVAILABLE or not key:
        return "AI Module Offline. Please verify your API Key and ensure `litellm` is installed."
    try:
        if provider == "OpenAI":
            os.environ["OPENAI_API_KEY"] = key
            model_str = model_choice
        elif provider == "Anthropic":
            os.environ["ANTHROPIC_API_KEY"] = key
            model_str = model_choice
        elif provider == "Google Gemini":
            os.environ["GEMINI_API_KEY"] = key
            model_str = f"gemini/{model_choice}"

        prompt = f"""
        Act as a {personality_str} for a high-performing professional.
        Review this daily plan summary:
        {plan_summary}
        
        Provide a short (3-4 sentences), highly motivational morning briefing highlighting what they need to focus on today. 
        """
        response = completion(
            model=model_str,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Initialization Error: {e}"

def generate_subtasks(title, description, key, provider, model_choice):
    if not LITELLM_AVAILABLE or not key:
        time.sleep(1) # simulate loading for demo
        return ["[DEMO MODE] Review requirements", "[DEMO MODE] Draft initial outline", "[DEMO MODE] Execute task"]
    
    try:
        if provider == "OpenAI":
            os.environ["OPENAI_API_KEY"] = key
            model_str = model_choice
        elif provider == "Anthropic":
            os.environ["ANTHROPIC_API_KEY"] = key
            model_str = model_choice
        elif provider == "Google Gemini":
            os.environ["GEMINI_API_KEY"] = key
            model_str = f"gemini/{model_choice}"

        prompt = f"Break down the following task into 3-4 highly actionable and short subtasks.\nTask: {title}\nDesc: {description}"
        response = completion(
            model=model_str,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.5
        )
        tasks = response.choices[0].message.content.strip().split('\n')
        return [t.strip("-").strip("1234567890. ") for t in tasks if t.strip()]
    except Exception as e:
        return [f"Error: {e}"]

# ==========================================
# MAIN CONTENT / TABS
# ==========================================
tab_dashboard, tab_insights, tab_nlp = st.tabs([
    "📊 Commander Dashboard", 
    "📈 Analytics & Insights", 
    "🗣️ Voice/Text Ingestion"
])

# ----------------- DATA LOADING -----------------
uploaded_file = st.sidebar.file_uploader("📂 Upload tasks.csv", type=["csv"], help="Or leave empty to use default local file.")
tasks = []

if uploaded_file is not None:
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    reader = csv.DictReader(stringio)
    for row in reader:
        try:
            tasks.append(agent.Task(
                title=(row.get("title") or "").strip(),
                description=(row.get("description") or "").strip(),
                deadline=agent.parse_date(row.get("deadline") or ""),
                effort_min=agent.parse_effort(row.get("effort") or ""),
                impact=agent.IMPACT_MAP.get((row.get("impact") or "medium").strip().lower(), 2),
                blocked=agent.parse_bool(row.get("blocked") or "no"),
                tags=[t.strip() for t in (row.get("tags") or "").split(",") if t.strip()]
            ))
        except:
            pass
else:
    try:
        tasks = agent.read_tasks("tasks.csv")
    except Exception as e:
        st.error(f"Error loading tasks: {e}")

if not tasks:
    st.info("No active tasks found in memory grid. Please upload a dataset.")
    st.stop()

plan = agent.build_plan(tasks)

# ----------------- T1: DASHBOARD -----------------
with tab_dashboard:
    allocated = plan.get('daily_effort_allocated', 0)
    limit = plan.get('daily_effort_limit', 1)
    
    # Exec Briefing Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Pending Tasks", len(tasks))
    m2.metric("Bandwidth Used", f"{allocated}m", f"MAX: {limit}m", delta_color="off")
    m3.metric("High Impact Targets", len([t for t in tasks if t.impact == 3]))
    m4.metric("Roadblocks (Blocked)", len([t for t in tasks if t.blocked]), delta_color="inverse")
    
    st.progress(min(allocated / limit, 1.0) if limit > 0 else 0)
    
    # --- AI Morning Briefing ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🌅 Executive AI Briefing <span class='ai-badge'>AUTO-GEN</span>", unsafe_allow_html=True)
    
    if st.button("Generate Today's Briefing 🤖"):
        with st.spinner("Compiling tactical briefing..."):
            summary_txt = agent.render_summary(plan)
            briefing = get_ai_briefing(summary_txt, ai_personality, api_key, provider, model_choice)
            st.info(briefing, icon="💬")
    
    st.markdown("<br>---", unsafe_allow_html=True)

    # --- Render Task Engine ---
    def display_premium_tasks(title, task_list, icon):
        st.markdown(f"### {icon} {title}")
        if not task_list:
            st.markdown("*No tasks mapping to this matrix.*", unsafe_allow_html=True)
            return
            
        for idx, task in enumerate(task_list, 1):
            with st.expander(f"{task['title']}  |  ⏱️ {task['effort_min']}m"):
                c1, c2, c3 = st.columns(3)
                c1.write(f"**Impact:** {'High' if task['impact']==3 else 'Medium' if task['impact']==2 else 'Low'}")
                c2.write(f"**Deadline:** {task['deadline'] if task['deadline'] else 'None'}")
                c3.write(f"**AI Engine Score:** {task['score']}")
                
                if task['description']:
                    st.markdown(f"<p style='color:#94A3B8; font-size: 0.9em;'>{task['description']}</p>", unsafe_allow_html=True)
                
                # Breakdown
                cols_b = st.columns(2)
                with cols_b[0]:
                    st.write("**Scoring Vector:**")
                    st.json(task['score_breakdown'])
                with cols_b[1]:
                    if st.button("Generate Sub-tasks 🤖", key=f"sub_{title}_{idx}"):
                        with st.spinner("AI is analyzing task dependencies..."):
                            subtasks = generate_subtasks(task['title'], task['description'], api_key, provider, model_choice)
                            st.write("**Recommended Action Plan:**")
                            for sbt in subtasks:
                                st.markdown(f"- {sbt}")

    # Layout logic
    c_left, c_right = st.columns(2)
    with c_left:
        display_premium_tasks("Alpha Priority", plan["top3"], "🚀")
        display_premium_tasks("Roadblocks", plan["unblock"], "🛑")
    with c_right:
        display_premium_tasks("Bravo (Next Items)", plan["next5"], "🎯")
        display_premium_tasks("Backlog / Delegable", plan["defer"], "💤")

    st.markdown("---")
    st.markdown("### 💾 Export Operational Plan")
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        st.download_button("Download Raw JSON", data=json.dumps(plan, indent=2), file_name="tactical_plan.json", mime="application/json")
    with col_ex2:
        st.download_button("Download Briefing TXT", data=agent.render_summary(plan), file_name="tactical_plan.txt", mime="text/plain")


# ----------------- T2: INSIGHTS & ANALYTICS -----------------
with tab_insights:
    st.header("📈 Algorithmic Insights")
    st.markdown("Deep dive into your workload distribution.")
    
    df_tasks = pd.DataFrame([{
        "Title": t.title, 
        "Effort (min)": t.effort_min, 
        "Impact Level": "High" if t.impact==3 else "Medium" if t.impact==2 else "Low",
        "Type": "Blocked" if t.blocked else "Clear",
        "Urgency Score": round(agent.urgency_score(agent.days_until(t.deadline)), 2)
    } for t in tasks])

    r1c1, r1c2 = st.columns(2)
    
    with r1c1:
        # Pie Chart of Impact
        fig_pie = px.pie(df_tasks, names='Impact Level', title="Workload by Impact Level", hole=0.4, 
                         color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B'])
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig_pie, use_container_width=True)

    with r1c2:
        # Scatter of Effort vs Urgency
        fig_scatter = px.scatter(df_tasks, x="Effort (min)", y="Urgency Score", color="Impact Level", size="Effort (min)", 
                                 hover_name="Title", title="Effort vs Urgency Matrix")
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Bar chart
    fig_bar = px.bar(df_tasks.sort_values('Effort (min)', ascending=False), x="Title", y="Effort (min)", color="Type", title="Task Bandwidth Requirements")
    fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
    st.plotly_chart(fig_bar, use_container_width=True)


# ----------------- T3: NLP INGESTION -----------------
with tab_nlp:
    st.header("🗣️ Intelligent Agent Entry")
    st.markdown("Ditch the forms. Talk to the system naturally, and the AI will extract variables automatically to push into your engine.")
    
    user_input = st.text_area("What's on your mind?", placeholder="e.g., Remind me to call John tomorrow to close the deal. Should take 15 mins, incredibly important.", height=150)
    
    if st.button("Ingest Task ⚡"):
        if not api_key:
            st.error("Access Denied: Please enter your OpenAI API key in the sidebar.")
        else:
            with st.spinner("Processing neural ingestion..."):
                try:
                    if provider == "OpenAI":
                        os.environ["OPENAI_API_KEY"] = api_key
                        model_str = model_choice
                    elif provider == "Anthropic":
                        os.environ["ANTHROPIC_API_KEY"] = api_key
                        model_str = model_choice
                    elif provider == "Google Gemini":
                        os.environ["GEMINI_API_KEY"] = api_key
                        model_str = f"gemini/{model_choice}"

                    prompt = f"""
                    Extract task details from this raw input: "{user_input}"
                    
                    Return ONLY valid JSON matching this schema exactly (no markdown formatting, no code blocks):
                    {{
                        "title": "Short succinct title",
                        "description": "Expanded description",
                        "deadline": "YYYY-MM-DD",
                        "effort_min": 15, // standard integer representing minutes
                        "impact": "high" // must be low, medium, or high
                    }}
                    """

                    response = completion(
                        model=model_str,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.1
                    )
                    
                    extracted_text = response.choices[0].message.content.strip()
                    # Strip standard markdown block string wrappers if it added them
                    if extracted_text.startswith("```json"):
                        extracted_text = extracted_text[7:-3].strip()
                    elif extracted_text.startswith("```"):
                        extracted_text = extracted_text[3:-3].strip()
                        
                    parsed = json.loads(extracted_text)
                    st.success("Task successfully ingested and processed by AI Engine.")
                    
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        st.json(parsed)
                    with col_p2:
                        st.markdown("### Extracted Values:")
                        st.write(f"**Title:** {parsed.get('title')}")
                        st.write(f"**Est. Effort:** {parsed.get('effort_min')}m")
                        st.write(f"**Impact:** {str(parsed.get('impact')).upper()}")
                    
                    st.info("💡 Note: In production mode, this object is directly written to your central tasks database overlay.")

                except Exception as e:
                    st.error(f"Neural processing failed. Is your prompt clear? System Error: {e}")
