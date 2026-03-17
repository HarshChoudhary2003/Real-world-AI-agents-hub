import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import date
import os
from agent import process_invoice, save_outputs

# Page Config
st.set_page_config(
    page_title="Invoice Intel AI | Enterprise Processing",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Persistent History Initialization
HISTORY_FILE = "invoice_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_history(data):
    history = load_history()
    # Add timestamp
    data['processed_at'] = date.today().isoformat()
    history.insert(0, data)
    # Keep last 20 for analytics
    history = history[0:20]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Advanced Glassmorphism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }
    
    .metric-box {
        background: rgba(56, 189, 248, 0.05);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    
    .metric-val {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    .metric-lab {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-pass { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid #22c55e; }
    .status-fail { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid #ef4444; }
    
    .flag-item {
        background: rgba(245, 158, 11, 0.05);
        border-left: 4px solid #f59e0b;
        padding: 10px;
        margin-top: 8px;
        font-size: 0.9rem;
    }
    
    h1, h2, h3 { color: #f8fafc !important; }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🧾 Invoice Intel AI")
    st.markdown("### Neural Invoice Extraction & Financial Verification Engine")
    
    with st.sidebar:
        st.markdown("### ⚙️ Engine Control")
        provider = st.selectbox("Intelligence Provider", ["OpenAI", "Anthropic", "Gemini", "Groq"])
        
        models = {
            "OpenAI": ["gpt-4o-mini", "gpt-4o"],
            "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229"],
            "Gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
            "Groq": ["llama-3.1-70b-versatile", "mixtral-8x7b-32768"]
        }
        
        selected_model = st.selectbox("Model Architecture", models[provider])
        
        api_key = st.text_input(f"{provider} API Key", type="password")
        st.caption(f"Leave empty to use {provider.upper()}_API_KEY from .env")
        
        st.divider()
        st.markdown("### 📄 Input Source")
        input_type = st.radio("Upload Method", ["Batch File Upload", "Context Area"])
        
        raw_inputs = []
        if input_type == "Context Area":
            text_area_val = st.text_area("Paste invoice content here:", height=300)
            if text_area_val: raw_inputs = [text_area_val]
        else:
            uploaded_files = st.file_uploader("Upload Text Documents", type=['txt'], accept_multiple_files=True)
            for f in uploaded_files:
                raw_inputs.append(f.getvalue().decode())
                
        process_btn = st.button("🚀 Execute Neural Extraction", use_container_width=True)

    if process_btn:
        if not raw_inputs:
            st.error("Error: Input buffer is empty.")
        else:
            with st.spinner(f"Agent synchronizing with {selected_model}..."):
                try:
                    all_results = []
                    for single_input in raw_inputs:
                        result = process_invoice(single_input, provider=provider, model=selected_model, api_key=api_key if api_key else None)
                        all_results.append(result)
                        save_outputs(result)
                        save_to_history(result)
                    
                    st.session_state['batch_results'] = all_results
                    st.session_state['invoice_result'] = all_results[0] # Default to first
                    st.toast(f"Neural Extraction Complete for {len(all_results)} invoices", icon="✅")
                except Exception as e:
                    st.error(f"Execution Fault: {str(e)}")

    # Sidebar History View
    history = load_history()
    if history:
        with st.sidebar:
            st.divider()
            st.markdown("### 🕒 Recent History")
            for i, entry in enumerate(history):
                # Using a safer way to get the list slice to avoid lint confusion
                short_vendor = (entry.get('vendor', 'Unknown'))[:15]
                if st.button(f"📄 {short_vendor} - {entry.get('invoice_number') or i}", key=f"hist_{i}"):
                    st.session_state['invoice_result'] = entry

    if 'batch_results' in st.session_state and len(st.session_state['batch_results']) > 1:
        st.markdown("### 📦 Batch Summary")
        batch_data = []
        for res in st.session_state['batch_results']:
            batch_data.append({
                "Vendor": res.get("vendor"),
                "Total": f"{res.get('currency', '')}{res.get('total')}",
                "Status": "✅ PASS" if res.get("validation_results", {}).get("math_check_passed") else "❌ FAIL"
            })
        st.table(pd.DataFrame(batch_data))
        
        selected_idx = st.selectbox("Select Invoice to Detail", range(len(st.session_state['batch_results'])), 
                                    format_func=lambda x: f"{st.session_state['batch_results'][x].get('vendor')} ({st.session_state['batch_results'][x].get('invoice_number')})")
        st.session_state['invoice_result'] = st.session_state['batch_results'][selected_idx]
        st.divider()

    if 'invoice_result' in st.session_state:
        data = st.session_state['invoice_result']
        val = data.get('validation_results', {})
        
        # Dashboard Layout
        t1, t2, t3, t4 = st.tabs(["📊 Verification Hub", "📋 Detailed Audit", "📈 Global Analytics", "🧬 Neural Raw"])
        
        with t1:
            # Top Metrics
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            with m_col1:
                st.markdown(f'<div class="metric-box"><div class="metric-lab">Vendor</div><div class="metric-val" style="font-size: 1.2rem; margin-top:10px;">{data.get("vendor")}</div></div>', unsafe_allow_html=True)
            with m_col2:
                st.markdown(f'<div class="metric-box"><div class="metric-lab">Total</div><div class="metric-val">{data.get("currency")}{data.get("total")}</div></div>', unsafe_allow_html=True)
            with m_col3:
                st.markdown(f'<div class="metric-box"><div class="metric-lab">Tax</div><div class="metric-val">{data.get("tax")}</div></div>', unsafe_allow_html=True)
            with m_col4:
                status_class = "status-pass" if val.get("math_check_passed") else "status-fail"
                status_text = "PASSED" if val.get("math_check_passed") else "FAILED"
                st.markdown(f'<div class="metric-box"><div class="metric-lab">Math Check</div><div class="metric-val"><span class="status-badge {status_class}">{status_text}</span></div></div>', unsafe_allow_html=True)

            st.divider()
            
            c_left, c_right = st.columns([2, 1])
            
            with c_left:
                st.markdown("#### 📦 Distribution of Costs")
                df_items = pd.DataFrame(data.get("line_items", []))
                if not df_items.empty:
                    fig = px.pie(df_items, values='amount', names='description', hole=.4, 
                                 color_discrete_sequence=px.colors.sequential.Tealgrn)
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                      font_color="white", showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                
            with c_right:
                st.markdown("#### 🚩 Discrepancy Analysis")
                if val.get("discrepancy", 0) != 0:
                    st.error(f"Discrepancy Detected: {data.get('currency')}{val.get('discrepancy')}")
                else:
                    st.success("Financial totals reconciled successfully.")
                    
                st.markdown("#### 📝 Financial Summary")
                st.info(data.get("financial_summary", "No summary provided."))

        with t2:
            st.markdown("#### 📑 Line Item Audit Table")
            if not df_items.empty:
                st.dataframe(df_items, use_container_width=True)
            
            st.divider()
            
            st.markdown("#### 🛡️ Validation System Logs")
            flags = val.get("flags", [])
            if flags:
                for f in flags:
                    st.markdown(f'<div class="flag-item">⚠ {f}</div>', unsafe_allow_html=True)
            else:
                st.write("No flags generated during audit.")
                
            st.divider()
            st.markdown("#### 💾 Export Artifacts")
            ex1, ex2 = st.columns(2)
            with ex1:
                st.download_button("Download JSON Audit", json.dumps(data, indent=2), "invoice_audit.json", "application/json", use_container_width=True)
            with ex2:
                # Simple summary text
                st.download_button("Download PDF Summary (Text)", data.get("financial_summary"), "invoice_summary.txt", "text/plain", use_container_width=True)

        with t3:
            st.markdown("#### 🌍 Historical Spend Intelligence")
            hist_data = load_history()
            if hist_data:
                h_df = pd.DataFrame([
                    {"Date": d.get("processed_at"), "Vendor": d.get("vendor"), "Total": d.get("total")}
                    for d in hist_data
                ])
                h_df["Total"] = pd.to_numeric(h_df["Total"], errors='coerce')
                
                fig_h = px.bar(h_df, x="Date", y="Total", color="Vendor", 
                               title="Historical Spent Distribution",
                               template="plotly_dark")
                fig_h.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_h, use_container_width=True)
                
                st.markdown("#### 🏁 Aggregate Vendor Statistics")
                v_stats = h_df.groupby("Vendor")["Total"].sum().reset_index()
                st.table(v_stats)
            else:
                st.info("Insufficient history for global analytics.")

        with t4:
            st.json(data)

if __name__ == "__main__":
    main()
