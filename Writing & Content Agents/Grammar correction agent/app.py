import streamlit as st
import json
import os
import difflib
from datetime import date
from dotenv import load_dotenv
import litellm

# Load environment variables
load_dotenv()

# Suppress litellm logging for a cleaner console
litellm.suppress_debug_info = True

# --- Page Configuration ---
st.set_page_config(
    page_title="GrammarPro | AI Editing Engine",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
/* Main background and text */
.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
}

/* Headers */
h1, h2, h3 {
    color: #58a6ff;
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
}

/* Custom styling for the main container */
.main-header {
    background: linear-gradient(90deg, #58a6ff 0%, #a371f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 3rem;
    margin-bottom: 0px;
    padding-bottom: 0px;
}

.sub-header {
    color: #8b949e;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

/* Cards for Content */
div.stChatMessage {
    background-color: #161b22;
    border-radius: 10px;
    border: 1px solid #30363d;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #58a6ff 0%, #a371f7 100%);
    color: #ffffff !important;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(88, 166, 255, 0.4);
}

/* Text Areas */
.stTextArea textarea {
    background-color: #161b22 !important;
    color: #ecf2f8 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px;
    font-size: 1.1rem !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 1px #58a6ff !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: #161b22;
    border-radius: 8px 8px 0px 0px;
    border: 1px solid #30363d;
    border-bottom: none;
    padding: 10px 20px;
    color: #8b949e;
}
.stTabs [aria-selected="true"] {
    background-color: #21262d !important;
    color: #58a6ff !important;
    border-bottom: 2px solid #58a6ff !important;
}

/* Diff Styling */
.diff-del {
    background-color: rgba(248, 81, 73, 0.2);
    color: #ff7b72;
    text-decoration: line-through;
    padding: 2px 4px;
    border-radius: 3px;
}
.diff-add {
    background-color: rgba(46, 160, 67, 0.2);
    color: #3fb950;
    font-weight: bold;
    padding: 2px 4px;
    border-radius: 3px;
}
.correction-note {
    background-color: #161b22;
    border-left: 4px solid #a371f7;
    padding: 10px 15px;
    margin-bottom: 10px;
    border-radius: 0 8px 8px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Agent Logic ---
def get_system_prompt(goal, strictness):
    if strictness == "Light Verification (Typos Only)":
        strict_text = "Fix ONLY obvious typos and objective grammatical errors. Do not improve style. Do not rewrite sentences."
    elif strictness == "Heavy Edit (Rewrite Awkward Sentences)":
        strict_text = "Fix typos, grammar, and aggressively rewrite clunky, awkward, or passive sentences to make them punchy and clear."
    else:
        strict_text = "Fix typos and grammar. Improve clarity while preserving the original meaning and structure where possible."

    return f"""
You are an Elite Grammar & Style Correction Agent.

Your precise mission:
1. Analyze the user's provided raw text.
2. Comply strictly with this editing strictness level: {strict_text}
3. Adjust the final text to align with this target audience/tone: {goal}.
4. Provide absolute factual accuracy—under NO circumstances should you add new ideas, facts, or alter the core argument of the original text.
5. Provide a short, specific array of "notes" explaining the most important changes you made (e.g. "Fixed subject-verb agreement in paragraph 2", "Changed passive voice to active voice").

Return strictly valid JSON matching this exact schema:
{{
  "corrected_text": "string (the fully corrected and polished version of the text)",
  "notes": ["string (note 1)", "string (note 2)"]
}}
"""

def process_text_api(raw_text, model_name, api_key, goal, strictness):
    if not api_key:
        raise ValueError("API Key is missing for the selected provider.")

    if "gpt" in model_name:
        os.environ["OPENAI_API_KEY"] = api_key
    elif "claude" in model_name:
        os.environ["ANTHROPIC_API_KEY"] = api_key
    elif "gemini" in model_name:
        os.environ["GEMINI_API_KEY"] = api_key
    elif "groq" in model_name:
        os.environ["GROQ_API_KEY"] = api_key

    system_content = get_system_prompt(goal, strictness)

    prompt = f"""
RAW TEXT INPUT:
{raw_text}

CRITICAL REQUIREMENT: Return ONLY valid JSON format with no Markdown wrappers, no thoughts, and no backticks.
"""
    
    response = litellm.completion(
        model=model_name,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1 # Very low temp for grammar stability
    )
    
    content = response.choices[0].message.content.strip()
    
    if content.startswith("```json"):
        content = content[7:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON from the model answer: {content}")

def render_diff(old_text, new_text):
    """Generates an HTML inline diff output to visualize deletions and additions"""
    matcher = difflib.SequenceMatcher(None, old_text.split(), new_text.split())
    result = []
    
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == 'equal':
            result.append(" ".join(old_text.split()[a0:a1]))
        elif opcode == 'insert':
            inserted = " ".join(new_text.split()[b0:b1])
            result.append(f"<span class='diff-add'>{inserted}</span>")
        elif opcode == 'delete':
            deleted = " ".join(old_text.split()[a0:a1])
            result.append(f"<span class='diff-del'>{deleted}</span>")
        elif opcode == 'replace':
            deleted = " ".join(old_text.split()[a0:a1])
            inserted = " ".join(new_text.split()[b0:b1])
            result.append(f"<span class='diff-del'>{deleted}</span> <span class='diff-add'>{inserted}</span>")
            
    return " ".join(result)

# --- UI Layout ---

# Sidebar for Settings
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/edit.png", width=64)
    st.title("GrammarPro")
    st.caption("v4.0.0 | Elite Editing Suite")
    
    st.markdown("---")
    
    st.subheader("⚙️ AI Engine Selection")
    
    model_options = {
        "Anthropic Claude 3.5 Sonnet (Best Editor)": "claude-3-5-sonnet-20240620",
        "OpenAI GPT-4o (Most Accurate)": "gpt-4o",
        "OpenAI GPT-4o Mini (Fast & Cheap)": "gpt-4o-mini",
        "Google Gemini 1.5 Pro (Deep Context)": "gemini/gemini-1.5-pro",
        "Groq LLaMA 3 70B (Ultra-Fast)": "groq/llama3-70b-8192"
    }
    selected_model_label = st.selectbox("LLM Provider", list(model_options.keys()))
    selected_model = model_options[selected_model_label]
    
    if "gpt" in selected_model:
        provider = "OpenAI"
        env_key = os.getenv("OPENAI_API_KEY", "")
    elif "claude" in selected_model:
        provider = "Anthropic"
        env_key = os.getenv("ANTHROPIC_API_KEY", "")
    elif "gemini" in selected_model:
        provider = "Google Gemini"
        env_key = os.getenv("GEMINI_API_KEY", "")
    elif "groq" in selected_model:
        provider = "Groq"
        env_key = os.getenv("GROQ_API_KEY", "")
    else:
        provider = "API"
        env_key = ""

    user_api_key = st.text_input(
        f"{provider} Key", 
        value=env_key, 
        type="password", 
        placeholder=f"Enter {provider} key..."
    )
        
    st.markdown("---")
    st.subheader("🎛️ Editing Constraints")
    
    strictness_choice = st.selectbox("Editing Aggressiveness", [
        "Standard (Fix Grammar, Adjust Flow)",
        "Light Verification (Typos Only)",
        "Heavy Edit (Rewrite Awkward Sentences)"
    ])
    
    goal_choice = st.selectbox("Intended Audience / Tone", [
        "Professional / Business",
        "Academic / Scientific",
        "Casual / Conversational",
        "Creative / Engaging"
    ])
    
    st.markdown("---")
    st.markdown("© 2026 AI Agent Factory")

# Main Dashboard
st.markdown('<h1 class="main-header">Perfect Your Prose Instantly</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced context-aware grammar logic. Fix typos, repair sentence structure, and elevate your vocabulary without losing your original voice.</p>', unsafe_allow_html=True)

page_tabs = st.tabs(["✍️ Intelligent Editor", "🔍 Diff / Change Visualizer"])

if "last_raw" not in st.session_state:
    st.session_state["last_raw"] = ""
    st.session_state["last_corrected"] = ""
    st.session_state["last_notes"] = []

with page_tabs[0]:
    raw_input = st.text_area(
        "Paste your rough draft here:", 
        height=300,
        placeholder="E.g.\nThis agent help user fix grammar mistakes. It dont change meaning but improve clarity. Writing look more professional after correction..."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn, col_empty = st.columns([1, 4])
    with col_btn:
        process_btn = st.button("✨ Refine & Polish", use_container_width=True)

    st.markdown("<hr style='border:1px solid #30363d; margin-top:1rem; margin-bottom:2rem;'>", unsafe_allow_html=True)

    if process_btn:
        if not raw_input:
            st.error("⚠️ Please provide text to analyze.")
        elif not user_api_key:
            st.error(f"⚠️ Your {provider} API Key is required.")
        else:
            try:
                with st.spinner(f"⚡ Processing through {provider} Engine... applying strictness logic..."):
                    result_json = process_text_api(raw_input, selected_model, user_api_key, goal_choice, strictness_choice)
                    st.session_state["last_raw"] = raw_input
                    st.session_state["last_corrected"] = result_json.get("corrected_text", "")
                    st.session_state["last_notes"] = result_json.get("notes", [])
                    
                st.success("🎯 Analysis complete! Your polished prose is ready.")
                
                # Auto-switch to output view mentally by displaying it here
            except Exception as e:
                st.error(f"❌ Edit Error: {str(e)}")
                st.info("Check API key validity and billing quotas for the selected provider.")
                
    # Display Results if they exist in session state
    if st.session_state["last_corrected"]:
        st.markdown("### ✨ Final Corrected Text")
        
        # Display the text in a code block or markdown for easy copying
        st.info(st.session_state["last_corrected"])
        
        col_dl, _ = st.columns([1, 3])
        with col_dl:
            st.download_button(
                label="📄 Download Clean Copy",
                data=st.session_state["last_corrected"],
                file_name=f"Corrected_Draft_{date.today()}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        st.markdown("### 📝 Editor's Diagnostics")
        if st.session_state["last_notes"]:
            for note in st.session_state["last_notes"]:
                st.markdown(f'<div class="correction-note">📌 {note}</div>', unsafe_allow_html=True)
        else:
            st.write("No major diagnostic changes flagged.")

with page_tabs[1]:
    st.markdown("## 🔍 Inline Correction Visualizer")
    st.markdown("See exactly what the AI changed to ensure your original meaning was preserved.")
    
    if st.session_state["last_raw"] and st.session_state["last_corrected"]:
        diff_html = render_diff(st.session_state["last_raw"], st.session_state["last_corrected"])
        
        st.markdown("""
        <div style="background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; line-height: 1.8; font-size: 1.1rem;">
            {}
        </div>
        """.format(diff_html), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_legend1, col_legend2, col_legend3 = st.columns([1,1,4])
        with col_legend1:
            st.markdown("<span class='diff-del'>Deletions</span>", unsafe_allow_html=True)
        with col_legend2:
            st.markdown("<span class='diff-add'>Additions</span>", unsafe_allow_html=True)
    else:
        st.info("⚠️ Process a raw text block first to visualize the algorithmic diff.")


with st.sidebar:
    st.markdown("---")
    st.caption("Developed by Harsh")
