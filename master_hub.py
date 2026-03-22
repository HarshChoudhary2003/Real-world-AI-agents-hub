import streamlit as st
import json
import re

st.set_page_config(
    page_title="Agent OS | Professional Hub",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

CATEGORIES_RAW = {
    "\ud83d\udcbc Business Operations Systems": [
        {
            "name": "\ud83e\uddec DataForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/CRM%20data%20enrichment%20agent",
            "desc": "Intelligence-led CRM enrichment & decision mapping."
        },
        {
            "name": "\ud83d\udcc4 InvoiceIntel",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Invoice%20processing%20agent",
            "desc": "Multi-model Vision layer for financial document extraction."
        },
        {
            "name": "\ud83c\udfaf LeadScore AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Lead%20qualification%20agent",
            "desc": "Precision lead qualification via BANT/CHAMP frameworks."
        },
        {
            "name": "\ud83e\udd1d SalesFollowAI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Sales%20follow-up%20agent",
            "desc": "High-conversion post-interaction narrative generator."
        },
        {
            "name": "\ud83d\udee1\ufe0f SupportCraft",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Customer%20support%20response%20agent",
            "desc": "Empathetic response intelligence & sentiment auditing."
        },
        {
            "name": "\ud83d\udcb8 ExpenseIQ",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Expense%20categorization%20agent",
            "desc": "Algorithmic category detection & anomaly audit."
        },
        {
            "name": "\ud83d\udccb SOPFlow AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Internal%20SOP%20generator%20agent",
            "desc": "Standardized Ops Architect for scaling procedures."
        },
        {
            "name": "\ud83d\udcb9 InsightCore",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/KPI%20dashboard%20insight%20agent",
            "desc": "Strategic KPI narrative & causality diagnostic."
        },
        {
            "name": "\ud83d\udcd1 ClauseClear",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Contract%20clause%20explanation%20agent",
            "desc": "Advanced legal plain-language engine & risk auditor."
        },
        {
            "name": "\u2696\ufe0f VendorFlow AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Business%20Operations%20Agents/Vendor%20comparison%20agent",
            "desc": "Strategic vendor comparative analysis grid."
        }
    ],
    "\ud83e\uddea Marketing & Growth Systems": [
        {
            "name": "\ud83c\udfa8 AdForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Ad%20copy%20generator%20agent",
            "desc": "Growth-studio with persona simulation logic."
        },
        {
            "name": "\ud83d\udcc8 AdIntel AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Campaign%20performance%20analysis%20agent",
            "desc": "Budget utility auditor & leaky bucket detector."
        },
        {
            "name": "\ud83e\uddea OptiTest AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/A%20B%20test%20suggestion%20agent",
            "desc": "Strategic A/B test architect with ICE scoring."
        },
        {
            "name": "\ud83d\udee1\ufe0f Persona-Forge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Customer%20persona%20builder%20agent",
            "desc": "Market data synthesis & customer architect."
        },
        {
            "name": "\u26a1 Funnel-Force",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Funnel%20optimization%20agent",
            "desc": "Performance diagnostic & conversion strategy."
        },
        {
            "name": "\ud83d\udce9 Email-Mind",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Email%20marketing%20agent",
            "desc": "High-conversion multi-model copywriting."
        },
        {
            "name": "\ud83e\udd1d Influence-Core",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Influencer%20outreach%20agent",
            "desc": "Relationship-first influencer outreach engine."
        },
        {
            "name": "\ud83d\ude80 Launch-Pad AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Product%20launch%20checklist%20agent",
            "desc": "GTM operational readiness & launch architecture."
        },
        {
            "name": "\ud83d\udcc5 Social-Sync",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Social%20media%20scheduling%20agent",
            "desc": "Cross-platform orchestration & scheduling."
        },
        {
            "name": "\ud83c\udfad Voice-Verify",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Marketing%20&%20Growth%20Agents/Brand%20voice%20consistency%20agent",
            "desc": "Brand voice & linguistic integrity audit."
        }
    ],
    "\ud83d\udcca Data & Automation Systems": [
        {
            "name": "\ud83e\uddec NeuralData AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/CSV%20data%20cleaning%20agent",
            "desc": "Multi-cloud batch CSV cleaning & integrity auditing."
        },
        {
            "name": "\ud83d\udd22 Sheet-Logic AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Spreadsheet%20formula%20generator%20agent",
            "desc": "Multinational spreadsheet formula & logic architect."
        },
        {
            "name": "\ud83d\udee1\ufe0f Data-Guard AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Data%20validation%20agent",
            "desc": "Neural dataset integrity & schema governance."
        },
        {
            "name": "\ud83d\udd0c API-Insight",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/API%20response%20interpreter%20agent",
            "desc": "Neural API response forensic & interpreter."
        },
        {
            "name": "\ud83d\udee1\ufe0f Log-Sentinel",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Log%20anomaly%20detection%20agent",
            "desc": "System telemetry forensic & anomaly detection."
        },
        {
            "name": "\ud83c\udfbc Orchestra-Core",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Workflow%20orchestration%20agent",
            "desc": "Multi-step execution architecture for complex missions."
        },
        {
            "name": "\ud83d\udcbe Pipeline-Forge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/ETL%20pipeline%20design%20agent",
            "desc": "High-performance ETL & cloud data architect."
        },
        {
            "name": "\ud83d\ude91 Error-Forensics",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Error%20classification%20agent",
            "desc": "SRE incident diagnosis & error classification."
        },
        {
            "name": "\ud83d\udcca Alert-Insight",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Monitoring%20alert%20explanation%20agent",
            "desc": "Monitoring alert translation & root-cause diagnostic."
        },
        {
            "name": "\ud83c\udfd7\ufe0f Auto-Strategist",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Automation%20recommendation%20agent",
            "desc": "Process mining & high-ROI automation strategist."
        }
    ],
    "\ud83e\udde0 Personal Productivity Systems": [
        {
            "name": "\ud83e\udde0 PriorityBrain",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/daily-priority-agent",
            "desc": "NLP task ingestion & algorithmic urgency sorting."
        },
        {
            "name": "\ud83d\uddc4\ufe0f BrainVault",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Personal%20knowledge%20base%20agent",
            "desc": "Local RAG knowledge base via vector space."
        },
        {
            "name": "\u26a1 ActionForge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Note-to-action%20item%20agent",
            "desc": "Unstructured text-to-task neural extraction."
        },
        {
            "name": "\ud83d\udce7 MailMind AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Email%20summarization%20agent",
            "desc": "Intelligent thread logic & summary mapping."
        },
        {
            "name": "\ud83d\udcc5 SyncGuard",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Calendar%20conflict%20resolver%20agent",
            "desc": "Conflict detection & resolution engine."
        },
        {
            "name": "\ud83d\udccb AgendaCraft",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Meeting%20agenda%20generator%20agent",
            "desc": "High-fidelity meeting timeline architect."
        },
        {
            "name": "\ud83e\uddd8 Reflect AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Daily%20goal%20reflection%20agent",
            "desc": "Algorithmic daily target analytics."
        },
        {
            "name": "\ud83d\udd14 PingCraft",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Smart%20reminder%20agent",
            "desc": "Distributed deadline alerting engine."
        },
        {
            "name": "\u23f3 ChronoBlock",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Time-blocking%20planner%20agent",
            "desc": "Continuous task packing logic planner."
        },
        {
            "name": "\ud83d\udd25 StreakForge",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Personal%20Productivity%20Agents/Habit%20tracking%20agent",
            "desc": "Persistence density metrics & habit tracking."
        }
    ],
    "\ud83d\udd2c Research & Analysis Systems": [
        {
            "name": "\ud83d\udd2c SWOT Horizon",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/SWOT%20analysis%20agent",
            "desc": "TOWS matrix & strategic opportunity analysis."
        },
        {
            "name": "\ud83c\udf10 Web Research",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Web%20research%20agent",
            "desc": "Autonomous multi-model executive research."
        },
        {
            "name": "\ud83c\udfac StreamBrief",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/YouTube%20video%20summary%20agent",
            "desc": "Neural video transcript distiller & insight mapper."
        },
        {
            "name": "\ud83d\udcb0 CapitalMind",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Investment%20thesis%20generator%20agent",
            "desc": "Evidence-driven investment thesis architect."
        },
        {
            "name": "\ud83d\udcb9 TrendSynthetix",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Market%20trend%20summarization",
            "desc": "Market context trend deconstruction."
        },
        {
            "name": "\ud83d\udcf0 NewsFlow",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/News%20aggregation%20agent",
            "desc": "Global thematic news intelligence digests."
        },
        {
            "name": "\u2696\ufe0f PolicyGuard",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Research%20&%20Analysis%20Agents/Policy%20document%20summarizer%20agent",
            "desc": "Thematic synthesis for regulatory frameworks."
        }
    ],
    "\u270d\ufe0f Writing & Content Systems": [
        {
            "name": "\ud83d\udcdd Blog Architect",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Blog%20post%20generator%20agent",
            "desc": "SEO-optimized post pipeline."
        },
        {
            "name": "\ud83d\udcbc CoverCraft",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Cover%20letter%20writing%20agent",
            "desc": "Job-specific tailored cover letter architect."
        },
        {
            "name": "\ud83d\udcac AI FAQ Gen",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/FAQ%20generation%20agent",
            "desc": "Credentialed FAQ generator."
        },
        {
            "name": "\u2728 GrammarPlus",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Grammar%20correction%20agent",
            "desc": "Semantic deep-edit & tone correction."
        },
        {
            "name": "\ud83d\udd17 HookGen Pro",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/LinkedIn%20post%20ideation%20agent",
            "desc": "LinkedIn post & hook ideation studio."
        },
        {
            "name": "\ud83d\udecd\ufe0f ProductCopy",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Product%20description%20agent",
            "desc": "Outcome-driven product descriptions."
        },
        {
            "name": "\ud83d\udcc4 ResumeAI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Resume%20optimization%20agent",
            "desc": "ATS-optimized enhancement engine."
        },
        {
            "name": "\ud83d\udd0e SEOClusters",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/SEO%20keyword%20expansion%20agent",
            "desc": "Predictive keyword expansion clusters."
        },
        {
            "name": "\ud83d\udcfd\ufe0f SlideForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Script-to-slide%20outline%20agent",
            "desc": "Script-to-slide visual architect."
        },
        {
            "name": "\ud83c\udfad ToneWizard",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Writing%20&%20Content%20Agents/Tone%20rewriting%20agent",
            "desc": "Multi-persona voice rewriter."
        }
    ],
    "\ud83d\udee0\ufe0f AI & Engineering Systems": [
        {
            "name": "\ud83e\udde0 ModelMind AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Model%20comparison%20agent",
            "desc": "Deep architectural trade-off analysis."
        },
        {
            "name": "\u2728 PromptForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/Data%20&%20Automation%20Agents/Prompt%20optimization%20agent",
            "desc": "Neural prompt engineering & linguistic structure optimization."
        },
        {
            "name": "\ud83d\udd0d SemanticForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/RAG%20document%20retrieval%20agent",
            "desc": "Orchestrated RAG document & contextual semantic retrieval."
        },
        {
            "name": "\u26a1 ToolForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Tool-calling%20agent",
            "desc": "Autonomous tool-call orchestration with multi-tool execution registry."
        },
        {
            "name": "\ud83e\udde9 ThinkForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Multi-step%20reasoning%20agent",
            "desc": "Structured multi-step decomposition & chain-of-thought reasoning engine."
        },
        {
            "name": "\ud83d\udee0\ufe0f CleanCode AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Code%20refactoring%20agent",
            "desc": "Advanced syntax architectural transformation & best practice adherence refactoring engine."
        },
        {
            "name": "\ud83d\udc1b BugSentinel AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Bug%20explanation%20agent",
            "desc": "Neural traceback analysis & root cause diagnostic forensics."
        },
        {
            "name": "\ud83d\udcd6 DocForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/API%20documentation%20agent",
            "desc": "Automated deterministic REST API schema documentation & contract logic compiler."
        },
        {
            "name": "\ud83e\uddea TestForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/Test%20case%20generation%20agent",
            "desc": "Rigorous test suite & edge case regression validation framework."
        },
        {
            "name": "\ud83c\udfd7\ufe0f ArchForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/AI%20%20&%20Engineering%20Agents/System%20architecture%20explainer%20agent",
            "desc": "Topological data-flow extraction & implicitly derived trade-off analytical engine."
        }
    ],
    "\ud83d\uddc4\ufe0f HR, Legal & Compliance Systems": [
        {
            "name": "\ud83d\udcbc TalentForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Job%20description%20generator%20agent",
            "desc": "Inclusive requisition & job description intelligence pipeline."
        },
        {
            "name": "\ud83d\udd0e ScreenGenius Pro AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Candidate%20screening%20agent",
            "desc": "Multi-axis algorithmic candidate screening matrix with red-flag detection & custom interview probes."
        },
        {
            "name": "\ud83c\udf99\ufe0f QuestForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Interview%20question%20generator%20agent",
            "desc": "Autonomous technical interview question architect."
        },
        {
            "name": "\ud83d\udcc8 ReviewForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Performance%20review%20agent",
            "desc": "Professional tone synthesis and constructive performance appraisal engine."
        },
        {
            "name": "\u2696\ufe0f ComplianceGuard AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Policy%20compliance%20checker%20agent",
            "desc": "Automated enterprise policy enforcement & liability prevention matrix."
        },
        {
            "name": "\u26a0\ufe0f RiskForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Risk%20assessment%20agent",
            "desc": "Threat modeling architecture resolving operational and deployment liabilities conditionally."
        },
        {
            "name": "\ud83d\udee1\ufe0f BriefForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Legal%20clause%20summarization%20agent",
            "desc": "Legal clause syntactic translation mechanism into executive language logic."
        },
        {
            "name": "\ud83d\udd10 PrivacyForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Data%20privacy%20explanation%20agent",
            "desc": "Contextual data privacy regulation compliance matrix mapping features to legal bounds."
        },
        {
            "name": "\ud83c\udf93 SkillForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Training%20content%20generator%20agent",
            "desc": "Auto-architected corporate learning & objective enablement module generator."
        },
        {
            "name": "\ud83d\udccb AuditForge AI",
            "url": "https://github.com/HarshChoudhary2003/Real-world-AI-agents-hub/tree/main/HR%20,%20Legal%20&%20Compliance%20Agents/Audit%20preparation%20agent",
            "desc": "Pre-audit readiness scanner identifying critical evidence gaps and mandatory remediations."
        }
    ],
    "1. Initialize Runtime": [],
    "2. Configure Credentials": [],
    "3. Launch the Master Brain": []
}

# Sanitize data for surrogate-sensitive environments
def sanitize(text):
    if not isinstance(text, str): return text
    return text.encode('utf-8', 'ignore').decode('utf-8').replace('"', '\\"').replace("'", "\\'")

CATEGORIES = {sanitize(k): [{sanitize(key): sanitize(val) if isinstance(val, str) else val for key, val in a.items()} for a in v] for k, v in CATEGORIES_RAW.items()}

def apply_styles():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-color: #0d1117;
        --sidebar-bg: #161b22;
        --card-bg: #0d1117;
        --card-border: #30363d;
        --card-hover: #1c212b;
        --accent: #2f81f7;
        --accent-glow: rgba(47, 129, 247, 0.15);
        --text-p: #f0f6fc;
        --text-s: #8b949e;
        --font-main: 'Inter', -apple-system, system-ui;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--text-p);
        font-family: var(--font-main);
    }

    header, footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--card-border);
    }

    .sidebar-header {
        padding: 32px 24px;
        margin-bottom: 24px;
        border-bottom: 1px solid var(--card-border);
        text-align: center;
    }

    .nav-category {
        padding: 8px 16px;
        border-radius: 6px;
        color: var(--text-s);
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
        display: block;
        margin: 2px 12px;
    }

    .nav-category:hover {
        background: rgba(177, 186, 196, 0.12);
        color: var(--text-p);
    }

    .block-container {
        padding-top: 48px !important;
        padding-left: 64px !important;
        padding-right: 64px !important;
        max-width: 1440px !important;
    }

    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 48px;
    }

    .stats-badge {
        background: var(--accent-glow);
        color: var(--accent);
        padding: 6px 16px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        border: 1px solid rgba(47, 129, 247, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .category-section {
        margin-bottom: 48px;
        scroll-margin-top: 48px;
    }

    .cat-head {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--card-border);
    }

    .cat-name {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-p);
    }

    .agent-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 6px;
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: border-color 0.2s, background-color 0.2s;
        cursor: pointer;
    }

    .agent-card:hover {
        border-color: #8b949e;
        background: #161b22;
    }

    .agent-name {
        color: var(--accent);
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .agent-desc {
        color: var(--text-s);
        font-size: 13.5px;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .card-footer {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: auto;
    }

    .tag {
        font-size: 11px;
        color: var(--text-s);
        padding: 2px 8px;
        background: #161b22;
        border: 1px solid var(--card-border);
        border-radius: 100px;
    }

    .stTextInput input {
        background-color: #0d1117 !important;
        border: 1px solid var(--card-border) !important;
        color: var(--text-p) !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
    }

    </style>
    ''', unsafe_allow_html=True)

def main():
    apply_styles()

    with st.sidebar:
        st.markdown('''
        <div class="sidebar-header">
            <h1 style="font-size: 24px; font-weight: 800; margin: 0; color: #f0f6fc;">Agent<span style="color:#2f81f7;">Registry</span></h1>
            <code style="font-size: 10px; color:#8b949e; background:none;">v2.4.0 OPERATIONAL</code>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<p style='padding: 0 24px; font-size: 11px; font-weight: 600; color:#484f58; text-transform: uppercase;'>Navigation</p>", unsafe_allow_html=True)
        
        for cat in CATEGORIES.keys():
            cat_id = cat.lower().replace(" ", "-").replace("&", "and")
            # Deeper sanitization to remove emojis that confuse Streamlit's markdown proto
            clean_name = re.sub(r'[^\x00-\x7F]+', '', cat).strip()
            st.markdown(f'<a href="#{cat_id}" class="nav-category">{clean_name}</a>', unsafe_allow_html=True)

    st.markdown('''
        <div class="top-bar">
            <div>
                <h2 style="font-size: 32px; font-weight: 600; margin: 0; color: #f0f6fc;">Systems Intelligence Hub</h2>
                <p style="color:#8b949e; font-size: 16px; margin-top: 8px;">Deterministic multi-agent orchestration registry for enterprise automation.</p>
            </div>
            <div class="stats-badge">78 Nodes Online</div>
        </div>
    ''', unsafe_allow_html=True)

    search_q = st.text_input("", placeholder="Search 78 specialized agents by name, capability, or department...").lower()

    if search_q:
        cols = st.columns(4)
        found = 0
        for cat_name, agents in CATEGORIES.items():
            for agent in agents:
                if search_q in agent['name'].lower() or search_q in agent['desc'].lower() or search_q in cat_name.lower():
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card">
                            <div>
                                <div class="agent-name">{name}</div>
                                <div class="agent-desc">{desc}</div>
                            </div>
                            <div class="card-footer">
                                <span class="tag">Production</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[found % 4]:
                        st.markdown(card_html, unsafe_allow_html=True)
                    found += 1
        if found == 0:
            st.warning("Query returned zero agents.")
    else:
        for cat_name, agents in CATEGORIES.items():
            cat_id = cat.lower().replace(" ", "-").replace("&", "and")
            st.markdown(f'''
                <div id="{cat_id}" class="category-section">
                    <div class="cat-head">
                        <div class="cat-name">{cat_name}</div>
                        <span style="color:#484f58; font-size: 12px; margin-left: auto;">{len(agents)} instances</span>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            chunk_size = 4
            for i in range(0, len(agents), chunk_size):
                chunk = agents[i:i+chunk_size]
                cols = st.columns(4)
                for j, agent in enumerate(chunk):
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card">
                            <div>
                                <div class="agent-name">{name}</div>
                                <div class="agent-desc">{desc}</div>
                            </div>
                            <div class="card-footer">
                                <span class="tag">Active</span>
                                <span style="font-size: 12px; color: #2f81f7;">Open Hub →</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[j]:
                        st.markdown(card_html, unsafe_allow_html=True)
                st.markdown('<div style="margin-bottom: 24px;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
