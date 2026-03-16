import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from agent import generate_swot, save_outputs
import os

# Page Config
st.set_page_config(
    page_title="SWOT Analysis Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #0f1116;
        color: #e0e0e0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        border: none;
    }
    .swot-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid;
    }
    .strength-card { border-left-color: #4CAF50; background-color: #1b2e1c; }
    .weakness-card { border-left-color: #f44336; background-color: #2e1b1b; }
    .opportunity-card { border-left-color: #2196F3; background-color: #1b232e; }
    .threat-card { border-left-color: #FF9800; background-color: #2e261b; }
    
    h1, h2, h3 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

def render_swot_grid(data):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🟢 Strengths")
        for s in data['strengths']:
            st.markdown(f"""<div class="swot-card strength-card">
                <strong>{s['factor']}</strong><br/>
                <small>Impact: {s['impact']}</small><br/>
                {s['description']}
            </div>""", unsafe_allow_html=True)
            
        st.subheader("🔵 Opportunities")
        for o in data['opportunities']:
            st.markdown(f"""<div class="swot-card opportunity-card">
                <strong>{o['factor']}</strong><br/>
                <small>Impact: {o['impact']}</small><br/>
                {o['description']}
            </div>""", unsafe_allow_html=True)

    with col2:
        st.subheader("🔴 Weaknesses")
        for w in data['weaknesses']:
            st.markdown(f"""<div class="swot-card weakness-card">
                <strong>{w['factor']}</strong><br/>
                <small>Impact: {w['impact']}</small><br/>
                {w['description']}
            </div>""", unsafe_allow_html=True)
            
        st.subheader("🟠 Threats")
        for t in data['threats']:
            st.markdown(f"""<div class="swot-card threat-card">
                <strong>{t['factor']}</strong><br/>
                <small>Impact: {t['impact']}</small><br/>
                {t['description']}
            </div>""", unsafe_allow_html=True)

def main():
    st.title("🎯 SWOT Analysis Expert Agent")
    st.markdown("Generate deep strategic insights and TOWS matrices for any business context.")

    with st.sidebar:
        st.header("⚙️ Configuration")
        
        provider = st.selectbox("AI Provider", ["OpenAI", "Anthropic", "Gemini", "Groq"])
        
        models = {
            "OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
            "Gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
            "Groq": ["llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"]
        }
        
        model = st.selectbox("Model", models[provider])
        
        # API Key Handling
        api_key_input = st.text_input(f"{provider} API Key", type="password", placeholder=f"Paste your {provider} key here")
        st.info(f"Leave empty if {provider.upper()}_API_KEY is in .env")

        st.divider()
        st.header("🏢 Input Context")
        input_method = st.radio("Choose Input Method", ["File Upload", "Text Area"])
        
        context_text = ""
        if input_method == "Text Area":
            context_text = st.text_area("Enter organization context, industry, and goals:", height=200, 
                                        placeholder="Entity: Apple Inc.\nIndustry: Technology\n...")
        else:
            uploaded_file = st.file_uploader("Upload context.txt", type=['txt'])
            if uploaded_file is not None:
                context_text = uploaded_file.getvalue().decode("utf-8")

        analyze_btn = st.button("🚀 Analyze Strategy")

    if analyze_btn:
        if not context_text:
            st.warning("Please provide context first!")
        else:
            with st.spinner(f"Agent is conducting deep research using {model}..."):
                try:
                    # Run the agent logic with selected provider and model
                    result = generate_swot(
                        context_text, 
                        provider=provider, 
                        model=model, 
                        api_key=api_key_input if api_key_input else None
                    )
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.info(f"Check your {provider} API key and network connection.")
                
                if 'result' in locals() and result:
                    st.success(f"Analysis Complete using {model}!")
                    st.session_state['swot_data'] = result
                    save_outputs(result)
                else:
                    st.error("Failed to generate analysis. Check your API key.")

    if 'swot_data' in st.session_state:
        data = st.session_state['swot_data']
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 SWOT Grid", "🧠 TOWS Matrix", "📈 Visualization", "📝 Detailed Report"])
        
        with tab1:
            render_swot_grid(data)
            
        with tab2:
            st.subheader("Strategic Strategies (TOWS)")
            t_col1, t_col2 = st.columns(2)
            tows = data.get('tows_strategies', {})
            
            with t_col1:
                st.info("💡 **SO Strategies** (Strengths + Opportunities)")
                for s in tows.get('so_strategies', []): st.write(f"- {s}")
                
                st.info("⚠️ **ST Strategies** (Strengths + Threats)")
                for s in tows.get('st_strategies', []): st.write(f"- {s}")
                
            with t_col2:
                st.success("🌱 **WO Strategies** (Weaknesses + Opportunities)")
                for s in tows.get('wo_strategies', []): st.write(f"- {s}")
                
                st.error("🛡️ **WT Strategies** (Weaknesses + Threats)")
                for s in tows.get('wt_strategies', []): st.write(f"- {s}")

        with tab3:
            st.subheader("Factor Impact Distribution")
            
            # Prepare data for visualization
            impact_data = []
            for category in ['strengths', 'weaknesses', 'opportunities', 'threats']:
                for item in data[category]:
                    impact_data.append({
                        "Category": category.capitalize(),
                        "Impact": item['impact']
                    })
            
            if impact_data:
                df = pd.DataFrame(impact_data)
                fig = go.Figure()
                
                colors = {'High': '#f44336', 'Medium': '#FF9800', 'Low': '#4CAF50'}
                
                for impact_level in ['High', 'Medium', 'Low']:
                    subset = df[df['Impact'] == impact_level]
                    counts = subset['Category'].value_counts()
                    
                    fig.add_trace(go.Bar(
                        name=impact_level,
                        x=counts.index,
                        y=counts.values,
                        marker_color=colors.get(impact_level)
                    ))
                
                fig.update_layout(
                    barmode='stack',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color="white",
                    title="Number of Factors by Impact Level",
                    xaxis_title="SWOT Category",
                    yaxis_title="Count"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for visualization.")

        with tab4:
            st.subheader("Strategic Observations")
            for obs in data.get('strategic_observations', []):
                st.write(f"📌 {obs}")
                
            st.divider()
            st.subheader("Download Artifacts")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button("Download JSON", 
                                   data=json.dumps(data, indent=2), 
                                   file_name="swot_analysis.json", 
                                   mime="application/json")
            with col_d2:
                # Basic text formatting for download
                txt_content = f"SWOT ANALYSIS REPORT\n{'='*20}\n"
                for k in ['strengths', 'weaknesses', 'opportunities', 'threats']:
                    txt_content += f"\n{k.upper()}:\n"
                    for item in data[k]:
                        txt_content += f"- {item['factor']}: {item['description']}\n"
                
                st.download_button("Download TXT", 
                                   data=txt_content, 
                                   file_name="swot_analysis.txt", 
                                   mime="text/plain")

if __name__ == "__main__":
    main()
