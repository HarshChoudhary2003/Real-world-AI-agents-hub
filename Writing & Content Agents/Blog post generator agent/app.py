import streamlit as st
import json
import os
from agent import generate_blog, save_outputs

st.set_page_config(page_title="Blog Post Generator Agent", page_icon="✍️", layout="wide")

# Custom CSS for a professional, beautiful look
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #E0E6ED;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
    }
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #A0AEC0;
        margin-bottom: 2rem;
    }
    .section-card {
        background-color: #1A1E27;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #2D3139;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">✍️ Blog Post Generator Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Instantly generate well-structured, professional blog posts tailored to your audience.</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 📝 Instruction Setup")
    
    topic = st.text_input("Topic", value="Why AI Agents Will Redefine Productivity in 2026")
    audience = st.text_input("Target Audience", value="Professionals and founders")
    
    col_t_l = st.columns(2)
    with col_t_l[0]:
        tone = st.text_input("Tone", value="Educational and forward-looking")
    with col_t_l[1]:
        length = st.text_input("Length", value="~800 words")
        
    key_points = st.text_area(
        "Key Points (one per line)", 
        value="- Difference between AI tools and AI agents\n- Real-world productivity examples\n- Why daily agent usage matters", 
        height=150
    )
    
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
    
    with st.expander("⚙️ Advanced Settings"):
        temperature = st.slider("Creativity Level (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        target_keywords = st.text_input("Target SEO Keywords (comma separated)")
        additional_context = st.text_area("Additional Context or Reference Data")
    
    api_key_input = st.text_input(key_label, type="password", help="Required. Your key is not saved across sessions.")
    
    generate_btn = st.button("🚀 Generate Blog Post", use_container_width=True)

with col2:
    st.markdown("### ✨ Generated Output")
    
    if generate_btn:
        if not api_key_input:
            st.error(f"Please provide your {key_label}.")
        else:
            os.environ[env_var] = api_key_input
            
            with st.spinner("Agent is writing your blog post... ⏳"):
                try:
                    # Construct instructions
                    instructions = f"Topic: {topic}\nAudience: {audience}\nTone: {tone}\nLength: {length}\nKey Points:\n{key_points}"
                    if target_keywords:
                        instructions += f"\nTarget Keywords: {target_keywords}"
                    if additional_context:
                        instructions += f"\nAdditional Context: {additional_context}"
                    
                    # Generate and save locally 
                    blog_data = generate_blog(instructions, model=ai_model, temperature=temperature)
                    save_outputs(blog_data)
                    
                    st.session_state.blog_data = blog_data
                    st.success("✅ Blog generated successfully! Saved to `blog.json` and `blog.txt`.")
                    
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    
    if 'blog_data' in st.session_state:
        blog = st.session_state.blog_data
        
        st.markdown(f"## {blog.get('title', 'Untitled')}")
        
        
        with st.expander("🔍 SEO & Metadata", expanded=True):
            st.markdown(f"**SEO Title:** {blog.get('seoTitle', '')}")
            st.markdown(f"**Slug:** `/{blog.get('slug', '')}`")
            st.markdown(f"**Meta Description:** {blog.get('metaDescription', '')}")
            st.markdown(f"**Keywords:** {', '.join(blog.get('keywords', []))}")
        
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.write(f"**{blog.get('hook', '')}**")
        st.write(blog.get('introduction', ''))
        st.markdown('</div>', unsafe_allow_html=True)
        
        for section in blog.get('sections', []):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(f"#### {section.get('header', '')}")
            st.write(section.get('content', ''))
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### Conclusion")
        st.write(blog.get('conclusion', ''))
        st.markdown(f"✨ **{blog.get('callToAction', '')}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if blog.get('socialMediaPost'):
            st.info(f"📱 **Social Media Promo:**\n\n{blog.get('socialMediaPost', '')}")
    else:
        st.info("Your generated blog post will appear here.")


st.markdown("---")
st.caption("Developed by Harsh")
