import streamlit as st
import json
import plotly.express as px
import pandas as pd
from datetime import date
from io import StringIO
import agent

# ==========================================
# PAGE CONFIGURATION & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="Reflect AI | Pro", page_icon="🧘", layout="wide")

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
        background: linear-gradient(135deg, #10B981 0%, #047857 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Info Cards */
    .insight-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        border-left: 4px solid #3B82F6;
        transition: transform 0.2s;
    }
    .insight-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }
    
    .lesson-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        border-left: 4px solid #F59E0B;
    }
    
    .suggestion-card {
        background: rgba(16, 185, 129, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px dashed #10B981;
        margin-bottom: 1rem;
    }

    /* Standard inputs */
    .stTextInput input, .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: white !important; 
        border: 1px solid #475569 !important;
    }
    
    .metric-value { font-size: 2.2em; font-weight: 900; }
    .metric-blue { color: #3B82F6; }
    .metric-red { color: #EF4444; }
    .metric-green { color: #10B981; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🧘 Reflect AI")
    st.markdown('<div class="premium-badge">Cognitive Mirror Engine</div>', unsafe_allow_html=True)
    st.markdown("Quantify your productivity. Compare what you planned against what you achieved, and let the AI extract deep operational insights and build algorithmic improvements for tomorrow.")

# ==========================================
# SIDEBAR / SETTINGS
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3257/3257258.png", width=60)
    st.title("Engine Config")
    
    st.markdown("### ⚙️ Provider Selection")
    provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic", "Google Gemini"])
    
    st.markdown("### 🔑 Authentication")
    api_key = st.text_input(f"{provider} API Key", type="password", help=f"Enter your {provider} API Key.")
    
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
tab_entry, tab_dashboard = st.tabs(["📝 Daily Input", "📊 Analytics Dashboard"])

with tab_entry:
    col_input, col_output = st.columns([1, 1.3], gap="large")
    
    with col_input:
        st.subheader("📥 Journal Context")
        
        # Interactive Form Entry
        t_planned = st.text_area("🎯 Planned Goals (What you wanted to do):", value="Finish client proposal\nReview PRs\nGo for a 30-minute walk", height=120)
        t_actual = st.text_area("✅ Actual Outcomes (What you actually did):", value="Finished client proposal\nReviewed only 1 PR\nSkipped walk", height=120)
        t_notes = st.text_area("🧠 Friction Notes (Why things changed):", value="Unexpected production issue took 2 hours.\nEnergy level was low in the afternoon.", height=120)
        
        day_text = f"Planned Goals:\n{t_planned}\n\nActual Outcomes:\n{t_actual}\n\nNotes:\n{t_notes}"
        
        process_btn = st.button("Generate AI Reflection 🚀", type="primary", use_container_width=True)

    with col_output:
        st.subheader("🧠 Synthesized Optics")
        
        if process_btn:
            if not api_key:
                st.error("Authentication Error: Active OpenAI API Key required.")
            elif not t_planned.strip() or not t_actual.strip():
                st.warning("Please provide both Planned and Actual outcomes to reflect upon.")
            else:
                with st.spinner(f"Neural networks ({provider}) are finding patterns..."):
                    try:
                        import os
                        from litellm import completion
                        
                        # Load the appropriate API key into environment for litellm
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
                                {"role": "user", "content": day_text}
                            ],
                            temperature=0.3
                        )
                        
                        content = response.choices[0].message.content.strip()
                        if content.startswith("```json"): content = content[7:-3].strip()
                        elif content.startswith("```"): content = content[3:-3].strip()
                        
                        result = json.loads(content)
                        st.session_state['latest_reflection'] = result # Save for analytics
                        
                        st.success("Successfully analyzed timeline friction.")
                        st.info(f"**Executive Summary:** {result.get('summary', 'Memory Empty.')}")
                        
                        # Results View
                        st.markdown("### 🔍 Core Insights")
                        for idx, insight in enumerate(result.get('insights', [])):
                            st.markdown(f"<div class='insight-card'>💡 {insight}</div>", unsafe_allow_html=True)
                            
                        st.markdown("### 📚 Lessons Learned")
                        for idx, lesson in enumerate(result.get('lessons_learned', [])):
                            st.markdown(f"<div class='lesson-card'>⚠️ {lesson}</div>", unsafe_allow_html=True)
                            
                        st.markdown("### 🌅 Actionable Protocol For Tomorrow")
                        for idx, sugg in enumerate(result.get('tomorrow_suggestions', [])):
                            st.markdown(f"<div class='suggestion-card'><strong>{idx+1}.</strong> {sugg}</div>", unsafe_allow_html=True)
                            
                        # Export Logic
                        st.markdown("---")
                        st.markdown("### 💾 Payload Export")
                        c1, c2 = st.columns(2)
                        c1.download_button("Download Raw JSON", data=json.dumps(result, indent=2), file_name="reflection.json", mime="application/json")
                        
                        txt_out = f"Daily Reflection ({date.today()})\n"
                        txt_out += "=" * 45 + "\n\n"
                        txt_out += "SUMMARY:\n" + result.get("summary", "") + "\n\n"
                        txt_out += "COMPLETED GOALS:\n"
                        for g in result.get("completed_goals", []): txt_out += f"- {g}\n"
                        txt_out += "\nMISSED GOALS:\n"
                        for g in result.get("missed_goals", []): txt_out += f"- {g}\n"
                        txt_out += "\nINSIGHTS:\n"
                        for i in result.get("insights", []): txt_out += f"- {i}\n"
                        txt_out += "\nLESSONS LEARNED:\n"
                        for l in result.get("lessons_learned", []): txt_out += f"- {l}\n"
                        txt_out += "\nSUGGESTIONS FOR TOMORROW:\n"
                        for s in result.get("tomorrow_suggestions", []): txt_out += f"- {s}\n"
                        
                        c2.download_button("Download Text Briefing", data=txt_out, file_name="reflection.txt", mime="text/plain")

                    except Exception as e:
                        st.error(f"Engine Failure: {str(e)}")
        else:
            if 'latest_reflection' not in st.session_state:
                st.markdown("""
                <div style="text-align: center; padding: 60px; color: #64748B; border: 2px dashed #334155; border-radius: 12px; margin-top: 20px;">
                    <h3>Awaiting Journal Logs</h3>
                    <p>Enter your daily achievements and friction logs to decode the patterns holding you back.</p>
                </div>
                """, unsafe_allow_html=True)

with tab_dashboard:
    st.header("Daily Velocity Analytics")
    if 'latest_reflection' in st.session_state:
        re_data = st.session_state['latest_reflection']
        
        completed = len(re_data.get('completed_goals', []))
        missed = len(re_data.get('missed_goals', []))
        total = completed + missed
        velocity = int((completed / total * 100)) if total > 0 else 0
        
        # Top Metrics
        m1, m2, m3 = st.columns(3)
        m1.markdown(f"<div style='text-align:center;'><div class='metric-value metric-green'>{completed}</div><div>Targets Destroyed 🎯</div></div>", unsafe_allow_html=True)
        m2.markdown(f"<div style='text-align:center;'><div class='metric-value metric-red'>{missed}</div><div>Targets Missed 🛑</div></div>", unsafe_allow_html=True)
        m3.markdown(f"<div style='text-align:center;'><div class='metric-value metric-blue'>{velocity}%</div><div>Daily Velocity ⚡</div></div>", unsafe_allow_html=True)
        
        st.markdown("<br><hr>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🎯 Accuracy Chart")
            if total > 0:
                df = pd.DataFrame({
                    "Status": ["Completed", "Missed"],
                    "Count": [completed, missed]
                })
                fig = px.pie(df, values="Count", names="Status", hole=0.5, color="Status", 
                             color_discrete_map={"Completed": "#10B981", "Missed": "#EF4444"})
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data mathematically tracked.")
                
        with c2:
            st.markdown("### 📝 Objective Breakdown")
            st.markdown("**Victory Logs:**")
            for g in re_data.get('completed_goals', []):
                st.markdown(f"- ✅ <span style='color:#10B981;'>{g}</span>", unsafe_allow_html=True)
                
            st.markdown("**Missed Objectives:**")
            for g in re_data.get('missed_goals', []):
                st.markdown(f"- 🛑 <span style='color:#EF4444;'>{g}</span>", unsafe_allow_html=True)
    else:
        st.info("Execute a reflection in the 'Daily Input' tab first to see quantified analytics.")


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
