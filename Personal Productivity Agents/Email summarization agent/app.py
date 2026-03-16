import streamlit as st
import json
from datetime import date
from io import StringIO
import agent

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="MailMind AI | Pro Edition", page_icon="📧", layout="wide")

st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background-color: #0B0F19;
        color: #F1F5F9;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
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

    /* Premium Badge */
    .premium-badge {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
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

    /* Cards Simulation */
    .result-card {
        background: #1E293B;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
    }
    
    .urgency-High { color: #EF4444; font-weight: 800; }
    .urgency-Medium { color: #F59E0B; font-weight: 800; }
    .urgency-Low { color: #3B82F6; font-weight: 800; }
    
    /* Input Area styling */
    .stTextArea textarea {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("📧 MailMind AI")
    st.markdown('<div class="premium-badge">Enterprise Email Intelligence</div>', unsafe_allow_html=True)
    st.markdown("Instantly digest long threads, extract strategic action items, and map project deadlines using advanced NLP.")

# ==========================================
# SIDEBAR / SETTINGS / INTELLIGENCE
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3059/3059502.png", width=60)
    st.title("Brain Settings")
    
    st.markdown("### ⚙️ Provider Selection")
    provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic", "Google Gemini"])
    
    st.markdown("### 🔑 Artificial Intelligence")
    api_key = st.text_input(f"{provider} API Key", type="password", help=f"Enter your {provider} API Key to unlock NLP summarization.")
    
    if not api_key:
        st.warning("⚠️ Enter API Key to unlock features.")
    else:
        st.success("🤖 Neural Engine Active")

    st.markdown("---")
    st.markdown("### ⚙️ Engine Parameters")
    if provider == "OpenAI":
        model_choice = st.selectbox("LLM Model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"], index=1)
    elif provider == "Anthropic":
        model_choice = st.selectbox("LLM Model", ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"], index=2)
    elif provider == "Google Gemini":
        model_choice = st.selectbox("LLM Model", ["gemini-1.5-pro-latest", "gemini-1.5-flash-latest"], index=1)
    
    st.markdown("*(Higher models provide highest logical extraction accuracy)*")

# ==========================================
# MAIN CONTENT / TABS
# ==========================================
tab_ingest, tab_history = st.tabs(["⚡ Live Processing", "📂 Batch Analytics (Coming Soon)"])

with tab_ingest:
    col_input, col_output = st.columns([1, 1.2], gap="large")
    
    with col_input:
        st.subheader("📥 Raw Context Ingestion")
        
        # Default Email Text
        default_email = """Subject: Project Timeline Update
 
Hi team,
 
We reviewed the Q1 project timeline and there are a few updates.
 
The client has requested that the initial prototype be delivered by March 10 instead of March 20.
This means design needs to finalize assets by March 5 at the latest.
 
Engineering should prioritize API integration this week.
We’ll review progress in Friday’s sync.
 
Let me know if there are concerns.
 
Thanks,
Sarah"""
        
        email_source = st.radio("Input Source:", ["Paste Text", "Upload .TXT"], horizontal=True)
        
        if email_source == "Paste Text":
            email_text = st.text_area("Paste the email chain here:", value=default_email, height=350)
        else:
            uploaded_file = st.file_uploader("Upload email/text file", type=["txt", "eml"])
            if uploaded_file is not None:
                # To read file as string:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                email_text = stringio.read()
            else:
                email_text = ""
                st.info("Awaiting file upload...")
                
        process_btn = st.button("Extract Intelligence 🚀", type="primary", use_container_width=True)

    with col_output:
        st.subheader("🧠 Synthesized Intelligence")
        
        if process_btn:
            if not api_key:
                st.error("Authentication Error: Please provide an active OpenAI API Key in the sidebar.")
            elif not email_text.strip():
                st.warning("Please provide email content to analyze.")
            else:
                with st.spinner("Neural networks are digesting context..."):
                    try:
                        # Override model via agent
                        agent_response = None
                        
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
                                {"role": "user", "content": email_text}
                            ],
                            temperature=0.2
                        )
                        content = response.choices[0].message.content.strip()
                        if content.startswith("```json"):
                            content = content[7:-3].strip()
                        elif content.startswith("```"):
                            content = content[3:-3].strip()
                            
                        result = json.loads(content)
                        
                        # --- DISPLAY RESULTS ---
                        urgency_val = result.get('urgency', 'Unknown')
                        u_class = f"urgency-{urgency_val}"
                        
                        st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
                        st.markdown(f"<h4>Urgency Level: <span class='{u_class}'>{urgency_val.upper()}</span></h4>", unsafe_allow_html=True)
                        st.markdown("---")
                        
                        st.write("### 📝 Executive Summary")
                        st.info(result.get('summary', 'No summary generated.'))
                        
                        st.write("### 🎯 Key Strategic Points")
                        for point in result.get('key_points', []):
                            st.markdown(f"- {point}")
                            
                        col_action, col_deadlines = st.columns(2)
                        with col_action:
                            st.write("### 🛠️ Action Items")
                            for ai in result.get('action_items', []):
                                st.markdown(f"- [ ] {ai}")
                                
                        with col_deadlines:
                            st.write("### ⏰ Deadlines Map")
                            for d in result.get('deadlines', []):
                                st.markdown(f"- ⏳ **{d}**")
                                
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Save functionality directly in UI
                        st.markdown("### 💾 Export Outputs")
                        dl1, dl2 = st.columns(2)
                        
                        json_str = json.dumps(result, indent=2)
                        dl1.download_button("Download JSON", data=json_str, file_name="summary_export.json", mime="application/json")
                        
                        # Re-create text summary manually for download
                        txt_out = f"Email Summary ({date.today()})\n"
                        txt_out += "=" * 40 + "\n\nSUMMARY:\n" + result.get('summary', '') + "\n\nKEY POINTS:\n"
                        for p in result.get('key_points', []): txt_out += f"- {p}\n"
                        txt_out += "\nACTION ITEMS:\n"
                        for a in result.get('action_items', []): txt_out += f"- {a}\n"
                        txt_out += "\nDEADLINES:\n"
                        for d in result.get('deadlines', []): txt_out += f"- {d}\n"
                        txt_out += f"\nURGENCY: {urgency_val}\n"
                        
                        dl2.download_button("Download Briefing TXT", data=txt_out, file_name="summary_export.txt", mime="text/plain")
                        
                        st.toast("Intelligence Extracted Successfully!", icon='🚀')
                        
                    except Exception as e:
                        st.error(f"Engine Failure: {str(e)}")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 50px; color: #64748B; border: 2px dashed #334155; border-radius: 12px;">
                <h4>Awaiting Context</h4>
                <p>Paste an email thread and hit Extract to see the magic happen.</p>
            </div>
            """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
