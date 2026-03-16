import streamlit as st
import pandas as pd
import json
import os
from datetime import date
from io import StringIO
import agent

# ==========================================
# PAGE CONFIGURATION & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="ActionForge AI | Pro", page_icon="⚡", layout="wide")

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
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 800;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Cards Simulation */
    .action-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
        transition: transform 0.2s;
        border-left: 4px solid #3B82F6;
    }
    .action-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }
    
    .priority-High { border-left-color: #EF4444 !important; }
    .priority-Medium { border-left-color: #F59E0B !important; }
    .priority-Low { border-left-color: #10B981 !important; }
    
    .meta-badge { background: #0B0F19; padding: 4px 10px; border-radius: 6px; font-size: 0.8em; font-weight: 600; color: #94A3B8; margin-right: 10px; display: inline-block; margin-top:10px;}
    
    /* Standard inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div { 
        background-color: #1E293B !important; 
        color: white !important; 
        border: 1px solid #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("⚡ ActionForge AI")
    st.markdown('<div class="premium-badge">Neural Task Extractor</div>', unsafe_allow_html=True)
    st.markdown("Instantly transform chaotic meeting notes, brainstorming rambles, or loose ideas into highly structured, actionable database entries.")

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
tab_ingest, tab_board = st.tabs(["📝 Ingest Notes", "📋 Action Board"])

with tab_ingest:
    col_input, col_output = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.subheader("📥 Raw Context")
        
        default_notes = "We agreed to finalize the onboarding checklist by next Friday.\nSomeone should follow up with the vendor about pricing.\nMarketing needs to prepare a launch email.\nThe new feature looks promising, but we need more user feedback.\nDecided to move the release to April."
        
        source = st.radio("Source Material", ["Paste Text", "File Upload"], horizontal=True)
        if source == "Paste Text":
            notes_text = st.text_area("Dump chaotic text here:", value=default_notes, height=350)
        else:
            uploaded = st.file_uploader("Upload .txt file")
            if uploaded:
                stringio = StringIO(uploaded.getvalue().decode("utf-8"))
                notes_text = stringio.read()
            else:
                notes_text = ""
                st.info("Awaiting file upload...")
                
        process_btn = st.button("Synthesize Tasks 🚀", type="primary", use_container_width=True)

    with col_output:
        st.subheader("🧠 Processed Intelligence")
        
        if process_btn:
            if not api_key:
                st.error("Authentication Error: Active API Key required.")
            elif not notes_text.strip():
                st.warning("Please provide notes to analyze.")
            else:
                with st.spinner(f"Neural networks ({provider}) are extracting variables..."):
                    try:
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
                                {"role": "user", "content": notes_text}
                            ],
                            temperature=0.2
                        )
                        
                        content = response.choices[0].message.content.strip()
                        if content.startswith("```json"): content = content[7:-3].strip()
                        elif content.startswith("```"): content = content[3:-3].strip()
                        
                        result = json.loads(content)
                        st.session_state['latest_actions'] = result # Save to session
                        tasks_extracted = result.get('actions', [])
                        
                        st.success(f"Successfully extracted {len(tasks_extracted)} structured actions.")
                        
                        # Preview Display
                        for a in tasks_extracted:
                            p_class = f"priority-{str(a.get('priority')).title()}"
                            st.markdown(f"""
                            <div class="action-card {p_class}">
                                <h4 style="margin:0;">{a.get('action')}</h4>
                                <div class="meta-badge">👤 {a.get('owner')}</div>
                                <div class="meta-badge">📅 {a.get('deadline')}</div>
                                <div class="meta-badge">⚠️ {a.get('priority')} Priority</div>
                                <p style="margin-top:10px; font-size: 0.9em; color:#64748B;"><i>"{a.get('source_context')}"</i></p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.error(f"Engine Failure: {str(e)}")
        else:
             if 'latest_actions' not in st.session_state:
                st.markdown("""
                <div style="text-align: center; padding: 60px; color: #64748B; border: 2px dashed #334155; border-radius: 12px; margin-top: 30px;">
                    <h3>Awaiting Upload</h3>
                    <p>Paste your chaotic meeting notes and let the system rip tasks out of them.</p>
                </div>
                """, unsafe_allow_html=True)


with tab_board:
    st.header("📋 Tactical Exports & Database Board")
    
    if 'latest_actions' in st.session_state:
        board_data = st.session_state['latest_actions'].get('actions', [])
        
        if len(board_data) > 0:
            df_board = pd.DataFrame(board_data)
            st.dataframe(df_board, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("### 💾 Core System Payload Export")
            
            c1, c2 = st.columns(2)
            json_dump = json.dumps(st.session_state['latest_actions'], indent=2)
            c1.download_button("Download API JSON payload", data=json_dump, file_name="actions.json", mime="application/json", use_container_width=True)
            
            txt_out = f"Extracted Action Items ({date.today()})\n"
            txt_out += "=" * 45 + "\n\n"
            for i, a in enumerate(board_data, 1):
                txt_out += f"{i}. {a.get('action')}\n"
                txt_out += f"   Owner: {a.get('owner')}\n"
                txt_out += f"   Deadline: {a.get('deadline')}\n"
                txt_out += f"   Priority: {a.get('priority')}\n"
                txt_out += f"   Source: {a.get('source_context')}\n\n"
            c2.download_button("Download Readable Markdown/Txt", data=txt_out, file_name="actions.txt", mime="text/plain", use_container_width=True)
            
        else:
             st.warning("No actionable tasks detected in the specific text block. Try dumping more notes.")
    else:
        st.info("Ingest notes from the parent tab first to view compiled board analytics.")


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
