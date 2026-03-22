import streamlit as st
import json
import re

st.set_page_config(
    page_title="Agent OS | Dynamic Hub",
    page_icon="🌈",
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
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-color: #0b0c10;
        --sidebar-bg: #14161f;
        --card-bg: #1f2833;
        --card-hover: #161b22;
        --accent: #45a29e;
        --glow: #66fcf1;
        --text-p: #c5c6c7;
        --text-bright: #66fcf1;
        --border: #45a29e;
        --font-main: 'Outfit', -apple-system, sans-serif;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--text-p);
        font-family: var(--font-main);
    }

    header, footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}

    /* Sidebar Navigation Rail */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid rgba(102, 252, 241, 0.1);
    }

    .nav-category {
        padding: 10px 20px;
        color: var(--text-p);
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        display: block;
        margin: 4px 12px;
        border-radius: 8px;
    }

    .nav-category:hover {
        background: rgba(102, 252, 241, 0.05);
        color: var(--glow);
        transform: translateX(5px);
    }

    /* Hero Section with Animated Gradient */
    .hero-container {
        text-align: center;
        padding: 60px 0 100px;
        position: relative;
        overflow: hidden;
    }

    .hero-title {
        font-size: 72px;
        font-weight: 800;
        background: linear-gradient(90deg, #66fcf1, #45a29e, #1f2833, #66fcf1);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: flowing-gradient 8s linear infinite;
        margin-bottom: 20px;
        letter-spacing: -2px;
    }

    @keyframes flowing-gradient {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 0%; }
    }

    .hero-sub {
        font-size: 24px;
        color: var(--text-p);
        opacity: 0.8;
        max-width: 800px;
        margin: 0 auto 40px;
        line-height: 1.4;
    }

    /* Colorful Card Styling with Hover Pop */
    @keyframes card-fade-in {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .agent-card {
        background: #14161f;
        border: 1px solid rgba(102, 252, 241, 0.1);
        border-radius: 12px;
        padding: 30px;
        height: 100%;
        position: relative;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: card-fade-in 0.6s ease-out backwards;
    }

    .agent-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: var(--glow);
        box-shadow: 0 15px 35px rgba(102, 252, 241, 0.1);
        background: #1c212b;
    }

    .agent-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #66fcf1, #45a29e);
        opacity: 0;
        transition: opacity 0.3s;
    }

    .agent-card:hover::before {
        opacity: 1;
    }

    .agent-name {
        color: #fff;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .agent-desc {
        color: var(--text-p);
        font-size: 14px;
        line-height: 1.6;
        opacity: 0.7;
    }

    .card-meta {
        margin-top: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .badge {
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        background: rgba(102, 252, 241, 0.1);
        color: var(--glow);
        border: 1px solid rgba(102, 252, 241, 0.2);
    }

    /* Category Headers */
    .cat-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 40px;
        border-left: 5px solid var(--glow);
        padding-left: 20px;
        color: #fff;
        scroll-margin-top: 50px;
    }

    .stTextInput input {
        background: rgba(20, 22, 31, 0.8) !important;
        border: 1px solid rgba(102, 252, 241, 0.1) !important;
        color: #fff !important;
        border-radius: 50px !important;
        padding: 15px 25px !important;
        font-size: 18px !important;
        transition: all 0.3s !important;
    }

    .stTextInput input:focus {
        border-color: var(--glow) !important;
        box-shadow: 0 0 20px rgba(102, 252, 241, 0.1) !important;
    }

    </style>
    ''', unsafe_allow_html=True)

def main():
    apply_styles()

    with st.sidebar:
        st.markdown('''
        <div style="padding: 40px 20px; text-align: center;">
            <h1 style="color: #66fcf1; font-weight: 900; letter-spacing: -2px; font-size: 36px;">A.O.S</h1>
            <p style="color: #45a29e; font-size: 12px; text-transform: uppercase; font-weight: 700; letter-spacing: 2px;">Neural Registry</p>
        </div>
        ''', unsafe_allow_html=True)
        
        for cat in CATEGORIES.keys():
            cat_id = cat.lower().replace(" ", "-").replace("&", "and")
            clean_name = re.sub(r'[^\w\s]', '', cat).strip()
            # If re.sub fails to clean everything for nav anchors, we use simple labels
            if not clean_name: clean_name = "Category"
            st.markdown(f'<a href="#{cat_id}" class="nav-category">{clean_name}</a>', unsafe_allow_html=True)

    st.markdown('''
    <div class="hero-container">
        <h1 class="hero-title">Beyond Software.</h1>
        <p class="hero-sub">The global registry for 78 autonomous agents architected to drive the post-SaaS economy infrastructure.</p>
    </div>
    ''', unsafe_allow_html=True)

    search_q = st.text_input("", placeholder="Search the decentralized agent intelligence registry...").lower()

    if search_q:
        cols = st.columns(3)
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
                            <div class="agent-name">{name}</div>
                            <div class="agent-desc">{desc}</div>
                            <div class="card-meta">
                                <span class="badge">Operational</span>
                                <span style="color: #66fcf1; font-size: 12px;">Explore →</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[found % 3]:
                        st.markdown(card_html, unsafe_allow_html=True)
                    found += 1
    else:
        for idx, (cat_name, agents) in enumerate(CATEGORIES.items()):
            cat_id = cat_name.lower().replace(" ", "-").replace("&", "and")
            st.markdown(f'<div id="{cat_id}" class="cat-title">{cat_name}</div>', unsafe_allow_html=True)
            
            chunk_size = 3
            for i in range(0, len(agents), chunk_size):
                chunk = agents[i:i+chunk_size]
                cols = st.columns(3)
                for j, agent in enumerate(chunk):
                    name = agent['name']
                    desc = agent['desc']
                    url = agent['url']
                    
                    # Add delay for staggered animation
                    delay = (i + j) * 0.05
                    
                    card_html = f'''
                    <a href="{url}" target="_blank" style="text-decoration:none;">
                        <div class="agent-card" style="animation-delay: {delay}s;">
                            <div class="agent-name">{name}</div>
                            <div class="agent-desc">{desc}</div>
                            <div class="card-meta">
                                <span class="badge">v1.8</span>
                                <span style="color: #66fcf1; font-size: 12px; font-weight: 600;">System Access →</span>
                            </div>
                        </div>
                    </a>
                    '''
                    with cols[j]:
                        st.markdown(card_html, unsafe_allow_html=True)
                st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
