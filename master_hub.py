import streamlit as st

st.set_page_config(
    page_title="AI Agent Hub",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def apply_apple_design():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Reset and Base typography */
    body, .stApp {
        background-color: #000000;
        color: #F5F5F7;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide heavy Streamlit UI elements */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .css-1rs6os {visibility: hidden;}
    .css-17ziqus {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    /* Top Layout Spacing */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 5rem !important;
        max-width: 1100px !important;
    }

    /* Master Headings */
    h1 {
        font-weight: 500;
        font-size: 3rem !important;
        letter-spacing: -0.015em;
        text-align: center;
        color: #F5F5F7;
        margin-bottom: 0.5rem;
    }
    
    .stMarkdown p.sub-header {
        text-align: center;
        color: #86868B;
        font-size: 1.15rem;
        font-weight: 400;
        letter-spacing: 0.005em;
        margin-bottom: 4rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }

    /* Category Headers */
    .category-title {
        color: #F5F5F7;
        font-size: 1.4rem;
        font-weight: 500;
        letter-spacing: 0.01em;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #333336;
        padding-bottom: 0.8rem;
    }

    /* Agent Cards (Grid simulated via Streamlit columns, styled via HTML) */
    .agent-link-wrapper {
        text-decoration: none;
    }
    
    .agent-card {
        background-color: #111111;
        border: 1px solid #222222;
        border-radius: 14px;
        padding: 24px;
        height: 100%;
        min-height: 140px;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        cursor: pointer;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    .agent-card:hover {
        background-color: #1A1A1A;
        border-color: #333333;
        transform: translateY(-2px);
    }

    .agent-name {
        color: #F5F5F7;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        text-decoration: none;
    }

    .agent-desc {
        color: #86868B;
        font-size: 0.85rem;
        line-height: 1.4;
        font-weight: 400;
    }
    
    </style>
    ''', unsafe_allow_html=True)

def main():
    apply_apple_design()

    st.markdown("<h1>Agent OS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>A curated ecosystem of autonomous enterprise intelligence. Click any agent to inspect its operational architecture.</p>", unsafe_allow_html=True)

    st.markdown("<div class='category-title'>💼 Business Operations Systems</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/CRM%20data%20enrichment%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🧬 DataForge AI</div>
                    <div class="agent-desc">Intelligence-led CRM enrichment & decision mapping.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Invoice%20processing%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📄 InvoiceIntel</div>
                    <div class="agent-desc">Multi-model Vision layer for financial document extraction.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Lead%20qualification%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🎯 LeadScore AI</div>
                    <div class="agent-desc">Precision lead qualification via BANT/CHAMP frameworks.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Sales%20follow-up%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🤝 SalesFollowAI</div>
                    <div class="agent-desc">High-conversion post-interaction narrative generator.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Customer%20support%20response%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🛡️ SupportCraft</div>
                    <div class="agent-desc">Empathetic response intelligence & sentiment auditing.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Expense%20categorization%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">💸 ExpenseIQ</div>
                    <div class="agent-desc">Algorithmic category detection & anomaly audit.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Internal%20SOP%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📋 SOPFlow AI</div>
                    <div class="agent-desc">Standardized Ops Architect for scaling procedures.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/KPI%20dashboard%20insight%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">💹 InsightCore</div>
                    <div class="agent-desc">Strategic KPI narrative & causality diagnostic.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Contract%20clause%20explanation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📑 ClauseClear</div>
                    <div class="agent-desc">Advanced legal plain-language engine & risk auditor.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Vendor%20comparison%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">⚖️ VendorFlow AI</div>
                    <div class="agent-desc">Strategic vendor comparative analysis grid.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("<div class='category-title'>🧪 Marketing & Growth Systems</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Ad%20copy%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🎨 AdForge AI</div>
                    <div class="agent-desc">Growth-studio with persona simulation logic.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Campaign%20performance%20analysis%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📈 AdIntel AI</div>
                    <div class="agent-desc">Budget utility auditor & leaky bucket detector.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/A%20B%20test%20suggestion%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🧪 OptiTest AI</div>
                    <div class="agent-desc">Strategic A/B test architect with ICE scoring.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Customer%20persona%20builder%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🛡️ Persona-Forge</div>
                    <div class="agent-desc">Market data synthesis & customer architect.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Funnel%20optimization%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">⚡ Funnel-Force</div>
                    <div class="agent-desc">Performance diagnostic & conversion strategy.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Email%20marketing%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📩 Email-Mind</div>
                    <div class="agent-desc">High-conversion multi-model copywriting.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Influencer%20outreach%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🤝 Influence-Core</div>
                    <div class="agent-desc">Relationship-first influencer outreach engine.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Product%20launch%20checklist%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🚀 Launch-Pad AI</div>
                    <div class="agent-desc">GTM operational readiness & launch architecture.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Social%20media%20scheduling%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📅 Social-Sync</div>
                    <div class="agent-desc">Cross-platform orchestration & scheduling.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Brand%20voice%20consistency%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🎭 Voice-Verify</div>
                    <div class="agent-desc">Brand voice & linguistic integrity audit.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("<div class='category-title'>📊 Data & Automation Systems</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/CSV%20data%20cleaning%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🧬 NeuralData AI</div>
                    <div class="agent-desc">Multi-cloud batch CSV cleaning & integrity auditing.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Spreadsheet%20formula%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔢 Sheet-Logic AI</div>
                    <div class="agent-desc">Multinational spreadsheet formula & logic architect.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Data%20validation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🛡️ Data-Guard AI</div>
                    <div class="agent-desc">Neural dataset integrity & schema governance.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/API%20response%20interpreter%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔌 API-Insight</div>
                    <div class="agent-desc">Neural API response forensic & interpreter.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Log%20anomaly%20detection%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🛡️ Log-Sentinel</div>
                    <div class="agent-desc">System telemetry forensic & anomaly detection.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Workflow%20orchestration%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🎼 Orchestra-Core</div>
                    <div class="agent-desc">Multi-step execution architecture for complex missions.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/ETL%20pipeline%20design%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">💾 Pipeline-Forge</div>
                    <div class="agent-desc">High-performance ETL & cloud data architect.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Error%20classification%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🚑 Error-Forensics</div>
                    <div class="agent-desc">SRE incident diagnosis & error classification.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Monitoring%20alert%20explanation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📊 Alert-Insight</div>
                    <div class="agent-desc">Monitoring alert translation & root-cause diagnostic.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Automation%20recommendation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🏗️ Auto-Strategist</div>
                    <div class="agent-desc">Process mining & high-ROI automation strategist.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("<div class='category-title'>🧠 Personal Productivity Systems</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/daily-priority-agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🧠 PriorityBrain</div>
                    <div class="agent-desc">NLP task ingestion & algorithmic urgency sorting.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Personal%20knowledge%20base%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🗄️ BrainVault</div>
                    <div class="agent-desc">Local RAG knowledge base via vector space.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Note-to-action%20item%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">⚡ ActionForge</div>
                    <div class="agent-desc">Unstructured text-to-task neural extraction.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Email%20summarization%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📧 MailMind AI</div>
                    <div class="agent-desc">Intelligent thread logic & summary mapping.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Calendar%20conflict%20resolver%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📅 SyncGuard</div>
                    <div class="agent-desc">Conflict detection & resolution engine.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Meeting%20agenda%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📋 AgendaCraft</div>
                    <div class="agent-desc">High-fidelity meeting timeline architect.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Daily%20goal%20reflection%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🧘 Reflect AI</div>
                    <div class="agent-desc">Algorithmic daily target analytics.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Smart%20reminder%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔔 PingCraft</div>
                    <div class="agent-desc">Distributed deadline alerting engine.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Time-blocking%20planner%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">⏳ ChronoBlock</div>
                    <div class="agent-desc">Continuous task packing logic planner.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Habit%20tracking%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔥 StreakForge</div>
                    <div class="agent-desc">Persistence density metrics & habit tracking.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("<div class='category-title'>🔬 Research & Analysis Systems</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/SWOT%20analysis%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔬 SWOT Horizon</div>
                    <div class="agent-desc">TOWS matrix & strategic opportunity analysis.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Web%20research%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🌐 Web Research</div>
                    <div class="agent-desc">Autonomous multi-model executive research.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/YouTube%20video%20summary%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🎬 StreamBrief</div>
                    <div class="agent-desc">Neural video transcript distiller & insight mapper.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Investment%20thesis%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">💰 CapitalMind</div>
                    <div class="agent-desc">Evidence-driven investment thesis architect.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Market%20trend%20summarization" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">💹 TrendSynthetix</div>
                    <div class="agent-desc">Market context trend deconstruction.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/News%20aggregation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📰 NewsFlow</div>
                    <div class="agent-desc">Global thematic news intelligence digests.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Policy%20document%20summarizer%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">⚖️ PolicyGuard</div>
                    <div class="agent-desc">Thematic synthesis for regulatory frameworks.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("<div class='category-title'>✍️ Writing & Content Systems</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Blog%20post%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📝 Blog Architect</div>
                    <div class="agent-desc">SEO-optimized post pipeline.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Cover%20letter%20writing%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">💼 CoverCraft</div>
                    <div class="agent-desc">Job-specific tailored cover letter architect.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/FAQ%20generation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">💬 AI FAQ Gen</div>
                    <div class="agent-desc">Credentialed FAQ generator.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Grammar%20correction%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">✨ GrammarPlus</div>
                    <div class="agent-desc">Semantic deep-edit & tone correction.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/LinkedIn%20post%20ideation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔗 HookGen Pro</div>
                    <div class="agent-desc">LinkedIn post & hook ideation studio.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Product%20description%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🛍️ ProductCopy</div>
                    <div class="agent-desc">Outcome-driven product descriptions.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Resume%20optimization%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📄 ResumeAI</div>
                    <div class="agent-desc">ATS-optimized enhancement engine.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/SEO%20keyword%20expansion%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔎 SEOClusters</div>
                    <div class="agent-desc">Predictive keyword expansion clusters.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Script-to-slide%20outline%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📽️ SlideForge AI</div>
                    <div class="agent-desc">Script-to-slide visual architect.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Tone%20rewriting%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🎭 ToneWizard</div>
                    <div class="agent-desc">Multi-persona voice rewriter.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("<div class='category-title'>🛠️ AI & Engineering Systems</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Model%20comparison%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🧠 ModelMind AI</div>
                    <div class="agent-desc">Deep architectural trade-off analysis.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Prompt%20optimization%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">✨ PromptForge AI</div>
                    <div class="agent-desc">Neural prompt engineering & linguistic structure optimization.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/RAG%20document%20retrieval%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔍 SemanticForge AI</div>
                    <div class="agent-desc">Orchestrated RAG document & contextual semantic retrieval.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Tool-calling%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">⚡ ToolForge AI</div>
                    <div class="agent-desc">Autonomous tool-call orchestration with multi-tool execution registry.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Multi-step%20reasoning%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🧩 ThinkForge AI</div>
                    <div class="agent-desc">Structured multi-step decomposition & chain-of-thought reasoning engine.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Code%20refactoring%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🛠️ CleanCode AI</div>
                    <div class="agent-desc">Advanced syntax architectural transformation & best practice adherence refactoring engine.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Bug%20explanation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🐛 BugSentinel AI</div>
                    <div class="agent-desc">Neural traceback analysis & root cause diagnostic forensics.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/API%20documentation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📖 DocForge AI</div>
                    <div class="agent-desc">Automated deterministic REST API schema documentation & contract logic compiler.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Test%20case%20generation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🧪 TestForge AI</div>
                    <div class="agent-desc">Rigorous test suite & edge case regression validation framework.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/System%20architecture%20explainer%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🏗️ ArchForge AI</div>
                    <div class="agent-desc">Topological data-flow extraction & implicitly derived trade-off analytical engine.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("<div class='category-title'>🗄️ HR, Legal & Compliance Systems</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Job%20description%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">💼 TalentForge AI</div>
                    <div class="agent-desc">Inclusive requisition & job description intelligence pipeline.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Candidate%20screening%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔎 ScreenGenius Pro AI</div>
                    <div class="agent-desc">Multi-axis algorithmic candidate screening matrix with red-flag detection & custom interview probes.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Interview%20question%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🎙️ QuestForge AI</div>
                    <div class="agent-desc">Autonomous technical interview question architect.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Performance%20review%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📈 ReviewForge AI</div>
                    <div class="agent-desc">Professional tone synthesis and constructive performance appraisal engine.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Policy%20compliance%20checker%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">⚖️ ComplianceGuard AI</div>
                    <div class="agent-desc">Automated enterprise policy enforcement & liability prevention matrix.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Risk%20assessment%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">⚠️ RiskForge AI</div>
                    <div class="agent-desc">Threat modeling architecture resolving operational and deployment liabilities conditionally.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Legal%20clause%20summarization%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🛡️ BriefForge AI</div>
                    <div class="agent-desc">Legal clause syntactic translation mechanism into executive language logic.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Data%20privacy%20explanation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🔐 PrivacyForge AI</div>
                    <div class="agent-desc">Contextual data privacy regulation compliance matrix mapping features to legal bounds.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Training%20content%20generator%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">🎓 SkillForge AI</div>
                    <div class="agent-desc">Auto-architected corporate learning & objective enablement module generator.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('''
            <a href="https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Audit%20preparation%20agent" target="_blank" class="agent-link-wrapper">
                <div class="agent-card">
                    <div class="agent-name">📋 AuditForge AI</div>
                    <div class="agent-desc">Pre-audit readiness scanner identifying critical evidence gaps and mandatory remediations.</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
