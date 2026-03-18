import streamlit as st
import os
import json
from agent import generate_ideas, save_outputs

st.set_page_config(page_title="LinkedIn Post Ideation Agent", page_icon="💡", layout="wide")

# Custom CSS for a professional, beautiful look tailored for LinkedIn
st.markdown("""
<style>
    .stApp {
        background-color: #0B0E14;
        color: #E2E8F0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(10, 102, 194, 0.4);
    }
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #0A66C2, #47A2FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #A0AEC0;
        margin-bottom: 2rem;
    }
    .idea-card {
        background-color: #1A1F29;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #2D3748;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        border-left: 5px solid #0A66C2;
    }
    .idea-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #E2E8F0;
        margin-bottom: 0.8rem;
    }
    .idea-label {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #0A66C2;
        letter-spacing: 1px;
        margin-top: 0.8rem;
        margin-bottom: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💡 LinkedIn Post Ideation Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Generate distinct, hook-driven content ideas optimized for professional audiences.</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📝 Input Criteria")
    
    topic = st.text_input("Topic", value="AI agents and productivity")
    audience = st.text_input("Target Audience", value="Tech leaders and founders")
    
    col_t_l = st.columns(2)
    with col_t_l[0]:
        intent = st.text_input("Intent", value="Educate and inspire")
    with col_t_l[1]:
        frequency = st.text_input("Posting Frequency", value="Daily posting")
        
    personal_angle = st.text_area(
        "Personal Angle / Story", 
        value="Building 100 AI agents in 100 days", 
        height=80
    )
    
    # Advanced options and Model selector
    ai_model = st.selectbox(
        "🤖 AI Model", 
        [
            "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "o1-preview", "o1-mini", "o3-mini",
            "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229",
            "gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash"
        ], 
        index=1
    )
    
    if ai_model.startswith("gpt-") or ai_model.startswith("o1-") or ai_model.startswith("o3-"):
        key_label = "🔑 OpenAI API Key"
        env_var = "OPENAI_API_KEY"
    elif ai_model.startswith("claude-"):
        key_label = "🔑 Anthropic API Key"
        env_var = "ANTHROPIC_API_KEY"
    elif ai_model.startswith("gemini-"):
        key_label = "🔑 Gemini API Key"
        env_var = "GEMINI_API_KEY"
        
    with st.expander("⚙️ Advanced Tuning"):
        temperature = st.slider("Creativity Level (Temperature)", min_value=0.0, max_value=1.5, value=0.7, step=0.1)
        additional_rules = st.text_area("Additional Guardrails or Tone Matching", help="Any specific formats, tones or exclusions.")
    
    api_key_input = st.text_input(key_label, type="password", help="Required. Your key is not saved across sessions.")
    
    generate_btn = st.button("🚀 Generate Post Ideas", use_container_width=True)

with col2:
    st.markdown("### ✨ Ideation Output")
    
    if generate_btn:
        if not api_key_input:
            st.error(f"Please provide your {key_label}.")
        else:
            os.environ[env_var] = api_key_input
            
            with st.spinner("Brainstorming post ideas... ⏳"):
                try:
                    # Construct instructions
                    instructions = f"Topic: {topic}\nAudience: {audience}\nIntent: {intent}\nPersonal Angle: {personal_angle}\nFrequency: {frequency}"
                    if additional_rules:
                        instructions += f"\nAdditional Rules: {additional_rules}"
                    
                    # Generate and save locally 
                    ideas_data = generate_ideas(instructions, model=ai_model, temperature=temperature)
                    save_outputs(ideas_data)
                    
                    st.session_state.ideas_data = ideas_data
                    st.success("✅ Ideas generated successfully! Saved to `ideas.json` and `ideas.txt`.")
                    
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    
    if 'ideas_data' in st.session_state:
        ideas_list = st.session_state.ideas_data.get("ideas", [])
        
        st.markdown(f"**Generated {len(ideas_list)} potential concepts:**")
        
        for i, idea in enumerate(ideas_list, 1):
            st.markdown('<div class="idea-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="idea-title">#{i} - {idea.get("title", "")} <span style="font-size: 0.9rem; color:#47A2FF;">(Score: {idea.get("estimated_engagement_score", "")})</span></div>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="idea-label">🧠 Framework: {idea.get("framework", "")}</div>', unsafe_allow_html=True)
            
            with st.expander("📝 View Strategy Details (Hook, Message, CTA, Visual)"):
                st.markdown("**🎯 Hook:**")
                st.write(f"_{idea.get('hook', '')}_")
                
                st.markdown("**📌 Core Message:**")
                st.write(idea.get('core_message', ''))
                
                st.markdown("**💬 Call To Action:**")
                st.write(idea.get('cta', ''))
                
                if idea.get('visual_suggestion'):
                    st.markdown("**🎨 Suggested Visual:**")
                    st.write(idea.get('visual_suggestion', ''))
                    
            st.markdown('<div class="idea-label">✍️ DRAFTED POST</div>', unsafe_allow_html=True)
            st.write(idea.get('full_post_draft', ''))
            
            if idea.get('hashtags'):
                st.markdown('<div class="idea-label">#️⃣ Hashtags</div>', unsafe_allow_html=True)
                st.code(' '.join(idea.get('hashtags', [])))
                
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Your AI-generated post ideas will appear here.")


st.markdown("---")
st.caption("Developed by Harsh")
